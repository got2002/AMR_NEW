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


def connect_to_ptt_pivot_db():
    global active_connection
    username = "PTT_PIVOT"
    password = "PTT_PIVOT"
    hostname = "10.100.56.3"
    port = "1521"
    service_name = "PTTAMR_MST"

    try:
        dsn = cx_Oracle.makedsn(hostname, port, service_name=service_name)
        connection = cx_Oracle.connect(username, password, dsn)
        active_connection = "PTT_PIVOT"
        print("Connected to PTT PIVOT database")
        return connection
    except cx_Oracle.Error as e:
        (error,) = e.args
        print("Oracle Error:", error)
        return None

def fetch_data(connection, query, params=None):
    try:
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







@app.route("/write_evc_old",methods=["GET"])
def Manualpoll_data_old():
    with connect_to_ptt_pivot_db() as ptt_pivot_connection:
        print("Active Connection:", active_connection)
       
        region_query = """
            SELECT * FROM AMR_REGION 
        """
        tag_query = """
            SELECT DISTINCT TAG_ID
            FROM AMR_FIELD_ID, AMR_PL_GROUP
            WHERE AMR_FIELD_ID.FIELD_ID = AMR_PL_GROUP.FIELD_ID
            AND AMR_PL_GROUP.PL_REGION_ID = :region_id
        """
        run_query = """
            SELECT DISTINCT METER_STREAM_NO
            FROM AMR_FIELD_ID , amr_field_meter
            WHERE amr_field_id.meter_id = amr_field_meter.meter_id
            AND amr_field_id.tag_id = :tag_id
        """
        region_results = fetch_data(ptt_pivot_connection,region_query)
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
                AMR_PORT_INFO.PORT_NO as port
            FROM
                AMR_FIELD_ID,
                AMR_USER,
                AMR_FIELD_CUSTOMER,
                AMR_FIELD_METER,
                AMR_PL_GROUP,
                AMR_VC_TYPE,
                AMR_PORT_INFO
            WHERE
                AMR_USER.USER_ENABLE=1 AND
                AMR_FIELD_ID.FIELD_ID = AMR_PL_GROUP.FIELD_ID AND
                AMR_FIELD_ID.METER_ID = AMR_USER.USER_GROUP AND
                AMR_FIELD_ID.CUST_ID = AMR_FIELD_CUSTOMER.CUST_ID AND
                AMR_FIELD_ID.METER_ID = AMR_FIELD_METER.METER_ID AND
                AMR_VC_TYPE.ID = AMR_FIELD_METER.METER_STREAM_TYPE AND
                AMR_FIELD_METER.METER_PORT_NO = AMR_PORT_INFO.ID
                {tag_condition}
                {region_condition}
                {run_condition}
        """

        tag_condition = "AND AMR_FIELD_ID.TAG_ID IS NOT NULL"
        region_condition = "AND amr_pl_group.pl_region_id = 'default_region_id'"
        run_condition = "AND AMR_FIELD_METER.METER_STREAM_NO IS NOT NULL"

        selected_tag = request.args.get("tag_dropdown")
        selected_region = request.args.get("region_dropdown")
        selected_run = request.args.get("run_dropdown")

        region_results = fetch_data(ptt_pivot_connection,region_query)
        region_options = [str(region[0]) for region in region_results]

        tag_results = fetch_data(ptt_pivot_connection,tag_query, params={"region_id": selected_region})
        tag_options = [str(tag[0]) for tag in tag_results]

        run_results = fetch_data(ptt_pivot_connection,run_query, params={"tag_id": selected_tag})
        run_options = [str(run[0]) for run in run_results]

        # Sort the tag options alphabetically
        tag_options.sort()

        

        if selected_tag:
            tag_condition = f"AND AMR_FIELD_ID.TAG_ID = '{selected_tag}'"
        if selected_region:
            region_condition = f"AND amr_pl_group.pl_region_id = '{selected_region}'"
        if selected_run:
            run_condition = f"AND AMR_FIELD_METER.METER_STREAM_NO = {selected_run}"


        query = query.format(tag_condition=tag_condition, region_condition=region_condition, run_condition=run_condition)

        results = fetch_data(ptt_pivot_connection,query)
        
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
            ],
        )
    tcp_ip = df.get(["IPAddress"]).values.tolist()
    if tcp_ip:
        ip_str = str(tcp_ip).strip("['']")
        print(ip_str)
    else:
        ip_str = [''] 


    tcp_port = df.get(["Port"]).values.tolist()
    if tcp_port:
        Port_str = str(tcp_port).strip("['']")
    else:
        Port_str = [''] 
    
    return render_template(
        "write_evc_old.html",
        tables=[df.to_html(classes="data")],
        titles=df.columns.values,
        selected_tag=selected_tag,
        selected_region=selected_region,
        selected_run=selected_run,
        region_options=region_options,
        tag_options=tag_options,
        run_options=run_options,
        df=df,ip_str=ip_str,tcp_port=tcp_port,Port_str=Port_str,tcp_ip=tcp_ip
    )


@app.route('/write_evc_old', methods=['POST'])
def read_data_old():
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

    
        with connect_to_ptt_pivot_db() as ptt_pivot_connection:
            print("Active Connection:", active_connection)
        
            region_query = """
                SELECT * FROM AMR_REGION 
            """
            tag_query = """
                SELECT DISTINCT TAG_ID
                FROM AMR_FIELD_ID, AMR_PL_GROUP
                WHERE AMR_FIELD_ID.FIELD_ID = AMR_PL_GROUP.FIELD_ID
                AND AMR_PL_GROUP.PL_REGION_ID = :region_id
            """
            run_query = """
                SELECT DISTINCT METER_STREAM_NO
                FROM AMR_FIELD_ID , amr_field_meter
                WHERE amr_field_id.meter_id = amr_field_meter.meter_id
                AND amr_field_id.tag_id = :tag_id
            """
            region_results = fetch_data(ptt_pivot_connection,region_query)
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
                    AMR_PORT_INFO.PORT_NO as port
                FROM
                    AMR_FIELD_ID,
                    AMR_USER,
                    AMR_FIELD_CUSTOMER,
                    AMR_FIELD_METER,
                    AMR_PL_GROUP,
                    AMR_VC_TYPE,
                    AMR_PORT_INFO
                WHERE
                    AMR_USER.USER_ENABLE=1 AND
                    AMR_FIELD_ID.FIELD_ID = AMR_PL_GROUP.FIELD_ID AND
                    AMR_FIELD_ID.METER_ID = AMR_USER.USER_GROUP AND
                    AMR_FIELD_ID.CUST_ID = AMR_FIELD_CUSTOMER.CUST_ID AND
                    AMR_FIELD_ID.METER_ID = AMR_FIELD_METER.METER_ID AND
                    AMR_VC_TYPE.ID = AMR_FIELD_METER.METER_STREAM_TYPE AND
                    AMR_FIELD_METER.METER_PORT_NO = AMR_PORT_INFO.ID
                    {tag_condition}
                    {region_condition}
                    {run_condition}
            """

            tag_condition = "AND AMR_FIELD_ID.TAG_ID IS NOT NULL"
            region_condition = "AND amr_pl_group.pl_region_id = 'default_region_id'"
            run_condition = "AND AMR_FIELD_METER.METER_STREAM_NO IS NOT NULL"

            selected_tag = request.args.get("tag_dropdown")
            selected_region = request.args.get("region_dropdown")
            selected_run = request.args.get("run_dropdown")

            region_results = fetch_data(ptt_pivot_connection,region_query)
            region_options = [str(region[0]) for region in region_results]

            tag_results = fetch_data(ptt_pivot_connection,tag_query, params={"region_id": selected_region})
            tag_options = [str(tag[0]) for tag in tag_results]

            run_results = fetch_data(ptt_pivot_connection,run_query, params={"tag_id": selected_tag})
            run_options = [str(run[0]) for run in run_results]

            # Sort the tag options alphabetically
            tag_options.sort()

            

            if selected_tag:
                tag_condition = f"AND AMR_FIELD_ID.TAG_ID = '{selected_tag}'"
            if selected_region:
                region_condition = f"AND amr_pl_group.pl_region_id = '{selected_region}'"
            if selected_run:
                run_condition = f"AND AMR_FIELD_METER.METER_STREAM_NO = {selected_run}"


            query = query.format(tag_condition=tag_condition, region_condition=region_condition, run_condition=run_condition)

            results = fetch_data(ptt_pivot_connection,query)
            
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
                ],
            )
        tcp_ip = df.get(["IPAddress"]).values.tolist()
        if tcp_ip:
            ip_str = str(tcp_ip).strip("['']")
            print(ip_str)
        else:
            ip_str = [''] 


        tcp_port = df.get(["Port"]).values.tolist()
        if tcp_port:
            Port_str = str(tcp_port).strip("['']")
        else:
            Port_str = [''] 
        

        return render_template('write_evc_old.html',   df=df,

            slave_id=slave_id,
            function_code=function_code,
            starting_address=starting_address,
            quantity=quantity,
            is_16bit=is_16bit,
            communication_traffic=communication_traffic,
            data=data,
            tables=[df.to_html(classes="data")],
            titles=df.columns.values,
            selected_tag=selected_tag,
            selected_region=selected_region,
            region_options=region_options,
            tag_options=tag_options,ip_str=ip_str,tcp_port=tcp_port,Port_str=Port_str,tcp_ip=tcp_ip)
        
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




@app.route("/get_tags", methods=["GET"])
def get_tags():
    with connect_to_ptt_pivot_db() as ptt_pivot_connection:
        print("Active Connection:", active_connection)
        selected_region = request.args.get("selected_region")

        tag_query = """
                SELECT DISTINCT TAG_ID
                FROM AMR_FIELD_ID, AMR_PL_GROUP
                WHERE AMR_FIELD_ID.FIELD_ID = AMR_PL_GROUP.FIELD_ID
                AND AMR_PL_GROUP.PL_REGION_ID = :region_id
            """

        tag_results = fetch_data(ptt_pivot_connection,tag_query, params={"region_id": selected_region})
        tag_options = [str(tag[0]) for tag in tag_results]
        tag_options.sort()
        return jsonify({"tag_options": tag_options})
    

@app.route("/get_runs", methods=["GET"])
def get_runs():
    with connect_to_ptt_pivot_db() as ptt_pivot_connection:
        print("Active Connection:", active_connection)
        selected_tag = request.args.get("selected_tag")

        run_query = """
            SELECT DISTINCT METER_STREAM_NO
            FROM AMR_FIELD_ID , amr_field_meter
            WHERE amr_field_id.meter_id = amr_field_meter.meter_id
            AND amr_field_id.tag_id = :tag_id
        """

        run_results = fetch_data(ptt_pivot_connection,run_query, params={"tag_id": selected_tag})
        run_options = [str(run[0]) for run in run_results]
        run_options.sort()
        return jsonify({"run_options": run_options})
    






if __name__ == "__main__":
    app.run(debug=True)
