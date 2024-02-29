from flask import Flask, render_template, request, jsonify, redirect, url_for
import pandas as pd
import cx_Oracle
from flask import flash
from datetime import datetime
import pandas as pd
import sqlite3
import plotly.express as px
from flask import (
    Flask,
    render_template,
    request,
    session,
    send_file,
    redirect,
    url_for,
    jsonify,
)
import socket
import struct
from pymodbus.utilities import computeCRC
from flask_wtf import FlaskForm
from werkzeug.security import generate_password_hash, check_password_hash
from wtforms import StringField, PasswordField, SubmitField, validators
from werkzeug.security import generate_password_hash
from sqlalchemy import desc
from flask import Flask, send_from_directory
from flask_migrate import Migrate
import hashlib
import os
import cx_Oracle
import plotly.subplots as sp
import plotly.graph_objs as go
import matplotlib as mpt
import time
import datetime
import pytz

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Replace these values with your actual database credentials
communication_traffic = []
change_to_32bit_counter = 0  # Initialize the counter to 2
def convert_to_binary_string(value, bytes_per_value):
    binary_string = bin(value)[
        2:
    ]  # Convert the value to binary string excluding the '0b' prefix
    return binary_string.zfill(
        bytes_per_value * 8
    )  # Zero-fill to fit the number of bits based on bytes_per_value
# Set the Flask secret key from the environment variable
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "fallback_secret_key")
def md5_hash(input_string):
    # เข้ารหัสรหัสผ่านโดยใช้ MD5
    return hashlib.md5(input_string.encode()).hexdigest()
############  connect database  #####################
username = "root"
password = "root"
hostname = "192.168.102.192"
port = "1521"
service_name = "orcl"


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
        (error,) = e.args
        print("Oracle Error:", error)
        return []

@app.route("/get_tags", methods=["GET"])
def get_tags():
    selected_region = request.args.get("selected_region")

    tag_query = """
    SELECT DISTINCT TAG_ID
    FROM AMR_FIELD_ID
    JOIN AMR_PL_GROUP ON AMR_FIELD_ID.FIELD_ID = AMR_PL_GROUP.FIELD_ID 
    WHERE AMR_PL_GROUP.PL_REGION_ID = :region_id
    """

    tag_results = fetch_data(tag_query, params={"region_id": selected_region})
    tag_options = [str(tag[0]) for tag in tag_results]

    # Sort the tag options alphabetically
    tag_options.sort()

    return jsonify({"tag_options": tag_options})


@app.route("/Manualpoll_data")
def Manualpoll_data():
    region_query = """
        SELECT * FROM AMR_REGION 
    """
    
    tag_query = """
        SELECT DISTINCT TAG_ID
        FROM AMR_FIELD_ID
        JOIN AMR_PL_GROUP ON AMR_FIELD_ID.FIELD_ID = AMR_PL_GROUP.FIELD_ID 
        WHERE AMR_PL_GROUP.PL_REGION_ID = :region_id
        AND TAG_ID NOT LIKE '%remove%
        """
    region_results = fetch_data(region_query)
    
    region_options = [str(region[0]) for region in region_results]
    query = """
        SELECT
            AMR_FIELD_METER.METER_STREAM_NO as RunNo,
            AMR_PL_GROUP.PL_REGION_ID as region,
            AMR_FIELD_ID.TAG_ID as Sitename,
            AMR_FIELD_METER.METER_NO_STREAM as NoRun,
            AMR_FIELD_METER.METER_ID as METERID,
            AMR_VC_TYPE.VC_NAME as VCtype,
            AMR_FIELD_ID.SIM_IP as IPAddress,
            
            AMR_PORT_INFO.PORT_NO as port,
            amr_poll_range.evc_type as evc_type,
    
   amr_vc_type.vc_name as vc_name ,
   amr_poll_range.poll_billing as poll_billing ,
    amr_poll_range.poll_config as poll_config,
    amr_poll_range.poll_billing_enable as poll_billing_enable ,
   amr_poll_range.poll_config_enable as poll_config_enable
        FROM
            AMR_FIELD_ID,
            AMR_USER,
            AMR_FIELD_CUSTOMER,
            AMR_FIELD_METER,
            AMR_PL_GROUP,
            AMR_VC_TYPE,
            AMR_PORT_INFO,
            amr_poll_range
        WHERE
            AMR_USER.USER_ENABLE=1 AND
            amr_vc_type.id=amr_poll_range.evc_type AND
            AMR_FIELD_ID.FIELD_ID = AMR_PL_GROUP.FIELD_ID AND
            AMR_FIELD_ID.METER_ID = AMR_USER.USER_GROUP AND
            AMR_FIELD_ID.CUST_ID = AMR_FIELD_CUSTOMER.CUST_ID AND
            AMR_FIELD_ID.METER_ID = AMR_FIELD_METER.METER_ID AND
            AMR_VC_TYPE.ID = AMR_FIELD_METER.METER_STREAM_TYPE AND
            AMR_FIELD_METER.METER_PORT_NO = AMR_PORT_INFO.ID
            {tag_condition}
            {region_condition}
        """
    tag_condition = "AND AMR_FIELD_ID.TAG_ID IS NOT NULL"
    region_condition = "AND amr_pl_group.pl_region_id = 'default_region_id'"
    selected_tag = request.args.get("tag_dropdown")
    selected_region = request.args.get("region_dropdown")
    region_results = fetch_data(region_query)
    region_options = [str(region[0]) for region in region_results]
    tag_results = fetch_data(tag_query, params={"region_id": selected_region})
    tag_options = [str(tag[0]) for tag in tag_results]
    # Sort the tag options alphabetically
    tag_options.sort()
    if selected_tag:
        tag_condition = f"AND AMR_FIELD_ID.TAG_ID = '{selected_tag}'"
    if selected_region:
        region_condition = f"AND amr_pl_group.pl_region_id = '{selected_region}'"
   
    query = query.format(tag_condition=tag_condition, region_condition=region_condition)
    results = fetch_data(query)
    
    df = pd.DataFrame(
        results,
        columns=[
            "RUN",
            "Region",
            "Sitename",
            "NoRun",
            "METERID",
            "VCtype",
            "IPAddress",
            "Port",
            "evc_type",
            "vc_name",
            "poll_billing",
            "poll_config",
            "poll_billing_enable",
            "poll_config_enable",
        ],
    )
    run = df.get(["RUN"]).values.tolist()
    METERID =df.get(["METERID"]).values.tolist()
   
    evc_type_list = df.get(["evc_type"]).values.tolist()
    
    poll_config_list = df.get(["poll_config"]).values.tolist()
    
    if poll_config_list:
        config_list_str = str(poll_config_list).strip("[]'").split(",")
    else:
        config_list_str = [''] * 10
    poll_billing_list = df.get(["poll_billing"]).values.tolist()
    if poll_billing_list:
        billing_list_str = str(poll_billing_list).strip("[]'").split(",")
    else:
        billing_list_str = [''] * 20
    poll_config_enable_list = df.get(["poll_config_enable"]).values.tolist()
    
    if poll_config_enable_list:
        poll_config_enable_str = str(poll_config_enable_list).strip("[]'").split(",")
    else:
        poll_config_enable_str = [''] * 20
        
    poll_billing_enable_list = df.get(["poll_billing_enable"]).values.tolist()
    if poll_billing_enable_list:
        poll_billing_enable_str = str(poll_billing_enable_list).strip("[]'").split(",")
    else:
        poll_billing_enable_str = [''] * 20
    tcp_ip = df.get(["IPAddress"]).values.tolist()
    if tcp_ip:
        ip_str = str(tcp_ip).strip("[]'").split(",")
    else:
        ip_str = [''] 
    
    tcp_port = df.get(["Port"]).values.tolist()
    if tcp_port:
        Port_str = str(tcp_port).strip("[]'").split(",")
    else:
        Port_str = [''] 
    
    zipped_data = zip(poll_config_list, poll_billing_list ,tcp_ip,tcp_port,poll_config_enable_list,poll_billing_enable_list,evc_type_list,run,METERID)
    
    return render_template(
        "Manual poll.html",
        tables=[df.to_html(classes="data")],
        titles=df.columns.values,
        zipped_data=zipped_data,
        selected_tag=selected_tag,
        selected_region=selected_region,
        region_options=region_options,
        tag_options=tag_options,df=df,run=run,METERID=METERID
        ,poll_config_list=poll_config_list,poll_billing_list=poll_billing_list,
        billing_list_str=billing_list_str,poll_billing_enable_list=poll_billing_enable_list,ip_str=ip_str,Port_str=Port_str,config_list_str=config_list_str,poll_billing_enable_str=poll_billing_enable_str,
        poll_config_enable_str=poll_config_enable_str,poll_config_enable_list=poll_config_enable_list,evc_type_list=evc_type_list
        # quantity_1=quantity_1
        # ,list_config=list_config,list_billing=list_billing,list_billing_enable=list_billing_enable,list_config_enable=list_config_enable
    )

    
    
@app.route("/Manualpoll_data", methods=["POST"])
def read_data():
    global change_to_32bit_counter  # Use the global variable
    slave_id = int(request.form["slave_id"])
    function_code = int(request.form["function_code"])
    
    tcp_ip = request.form["tcp_ip"]
    tcp_port = int(request.form["tcp_port"])
    evc_type = int(request.form["evc_type"])
    run = int(request.form["run"])
    run = run
    METERID = str(request.form["METERID"])
    
    poll_config_enable_list = str(request.form["poll_config_enable_list"])
    print(poll_config_enable_list)
    

    ##### config #####
    
    data= {'starting_address_i': [0], 
           'quantity_i': [0], 
           'adjusted_quantity_i': [7]}
    df = pd.DataFrame(data)
    print(df)
    df = df.append(data, ignore_index=True)
    for i in range(1, 6):
    
        if poll_config_enable_list[i-1] == '1':
            print(poll_config_enable_list)
            starting_address_i = int(request.form[f'starting_address_{i}'])
            quantity_i = int(request.form[f'quantity_{i}'])
            adjusted_quantity_i = quantity_i - starting_address_i + 1
            data= {'starting_address_i': [starting_address_i], 
                   'quantity_i': [quantity_i], 
                   'adjusted_quantity_i': [adjusted_quantity_i]}
            # df = df.append(data, ignore_index=True)
            
                    
            #print(df)
            #print(data)
        
        
        
    
    
    
    
        is_16bit = request.form.get("is_16bit") == "true"
        if is_16bit:
            bytes_per_value = 2
        else:
            bytes_per_value = 4
            if change_to_32bit_counter > 0:
                adjusted_quantity_i *= 2
                change_to_32bit_counter -= 1
    
        request_message_i = bytearray(
        [slave_id, function_code, starting_address_i >> 8, starting_address_i & 0xFF, adjusted_quantity_i >> 8, adjusted_quantity_i & 0xFF]
    )
        crc_i = computeCRC(request_message_i)
        request_message_i += crc_i.to_bytes(2, byteorder="big")

        sock_i = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock_i.connect((tcp_ip, tcp_port))
        communication_traffic_i = []
    
        # Store the TX message in communication_traffic_1
        communication_traffic_i.append({"direction": "TX", "data": request_message_i.hex()})
        sock_i.send(request_message_i)
        response_i = sock_i.recv(1024)
        # Store the RX message in communication_traffic_1
        communication_traffic_i.append({"direction": "RX", "data": response_i.hex()})
        # print(communication_traffic_i)
        dataframes = {
            'direction': [item['direction'] for item in communication_traffic_i],
            'data': [item['data'] for item in communication_traffic_i]
        }

        # สร้าง DataFrame จากลิสต์ของดิกชันนารี dataframes
        communication_traffic_df = pd.DataFrame(dataframes)
        # print(communication_traffic_df)
        sock_i.close()
        data_i = response_i[3:]
        
        values_i = [
            int.from_bytes(data_i[i: i + bytes_per_value], byteorder="big", signed=False)
            for i in range(0, len(data_i), bytes_per_value)
        ]
    
   
    
        if "32bit" in request.form and request.form["32bit"] == "true":
            is_32bit = True
        else:
            is_32bit = False
        data_list_i = []
        
        
        value = 0
        values_i = values_i[:-1]
        address = starting_address_i
        formatted_data = []
        evc_type = evc_type
        data_list_i = []
        for i, value in enumerate(values_i):
            address = starting_address_i + i * 2
            
        
            
            
            
            if address is not None:
                
                type_value = get_type_value_from_database(address, evc_type)
            
                if type_value is not None:
                    hex_value = hex(value)
                    binary_value = convert_to_binary_string(value, bytes_per_value)
                    ulong_value = value
                    float_value = struct.unpack("!f", struct.pack("!I", value))[0]
                    description = get_description_from_database(address)
                    if description is None:
                        description = f"Address {address}"
                        address += 0

                    if is_16bit:
                        signed_value = value - 2**16 if value >= 2**15 else value
                        is_16bit_value = True
                        float_display_value = f"16-bit signed: {signed_value}, float: {float_value}, ulong: {ulong_value}"
                    else:
                        signed_value = value - 2**32 if value >= 2**31 else value
                        is_16bit_value = False
                        float_value = (
                            float_value
                            if is_16bit_value
                            else struct.unpack("!f", struct.pack("!I", value))[0]
                        )
                        if type_value == "Float":
                            float_display_value = float_value
                        elif type_value == "signed":
                            float_display_value = signed_value
                        elif type_value == "Ulong":
                            float_display_value = ulong_value
                        elif type_value == "Date":
                            date_value_utc = datetime.datetime.utcfromtimestamp(value)
                            local_timezone = pytz.timezone('Asia/Bangkok')
                            date_value_local = date_value_utc.replace(tzinfo=datetime.timezone.utc).astimezone(local_timezone)
                            float_display_value = date_value_local.strftime("%d-%b-%y")
                        else:
                            float_display_value = "Undefined"
               
                    data_list_i.append(
                        {
                            "description": description,
                            "address": address,
                            "value": value,
                            # "hex_value": hex_value,
                            # "binary_value": binary_value,
                            
                            "float_value": float_display_value,
                        
                        }
                    )

                    # if i == len(values_i) - 1:
                    #     for float_display_value in data_list_i:
                    #         print(float_display_value)
    test = pd.DataFrame(data_list_i)
    # print(test)
    # test_2 = pd.DataFrame(data_list[1])
    # result = pd.concat([test, test_2])
    # print(result)
            

    
        
    combined_data = {
        "data_i": data_i,
        "communication_traffic_i": communication_traffic_i, 
    }
    
    session["tcp_ip"] = tcp_ip
    session["tcp_port"] = tcp_port
    
    if not is_16bit:
      
        data_list_16bit = []
        for data_16bit in data_list_i:
            address_16bit = data_16bit["address"]
            value_16bit = (
                data_16bit["value"] * 2
            )  
            data_list_16bit.append({"address": address_16bit, "value": value_16bit})
    
    
    # print(desired_data)
    # query = "SELECT ADDRESS FROM AMR_MAPPING_CONFIG WHERE evc_type = :evc_type AND address = :address ORDER BY OR_DER"

    # params = {"evc_type": evc_type, "address":address}
    # result = fetch_data(query, params)
    # # result_df = pd.DataFrame(result, columns=['DESCRIPTION', 'ADDRESS', 'float_value'])

    # print(result)
   
        
    
    
    


           
   
    
    region_query = """
        SELECT * FROM AMR_REGION 
        """
    
    tag_query = """
        SELECT DISTINCT TAG_ID
        FROM AMR_FIELD_ID
        JOIN AMR_PL_GROUP ON AMR_FIELD_ID.FIELD_ID = AMR_PL_GROUP.FIELD_ID 
        WHERE AMR_PL_GROUP.PL_REGION_ID = :region_id
        """
    region_results = fetch_data(region_query)
    
    region_options = [str(region[0]) for region in region_results]
    query = """
        SELECT
            AMR_FIELD_METER.METER_STREAM_NO as RunNo,
            AMR_PL_GROUP.PL_REGION_ID as region,
            AMR_FIELD_ID.TAG_ID as Sitename,
            AMR_FIELD_METER.METER_NO_STREAM as NoRun,
            AMR_FIELD_METER.METER_ID as METERID,
            AMR_VC_TYPE.VC_NAME as VCtype,
            AMR_FIELD_ID.SIM_IP as IPAddress,
            
             AMR_PORT_INFO.PORT_NO as port,
            amr_poll_range.evc_type as evc_type,
    
   amr_vc_type.vc_name as vc_name ,
   amr_poll_range.poll_billing as poll_billing ,
    amr_poll_range.poll_config as poll_config,
    amr_poll_range.poll_billing_enable as poll_billing_enable ,
   amr_poll_range.poll_config_enable as poll_config_enable
        FROM
            AMR_FIELD_ID,
            AMR_USER,
            AMR_FIELD_CUSTOMER,
            AMR_FIELD_METER,
            AMR_PL_GROUP,
            AMR_VC_TYPE,
            AMR_PORT_INFO,
            amr_poll_range
        WHERE
            AMR_USER.USER_ENABLE=1 AND
            amr_vc_type.id=amr_poll_range.evc_type AND
            AMR_FIELD_ID.FIELD_ID = AMR_PL_GROUP.FIELD_ID AND
            AMR_FIELD_ID.METER_ID = AMR_USER.USER_GROUP AND
            AMR_FIELD_ID.CUST_ID = AMR_FIELD_CUSTOMER.CUST_ID AND
            AMR_FIELD_ID.METER_ID = AMR_FIELD_METER.METER_ID AND
            AMR_VC_TYPE.ID = AMR_FIELD_METER.METER_STREAM_TYPE AND
            AMR_FIELD_METER.METER_PORT_NO = AMR_PORT_INFO.ID
            {tag_condition}
            {region_condition}
        """
    tag_condition = "AND AMR_FIELD_ID.TAG_ID IS NOT NULL"
    region_condition = "AND amr_pl_group.pl_region_id IS NOT NULL"
    selected_tag = request.args.get("tag_dropdown")
    selected_region = request.args.get("region_dropdown")
    region_results = fetch_data(region_query)
    region_options = [str(region[0]) for region in region_results]
    tag_results = fetch_data(tag_query, params={"region_id": selected_region})
    tag_options = [str(tag[0]) for tag in tag_results]
    # Sort the tag options alphabetically
    tag_options.sort()
    if selected_tag:
        tag_condition = f"AND AMR_FIELD_ID.TAG_ID = '{selected_tag}'"
    if selected_region:
        region_condition = f"AND amr_pl_group.pl_region_id = '{selected_region}'"
    query = query.format(tag_condition=tag_condition, region_condition=region_condition)
    
    df = pd.DataFrame(
        columns=[
            "RUN",
            "Region",
            "Sitename",
            "NoRun",
            "METERID",
            "VCtype",
            "IPAddress",
            "Port",
            "evc_type",
            "vc_name",
            "poll_billing",
            "poll_config",
            "poll_billing_enable",
            "poll_config_enable",
        ]
    )
    
    if selected_region:
        results = fetch_data(query)
        df = pd.DataFrame(
            results,
            columns=[
                "RUN",
                "Region",
                "Sitename",
                "NoRun",
                "METERID",
                "VCtype",
                "IPAddress",
                "Port",
                "evc_type",
                "vc_name",
                "poll_billing",
                "poll_config",
                "poll_billing_enable",
                "poll_config_enable",
            ],
        )
        METERID =df.get(["METERID"]).values.tolist()
        run = df.get(["RUN"]).values.tolist() 
        evc_type_list = df.get(["evc_type"]).values.tolist() 
       
        # print(evc_type_list)
        
        poll_config_list = df.get(["poll_config"]).values.tolist()
        # print(poll_config_list)
        
        if poll_config_list:
            config_list_str = str(poll_config_list).strip("[]'").split(",")
            # print(config_list_str)
        else:
        # Provide a default value if poll_config_list is empty
            config_list_str = [''] * 10
        poll_billing_list = df.get(["poll_billing"]).values.tolist()
        if poll_billing_list:
            billing_list_str = str(poll_billing_list[0]).strip("[]'").split(",")
            # print(billing_list_str)
        else:
        # Provide a default value if poll_config_list is empty
            billing_list_str = [''] * 20
        poll_config_enable_list = df.get(["poll_config_enable"]).values.tolist()
        
        if poll_config_enable_list:
            poll_config_enable_str = str(poll_config_enable_list).strip("[]'").split(",")
        else:
            poll_config_enable_str = [''] * 20
            
        poll_billing_enable_list = df.get(["poll_billing_enable"]).values.tolist()
        
        if poll_billing_enable_list:
            poll_billing_enable_str = str(poll_billing_enable_list).strip("[]'").split(",")
        else:
            poll_billing_enable_str = [''] * 20
        tcp_ip = df.get(["IPAddress"]).values.tolist()
        if tcp_ip:
            ip_str = str(tcp_ip[0]).strip("[]'").split(",")
            
        else:
        # Provide a default value if poll_config_list is empty
            ip_str = [''] 
        # print(ip_str)
        tcp_port = df.get(["Port"]).values.tolist()
        if tcp_port:
            Port_str = str(tcp_port[0]).strip("[]'").split(",")
            # print(Port_str)
        else:
        # Provide a default value if poll_config_list is empty
            Port_str = [''] 
    
        zipped_data = zip(poll_config_list, poll_billing_list ,tcp_ip,tcp_port,poll_config_enable_list,poll_billing_enable_list,evc_type_list,run,METERID)
        
    return render_template(
        "Manual poll.html",
        df=df,METERID=METERID,test=test,
        
        slave_id=slave_id,
        function_code=function_code,
        starting_address_i=starting_address_i,
        quantity_i=quantity_i,
        is_16bit=is_16bit,
        communication_traffic_i=communication_traffic_i,
        
        zipped_data=zipped_data,run=run,
        poll_config_list=poll_config_list,poll_billing_list=poll_billing_list,
        billing_list_str=billing_list_str,poll_config_enable_list=poll_config_enable_list,poll_billing_enable_list=poll_billing_enable_list,evc_type_list=evc_type_list,
        
        tables=[df.to_html(classes="data")],
        titles=df.columns.values,
        selected_tag=selected_tag,
        selected_region=selected_region,
        region_options=region_options,
        tag_options=tag_options,combined_data=combined_data
    )
    
    
def handle_actaris_action(i, address):
    return address
def handle_action_configuration(i, value, address):
    return value, address




    
@app.route("/process_selected_rows", methods=["POST"])
def process_selected_rows():
    selected_rows = request.form.getlist("selected_rows")
    return "Selected rows processed successfully"


def get_description_from_database_billing(address):
    query = "SELECT DESCRIPTION FROM amr_mapping_billing WHERE ADDRESS = :address"
    params = {"address": address}
    result = fetch_data(query, params)
    
    return result[0][0] if result else None
def get_type_value_from_database_billing(address,evc_type):
    query = "SELECT data_type FROM amr_mapping_billing WHERE ADDRESS = :address AND evc_type = :evc_type "
    result = fetch_data(query, params={"address": address, "evc_type" :evc_type})
    
    if result:
        return result[0][0]  
    return None



def get_description_from_database(address):
    query = "SELECT DESCRIPTION FROM AMR_MAPPING_CONFIG WHERE ADDRESS = :address order by address DESC"
    params = {"address": address}
    result = fetch_data(query, params)
    return result[0][0] if result else None


# def get_address_from_database(evc_type, address):
#     query = "SELECT address, or_der FROM AMR_MAPPING_CONFIG WHERE evc_type = :evc_type AND ADDRESS = :address  ORDER BY or_der "
#     params = {"evc_type": evc_type, "address": address}
    
#     result = fetch_data(query, params)
    
#     return result[0][0] if result else None


# def get_address_test_from_database(te,evc_type):
    
#     query = "SELECT address FROM AMR_MAPPING_CONFIG WHERE  ADDRESS = :te AND evc_type = :evc_type  ORDER BY or_der "
#     params = {"te": te,"evc_type": evc_type}
    
#     result = fetch_data(query, params)
#     # print(result)
    
#     return result[0][0] if result else None

def get_type_value_from_database(address,evc_type):
    query = "SELECT data_type FROM AMR_MAPPING_CONFIG WHERE ADDRESS = :address AND evc_type = :evc_type ORDER BY or_der" 
    result = fetch_data(query, params={"address": address , "evc_type" :evc_type })
    if result:
        return result[0][0] 
    return None


def insert_data(data_0,run, evc_type, METERID):
    try:
        with cx_Oracle.connect(username, password, f"{hostname}:{port}/{service_name}") as connection:
            with connection.cursor() as cursor:
                sql = """
                    INSERT INTO AMR_CONFIGURED_DATA (DATA_DATE, METER_STREAM_NO, AMR_VC_TYPE, METER_ID) 
                    VALUES (TO_DATE(:data_0, 'DD-MON-YY'), :run, :evc_type, :METERID)
                    """
                cursor.execute(sql, {'data_0': data_0, 'run': run, 'evc_type': evc_type, 'METERID': METERID})
                connection.commit()
                print("insert_data_ek successful")  
    except cx_Oracle.Error as error:
        print("Oracle Error:", error)

        







if __name__ == "__main__":
    app.run(debug=True)
