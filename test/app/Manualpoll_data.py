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


from flask import Blueprint
from flask import Flask, render_template

from .connect_db import fetch_data,connect_to_amr_db,connect_to_ptt_pivot_db

Manualpoll_data = Blueprint('Manualpoll', __name__)






communication_traffic = []
change_to_32bit_counter = 1  # Initialize the counter to 2
def convert_to_binary_string(value, bytes_per_value):
    binary_string = bin(value)[
        2:
    ]  # Convert the value to binary string excluding the '0b' prefix
    return binary_string.zfill(
        bytes_per_value * 8
    )

@Manualpoll_data.route("/get_tags", methods=["GET"])
def get_tags():
    with connect_to_amr_db() as amr_connection:
        print("Active Connection:", active_connection)
        selected_region = request.args.get("selected_region")
        tag_query = """
        SELECT DISTINCT TAG_ID
        FROM AMR_FIELD_ID
        JOIN AMR_PL_GROUP ON AMR_FIELD_ID.FIELD_ID = AMR_PL_GROUP.FIELD_ID 
        WHERE AMR_PL_GROUP.PL_REGION_ID = :region_id
        """
        tag_results = fetch_data(active_connection,tag_query, params={"region_id": selected_region})
        tag_options = [str(tag[0]) for tag in tag_results]
        tag_options.sort()
        return jsonify({"tag_options": tag_options})






@Manualpoll_data.route("/Manualpoll_data")
def Manualpoll():
    with connect_to_amr_db() as amr_connection:
        print("Active Connection:", active_connection)
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
        region_results = fetch_data(amr_connection,region_query)
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
        region_results = fetch_data(amr_connection,region_query)
        region_options = [str(region[0]) for region in region_results]
        tag_results = fetch_data(amr_connection,tag_query, params={"region_id": selected_region})
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
        
        zipped_data = zip(poll_config_list, poll_billing_list ,tcp_ip,tcp_port,poll_config_enable_list,poll_billing_enable_list)
        return render_template(
            "Manual poll.html",
            tables=[df.to_html(classes="data")],
            titles=df.columns.values,
            zipped_data=zipped_data,
            selected_tag=selected_tag,
            selected_region=selected_region,
            region_options=region_options,
            tag_options=tag_options,df=df
            ,poll_config_list=poll_config_list,poll_billing_list=poll_billing_list,
            billing_list_str=billing_list_str,poll_billing_enable_list=poll_billing_enable_list,ip_str=ip_str,Port_str=Port_str,config_list_str=config_list_str,poll_billing_enable_str=poll_billing_enable_str,
            poll_config_enable_str=poll_config_enable_str,poll_config_enable_list=poll_config_enable_list
            # quantity_1=quantity_1
            # ,list_config=list_config,list_billing=list_billing,list_billing_enable=list_billing_enable,list_config_enable=list_config_enable
        )
    @Manualpoll_data.route("/Manualpoll_data", methods=["POST"])
    def read_data():
        global change_to_32bit_counter  # Use the global variable
        slave_id = int(request.form["slave_id"])
        function_code = int(request.form["function_code"])
        starting_address_1 = int(request.form['starting_address_1'])
        quantity_1 = int(request.form['quantity_1'])
        adjusted_quantity_1 = quantity_1 - starting_address_1 + 1
        starting_address_2 = int(request.form['starting_address_2'])
        quantity_2 = int(request.form['quantity_2'])
        adjusted_quantity_2 = quantity_2 - starting_address_2 + 1
        starting_address_3 = int(request.form['starting_address_3'])
        quantity_3 = int(request.form['quantity_3'])
        adjusted_quantity_3 = quantity_3 - starting_address_3 + 1
        starting_address_4 = int(request.form['starting_address_4'])
        quantity_4 = int(request.form['quantity_4'])
        adjusted_quantity_4 = quantity_4- starting_address_4 + 1
        starting_address_5 = int(request.form['starting_address_5'])
        quantity_5 = int(request.form['quantity_5'])
        adjusted_quantity_5 = quantity_5- starting_address_5 + 1
        
        starting_address_6 = int(request.form['starting_address_6'])
        quantity_6 = int(request.form['quantity_6'])
        adjusted_quantity_6 = quantity_6 - starting_address_6 + 1
        starting_address_7 = int(request.form['starting_address_7'])
        quantity_7 = int(request.form['quantity_7'])
        adjusted_quantity_7 = quantity_7 - starting_address_7 + 1
        starting_address_8 = int(request.form['starting_address_8'])
        quantity_8 = int(request.form['quantity_8'])
        adjusted_quantity_8 = quantity_8 - starting_address_8 + 1
        starting_address_9 = int(request.form['starting_address_9'])
        quantity_9 = int(request.form['quantity_9'])
        adjusted_quantity_9 = quantity_9 - starting_address_9 + 1
        starting_address_10 = int(request.form['starting_address_10'])
        quantity_10 = int(request.form['quantity_10'])
        adjusted_quantity_10 = quantity_10 - starting_address_10 + 1
        starting_address_11 = int(request.form['starting_address_11'])
        quantity_11 = int(request.form['quantity_11'])
        adjusted_quantity_11 = quantity_11 - starting_address_11 + 1
        starting_address_12 = int(request.form['starting_address_12'])
        quantity_12 = int(request.form['quantity_12'])
        adjusted_quantity_12 = quantity_12 - starting_address_12 + 1
        starting_address_13 = int(request.form['starting_address_13'])
        quantity_13 = int(request.form['quantity_13'])
        adjusted_quantity_13 = quantity_13 - starting_address_13 + 1
        starting_address_14 = int(request.form['starting_address_14'])
        quantity_14 = int(request.form['quantity_14'])
        adjusted_quantity_14 = quantity_14 - starting_address_14 + 1
        starting_address_15 = int(request.form['starting_address_15'])
        quantity_15 = int(request.form['quantity_15'])
        adjusted_quantity_15 = quantity_15 - starting_address_15 + 1
    
        tcp_ip = request.form["tcp_ip"]
        tcp_port = int(request.form["tcp_port"])
        # Check if the data should be displayed in 16-bit format or 32-bit format
        is_16bit = request.form.get("is_16bit") == "true"
        if is_16bit:
            bytes_per_value = 2
        else:
            bytes_per_value = 4
            if change_to_32bit_counter > 0:
                adjusted_quantity_1 *= 2
                adjusted_quantity_2 *= 2
                adjusted_quantity_3 *= 2
                adjusted_quantity_4 *= 2
                adjusted_quantity_5 *= 2
                adjusted_quantity_6 *= 2
                adjusted_quantity_7 *= 2
                adjusted_quantity_8 *= 2
                adjusted_quantity_9 *= 2
                adjusted_quantity_10 *= 2
                adjusted_quantity_11*= 2
                adjusted_quantity_12*= 2
                adjusted_quantity_13*= 2
                adjusted_quantity_14*= 2
                adjusted_quantity_15*= 2
                change_to_32bit_counter -= 1
        # Build the request message
        request_message_1 = bytearray(
        [slave_id, function_code, starting_address_1 >> 8, starting_address_1 & 0xFF, adjusted_quantity_1 >> 8, adjusted_quantity_1 & 0xFF]
    )
        crc_1 = computeCRC(request_message_1)
        request_message_1 += crc_1.to_bytes(2, byteorder="big")
        request_message_2 = bytearray(
        [slave_id, function_code, starting_address_2 >> 8, starting_address_2 & 0xFF, adjusted_quantity_2 >> 8, adjusted_quantity_2 & 0xFF]
    )
        crc_2 = computeCRC(request_message_2)
        request_message_2 += crc_2.to_bytes(2, byteorder="big")
        request_message_3 = bytearray(
        [slave_id, function_code, starting_address_3 >> 8, starting_address_3 & 0xFF, adjusted_quantity_3 >> 8, adjusted_quantity_3 & 0xFF]
    )
        crc_3 = computeCRC(request_message_3)
        request_message_3 += crc_3.to_bytes(2, byteorder="big")
        request_message_4 = bytearray(
        [slave_id, function_code, starting_address_4 >> 8, starting_address_4 & 0xFF, adjusted_quantity_4 >> 8, adjusted_quantity_4 & 0xFF]
    )
        crc_4 = computeCRC(request_message_4)
        request_message_4 += crc_4.to_bytes(2, byteorder="big")
        request_message_5 = bytearray(
        [slave_id, function_code, starting_address_5 >> 8, starting_address_5 & 0xFF, adjusted_quantity_5 >> 8, adjusted_quantity_5 & 0xFF]
    )
        crc_5 = computeCRC(request_message_5)
        request_message_5 += crc_5.to_bytes(2, byteorder="big")
        request_message_6 = bytearray(
        [slave_id, function_code, starting_address_6 >> 8, starting_address_6 & 0xFF, adjusted_quantity_6 >> 8, adjusted_quantity_6 & 0xFF]
    )
        crc_6 = computeCRC(request_message_6)
        request_message_6 += crc_6.to_bytes(2, byteorder="big")
        
        request_message_7 = bytearray(
        [slave_id, function_code, starting_address_7 >> 8, starting_address_7 & 0xFF, adjusted_quantity_7 >> 8, adjusted_quantity_7 & 0xFF]
    )
        crc_7 = computeCRC(request_message_7)
        request_message_7 += crc_7.to_bytes(2, byteorder="big")
        request_message_8 = bytearray(
        [slave_id, function_code, starting_address_8 >> 8, starting_address_8 & 0xFF, adjusted_quantity_8 >> 8, adjusted_quantity_8 & 0xFF]
    )
        crc_8 = computeCRC(request_message_8)
        request_message_8 += crc_8.to_bytes(2, byteorder="big")
        request_message_9 = bytearray(
        [slave_id, function_code, starting_address_9 >> 8, starting_address_9 & 0xFF, adjusted_quantity_9 >> 8, adjusted_quantity_9 & 0xFF]
    )
        crc_9 = computeCRC(request_message_9)
        request_message_9 += crc_9.to_bytes(2, byteorder="big")
        request_message_10 = bytearray(
        [slave_id, function_code, starting_address_10 >> 8, starting_address_10 & 0xFF, adjusted_quantity_10 >> 8, adjusted_quantity_10 & 0xFF]
    )
        crc_10 = computeCRC(request_message_10)
        request_message_10 += crc_10.to_bytes(2, byteorder="big")
        request_message_11 = bytearray(
        [slave_id, function_code, starting_address_11 >> 8, starting_address_11 & 0xFF, adjusted_quantity_11 >> 8, adjusted_quantity_11 & 0xFF]
    )
        crc_11 = computeCRC(request_message_11)
        request_message_11 += crc_11.to_bytes(2, byteorder="big")
        request_message_12 = bytearray(
        [slave_id, function_code, starting_address_12 >> 8, starting_address_12 & 0xFF, adjusted_quantity_12 >> 8, adjusted_quantity_12 & 0xFF]
    )
        crc_12 = computeCRC(request_message_12)
        request_message_12 += crc_12.to_bytes(2, byteorder="big")
        request_message_13 = bytearray(
        [slave_id, function_code, starting_address_13 >> 8, starting_address_13 & 0xFF, adjusted_quantity_13 >> 8, adjusted_quantity_13 & 0xFF]
    )
        crc_13 = computeCRC(request_message_13)
        request_message_13 += crc_13.to_bytes(2, byteorder="big")
        request_message_14 = bytearray(
        [slave_id, function_code, starting_address_14 >> 8, starting_address_14 & 0xFF, adjusted_quantity_14 >> 8, adjusted_quantity_14 & 0xFF]
    )
        crc_14 = computeCRC(request_message_14)
        request_message_14 += crc_14.to_bytes(2, byteorder="big")
        request_message_15 = bytearray(
        [slave_id, function_code, starting_address_15 >> 8, starting_address_15 & 0xFF, adjusted_quantity_15 >> 8, adjusted_quantity_15 & 0xFF]
    )
        crc_15 = computeCRC(request_message_15)
        request_message_15 += crc_15.to_bytes(2, byteorder="big")
        
        sock_1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock_1.connect((tcp_ip, tcp_port))
        communication_traffic_1 = []
        # Store the TX message in communication_traffic_1
        communication_traffic_1.append({"direction": "TX", "data": request_message_1.hex()})
        sock_1.send(request_message_1)
        response_1 = sock_1.recv(1024)
        # Store the RX message in communication_traffic_1
        communication_traffic_1.append({"direction": "RX", "data": response_1.hex()})
        sock_1.close()
        data_1 = response_1[3:]
        
        values_1 = [
            int.from_bytes(data_1[i: i + bytes_per_value], byteorder="big", signed=False)
            for i in range(0, len(data_1), bytes_per_value)
        ]
        
        sock_2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock_2.connect((tcp_ip, tcp_port))
        communication_traffic_2 = []
        
        # Store the TX message in communicat    ion_traffic_1
        communication_traffic_2.append({"direction": "TX", "data": request_message_2.hex()})
        sock_2.send(request_message_2)
        response_2 = sock_2.recv(1024)
        # Store the RX message in communication_traffic_1
        communication_traffic_2.append({"direction": "RX", "data": response_2.hex()})
        sock_2.close()
        data_2 = response_2[3:]
        
        values_2 = [
            int.from_bytes(data_2[i: i + bytes_per_value], byteorder="big", signed=False)
            for i in range(0, len(data_2), bytes_per_value)
        ]
        sock_3 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock_3.connect((tcp_ip, tcp_port))
        communication_traffic_3 = []
        
        # Store the TX message in communicat    ion_traffic_1
        communication_traffic_3.append({"direction": "TX", "data": request_message_3.hex()})
        sock_3.send(request_message_3)
        response_3 = sock_3.recv(1024)
        # Store the RX message in communication_traffic_1
        communication_traffic_3.append({"direction": "RX", "data": response_3.hex()})
        sock_3.close()
        data_3 = response_3[3:]
        
        values_3 = [
            int.from_bytes(data_3[i: i + bytes_per_value], byteorder="big", signed=False)
            for i in range(0, len(data_3), bytes_per_value)
        ]
        sock_4 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock_4.connect((tcp_ip, tcp_port))
        communication_traffic_4 = []
        
        # Store the TX message in communicat    ion_traffic_1
        communication_traffic_4.append({"direction": "TX", "data": request_message_4.hex()})
        sock_4.send(request_message_4)
        response_4 = sock_4.recv(1024)
        # Store the RX message in communication_traffic_1
        communication_traffic_4.append({"direction": "RX", "data": response_4.hex()})
        sock_4.close()
        data_4 = response_4[3:]
        
        values_4 = [
            int.from_bytes(data_4[i: i + bytes_per_value], byteorder="big", signed=False)
            for i in range(0, len(data_4), bytes_per_value)
        ]
        sock_5 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock_5.connect((tcp_ip, tcp_port))
        communication_traffic_5 = []
        
        # Store the TX message in communicat    ion_traffic_1
        communication_traffic_5.append({"direction": "TX", "data": request_message_5.hex()})
        sock_5.send(request_message_5)
        response_5 = sock_5.recv(1024)
        # Store the RX message in communication_traffic_1
        communication_traffic_5.append({"direction": "RX", "data": response_5.hex()})
        sock_5.close()
        data_5 = response_5[3:]
        
        values_5 = [
            int.from_bytes(data_5[i: i + bytes_per_value], byteorder="big", signed=False)
            for i in range(0, len(data_5), bytes_per_value)
        ]
        sock_6 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock_6.connect((tcp_ip, tcp_port))
        communication_traffic_6 = []
        
        # Store the TX message in communicat    ion_traffic_1
        communication_traffic_6.append({"direction": "TX", "data": request_message_6.hex()})
        sock_6.send(request_message_6)
        response_6 = sock_6.recv(1024)
        # Store the RX message in communication_traffic_1
        communication_traffic_6.append({"direction": "RX", "data": response_6.hex()})
        sock_6.close()
        data_6 = response_6[3:]
        
        values_6 = [
            int.from_bytes(data_6[i: i + bytes_per_value], byteorder="big", signed=False)
            for i in range(0, len(data_6), bytes_per_value)
        ]
        sock_7 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock_7.connect((tcp_ip, tcp_port))
        communication_traffic_7 = []
        
        # Store the TX message in communicat    ion_traffic_1
        communication_traffic_7.append({"direction": "TX", "data": request_message_7.hex()})
        sock_7.send(request_message_7)
        response_7 = sock_7.recv(1024)
        # Store the RX message in communication_traffic_1
        communication_traffic_7.append({"direction": "RX", "data": response_7.hex()})
        sock_7.close()
        data_7 = response_7[3:]
        
        values_7 = [
            int.from_bytes(data_7[i: i + bytes_per_value], byteorder="big", signed=False)
            for i in range(0, len(data_7), bytes_per_value)
        ]
        sock_8 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock_8.connect((tcp_ip, tcp_port))
        communication_traffic_8 = []
        
        # Store the TX message in communicat    ion_traffic_1
        communication_traffic_8.append({"direction": "TX", "data": request_message_8.hex()})
        sock_8.send(request_message_8)
        response_8 = sock_8.recv(1024)
        # Store the RX message in communication_traffic_1
        communication_traffic_8.append({"direction": "RX", "data": response_8.hex()})
        sock_8.close()
        data_8 = response_8[3:]
        
        values_8 = [
            int.from_bytes(data_8[i: i + bytes_per_value], byteorder="big", signed=False)
            for i in range(0, len(data_8), bytes_per_value)
        ]
        sock_9 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock_9.connect((tcp_ip, tcp_port))
        communication_traffic_9 = []
        
        # Store the TX message in communicat    ion_traffic_1
        communication_traffic_9.append({"direction": "TX", "data": request_message_9.hex()})
        sock_9.send(request_message_9)
        response_9 = sock_9.recv(1024)
        # Store the RX message in communication_traffic_1
        communication_traffic_9.append({"direction": "RX", "data": response_9.hex()})
        sock_9.close()
        data_9 = response_9[3:]
        
        values_9 = [
            int.from_bytes(data_9[i: i + bytes_per_value], byteorder="big", signed=False)
            for i in range(0, len(data_9), bytes_per_value)
        ]
        sock_10 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock_10.connect((tcp_ip, tcp_port))
        communication_traffic_10 = []
        
        # Store the TX message in communicat    ion_traffic_1
        communication_traffic_10.append({"direction": "TX", "data": request_message_10.hex()})
        sock_10.send(request_message_10)
        response_10 = sock_10.recv(1024)
        # Store the RX message in communication_traffic_1
        communication_traffic_10.append({"direction": "RX", "data": response_10.hex()})
        sock_10.close()
        data_10 = response_10[3:]
        
        values_10 = [
            int.from_bytes(data_10[i: i + bytes_per_value], byteorder="big", signed=False)
            for i in range(0, len(data_10), bytes_per_value)
        ]
        sock_11 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock_11.connect((tcp_ip, tcp_port))
        communication_traffic_11 = []
        
        # Store the TX message in communicat    ion_traffic_1
        communication_traffic_11.append({"direction": "TX", "data": request_message_11.hex()})
        sock_11.send(request_message_11)
        response_11 = sock_11.recv(1024)
        # Store the RX message in communication_traffic_1
        communication_traffic_11.append({"direction": "RX", "data": response_11.hex()})
        sock_11.close()
        data_11 = response_11[3:]
        
        values_11 = [
            int.from_bytes(data_11[i: i + bytes_per_value], byteorder="big", signed=False)
            for i in range(0, len(data_11), bytes_per_value)
        ]
        sock_12 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock_12.connect((tcp_ip, tcp_port))
        communication_traffic_12 = []
        
        # Store the TX message in communicat    ion_traffic_1
        communication_traffic_12.append({"direction": "TX", "data": request_message_12.hex()})
        sock_12.send(request_message_12)
        response_12 = sock_12.recv(1024)
        # Store the RX message in communication_traffic_1
        communication_traffic_12.append({"direction": "RX", "data": response_12.hex()})
        sock_12.close()
        data_12 = response_12[3:]
        
        values_12 = [
            int.from_bytes(data_12[i: i + bytes_per_value], byteorder="big", signed=False)
            for i in range(0, len(data_12), bytes_per_value)
        ]
        sock_13 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock_13.connect((tcp_ip, tcp_port))
        communication_traffic_13 = []
        
        # Store the TX message in communicat    ion_traffic_1
        communication_traffic_13.append({"direction": "TX", "data": request_message_13.hex()})
        sock_13.send(request_message_13)
        response_13 = sock_13.recv(1024)
        # Store the RX message in communication_traffic_1
        communication_traffic_13.append({"direction": "RX", "data": response_13.hex()})
        sock_13.close()
        data_13 = response_13[3:]
        
        values_13 = [
            int.from_bytes(data_13[i: i + bytes_per_value], byteorder="big", signed=False)
            for i in range(0, len(data_13), bytes_per_value)
        ]
        sock_14 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock_14.connect((tcp_ip, tcp_port))
        communication_traffic_14 = []
        
        # Store the TX message in communicat    ion_traffic_1
        communication_traffic_14.append({"direction": "TX", "data": request_message_14.hex()})
        sock_14.send(request_message_14)
        response_14 = sock_14.recv(1024)
        # Store the RX message in communication_traffic_1
        communication_traffic_14.append({"direction": "RX", "data": response_14.hex()})
        sock_14.close()
        data_14 = response_14[3:]
        
        values_14 = [
            int.from_bytes(data_14[i: i + bytes_per_value], byteorder="big", signed=False)
            for i in range(0, len(data_14), bytes_per_value)
        ]
        sock_15 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock_15.connect((tcp_ip, tcp_port))
        communication_traffic_15 = []
        
        # Store the TX message in communicat    ion_traffic_1
        communication_traffic_15.append({"direction": "TX", "data": request_message_15.hex()})
        sock_15.send(request_message_15)
        response_15 = sock_15.recv(1024)
        # Store the RX message in communication_traffic_1
        communication_traffic_15.append({"direction": "RX", "data": response_15.hex()})
        sock_15.close()
        data_15 = response_15[3:]
        
        values_15 = [
            int.from_bytes(data_15[i: i + bytes_per_value], byteorder="big", signed=False)
            for i in range(0, len(data_15), bytes_per_value)
        ]
        
        if "32bit" in request.form and request.form["32bit"] == "true":
            is_32bit = True
        else:
            is_32bit = False
        data_list_1 = []
        data_list_2 = []
        data_list_3 = []
        data_list_4 = []
        data_list_5 = []
        data_list_6 = []
        data_list_7 = []
        data_list_8 = []
        data_list_9 = []
        data_list_10 = []
        data_list_11 = []
        data_list_12 = []
        data_list_13 = []
        data_list_14 = []
        data_list_15 = []
        
        
        address = starting_address_1
        address = starting_address_2
        address = starting_address_3
        address = starting_address_4
        address = starting_address_5
        address = starting_address_6
        address = starting_address_7
        address = starting_address_8
        address = starting_address_9
        address = starting_address_10
        address = starting_address_11
        address = starting_address_12
        address = starting_address_13
        address = starting_address_14
        address = starting_address_15
        
        value = 0
        values_1 = values_1[:-1]
        values_2 = values_2[:-1]
        values_3 = values_3[:-1]
        values_4 = values_4[:-1]
        values_5 = values_5[:-1]
        values_6 = values_6[:-1]
        values_7 = values_7[:-1]
        values_8 = values_8[:-1]
        values_9 = values_9[:-1]
        values_10 = values_10[:-1]
        values_11 = values_11[:-1]
        values_12 = values_12[:-1]
        values_13 = values_13[:-1]
        values_14 = values_14[:-1]
        values_15 = values_15[:-1]
        for i, value in enumerate(values_1):
            address = starting_address_1 + i * 2
            
            type_value = get_type_value_from_database(address)
            hex_value = hex(value)  # Convert the decimal value to HEX
            binary_value = convert_to_binary_string(value, bytes_per_value)
            float_value = struct.unpack("!f", struct.pack("!I", value))[0]
            description = get_description_from_database(address)
            if description is None:
                description = f"Address {address}"
                address += 0
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
                # Apply type_value check after determining 16-bit or 32-bit format
                if type_value == "Float":
                    # Set float_display_value to the float representation
                    float_display_value = float_value
                elif type_value == "signed":
                    # Set float_display_value to the signed representation
                    float_display_value = signed_value
                else:
                    # Handle other cases or set a default behavior
                    float_display_value = "Undefined"
                    print(f"Type Value for address {address}: {type_value}")
            data_list_1.append(
                {
                    "description": description,
                    "address": address,
                    "value": value,
                    "hex_value": hex_value,
                    "binary_value": binary_value,
                    "float_value": float_display_value,
                    "signed_value": signed_value,
                    "is_16bit": is_16bit_value,
                    "float_signed_value": signed_value,
                }
            )
            
            value, updated_address = handle_action_configuration(i, value, address)
            
        for i, value in enumerate(values_2):
            
            address = starting_address_2 + i * 2
            type_value = get_type_value_from_database(address)
            hex_value = hex(value)  # Convert the decimal value to HEX
            binary_value = convert_to_binary_string(value, bytes_per_value)
            float_value = struct.unpack("!f", struct.pack("!I", value))[0]
            description = get_description_from_database(address)
            if description is None:
                description = f"Address {address}"
                address += 0
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
                # Apply type_value check after determining 16-bit or 32-bit format
                if type_value == "Float":
                    # Set float_display_value to the float representation
                    float_display_value = float_value
                elif type_value == "signed":
                    # Set float_display_value to the signed representation
                    float_display_value = signed_value
                else:
                    # Handle other cases or set a default behavior
                    float_display_value = "Undefined"
                    print(f"Type Value for address {address}: {type_value}")
            data_list_2.append(
                {
                    "description": description,
                    "address": address,
                    "value": value,
                    "hex_value": hex_value,
                    "binary_value": binary_value,
                    "float_value": float_display_value,
                    "signed_value": signed_value,
                    "is_16bit": is_16bit_value,
                    "float_signed_value": signed_value,
                }
            )
            value, updated_address = handle_action_configuration(i, value, address)
        for i, value in enumerate(values_3):
            
            address = starting_address_3 + i * 2
            type_value = get_type_value_from_database(address)
            hex_value = hex(value)  # Convert the decimal value to HEX
            binary_value = convert_to_binary_string(value, bytes_per_value)
            float_value = struct.unpack("!f", struct.pack("!I", value))[0]
            description = get_description_from_database(address)
            if description is None:
                description = f"Address {address}"
                address += 0
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
                # Apply type_value check after determining 16-bit or 32-bit format
                if type_value == "Float":
                    # Set float_display_value to the float representation
                    float_display_value = float_value
                elif type_value == "signed":
                    # Set float_display_value to the signed representation
                    float_display_value = signed_value
                else:
                    # Handle other cases or set a default behavior
                    float_display_value = "Undefined"
                    print(f"Type Value for address {address}: {type_value}")
            data_list_3.append(
                {
                    "description": description,
                    "address": address,
                    "value": value,
                    "hex_value": hex_value,
                    "binary_value": binary_value,
                    "float_value": float_display_value,
                    "signed_value": signed_value,
                    "is_16bit": is_16bit_value,
                    "float_signed_value": signed_value,
                }
            )
            
            value, updated_address = handle_action_configuration(i, value, address)
        for i, value in enumerate(values_4):
            
            address = starting_address_4 + i * 2
            type_value = get_type_value_from_database(address)
            hex_value = hex(value)  # Convert the decimal value to HEX
            binary_value = convert_to_binary_string(value, bytes_per_value)
            float_value = struct.unpack("!f", struct.pack("!I", value))[0]
            description = get_description_from_database(address)
            if description is None:
                description = f"Address {address}"
                address += 0
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
                # Apply type_value check after determining 16-bit or 32-bit format
                if type_value == "Float":
                    # Set float_display_value to the float representation
                    float_display_value = float_value
                elif type_value == "signed":
                    # Set float_display_value to the signed representation
                    float_display_value = signed_value
                else:
                    # Handle other cases or set a default behavior
                    float_display_value = "Undefined"
                    print(f"Type Value for address {address}: {type_value}")
            data_list_4.append(
                {
                    "description": description,
                    "address": address,
                    "value": value,
                    "hex_value": hex_value,
                    "binary_value": binary_value,
                    "float_value": float_display_value,
                    "signed_value": signed_value,
                    "is_16bit": is_16bit_value,
                    "float_signed_value": signed_value,
                }
            )
            value, updated_address = handle_action_configuration(i, value, address)
        for i, value in enumerate(values_5):
            
            address = starting_address_5 + i * 2
            type_value = get_type_value_from_database(address)
            hex_value = hex(value)  # Convert the decimal value to HEX
            binary_value = convert_to_binary_string(value, bytes_per_value)
            float_value = struct.unpack("!f", struct.pack("!I", value))[0]
            description = get_description_from_database(address)
            if description is None:
                description = f"Address {address}"
                address += 0
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
                # Apply type_value check after determining 16-bit or 32-bit format
                if type_value == "Float":
                    # Set float_display_value to the float representation
                    float_display_value = float_value
                elif type_value == "signed":
                    # Set float_display_value to the signed representation
                    float_display_value = signed_value
                else:
                    # Handle other cases or set a default behavior
                    float_display_value = "Undefined"
                    print(f"Type Value for address {address}: {type_value}")
            data_list_5.append(
                {
                    "description": description,
                    "address": address,
                    "value": value,
                    "hex_value": hex_value,
                    "binary_value": binary_value,
                    "float_value": float_display_value,
                    "signed_value": signed_value,
                    "is_16bit": is_16bit_value,
                    "float_signed_value": signed_value,
                }
            )
        for i, value in enumerate(values_6):
            
                address = starting_address_6 + i * 2
                type_value = get_type_value_from_database(address)
                hex_value = hex(value)  # Convert the decimal value to HEX
                binary_value = convert_to_binary_string(value, bytes_per_value)
                float_value = struct.unpack("!f", struct.pack("!I", value))[0]
                description = get_description_from_database(address)
                if description is None:
                    description = f"Address {address}"
                    address += 0
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
                    # Apply type_value check after determining 16-bit or 32-bit format
                    if type_value == "Float":
                        # Set float_display_value to the float representation
                        float_display_value = float_value
                    elif type_value == "signed":
                        # Set float_display_value to the signed representation
                        float_display_value = signed_value
                    else:
                        # Handle other cases or set a default behavior
                        float_display_value = "Undefined"
                        print(f"Type Value for address {address}: {type_value}")
                data_list_6.append(
                    {
                        "description": description,
                        "address": address,
                        "value": value,
                        "hex_value": hex_value,
                        "binary_value": binary_value,
                        "float_value": float_display_value,
                        "signed_value": signed_value,
                        "is_16bit": is_16bit_value,
                        "float_signed_value": signed_value,
                    }
                )
                
        for i, value in enumerate(values_7):
            
                address = starting_address_7 + i * 2
                type_value = get_type_value_from_database(address)
                hex_value = hex(value)  # Convert the decimal value to HEX
                binary_value = convert_to_binary_string(value, bytes_per_value)
                float_value = struct.unpack("!f", struct.pack("!I", value))[0]
                description = get_description_from_database(address)
                if description is None:
                    description = f"Address {address}"
                    address += 0
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
                    # Apply type_value check after determining 16-bit or 32-bit format
                    if type_value == "Float":
                        # Set float_display_value to the float representation
                        float_display_value = float_value
                    elif type_value == "signed":
                        # Set float_display_value to the signed representation
                        float_display_value = signed_value
                    else:
                        # Handle other cases or set a default behavior
                        float_display_value = "Undefined"
                        print(f"Type Value for address {address}: {type_value}")
                data_list_7.append(
                    {
                        "description": description,
                        "address": address,
                        "value": value,
                        "hex_value": hex_value,
                        "binary_value": binary_value,
                        "float_value": float_display_value,
                        "signed_value": signed_value,
                        "is_16bit": is_16bit_value,
                        "float_signed_value": signed_value,
                    }
                )
        for i, value in enumerate(values_8):
            
                address = starting_address_8 + i * 2
                type_value = get_type_value_from_database(address)
                hex_value = hex(value)  # Convert the decimal value to HEX
                binary_value = convert_to_binary_string(value, bytes_per_value)
                float_value = struct.unpack("!f", struct.pack("!I", value))[0]
                description = get_description_from_database(address)
                if description is None:
                    description = f"Address {address}"
                    address += 0
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
                    # Apply type_value check after determining 16-bit or 32-bit format
                    if type_value == "Float":
                        # Set float_display_value to the float representation
                        float_display_value = float_value
                    elif type_value == "signed":
                        # Set float_display_value to the signed representation
                        float_display_value = signed_value
                    else:
                        # Handle other cases or set a default behavior
                        float_display_value = "Undefined"
                        print(f"Type Value for address {address}: {type_value}")
                data_list_8.append(
                    {
                        "description": description,
                        "address": address,
                        "value": value,
                        "hex_value": hex_value,
                        "binary_value": binary_value,
                        "float_value": float_display_value,
                        "signed_value": signed_value,
                        "is_16bit": is_16bit_value,
                        "float_signed_value": signed_value,
                    }
                )
                
        for i, value in enumerate(values_9):
            
                address = starting_address_9 + i * 2
                type_value = get_type_value_from_database(address)
                hex_value = hex(value)  # Convert the decimal value to HEX
                binary_value = convert_to_binary_string(value, bytes_per_value)
                float_value = struct.unpack("!f", struct.pack("!I", value))[0]
                description = get_description_from_database(address)
                if description is None:
                    description = f"Address {address}"
                    address += 0
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
                    # Apply type_value check after determining 16-bit or 32-bit format
                    if type_value == "Float":
                        # Set float_display_value to the float representation
                        float_display_value = float_value
                    elif type_value == "signed":
                        # Set float_display_value to the signed representation
                        float_display_value = signed_value
                    else:
                        # Handle other cases or set a default behavior
                        float_display_value = "Undefined"
                        print(f"Type Value for address {address}: {type_value}")
                data_list_9.append(
                    {
                        "description": description,
                        "address": address,
                        "value": value,
                        "hex_value": hex_value,
                        "binary_value": binary_value,
                        "float_value": float_display_value,
                        "signed_value": signed_value,
                        "is_16bit": is_16bit_value,
                        "float_signed_value": signed_value,
                    }
                )
        for i, value in enumerate(values_10):
            
                address = starting_address_10 + i * 2
                type_value = get_type_value_from_database(address)
                hex_value = hex(value)  # Convert the decimal value to HEX
                binary_value = convert_to_binary_string(value, bytes_per_value)
                float_value = struct.unpack("!f", struct.pack("!I", value))[0]
                description = get_description_from_database(address)
                if description is None:
                    description = f"Address {address}"
                    address += 0
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
                    # Apply type_value check after determining 16-bit or 32-bit format
                    if type_value == "Float":
                        # Set float_display_value to the float representation
                        float_display_value = float_value
                    elif type_value == "signed":
                        # Set float_display_value to the signed representation
                        float_display_value = signed_value
                    else:
                        # Handle other cases or set a default behavior
                        float_display_value = "Undefined"
                        print(f"Type Value for address {address}: {type_value}")
                data_list_10.append(
                    {
                        "description": description,
                        "address": address,
                        "value": value,
                        "hex_value": hex_value,
                        "binary_value": binary_value,
                        "float_value": float_display_value,
                        "signed_value": signed_value,
                        "is_16bit": is_16bit_value,
                        "float_signed_value": signed_value,
                    }
                )
        for i, value in enumerate(values_11):
            
                address = starting_address_11 + i * 2
                type_value = get_type_value_from_database(address)
                hex_value = hex(value)  # Convert the decimal value to HEX
                binary_value = convert_to_binary_string(value, bytes_per_value)
                float_value = struct.unpack("!f", struct.pack("!I", value))[0]
                description = get_description_from_database(address)
                if description is None:
                    description = f"Address {address}"
                    address += 0
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
                    # Apply type_value check after determining 16-bit or 32-bit format
                    if type_value == "Float":
                        # Set float_display_value to the float representation
                        float_display_value = float_value
                    elif type_value == "signed":
                        # Set float_display_value to the signed representation
                        float_display_value = signed_value
                    else:
                        # Handle other cases or set a default behavior
                        float_display_value = "Undefined"
                        print(f"Type Value for address {address}: {type_value}")
                data_list_11.append(
                    {
                        "description": description,
                        "address": address,
                        "value": value,
                        "hex_value": hex_value,
                        "binary_value": binary_value,
                        "float_value": float_display_value,
                        "signed_value": signed_value,
                        "is_16bit": is_16bit_value,
                        "float_signed_value": signed_value,
                    }
                )
            
        for i, value in enumerate(values_12):
            
                address = starting_address_12 + i * 2
                type_value = get_type_value_from_database(address)
                hex_value = hex(value)  # Convert the decimal value to HEX
                binary_value = convert_to_binary_string(value, bytes_per_value)
                float_value = struct.unpack("!f", struct.pack("!I", value))[0]
                description = get_description_from_database(address)
                if description is None:
                    description = f"Address {address}"
                    address += 0
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
                    # Apply type_value check after determining 16-bit or 32-bit format
                    if type_value == "Float":
                        # Set float_display_value to the float representation
                        float_display_value = float_value
                    elif type_value == "signed":
                        # Set float_display_value to the signed representation
                        float_display_value = signed_value
                    else:
                        # Handle other cases or set a default behavior
                        float_display_value = "Undefined"
                        print(f"Type Value for address {address}: {type_value}")
                data_list_12.append(
                    {
                        "description": description,
                        "address": address,
                        "value": value,
                        "hex_value": hex_value,
                        "binary_value": binary_value,
                        "float_value": float_display_value,
                        "signed_value": signed_value,
                        "is_16bit": is_16bit_value,
                        "float_signed_value": signed_value,
                    }
                )
        for i, value in enumerate(values_13):
            
                address = starting_address_13 + i * 2
                type_value = get_type_value_from_database(address)
                hex_value = hex(value)  # Convert the decimal value to HEX
                binary_value = convert_to_binary_string(value, bytes_per_value)
                float_value = struct.unpack("!f", struct.pack("!I", value))[0]
                description = get_description_from_database(address)
                if description is None:
                    description = f"Address {address}"
                    address += 0
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
                    # Apply type_value check after determining 16-bit or 32-bit format
                    if type_value == "Float":
                        # Set float_display_value to the float representation
                        float_display_value = float_value
                    elif type_value == "signed":
                        # Set float_display_value to the signed representation
                        float_display_value = signed_value
                    else:
                        # Handle other cases or set a default behavior
                        float_display_value = "Undefined"
                        print(f"Type Value for address {address}: {type_value}")
                data_list_13.append(
                    {
                        "description": description,
                        "address": address,
                        "value": value,
                        "hex_value": hex_value,
                        "binary_value": binary_value,
                        "float_value": float_display_value,
                        "signed_value": signed_value,
                        "is_16bit": is_16bit_value,
                        "float_signed_value": signed_value,
                    }
                )
        for i, value in enumerate(values_14):
            
                address = starting_address_14 + i * 2
                type_value = get_type_value_from_database(address)
                hex_value = hex(value)  # Convert the decimal value to HEX
                binary_value = convert_to_binary_string(value, bytes_per_value)
                float_value = struct.unpack("!f", struct.pack("!I", value))[0]
                description = get_description_from_database(address)
                if description is None:
                    description = f"Address {address}"
                    address += 0
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
                    # Apply type_value check after determining 16-bit or 32-bit format
                    if type_value == "Float":
                        # Set float_display_value to the float representation
                        float_display_value = float_value
                    elif type_value == "signed":
                        # Set float_display_value to the signed representation
                        float_display_value = signed_value
                    else:
                        # Handle other cases or set a default behavior
                        float_display_value = "Undefined"
                        print(f"Type Value for address {address}: {type_value}")
                data_list_14.append(
                    {
                        "description": description,
                        "address": address,
                        "value": value,
                        "hex_value": hex_value,
                        "binary_value": binary_value,
                        "float_value": float_display_value,
                        "signed_value": signed_value,
                        "is_16bit": is_16bit_value,
                        "float_signed_value": signed_value,
                    }
                )
        for i, value in enumerate(values_15):
            
                address = starting_address_15 + i * 2
                type_value = get_type_value_from_database(address)
                hex_value = hex(value)  # Convert the decimal value to HEX
                binary_value = convert_to_binary_string(value, bytes_per_value)
                float_value = struct.unpack("!f", struct.pack("!I", value))[0]
                description = get_description_from_database(address)
                if description is None:
                    description = f"Address {address}"
                    address += 0
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
                    # Apply type_value check after determining 16-bit or 32-bit format
                    if type_value == "Float":
                        # Set float_display_value to the float representation
                        float_display_value = float_value
                    elif type_value == "signed":
                        # Set float_display_value to the signed representation
                        float_display_value = signed_value
                    else:
                        # Handle other cases or set a default behavior
                        float_display_value = "Undefined"
                        print(f"Type Value for address {address}: {type_value}")
                data_list_15.append(
                    {
                        "description": description,
                        "address": address,
                        "value": value,
                        "hex_value": hex_value,
                        "binary_value": binary_value,
                        "float_value": float_display_value,
                        "signed_value": signed_value,
                        "is_16bit": is_16bit_value,
                        "float_signed_value": signed_value,
                    }
                )
        value, updated_address = handle_action_configuration(i, value, address)
            
        combined_data = {
            "data_1": data_1,
            "data_2": data_2,
            "data_3": data_3,
            "data_4": data_4,
            "data_5": data_5,
            "data_6": data_6,
            "data_7": data_7,
            "data_8": data_8,
            "data_9": data_9,
            "data_10": data_10,
            "data_11": data_11,
            "data_12": data_12,
            "data_13": data_13,
            "data_14": data_14,
            "data_15": data_15,
        
            "communication_traffic_1": communication_traffic_1,
            "communication_traffic_2": communication_traffic_2,
            "communication_traffic_3": communication_traffic_3,
            "communication_traffic_4": communication_traffic_4,
            "communication_traffic_5": communication_traffic_5,
            "communication_traffic_6": communication_traffic_6,
            "communication_traffic_7": communication_traffic_7,
            "communication_traffic_8": communication_traffic_8,
            "communication_traffic_9": communication_traffic_9,
            "communication_traffic_10": communication_traffic_10,
            "communication_traffic_11": communication_traffic_11,
            "communication_traffic_12": communication_traffic_12,
            "communication_traffic_13": communication_traffic_13,
            "communication_traffic_14": communication_traffic_14,
            "communication_traffic_15": communication_traffic_15,
        
            
        }
        
        session["tcp_ip"] = tcp_ip
        session["tcp_port"] = tcp_port
        
        if not is_16bit:
        
            data_list_16bit = []
            for data_16bit in data_list_1:
                address_16bit = data_16bit["address"]
                value_16bit = (
                    data_16bit["value"] * 2
                )  
                data_list_16bit.append({"address": address_16bit, "value": value_16bit})
        
        region_query = """
            SELECT * FROM AMR_REGION 
            """
        tag_query = """
            SELECT DISTINCT TAG_ID
            FROM AMR_FIELD_ID
            JOIN AMR_PL_GROUP ON AMR_FIELD_ID.FIELD_ID = AMR_PL_GROUP.FIELD_ID 
            WHERE AMR_PL_GROUP.PL_REGION_ID = :region_id
            """
        region_results = fetch_data(amr_connection,region_query)
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
        region_results = fetch_data(amr_connection,region_query)
        region_options = [str(region[0]) for region in region_results]
        tag_results = fetch_data(amr_connection,tag_query, params={"region_id": selected_region})
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
            results = fetch_data(amr_connection,query)
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
            # ... (other code)
            poll_config_list = df.get(["poll_config"]).values.tolist()
            print(poll_config_list)
            
            if poll_config_list:
                config_list_str = str(poll_config_list).strip("[]'").split(",")
                print(config_list_str)
            else:
            # Provide a default value if poll_config_list is empty
                config_list_str = [''] * 10
            poll_billing_list = df.get(["poll_billing"]).values.tolist()
            if poll_billing_list:
                billing_list_str = str(poll_billing_list[0]).strip("[]'").split(",")
                print(billing_list_str)
            else:
            # Provide a default value if poll_config_list is empty
                billing_list_str = [''] * 20
            poll_config_enable_list = df.get(["poll_config_enable"]).values.tolist()
            print(poll_config_enable_list)
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
            print(ip_str)
            tcp_port = df.get(["Port"]).values.tolist()
            if tcp_port:
                Port_str = str(tcp_port[0]).strip("[]'").split(",")
                print(Port_str)
            else:
            # Provide a default value if poll_config_list is empty
                Port_str = [''] 
        
            zipped_data = zip(poll_config_list, poll_billing_list ,tcp_ip,tcp_port,poll_config_enable_list,poll_billing_enable_list)
        return render_template(
            "Manual poll.html",
            df=df,
            data_list_1=data_list_1,data_list_2=data_list_2,data_list_3=data_list_3,data_list_4=data_list_4,data_list_5=data_list_5,data_list_6=data_list_6,data_list_7=data_list_7,data_list_8=data_list_8,
            data_list_9=data_list_9,data_list_10=data_list_10,data_list_11=data_list_11,data_list_12=data_list_12,data_list_13=data_list_13,data_list_14=data_list_14,data_list_15=data_list_15,
            slave_id=slave_id,
            function_code=function_code,
            starting_address_1=starting_address_1,
            quantity_1=quantity_1,starting_address_2=starting_address_2,quantity_2=quantity_2,starting_address_3=starting_address_3,quantity_3=quantity_3,
            starting_address_4=starting_address_4,quantity_4=quantity_4,starting_address_5=starting_address_5,quantity_5=quantity_5,starting_address_6=starting_address_6,quantity_6=quantity_6,
            starting_address_7=starting_address_7,quantity_7=quantity_7,starting_address_8=starting_address_8,quantity_8=quantity_8,starting_address_9=starting_address_9,quantity_9=quantity_9,
            starting_address_10=starting_address_10,quantity_10=quantity_10,starting_address_11=starting_address_11,quantity_11=quantity_11,
            starting_address_12=starting_address_12,quantity_12=quantity_12,starting_address_13=starting_address_13,quantity_13=quantity_13,starting_address_14=starting_address_14,quantity_14=quantity_14,
            starting_address_15=starting_address_15,quantity_15=quantity_15,
            is_16bit=is_16bit,
            communication_traffic_1=communication_traffic_1,
            communication_traffic_2=communication_traffic_2,
            communication_traffic_3=communication_traffic_3,
            communication_traffic_4=communication_traffic_4,
            communication_traffic_5=communication_traffic_5,
            communication_traffic_6=communication_traffic_6,
            communication_traffic_7=communication_traffic_7,
            communication_traffic_8=communication_traffic_8,
            communication_traffic_9=communication_traffic_9,
            communication_traffic_10=communication_traffic_10,
            communication_traffic_11=communication_traffic_11,
            communication_traffic_12=communication_traffic_12,
            communication_traffic_13=communication_traffic_13,
            communication_traffic_14=communication_traffic_14,
            communication_traffic_15=communication_traffic_15,
            zipped_data=zipped_data,
            poll_config_list=poll_config_list,poll_billing_list=poll_billing_list,
            billing_list_str=billing_list_str,poll_config_enable_list=poll_config_enable_list,poll_billing_enable_list=poll_billing_enable_list,
            
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


def get_description_from_database(address):
    with connect_to_amr_db() as amr_connection:
        print("Active Connection:", active_connection)
        query = "SELECT DESCRIPTION FROM AMR_MAPPING_CONFIG WHERE ADDRESS = :address"
        params = {"address": address}
        result = fetch_data(amr_connection,query, params)
        return result[0][0] if result else None
@Manualpoll_data.route("/process_selected_rows", methods=["POST"])
def process_selected_rows():
    selected_rows = request.form.getlist("selected_rows")
    return "Selected rows processed successfully"


def get_type_value_from_database(address):
    with connect_to_amr_db() as amr_connection:
        print("Active Connection:", active_connection)
        query = "SELECT TYPE_VALUE FROM AMR_MAPPING_CONFIG WHERE ADDRESS = :address"
        result = fetch_data(amr_connection,query, params={"address": address})
        if result:
            return result[0][0]  # Assuming TYPE_VALUE is the first column in the result
        return None