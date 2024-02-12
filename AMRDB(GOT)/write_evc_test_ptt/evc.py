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
from flask import g
app = Flask(__name__)
app.secret_key = "your_secret_key_here"
communication_traffic = []
change_to_32bit_counter = 0  # Initialize the counter to 2

def computeCRC(data):
  
    crc = 0xFFFF
    for byte in data:
        crc ^= byte
        for _ in range(8):
            if crc & 0x0001:
                crc >>= 1
                crc ^= 0xA001
            else:
                crc >>= 1
    return crc.to_bytes(2, byteorder="little")

def format_tx_message(slave_id, function_code, starting_address, quantity, data):
    tx_message = bytearray([
        slave_id,          
        function_code,       
        starting_address >> 8, starting_address & 0xFF,  
        quantity >> 8, quantity & 0xFF,                 
        len(data) // 1    
    ])
    tx_message.extend(data)
    
    crc = computeCRC(tx_message)
    tx_message += crc  
    
    return tx_message




@app.route('/manual_write')
def write_test():

    global tcp_ip, tcp_port
    return render_template('write_test_ptt.html', slave_id=0, function_code=0, starting_address=0, quantity=0, data_list=[], is_16bit=False, communication_traffic=communication_traffic)
@app.route('/manual_write', methods=['POST'])
def read_data_write():
    try:
        global change_to_32bit_counter, communication_traffic
        
        # Fetch form data
        slave_id = int(request.form['slave_id'])
        function_code = int(request.form['function_code'])
        starting_address = int(request.form['starting_address'])
        quantity = int(request.form['quantity'])
        tcp_ip = request.form['tcp_ip']
        tcp_port = int(request.form['tcp_port'])
        is_16bit = request.form.get('is_16bit') == 'true'

        # Adjust quantity based on data format
        if not is_16bit and change_to_32bit_counter > 0:
            quantity *= 2
            change_to_32bit_counter -= 1

        
        request_data = bytearray()
        for i in range(quantity // 2):
            data_i = float(request.form.get(f'data_{i}'))  
            request_data.extend(struct.pack('>f', data_i)) 

        
        request_message = format_tx_message(slave_id, function_code, starting_address, quantity, request_data)
       
        # Connect to Modbus TCP server
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((tcp_ip, tcp_port))
            communication_traffic = []

            communication_traffic.append({"direction": "TX", "data": request_message.hex()})
            sock.send(request_message)
            response = sock.recv(1024)

            communication_traffic.append({"direction": "RX", "data": response.hex()})

            data = response[3:]
            
            
         
            
            
            session['tcp_ip'] = tcp_ip
            session['tcp_port'] = tcp_port

    

        return render_template('write_test_ptt.html',  
            slave_id=slave_id,
            function_code=function_code,
            starting_address=starting_address,
            quantity=quantity,
            is_16bit=is_16bit,
            communication_traffic=communication_traffic,
            data=data,
            
           )
        
    except Exception as e:
        
        print("Error:", str(e))
        return render_template('error.html', error=str(e))


@app.before_request
def before_request():
    g.start = time.time()

@app.after_request
def after_request(response):
    diff = time.time() - g.start
    if diff > 15:
        print("Request took too long:", diff)
        
        return render_template('error.html',  error="Error sending data: Connection timed out")
    return response










if __name__ == "__main__":
    app.run(debug=True)
