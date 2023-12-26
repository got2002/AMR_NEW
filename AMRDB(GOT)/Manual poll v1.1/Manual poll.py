from flask import Flask, render_template, request, jsonify
import pandas as pd
import cx_Oracle
from flask import flash
from datetime import datetime
import pandas as pd
import sqlite3
from flask import Flask, render_template, request, session,send_file, redirect, url_for,jsonify
import socket
import struct
from pymodbus.utilities import computeCRC
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, validators
from werkzeug.security import generate_password_hash
from sqlalchemy import desc
from flask import Flask, send_from_directory
from flask_migrate import Migrate
import threading
import cx_Oracle


app = Flask(__name__)   
app.secret_key = "your_secret_key_here"
# Replace these values with your actual database credentials
communication_traffic = []
change_to_32bit_counter = 1  # Initialize the counter to 2


def convert_to_binary_string(value, bytes_per_value):
    binary_string = bin(value)[2:]  # Convert the value to binary string excluding the '0b' prefix
    return binary_string.zfill(bytes_per_value * 8)  # Zero-fill to fit the number of bits based on bytes_per_value
username = 'root'
password = 'root'
hostname = '192.168.102.192'
port = '1521'
service_name = 'orcl'

def fetch_data(query, params=None):
    try:
        dsn = cx_Oracle.makedsn(hostname, port, service_name)
        with cx_Oracle.connect(username, password, dsn) as connection:
            with connection.cursor() as cursor:
                if params:
                    cursor.execute(query, params)
                else:
                    cursor.execute(query)
                results = cursor.fetchall()
        return results
    except cx_Oracle.Error as e:
        error, = e.args
        print("Oracle Error:", error)
        return []

@app.route('/get_tags', methods=['GET'])
def get_tags():
    selected_region = request.args.get('selected_region')

    tag_query = """
    SELECT DISTINCT TAG_ID
    FROM AMR_FIELD_ID
    JOIN AMR_PL_GROUP ON AMR_FIELD_ID.FIELD_ID = AMR_PL_GROUP.FIELD_ID 
    WHERE AMR_PL_GROUP.PL_REGION_ID = :region_id
    """

    tag_results = fetch_data(tag_query, params={'region_id': selected_region})
    tag_options = [str(tag[0]) for tag in tag_results]

    # Sort the tag options alphabetically
    tag_options.sort()

    return jsonify({'tag_options': tag_options})

@app.route('/')
def index():
    
        # Fetch regions
        region_query = "SELECT * FROM AMR_REGION"
        region_results = fetch_data(region_query)
        region_options = [str(region[0]) for region in region_results]

    # Fetch tags based on the selected region
        tag_query = "SELECT DISTINCT TAG_ID FROM AMR_FIELD_ID JOIN AMR_PL_GROUP ON AMR_FIELD_ID.FIELD_ID = AMR_PL_GROUP.FIELD_ID WHERE AMR_PL_GROUP.PL_REGION_ID = :region_id"
        selected_region = request.args.get('region_dropdown')
        tag_results = fetch_data(tag_query, params={'region_id': selected_region})
        tag_options = [str(tag[0]) for tag in tag_results]
        tag_options.sort()

        # Construct the main query conditions
        conditions = [
            "AMR_USER.USER_ENABLE = 1",
            "AMR_FIELD_ID.FIELD_ID = AMR_PL_GROUP.FIELD_ID",
            "AMR_FIELD_ID.METER_ID = AMR_USER.USER_GROUP",
            "AMR_FIELD_ID.CUST_ID = AMR_FIELD_CUSTOMER.CUST_ID",
            "AMR_FIELD_ID.METER_ID = AMR_FIELD_METER.METER_ID",
            "AMR_VC_TYPE.ID = AMR_FIELD_METER.METER_STREAM_TYPE",
            "AMR_FIELD_METER.METER_PORT_NO = AMR_PORT_INFO.ID",
            "AMR_FIELD_ID.TAG_ID IS NOT NULL"  # Default tag condition
        ]

        # Update conditions based on user inputs
        selected_tag = request.args.get('tag_dropdown')
        if selected_tag:
            conditions.append(f"AMR_FIELD_ID.TAG_ID = '{selected_tag}'")

        if selected_region:
            conditions.append(f"AMR_PL_GROUP.PL_REGION_ID = '{selected_region}'")

        # Construct the final query
        query = f"""
            SELECT
                AMR_FIELD_METER.METER_STREAM_NO as RUN,
                AMR_PL_GROUP.PL_REGION_ID as Region,
                AMR_FIELD_ID.TAG_ID as Sitename,
                AMR_FIELD_METER.METER_NO_STREAM as NoRun,
                AMR_FIELD_METER.METER_ID as METERID,
                AMR_VC_TYPE.VC_NAME as VCtype,
                AMR_FIELD_ID.SIM_IP as IPAddress,
                AMR_PORT_INFO.PORT_NO as Port
            FROM
                AMR_FIELD_ID,
                AMR_USER,
                AMR_FIELD_CUSTOMER,
                AMR_FIELD_METER,
                AMR_PL_GROUP,
                AMR_VC_TYPE,
                AMR_PORT_INFO
            WHERE
                {' AND '.join(conditions)}
        """

        # Fetch and convert the data to a DataFrame
        if selected_region:
            results = fetch_data(query)
            df = pd.DataFrame(results, columns=['RUN', 'Region', 'Sitename', 'NoRun', 'METERID', 'VCtype', 'IPAddress', 'Port'])
            data_list = df.to_dict(orient='records')

            session['data_list'] = data_list
            session['selected_tag'] = selected_tag
            session['selected_region'] = selected_region
            session['region_options'] = region_options
            session['tag_options'] = tag_options

            return render_template('Manual poll.html', data_list=data_list, selected_tag=selected_tag, selected_region=selected_region, region_options=region_options, tag_options=tag_options, df=df)
        else:
            data_list = []
            # Render the template without executing the query
            return render_template('Manual poll.html',data_list=data_list, selected_region=selected_region, region_options=region_options)    
    



@app.route('/', methods=['POST'])

def read_data():
    data_list = session.get('data_list', [])
    selected_region = session.get('selected_region', None)
    global change_to_32bit_counter  # Use the global variable

    slave_id = int(request.form['slave_id'])
    function_code = int(request.form['function_code'])
    if request.form['starting_address'] == 'custom':
        if 'custom_starting_address' in request.form:
            starting_address = int(request.form['custom_starting_address'])
        else:
            starting_address = 0  # หรือใส่ค่าเริ่มต้นที่คุณต้องการ
    else:
        starting_address = int(request.form['starting_address'])
    quantity = int(request.form['quantity'])
    tcp_ip = request.form['tcp_ip']
    tcp_port = int(request.form['tcp_port'])
    
    # Check if the data should be displayed in 16-bit format or 32-bit format
    is_16bit = request.form.get('is_16bit') == 'true'

    if is_16bit:
        bytes_per_value = 2
    else:
        bytes_per_value = 4
        if change_to_32bit_counter > 0:
            quantity *= 2
            change_to_32bit_counter -= 1

    
    
    

    # Build the request message
    request_message = bytearray(
        [slave_id, function_code, starting_address >> 8, starting_address & 0xFF, quantity >> 8, quantity & 0xFF])

    crc = computeCRC(request_message)
    request_message += crc.to_bytes(2, byteorder='big')

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((tcp_ip, tcp_port))

    # Store the TX message in communication_traffic
    communication_traffic.append({'direction': 'TX', 'data': request_message.hex()})

    sock.send(request_message)

    response = sock.recv(1024)

    # Store the RX message in communication_traffic
    communication_traffic.append({'direction': 'RX', 'data': response.hex()})

    sock.close()

    data = response[3:]

    values = [int.from_bytes(data[i:i + bytes_per_value], byteorder='big', signed=False) for i in
              range(0, len(data), bytes_per_value)]
    

    if '32bit' in request.form and request.form['32bit'] == 'true':
        is_32bit = True
    else:
        is_32bit = False
    
    
    
    data_list = []
    address = starting_address
    value = 0
    
    for i, value in enumerate(values):
       

        address = starting_address + i * 2
               
        hex_value = hex(value)  # Convert the decimal value to HEX
        binary_value = convert_to_binary_string(value, bytes_per_value)
        float_value = struct.unpack('!f', struct.pack('!I', value))[0]
        description = f"Address {address}"
            # elster ek
        if address == 8000 or address == 8010 or address == 8020 or address == 8030 or address == 8040 or address == 8050 or address == 8060:
            description = "Time Stamp"
        if address == 8002 or address == 8012 or address == 8022 or address == 8032 or address == 8042 or address == 8052 or address == 8062:
            description = "Converted Index (VmT)"
        if address == 8004 or address == 8014 or address == 8024 or address == 8034 or address == 8044 or address == 8054 or address == 8064:
            description = "Unconverted Index (VbT)"
        if address == 8006 or address == 8016 or address == 8026 or address == 8036 or address == 8046 or address == 8056 or address == 8066:
            description = "Pressure Daily Average"
        if address == 8008 or address == 8018 or address == 8028 or address == 8038 or address == 8048 or address == 8058 or address == 8068:
            description = "Temperature Daily Average"
        if address == 7001 :
            description = "Serial No."
        if address == 7003 :
            description = "Time & Date"
        if address == 7005 :
            description = "Pressure"
        if address == 7007 :
            description = "Temperature"
        if address == 7009 :
            description = "Pressure Base"
        if address == 7011 :
            description = "Temperature base"
        if address ==  7013:
            description = " Actual Flowrate Qm"
        if address == 7015 :
            description = "Vt(Turbine index)"
        if address == 7017 :
            description = "Vm total (Actual vol cumulative)"
        if address == 7019 :
            description = "Vb total (Actual vol cumulative)"
        if address == 7021 :
            description = "AGA-8 Equation"
        if address == 7023 :
            description = "Zb"
        if address == 7025 :
            description = "Zf"
        if address == 7027 :
            description = "Pulse weight"
        if address == 7029 :
            description = "Qm max"
        if address == 7031 :
            description = "Qm min"
        if address == 7033 :
            description = "CO2"
        if address == 7035 :
            description = "N2"
        if address == 7037 :
            description = "SG"
        if address == 7039 :
            description = "LowBattery Alarm"
    
        # Actaris
        if address == 20482 :
            description = "Time Stamp"
        if address == 20498 :
            description = "Converted Index (VmT)"
        if address == 20494 :
            description = "Unconverted Index (VbT)"
        if address ==  20486:
            description = "Pressure Daily Average"
        if address ==  20484:
            description = "Temperature Daily Average"
        # config
        if address == 32 :
            description = "Specific Gravity"
        if address == 34 :
            description = "Base Pressure"
        if address == 38 :
            description = "Base Pressure. For Z Calculate"
        if address == 40 :
            description = "Base Temperature. For Z Calculate"
        if address == 42 :
            description = "Input Pulse Weight"
        if address == 44 :
            description = "Base Temperature"
        if address ==  78:
            description = " Carbon dioxide"
        if address == 82 :
            description = "Nitrogen"
        if address == 546 :
            description = "Current Time"
        if address == 756 :
            description = "Battery Alarm Warning"
        if address == 822 :
            description = "Actual Flow rate"
        if address == 824 :
            description = "Standard Flow rate"
        if address == 834 :
            description = "Current Temperature"
        if address == 836 :
            description = "Current Pressure"
        if address == 838 :
            description = "Conversion Factor"
        if address == 840 :
            description = "Act. Compressibility Factor"
        if address == 842 :
            description = "Fpv2"
        
      

        if is_16bit:
            signed_value = value - 2 ** 16 if value >= 2 ** 15 else value
            is_16bit_value = True
            float_value = value if is_16bit_value else float_value
            float_display_value = f"16-bit signed: {signed_value}, float: {float_value}"
        else:
            signed_value = value - 2 ** 32 if value >= 2 ** 31 else value
            is_16bit_value = False
            float_value = float_value if is_16bit_value else struct.unpack('!f', struct.pack('!I', value))[0]
            float_signed_value = signed_value if is_16bit_value else None  # Set signed_value to None for 32-bit
            float_display_value = float_value

        data_list.append({
            'description': description,
            'address': address,
            'value': value,
            'hex_value': hex_value,
            'binary_value': binary_value,
            'float_value': float_display_value,
            'signed_value': signed_value,
                'is_16bit': is_16bit_value,
    'float_signed_value': signed_value
            })
        value, updated_address = handle_action_configuration(i, value, address)
        # หลังจาก values = [int.from_bytes(data[i:i + bytes_per_value], byteorder='big', signed=False) for i in range(0, len(data), bytes_per_value)]
# แทนที่ด้วย:

    values = [int.from_bytes(data[i:i + bytes_per_value], byteorder='big', signed=False) for i in range(0, len(data), bytes_per_value)]

# หากต้องการแปลงเฉพาะแถวแรก สามารถทำได้เช่นนี้:


    session['tcp_ip'] = tcp_ip
    session['tcp_port'] = tcp_port
        
        
    # ตรวจสอบค่า is_16bit เพื่อเพิ่มข้อมูลลงในตาราง 16-bit
    if not is_16bit:
        # เพิ่มข้อมูลลงในตาราง 16-bit โดยเพิ่มค่าลงในตารางเดิมและเพิ่มค่าอีก 1
        data_list_16bit = []
        for data_16bit in data_list:
            address_16bit = data_16bit['address']
            value_16bit = data_16bit['value'] * 2  # เพิ่มค่าขึ้นเป็น 2 เท่าเพื่อให้เป็น 1 เท่าของข้อมูลเดิม
            data_list_16bit.append({'address': address_16bit, 'value': value_16bit})
    if 'action_actaris' in request.form: 
        
        data_list[3], data_list[7] = data_list[7], data_list[3]
        del data_list[3]
        
        data_list[4], data_list[5] = data_list[5], data_list[4]
        del data_list[3]
        data_list[5], data_list[7] = data_list[7], data_list[5]
        del data_list[4]
        data_list[4], data_list[5] = data_list[5], data_list[4]
    if 'action_configuration' in request.form:
               
      
       
        if len(data_list) >= 6:
            data_list[4], data_list[5] = data_list[5], data_list[4]
        if len(data_list) > 2:
            del data_list[2]  
        if len(data_list) >= 5:
            data_list[3], data_list[4] = data_list[4], data_list[3]
        data_list[6], data_list[22] = data_list[22], data_list[6] 
        del data_list[7] 
        data_list[7], data_list[23] = data_list[23], data_list[7] 
        

    return render_template('Manual poll.html', data_list=data_list, slave_id=slave_id, function_code=function_code,
                           starting_address=starting_address, quantity=quantity, is_16bit=is_16bit,
                           communication_traffic=communication_traffic, data=data
                           )


def handle_actaris_action(i, address):
    
   
    return  address

def handle_action_configuration(i, value, address):
    

    return value, address

    # ตรวจสอบเงื่อนไขอื่น ๆ ที่คุณต้องการได้ต่อจากนี้


@app.route('/process_selected_rows', methods=['POST'])
def process_selected_rows():
    selected_rows = request.form.getlist('selected_rows')
    
    # Perform any processing with the selected rows here
    # Access the selected METERID values from the selected_rows list
    
    return "Selected rows processed successfully"



if __name__ == '__main__':
    app.run(debug=True)
