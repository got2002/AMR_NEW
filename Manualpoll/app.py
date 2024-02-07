from flask import Flask, render_template, request,session
import socket
import struct
from pymodbus.utilities import computeCRC
app = Flask(__name__)
app.secret_key = "your_secret_key_here"
communication_traffic = []
change_to_32bit_counter = 0  # Initialize the counter to 2

def convert_to_binary_string(value, bytes_per_value):
    binary_string = bin(value)[2:]  # Convert the value to binary string excluding the '0b' prefix
    return binary_string.zfill(bytes_per_value * 8)  # Zero-fill to fit the number of bits based on bytes_per_value

@app.route('/Manualpoll')
def index():

    global tcp_ip, tcp_port
    return render_template('index.html', slave_id=0, function_code=0, starting_address=0, quantity=0, data_list=[], is_16bit=False, communication_traffic=communication_traffic)

@app.route('/Manualpoll', methods=['POST'])
def read_data_old():
    global change_to_32bit_counter  # Use the global variable
    
    

    slave_id = int(request.form['slave_id'])
    function_code = int(request.form['function_code'])
    starting_address = int(request.form['starting_address'])
    quantity = int(request.form['quantity'])
    tcp_ip = request.form['tcp_ip']
    tcp_port = int(request.form['tcp_port'])


    # Check if the data should be displayed in 16-bit format or 32-bit format
    is_16bit = request.form.get("is_16bit") == "true"

    if is_16bit:
        bytes_per_value = 2
    else:
        bytes_per_value = 4
        if change_to_32bit_counter > 0:
            quantity *= 2
            change_to_32bit_counter -= 1

    # Build the request message
    request_message = bytearray(
        [
            slave_id,
            function_code,
            starting_address >> 8,
            starting_address & 0xFF,
            quantity >> 8,
            quantity & 0xFF,
        ]
    )

    crc = computeCRC(request_message)
    request_message += crc.to_bytes(2, byteorder="big")

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((tcp_ip, tcp_port))

    # Store the TX message in communication_traffic
    communication_traffic.append({"direction": "TX", "data": request_message.hex()})

    sock.send(request_message)

    response = sock.recv(1024)

    # Store the RX message in communication_traffic
    communication_traffic.append({"direction": "RX", "data": response.hex()})

    sock.close()

    data = response[3:]

    values = [
        int.from_bytes(data[i : i + bytes_per_value], byteorder="big", signed=False)
        for i in range(0, len(data), bytes_per_value)
    ]
    data_list = []
    values = values[:-1]
    address = starting_address
    for i, value in enumerate(values):
        address = starting_address + i
        hex_value = hex(value)  # Convert the decimal value to HEX
        binary_value = convert_to_binary_string(value, bytes_per_value)  # Convert the decimal value to Binary

        # Calculate the 32-bit Float Decimal Representation
        float_value = struct.unpack('!f', struct.pack('!I', value))[0]
        if is_16bit:
            signed_value = value - 2**16 if value >= 2**15 else value
            is_16bit_value = True
            float_value = value if is_16bit_value else float_value
            float_display_value = f"16-bit signed: {signed_value}, float: {float_value}"
        else:
            signed_value = value - 2**32 if value >= 2**31 else value
            is_16bit_value = False
            float_value = (
                float_value
                if is_16bit_value
                else struct.unpack("!f", struct.pack("!I", value))[0]
            )
            float_signed_value = (
                signed_value if is_16bit_value else None
            )  # Set signed_value to None for 32-bit
          
        data_list.append({
            'address': address,
            'value': value,
            'hex_value': hex_value,
            'binary_value': binary_value,
            'float_value': float_value  # Add the Decimal Representation to the data list
        })
    # Store the RX message in communication_traffic

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

    return render_template('index.html', data_list=data_list, slave_id=slave_id, function_code=function_code,
                           starting_address=starting_address, quantity=quantity, is_16bit=is_16bit, communication_traffic=communication_traffic)

if __name__ == '__main__':
    app.run(debug=True)
