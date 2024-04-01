from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask import flash
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
import traceback
import numpy as np
from flask import abort

app = Flask(__name__)
app.secret_key = 'your_secret_key'


communication_traffic = []
change_to_32bit_counter = 0 
def convert_to_binary_string(value, bytes_per_value):
    binary_string = bin(value)[
        2:
    ]  
    return binary_string.zfill(
        bytes_per_value * 8
    )  

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
    # print(region_results)
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
    result_billing = []
    result_config = []
    
        #print(df_mapping)
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
    # print(poll_config_enable_list)
    poll_billing_enable_list = str(request.form["poll_billing_enable_list"])
    # print(poll_billing_enable_list)
    
    #query Pollrange
    ##### config #####
    
    data= {'starting_address_i': [], 
           'quantity_i': [], 
           'adjusted_quantity_i': []}
    df_pollRange = pd.DataFrame(data)
    df_pollBilling = pd.DataFrame(data)
    
    for i in range(1, 6):
        # print(i)
        # print(poll_config_enable_list[i-1])
        if poll_config_enable_list[i-1] == '1':
            # print(poll_config_enable_list[i-1])
            
            starting_address_i = int(request.form[f'starting_address_{i}'])
            # print(starting_address_i)            
            quantity_i = int(request.form[f'quantity_{i}'])
            
            adjusted_quantity_i = quantity_i - starting_address_i + 1
            data= {'starting_address_i': [starting_address_i], 
                   'quantity_i': [quantity_i], 
                   'adjusted_quantity_i': [adjusted_quantity_i]}
            df_2 = pd.DataFrame(data)
            
            df_pollRange = pd.concat([df_pollRange,df_2] , ignore_index=True)
            # print(df_pollRange)
            
    for i in range(7, 17): 
        if poll_billing_enable_list[i-7] == '1': 
            # print("i",i)
            # print(poll_billing_enable_list[i-7])
            starting_address_i = int(request.form[f'starting_address_{i-1}'])
            # print(starting_address_i)
            quantity_i = int(request.form[f'quantity_{i-1}'])
            # print(quantity_i)
            adjusted_quantity_i = quantity_i - starting_address_i + 1
            data= {'starting_address_i': [starting_address_i], 
                   'quantity_i': [quantity_i], 
                   'adjusted_quantity_i': [adjusted_quantity_i]}
            # print(data)
            df_2 = pd.DataFrame(data)
            
            df_pollBilling = pd.concat([df_pollBilling,df_2] , ignore_index=True)
    # print(df_pollBilling)
    # poll to EVC
        
    dataframes = {
            'address_start': [],
            'finish': [],
            'TX': [],
            'RX': []
        }
    df_Modbus = pd.DataFrame(dataframes)
    df_Modbusbilling = pd.DataFrame(dataframes)
    # print(df_data)
    for i in range(0, len(df_pollRange)):
        
        # print(i)
        start_address = int(df_pollRange.loc[i,'starting_address_i'])
        # print(start_address)
        adjusted_quantity = int(df_pollRange.loc[i,'adjusted_quantity_i'])
        
        is_16bit = request.form.get("is_16bit") == "true"
        if is_16bit:
            bytes_per_value = 2
        else:
            bytes_per_value = 4
            if change_to_32bit_counter > 0:
                adjusted_quantity *= 2
                change_to_32bit_counter -= 1
        
        request_message_i = bytearray(
        [slave_id, function_code, start_address >> 8, start_address & 0xFF, adjusted_quantity >> 8, adjusted_quantity & 0xFF])
        crc_i = computeCRC(request_message_i)
        request_message_i += crc_i.to_bytes(2, byteorder="big")
        
        
        sock_i = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock_i.connect((tcp_ip, tcp_port))
        communication_traffic_i = []
    
        communication_traffic_i.append(request_message_i.hex())
        sock_i.send(request_message_i)
        response_i = sock_i.recv(1024)
        # print(response_i)
 
        communication_traffic_i.append(response_i.hex())
        # print("TX config:",communication_traffic_i[0])
        # print("RX config:", communication_traffic_i[1])
        tx_config_safe = f"TX config: {communication_traffic_i[0]}"
        rx_config_safe = f"RX config: {communication_traffic_i[1]}"
        print(tx_config_safe ,rx_config_safe)
    
        if response_i[1:2] != b'\x03':
            
            abort(400, f"Error: Unexpected response code from device {communication_traffic_i[1]}!")
        else:
            pass
 
        data = {
            'address_start': [int(start_address)],
            'finish': [int(start_address+adjusted_quantity)],
            'TX': [communication_traffic_i[0]],
            'RX': [communication_traffic_i[1]]
        }
        # print(data)
        df_2 = pd.DataFrame(data)
        df_Modbus = pd.concat([df_Modbus, df_2], ignore_index=True)        
        # print(df_Modbus)               
        sock_i.close()
            
    ##############   billing
    for i in range(0, len(df_pollBilling)):
       
        # print(i)
        start_address = int(df_pollBilling.loc[i,'starting_address_i'])
        # print(start_address)
        adjusted_quantity = int(df_pollBilling.loc[i,'adjusted_quantity_i'])
        # print(adjusted_quantity)
        
        is_16bit = request.form.get("is_16bit") == "true"
        if is_16bit:
            bytes_per_value = 2
        else:
            bytes_per_value = 4
            if change_to_32bit_counter > 0:
                adjusted_quantity *= 2
                change_to_32bit_counter -= 1
        
        request_message_i = bytearray(
        [slave_id, function_code, start_address >> 8, start_address & 0xFF, adjusted_quantity >> 8, adjusted_quantity & 0xFF])
        crc_i = computeCRC(request_message_i)
        request_message_i += crc_i.to_bytes(2, byteorder="big")
        
        
        sock_i = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock_i.connect((tcp_ip, tcp_port))
        communication_traffic_i = []
           
        communication_traffic_i.append(request_message_i.hex())
        
        sock_i.send(request_message_i)
        response_i = sock_i.recv(1024)
             
        communication_traffic_i.append(response_i.hex())
        # print("TX billing:",communication_traffic_i[0])
        # print("RX billing:", communication_traffic_i[1])
        tx_billing_safe = f"TX billing: {communication_traffic_i[0]}"
        rx_billing_safe = f"RX billing: {communication_traffic_i[1]}"
        print(tx_billing_safe,rx_billing_safe)
        
        if response_i[1:2] != b'\x03':
            # print("billing", response_i[1:2])
            abort(400, f"Error: Unexpected response code from device {communication_traffic_i[1]}!")
        else:
            pass      
        
        # print(communication_traffic_i)
        data = {
            'address_start': [int(start_address)],
            'finish': [int(start_address+adjusted_quantity-1)],
            'TX': [communication_traffic_i[0]],
            'RX': [communication_traffic_i[1]]
        }
        # print(data)
        df_2 = pd.DataFrame(data)
        df_Modbusbilling = pd.concat([df_Modbusbilling, df_2], ignore_index=True)
             
        # print(df_Modbusbilling)
               
        sock_i.close()
    
       
        encode_data_dict = {} 
        

        evc_type = evc_type
        query = """
        select amc.or_der as order1 , amc.address as address1, amc.description as desc1, amc.data_type as dtype1
        from amr_mapping_config amc
        where amc.evc_type = :evc_type AND address is not null 
        order by order1
        """
        poll_results = fetch_data(query, params={"evc_type": evc_type})
        df_mapping = pd.DataFrame(poll_results, columns=['order', 'address', 'desc', 'data_type'])
        # print(df_mapping)
             
        list_of_values_configured = []
        for i in range(0, len(df_mapping)):
            
            address = int(df_mapping.iloc[i,1])
            
            data_type = str(df_mapping.iloc[i,3])
            
            for j in range(0,len(df_Modbus)):
                address_start = int(df_Modbus.iloc[j,0])
                address_finish = int(df_Modbus.iloc[j,1])
                #print(address)
                if address >= address_start and address <= address_finish:
                    # print(address_start, address_finish, df_Modbus.iloc[j,3])
                    location_data = (address - address_start)*int(8/2)
                    frameRx = (df_Modbus.iloc[j,3])
                    #
                    raw_data = frameRx[location_data + 6: location_data + 14]
                                    
                    list_of_values_configured.append(convert_raw_to_value(data_type,raw_data))
                    # print(list_of_values_configured)
                    break
        # print(list_of_values_configured)
        value_config = pd.DataFrame(list_of_values_configured,columns=['Value'])
        result_config = pd.concat([df_mapping, value_config], axis=1)       
        result_config_html = result_config.to_html(classes="data", index=False)
                           
    ### list_of_balue_billing
        evc_type = evc_type
        query = """
        SELECT amb.daily ,amb.or_der ,amb.address,amb.description,amb.data_type  FROM amr_mapping_billing amb WHERE amb.evc_type = :evc_type AND address is not null order by amb.daily
        ,amb.or_der
        """
        poll_resultsbilling = fetch_data(query, params={"evc_type": evc_type})
        # print(poll_resultsbilling)
        df_mappingbilling = pd.DataFrame(poll_resultsbilling, columns=['daily','or_der', 'address', 'description', 'data_type'])
        
        
        # print(df_Modbusbilling)   
        list_of_values_billing = []
        for i in range(0, len(df_mappingbilling)):    
            address = int(df_mappingbilling.iloc[i,2])
            data_type = str(df_mappingbilling.iloc[i,4])           
            for j in range(0,len(df_Modbusbilling)):
                address_start = int(df_Modbusbilling.iloc[j,0])
                address_finish = int(df_Modbusbilling.iloc[j,1])
               
                if address >= address_start and address <= address_finish:
                    # print(address)
                    # print(address_start, address_finish)
                    location_data = (address - address_start)*int(8/2)
                    # print(location_data)
                    frameRx = (df_Modbusbilling.iloc[j,3])
                   
                    raw_data = frameRx[location_data + 6: location_data + 14]
                    # print(raw_data)
                    
                    list_of_values_billing.append(convert_raw_to_value(data_type,raw_data))   
                    
                    break
        value_billing = pd.DataFrame(list_of_values_billing,columns=['Value'])
        # print()
        result_billing = pd.concat([df_mappingbilling, value_billing], axis=1)
        # ['description']
        # print(result_billing)
        result_billing_html = result_billing.to_html(classes="data", index=False)
    
    combined_data = {
        
        "communication_traffic_i": communication_traffic_i, 
    }
    data_list_i = []
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
        df=df,METERID=METERID,df_mapping=df_mapping,df_mappingbilling=df_mappingbilling,result_billing=result_billing,result_config=result_config,
        result_config_html=result_config_html,result_billing_html=result_billing_html,tx_config=tx_config_safe, rx_config=rx_config_safe,tx_billing=tx_billing_safe, rx_billing=rx_billing_safe,
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
 
 
 
 
    
def convert_raw_to_value(data_type, raw_data):
    if data_type == "Date":
        raw_data_as_int = int(raw_data, 16)
        date_object = datetime.datetime.fromtimestamp(raw_data_as_int).date()
        
        
        modified_date = date_object - datetime.timedelta(days=1)
        
        formatted_date = modified_date.strftime('%d-%m-%Y') 
        
        return formatted_date
    elif data_type == "Float":
        
        return struct.unpack('!f', bytes.fromhex(raw_data))[0]
    elif data_type == "Ulong":
        return int(raw_data, 16)
    else:
       
        return raw_data 

def delete_data(sql_text_config_delete, sql_text_billing_delete):
    # print(sql_text_config_delete, sql_text_bolling_delete)
    try:
        with cx_Oracle.connect(username, password, f"{hostname}:{port}/{service_name}") as connection:
            with connection.cursor() as cursor:
                cursor.execute(sql_text_config_delete)
                connection.commit()
                print("delete data config successful")  
                
                cursor.execute(sql_text_billing_delete)
                connection.commit()
                print("delete data billing successful")  
                
    except cx_Oracle.Error as error:
        print("Oracle Error:", error)


def insert_data( full_sql_text):
    try:
        with cx_Oracle.connect(username, password, f"{hostname}:{port}/{service_name}") as connection:
            with connection.cursor() as cursor:
                for sql_statement in full_sql_text.split(";"):
                    if sql_statement.strip():
                        cursor.execute(sql_statement.strip())
                connection.commit()
                print("Insert data billing successful")
    except cx_Oracle.Error as error:
        print("Oracle Error:", error)




@app.route("/save_to_oracle_manualpoll", methods=["POST"])
def save_to_oracle_manualpoll():
    global change_to_32bit_counter
    try:
        
        data = request.get_json()
        
        evc_type = data["evc_type"]
        
        slave_id = int(data.get("slave_id"))
       
        function_code= int(data.get("function_code"))
        
        tcp_ip = data.get("tcp_ip")
      
        tcp_port = int(data.get("tcp_port"))
        
        run = int(data.get("run"))
        
        METERID = str(data.get("METERID"))
       
        poll_config_enable_list = str(data.get("poll_config_enable_list"))
        
        poll_billing_enable_list = str(data.get("poll_billing_enable_list"))
        
    
        starting_address_values = data["starting_address_values"]
        quantity_values = data["quantity_values"]
        data= {'starting_address': [], 
           'quantity': [], 
           'adjusted_quantity': []}
        df_pollRange = pd.DataFrame(data)
        df_pollBilling = pd.DataFrame(data)
        for i in range(1, 6):  
            if poll_config_enable_list[i-1] == '1':
                starting_address_key = "starting_address_" + str(i)
                quantity_key = "quantity_" + str(i)
                if starting_address_key in starting_address_values and quantity_key in quantity_values:
                    starting_address = starting_address_values[starting_address_key]
                    quantity = quantity_values[quantity_key]
                    adjusted_quantity = int(quantity) - int(starting_address) + 1
                    data= {'starting_address': [starting_address], 
                   'quantity': [quantity], 
                   'adjusted_quantity': [adjusted_quantity]}
                    df_2 = pd.DataFrame(data)
            
                df_pollRange = pd.concat([df_pollRange,df_2] , ignore_index=True)
                # print(df_pollRange)
        
        for i in range(7, 17): 
        
            if poll_billing_enable_list[i-7] == '1': 
                # print("i",i)
                # print(poll_billing_enable_list[i-7])
                starting_address_key = "starting_address_" + str(i-1)
                quantity_key = "quantity_" + str(i-1)
                # print(quantity_i)
                if starting_address_key in starting_address_values and quantity_key in quantity_values:
                    starting_address = starting_address_values[starting_address_key]
                    quantity = quantity_values[quantity_key]
                    adjusted_quantity = int(quantity) - int(starting_address) + 1
                    data= {'starting_address': [starting_address], 
                   'quantity': [quantity], 
                   'adjusted_quantity': [adjusted_quantity]}
                    df_2 = pd.DataFrame(data)
                
                df_pollBilling = pd.concat([df_pollBilling,df_2] , ignore_index=True)        
        
                # print(df_pollBilling)
        
        dataframes = {
            'address_start': [],
            'finish': [],
            'TX': [],
            'RX': []
        }
        df_Modbus = pd.DataFrame(dataframes)
        df_Modbusbilling = pd.DataFrame(dataframes)
        
        for i in range(0, len(df_pollRange)):
        
            # print(i)
            start_address = int(df_pollRange.loc[i,'starting_address'])
            # print(start_address)
            adjusted_quantity = int(df_pollRange.loc[i,'adjusted_quantity'])
            

            is_16bit = request.form.get("is_16bit") == "true"
            if is_16bit:
                bytes_per_value = 2
            else:
                bytes_per_value = 4
                if change_to_32bit_counter > 0:
                    adjusted_quantity *= 2
                    change_to_32bit_counter -= 1
            
            request_message_i = bytearray(
            [slave_id, function_code, start_address >> 8, start_address & 0xFF, adjusted_quantity >> 8, adjusted_quantity & 0xFF])
            crc_i = computeCRC(request_message_i)
            request_message_i += crc_i.to_bytes(2, byteorder="big")
            
            
            sock_i = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock_i.connect((tcp_ip, tcp_port))
            communication_traffic_i = []
        
            
            communication_traffic_i.append(request_message_i.hex())
            sock_i.send(request_message_i)
            response_i = sock_i.recv(1024)
            # print(response_i)
                 
            communication_traffic_i.append(response_i.hex())
            
            if response_i[1:2] != b'\x03':
            # print("billing", response_i[1:2])
                abort(400, f"Error: Unexpected response code from device {communication_traffic_i[1]}!")
            else:
                pass
                        
            data = {
                'address_start': [int(start_address)],
                'finish': [int(start_address+adjusted_quantity)],
                'TX': [communication_traffic_i[0]],
                'RX': [communication_traffic_i[1]]
            }
            # print(data)
            df_2 = pd.DataFrame(data)
            df_Modbus = pd.concat([df_Modbus, df_2], ignore_index=True)

            
            # print(df_Modbus)
            
            
            sock_i.close()
        
        for i in range(0, len(df_pollBilling)):
        
            
            # print(i)
            start_address = int(df_pollBilling.loc[i,'starting_address'])
            # print(start_address)
            adjusted_quantity = int(df_pollBilling.loc[i,'adjusted_quantity'])
            # print(adjusted_quantity) 

            is_16bit = request.form.get("is_16bit") == "true"
            if is_16bit:
                bytes_per_value = 2
            else:
                bytes_per_value = 4
                if change_to_32bit_counter > 0:
                    adjusted_quantity *= 2
                    change_to_32bit_counter -= 1
            
            request_message_i = bytearray(
            [slave_id, function_code, start_address >> 8, start_address & 0xFF, adjusted_quantity >> 8, adjusted_quantity & 0xFF])
            crc_i = computeCRC(request_message_i)
            request_message_i += crc_i.to_bytes(2, byteorder="big")
            
            sock_i = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock_i.connect((tcp_ip, tcp_port))
            communication_traffic_i = []
        
            communication_traffic_i.append(request_message_i.hex())
            
            sock_i.send(request_message_i)
            response_i = sock_i.recv(1024)
             
            communication_traffic_i.append(response_i.hex())
            if response_i[1:2] != b'\x03':
                # print("billing", response_i[1:2])
                abort(400, f"Error: Unexpected response code from device {communication_traffic_i[1]}!")
            else:
                pass

            # print(communication_traffic_i)
            data = {
                'address_start': [int(start_address)],
                'finish': [int(start_address+adjusted_quantity-1)],
                'TX': [communication_traffic_i[0]],
                'RX': [communication_traffic_i[1]]
            }
            # print(data)
            df_2 = pd.DataFrame(data)
            df_Modbusbilling = pd.concat([df_Modbusbilling, df_2], ignore_index=True)

            # print(df_Modbusbilling)
            
            sock_i.close()
        
            encode_data_dict = {} 
            
            evc_type = evc_type
            query = """
            select amc.or_der as order1 , amc.address as address1, amc.description as desc1, amc.data_type as dtype1
            from amr_mapping_config amc
            where amc.evc_type = :evc_type AND address is not null 
            order by order1
            """
            poll_results = fetch_data(query, params={"evc_type": evc_type})
            # print(poll_results)
            df_mapping = pd.DataFrame(poll_results, columns=['order', 'address', 'desc', 'data_type'])
                
            list_of_values_configured = []
            for i in range(0, len(df_mapping)): 
                address = int(df_mapping.iloc[i,1])
                # print(address)
                data_type = str(df_mapping.iloc[i,3])
                # print(data_type)
                  
                for j in range(0,len(df_Modbus)):
                    address_start = int(df_Modbus.iloc[j,0])
                    address_finish = int(df_Modbus.iloc[j,1])
                    #print(address)
                    if address >= address_start and address <= address_finish:
                        # print(df_Modbus.iloc[j,3])
                        location_data = (address - address_start)*int(8/2)
                        # print(location_data)
                        frameRx = (df_Modbus.iloc[j,3])
                        
                        raw_data = frameRx[location_data + 6: location_data + 14]
                        # print(raw_data)
                        list_of_values_configured.append(convert_raw_to_value(data_type,raw_data))
                        break
            # print(list_of_values_configured)
                  
            evc_type = evc_type
            query = """
            SELECT amb.daily ,amb.or_der ,amb.address,amb.description,amb.data_type  FROM amr_mapping_billing amb WHERE amb.evc_type = :evc_type AND address is not null order by amb.daily
            ,amb.or_der
            """
            poll_resultsbilling = fetch_data(query, params={"evc_type": evc_type})
        
            df_mappingbilling = pd.DataFrame(poll_resultsbilling, columns=['daily','or_der', 'address', 'description', 'data_type'])
            
            list_of_values_billing = []
            for i in range(0, len(df_mappingbilling)):
                address = int(df_mappingbilling.iloc[i,2])
                data_type = str(df_mappingbilling.iloc[i,4])
                for j in range(0,len(df_Modbusbilling)):
                    address_start = int(df_Modbusbilling.iloc[j,0])
                    address_finish = int(df_Modbusbilling.iloc[j,1])
                    
                    if address >= address_start and address <= address_finish:
                        # print(address)
                        
                        location_data = (address - address_start)*int(8/2)
                        
                        frameRx = (df_Modbusbilling.iloc[j,3])
                        # print(frameRx)
                        raw_data = frameRx[location_data + 6: location_data + 14]
                        
                        
                        list_of_values_billing.append(convert_raw_to_value(data_type,raw_data))   
                        
                        break
       
        # for i in range(0, len(df_mappingbilling), 5):
        #     values_subset = list_of_values_billing[i:i+5]
        #     print(values_subset)
                             
        date_system = datetime.datetime.now().strftime('%d-%m-%Y')   
        sql_text_config_delete = f"""delete from AMR_CONFIGURED_DATA where METER_ID = '{METERID}' AND METER_STREAM_NO = '{run}' AND DATA_DATE = TO_DATE('{date_system}', 'DD-MM-YYYY')"""
    
        sql_text_config_insert = "insert into AMR_CONFIGURED_DATA (DATA_DATE, METER_ID,METER_STREAM_NO, AMR_VC_TYPE, "
        for i in range(0, len(df_mapping)):  
            sql_text_config_insert+=f" AMR_CONFIG{i+1},"

        sql_text_config_insert+=" CREATED_BY) values ("     
        sql_text_config_insert+=f"TO_DATE('{date_system}', 'DD-MM-YYYY'), '{METERID}','{run}','{evc_type}',"
    
        for i in range(0, len(df_mapping)):
            sql_text_config_insert+=f"'{str(list_of_values_configured[i])}',"
            
        sql_text_config_insert+="'')" 
        # print(sql_text_config_insert)
        
        get_maxdate =f"SELECT MAX(DATA_DATE) FROM amr_configured_data WHERE meter_id = '{METERID}' AND meter_stream_no = '{run}'"
        results_maxdaily = fetch_data(get_maxdate)
       
        config_db = pd.DataFrame(results_maxdaily,columns=['DATA_DATE'])
        
        config_db['DATA_DATE'] = pd.to_datetime(config_db['DATA_DATE'])

        # Access the first row and format the date
        config_db_1 = config_db.iloc[0]['DATA_DATE'].strftime('%d-%m-%Y')
        # print(date_system , ":",config_db_1)
        # if date_system == config_db_1:
        #     print("config มีข้อมูลของวันนี้เเล้ว")
            
        #     config_delete = f"DELETE FROM AMR_CONFIGURED_DATA WHERE DATA_DATE = TO_DATE('{date_system}', 'DD-MM-YYYY') AND METER_ID = '{METERID}' AND METER_STREAM_NO = '{run}' AND AMR_VC_TYPE = '{evc_type}'"
            
        #     with cx_Oracle.connect(username, password, f"{hostname}:{port}/{service_name}") as connection:
        #         with connection.cursor() as cursor:
        #             cursor.execute(config_delete)  
        #         connection.commit()  
        #         print("Insert data 'config_delete' successful")
                
        #     with cx_Oracle.connect(username, password, f"{hostname}:{port}/{service_name}") as connection:
        #         with connection.cursor() as cursor:
        #             cursor.execute(sql_text_config_insert)  
        #         connection.commit()  
        #         print("Insert data 'config' successful")
            
        # else:
           
        #     with cx_Oracle.connect(username, password, f"{hostname}:{port}/{service_name}") as connection:
        #         with connection.cursor() as cursor:
        #             cursor.execute(sql_text_config_insert)  
        #         connection.commit()  
        #         print("Insert data 'config' successful")
                
        sql_texts = []
        for i in range(0, len(df_mappingbilling), 5):
             
            values_subset = list_of_values_billing[i:i+5]
            # print(values_subset)
            
            # print(sql_text_billing_delete)
            sql_text_billing_insert = f"INSERT INTO AMR_BILLING_DATA (METER_ID, METER_STREAM_NO, DATA_DATE, CORRECTED_VOL, UNCORRECTED_VOL, AVR_PF, AVR_TF) VALUES ('{METERID}', '{run}', TO_DATE('{values_subset[0]}', 'DD-MM-YYYY')"
    
            for value in values_subset[1:]:
                sql_text_billing_insert += f", '{value}'"
            
            sql_text_billing_insert += ");"
        
            sql_text_billing_insert = sql_text_billing_insert.rstrip(',')
            
            sql_texts.append(sql_text_billing_insert)

        full_sql_text = "\n".join(sql_texts)
        # print()
        # print(full_sql_text)
        # with cx_Oracle.connect(username, password, f"{hostname}:{port}/{service_name}") as connection:
        #     with connection.cursor() as cursor:
        #         for sql_statement in full_sql_text.split(";"):
        #             if sql_statement.strip():
        #                 cursor.execute(sql_statement.strip())
        #         connection.commit()
        #         print("Insert data billing successful")

    # ############ billing #######################
        # query_maxdaily = f"""SELECT MAX(DAILY)FROM amr_mapping_billing WHERE evc_type = '{evc_type}'"""
        # results_maxdaily = fetch_data(query_maxdaily)
        # max_daily_value = results_maxdaily[0][0] 
        # # print("max_daily_value",":",max_daily_value)
         
        # query_maxdaily_1 = f"""SELECT MAX(DAILY)-1 FROM amr_mapping_billing WHERE evc_type = '{evc_type}'"""
        # results_maxdaily_1 = fetch_data(query_maxdaily_1)
        # max_daily_value_1 = results_maxdaily_1[0][0]

        # query_maxdate = """SELECT DATA_DATE FROM (SELECT DATA_DATE, ROW_NUMBER() OVER (ORDER BY DATA_DATE DESC) AS rn FROM amr_billing_data WHERE DATA_DATE = (SELECT MAX(DATA_DATE) FROM amr_billing_data))WHERE rn = 2"""
        # maxdate_db = fetch_data(query_maxdate)
        # maxdate_billing_1 = pd.DataFrame(maxdate_db)
        
        # if maxdate_billing_1.empty:
        #     maxdate_billing_str_1 = "0-0-0"
        # else:
        #     maxdate_billing_1 = maxdate_billing_1.iloc[0]
        
        #     maxdate_billing_str_1 = maxdate_billing_1.iloc[0].strftime('%d-%m-%Y')

        # query_maxdate = """SELECT MAX(DATA_DATE) - 1 FROM amr_billing_data"""
        # maxdate_db = fetch_data(query_maxdate)
        # maxdate_billing = pd.DataFrame(maxdate_db)
        # maxdate_billing = maxdate_billing.iloc[0]
        # maxdate_billing_str = maxdate_billing.iloc[0].strftime('%d-%m-%Y')

        # values_subset_1 = list_of_values_billing[0]
        
        # values_subset = list_of_values_billing[5]

        # ########### เช็คค่า poll ซ้ำ #####################
        # if values_subset_1 == maxdate_billing_str_1:
        #         print(values_subset_1 ,":",maxdate_billing_str_1)
        #         print("poll ซ้ำ")
                
        #         query = f"""SELECT  DATA_DATE, CORRECTED_VOL, UNCORRECTED_VOL 
        #                     FROM amr_billing_data 
        #                     WHERE DATA_DATE BETWEEN TO_DATE('{values_subset_1}', 'DD-MM-YYYY') - INTERVAL '{max_daily_value}' DAY AND TO_DATE('{values_subset_1}', 'DD-MM-YYYY') 
        #                     AND meter_id = '{METERID}' 
        #                     AND meter_stream_no = '{run}' 
        #                     ORDER BY DATA_DATE DESC"""
        #         # print(query)
        #         results_billing = fetch_data(query)

        #         df_billing = pd.DataFrame(results_billing , columns=['DATA_DATE','CORRECTED_VOL', 'UNCORRECTED_VOL'])
        #         df_billing['DATA_DATE'] = df_billing['DATA_DATE'].dt.strftime('%d-%m-%Y')
        #         # print(df_billing_1)
        #         df_billing['DATA_DATE'] = pd.to_datetime(df_billing['DATA_DATE'], format='%d-%m-%Y')
        #         date_counts = df_billing['DATA_DATE'].value_counts()

                
        #         single_dates = date_counts[date_counts == 1].index.tolist()

        #         single_dates_formatted = pd.to_datetime(single_dates).strftime('%d-%m-%Y')
        #         single_date_rows = df_billing[df_billing['DATA_DATE'].isin(single_dates)]

            
        #         df_billing = df_billing[~df_billing['DATA_DATE'].isin(single_dates)]
        
        #         if len(single_dates_formatted) > 0:
        #             print(single_dates_formatted)
        #             for date_formatted in single_dates_formatted:
                    
        #                 sql_text_billing_NotMatched = f"""SELECT DATA_DATE, METER_ID, METER_STREAM_NO FROM amr_billing_data_error
        #                                                 WHERE DATA_DATE = TO_DATE('{date_formatted}', 'DD-MM-YYYY')
        #                                                 AND METER_ID = '{METERID}' 
        #                                                 AND METER_STREAM_NO = '{run}'"""
        #                 billing_NotMatched = fetch_data(sql_text_billing_NotMatched)
        #                 if len(billing_NotMatched) > 0:
        #                         print("มีข้อมูล ใน error")
        #                         sql_text_billing_NotMatched_delete= f"""DELETE FROM AMR_BILLING_DATA 
        #                                                         WHERE DATA_DATE = TO_DATE('{date_formatted}', 'DD-MM-YYYY') 
        #                                                         AND METER_ID = '{METERID}' 
        #                                                         AND METER_STREAM_NO = '{run}'"""
        #                         print(sql_text_billing_NotMatched_delete)
        #                         with cx_Oracle.connect(username, password, f"{hostname}:{port}/{service_name}") as connection:
        #                                 with connection.cursor() as cursor:
        #                                     cursor.execute(sql_text_billing_NotMatched_delete)
        #                                     connection.commit()
        #                                     print("Deleted 'Not' Matched data from billing successfully")
  
        #                 else:
        #                         print("ไม่มีข้อมูล ใน error ")
        #                         print("insert poll เรียบร้อย")
                                
        #             for i in range(0, len(df_billing), 2):
        #                     db_test_matched = df_billing[i:i+2] 
        #                             # print(db_test_matched)
        #                     db_test_matched['DATA_DATE'] = pd.to_datetime(db_test_matched['DATA_DATE']).dt.strftime('%d-%m-%Y')
        #                     if db_test_matched['DATA_DATE'].nunique() == 1 and db_test_matched['CORRECTED_VOL'].nunique() == 1 and db_test_matched['UNCORRECTED_VOL'].nunique() == 1:
        #                                         print("Matched:", db_test_matched)
                                            
        #                                         sql_text_billing_matched_delete= f"""DELETE FROM AMR_BILLING_DATA 
        #                                                                     WHERE DATA_DATE = TO_DATE('{db_test_matched['DATA_DATE'].iloc[0]}', 'DD-MM-YYYY') 
        #                                                                     AND CORRECTED_VOL = {db_test_matched['CORRECTED_VOL'].iloc[0]} 
        #                                                                     AND UNCORRECTED_VOL = {db_test_matched['UNCORRECTED_VOL'].iloc[0]} 
        #                                                                     AND METER_ID = '{METERID}' 
        #                                                                     AND METER_STREAM_NO = '{run}'
        #                                                                     AND ROWNUM = 1"""
        #                                         # print(sql_text_billing_matched_delete)
        #                                         with cx_Oracle.connect(username, password, f"{hostname}:{port}/{service_name}") as connection:
        #                                             with connection.cursor() as cursor:
        #                                                 cursor.execute(sql_text_billing_matched_delete)
        #                                                 connection.commit()
        #                                                 print("Deleted matched data from billing successfully")  
                                            
                                            
                                            
        #                     else:
        #                             print("Not Matched:", db_test_matched)
        #                             query = f"""SELECT   DATA_DATE, CORRECTED_VOL, UNCORRECTED_VOL, AVR_PF, AVR_TF 
        #                                         FROM amr_billing_data 
        #                                         WHERE DATA_DATE = TO_DATE('{db_test_matched['DATA_DATE'].iloc[0]}', 'DD-MM-YYYY') 
        #                                         AND meter_id = '{METERID}' 
        #                                         AND meter_stream_no = '{run}' 
        #                                         ORDER BY DATA_DATE DESC"""
                                    
        #                             results_billing = fetch_data(query)
        #                             for row in results_billing:
        #                                     print(row) 
                                
        #                             sql_texts = []
                                    
        #                             for row in results_billing:
        #                                 formatted_date = row[0].strftime('%d-%m-%Y')  
        #                                 sql_text_billing_insert = f"INSERT INTO AMR_BILLING_DATA_ERROR (METER_ID, METER_STREAM_NO, DATA_DATE, CORRECTED_VOL, UNCORRECTED_VOL, AVR_PE, AVR_TF) VALUES "
        #                                 sql_text_billing_insert += f"('{METERID}', '{run}', TO_DATE('{formatted_date}', 'DD-MM-YYYY')"
        #                                 sql_text_billing_insert += f", '{row[1]}', '{row[2]}', '{row[3]}', '{row[4]}');"
        #                                 sql_texts.append(sql_text_billing_insert)

        #                             full_sql_text = "\n".join(sql_texts)
        #                             with cx_Oracle.connect(username, password, f"{hostname}:{port}/{service_name}") as connection:
        #                                 with connection.cursor() as cursor:
        #                                     for sql_statement in full_sql_text.split(";"):
        #                                         if sql_statement.strip():
        #                                             cursor.execute(sql_statement.strip())
        #                                     connection.commit()
        #                                     print("Insert data ERROR successful")
                                    
        #                             sql_text_billing_NotMatched_delete= f"""DELETE FROM AMR_BILLING_DATA 
        #                                                         WHERE DATA_DATE = TO_DATE('{db_test_matched['DATA_DATE'].iloc[0]}', 'DD-MM-YYYY') 
        #                                                         AND METER_ID = '{METERID}' 
        #                                                         AND METER_STREAM_NO = '{run}'
        #                                                         """
        #                             with cx_Oracle.connect(username, password, f"{hostname}:{port}/{service_name}") as connection:
        #                                 with connection.cursor() as cursor:
        #                                     cursor.execute(sql_text_billing_NotMatched_delete)
        #                                     connection.commit()
        #                                     print("Deleted 'Not' Matched data from billing successfully")  
                                    
        #         else:
        #                     for i in range(0, len(df_billing), 2):
        #                         db_test_matched = df_billing[i:i+2] 
        #                                 # print(db_test_matched)
        #                         db_test_matched['DATA_DATE'] = pd.to_datetime(db_test_matched['DATA_DATE']).dt.strftime('%d-%m-%Y')
        #                         if db_test_matched['DATA_DATE'].nunique() == 1 and db_test_matched['CORRECTED_VOL'].nunique() == 1 and db_test_matched['UNCORRECTED_VOL'].nunique() == 1:
        #                                             print("Matched:", db_test_matched)
                                                
        #                                             sql_text_billing_matched_delete= f"""DELETE FROM AMR_BILLING_DATA 
        #                                                                         WHERE DATA_DATE = TO_DATE('{db_test_matched['DATA_DATE'].iloc[0]}', 'DD-MM-YYYY') 
        #                                                                         AND CORRECTED_VOL = {db_test_matched['CORRECTED_VOL'].iloc[0]} 
        #                                                                         AND UNCORRECTED_VOL = {db_test_matched['UNCORRECTED_VOL'].iloc[0]} 
        #                                                                         AND METER_ID = '{METERID}' 
        #                                                                         AND METER_STREAM_NO = '{run}'
        #                                                                         AND ROWNUM = 1"""
        #                                             # print(sql_text_billing_matched_delete)
        #                                             with cx_Oracle.connect(username, password, f"{hostname}:{port}/{service_name}") as connection:
        #                                                 with connection.cursor() as cursor:
        #                                                     cursor.execute(sql_text_billing_matched_delete)
        #                                                     connection.commit()
        #                                                     print("Deleted matched data from billing successfully")  
                                                             
        #                         else:
        #                                 print("Not Matched:", db_test_matched)
        #                                 query = f"""SELECT   DATA_DATE, CORRECTED_VOL, UNCORRECTED_VOL, AVR_PF, AVR_TF 
        #                                             FROM amr_billing_data 
        #                                             WHERE DATA_DATE = TO_DATE('{db_test_matched['DATA_DATE'].iloc[0]}', 'DD-MM-YYYY') 
        #                                             AND meter_id = '{METERID}' 
        #                                             AND meter_stream_no = '{run}' 
        #                                             ORDER BY DATA_DATE DESC"""
                                        
        #                                 results_billing = fetch_data(query)
        #                                 for row in results_billing:
        #                                         print(row) 
                                    
        #                                 sql_texts = []
                                        
        #                                 for row in results_billing:
        #                                     formatted_date = row[0].strftime('%d-%m-%Y')  
        #                                     sql_text_billing_insert = f"INSERT INTO AMR_BILLING_DATA_ERROR (METER_ID, METER_STREAM_NO, DATA_DATE, CORRECTED_VOL, UNCORRECTED_VOL, AVR_PE, AVR_TF) VALUES "
        #                                     sql_text_billing_insert += f"('{METERID}', '{run}', TO_DATE('{formatted_date}', 'DD-MM-YYYY')"
        #                                     sql_text_billing_insert += f", '{row[1]}', '{row[2]}', '{row[3]}', '{row[4]}');"
        #                                     sql_texts.append(sql_text_billing_insert)

        #                                 full_sql_text = "\n".join(sql_texts)
        #                                 with cx_Oracle.connect(username, password, f"{hostname}:{port}/{service_name}") as connection:
        #                                     with connection.cursor() as cursor:
        #                                         for sql_statement in full_sql_text.split(";"):
        #                                             if sql_statement.strip():
        #                                                 cursor.execute(sql_statement.strip())
        #                                         connection.commit()
        #                                         print("Insert data ERROR successful")
                                        
        #                                 sql_text_billing_NotMatched_delete= f"""DELETE FROM AMR_BILLING_DATA 
        #                                                             WHERE DATA_DATE = TO_DATE('{db_test_matched['DATA_DATE'].iloc[0]}', 'DD-MM-YYYY') 
        #                                                             AND METER_ID = '{METERID}' 
        #                                                             AND METER_STREAM_NO = '{run}'
        #                                                             """
        #                                 with cx_Oracle.connect(username, password, f"{hostname}:{port}/{service_name}") as connection:
        #                                     with connection.cursor() as cursor:
        #                                         cursor.execute(sql_text_billing_NotMatched_delete)
        #                                         connection.commit()
        #                                         print("Deleted 'Not' Matched data from billing successfully")
            
        # ########### เช็คค่า poll ปกติ #####################
        # else:
                    
        #     if values_subset == maxdate_billing_str:
        #         print(values_subset ,":",maxdate_billing_str)
        #         print("ปกติ")
                
        #         query = f"""SELECT  DATA_DATE, CORRECTED_VOL, UNCORRECTED_VOL 
        #                     FROM amr_billing_data 
        #                     WHERE DATA_DATE BETWEEN TO_DATE('{values_subset}', 'DD-MM-YYYY') - INTERVAL '{max_daily_value}' DAY AND TO_DATE('{values_subset}', 'DD-MM-YYYY') 
        #                     AND meter_id = '{METERID}' 
        #                     AND meter_stream_no = '{run}' 
        #                     ORDER BY DATA_DATE DESC"""
            
        #         results_billing = fetch_data(query)

        #         df_billing = pd.DataFrame(results_billing , columns=['DATA_DATE','CORRECTED_VOL', 'UNCORRECTED_VOL'])
        #         df_billing['DATA_DATE'] = df_billing['DATA_DATE'].dt.strftime('%d-%m-%Y')
        #         df_billing['DATA_DATE'] = pd.to_datetime(df_billing['DATA_DATE'], format='%d-%m-%Y')
        #         date_counts = df_billing['DATA_DATE'].value_counts()

                
        #         single_dates = date_counts[date_counts == 1].index.tolist()

        #         single_dates_formatted = pd.to_datetime(single_dates).strftime('%d-%m-%Y')
        #         single_date_rows = df_billing[df_billing['DATA_DATE'].isin(single_dates)]
 
        #         df_billing = df_billing[~df_billing['DATA_DATE'].isin(single_dates)]
                
        #         if len(single_dates_formatted) > 0:
        #             print(single_dates_formatted)
        #             for date_formatted in single_dates_formatted:
                    
        #                 sql_text_billing_NotMatched = f"""SELECT DATA_DATE, METER_ID, METER_STREAM_NO FROM amr_billing_data_error
        #                                                 WHERE DATA_DATE = TO_DATE('{date_formatted}', 'DD-MM-YYYY')
        #                                                 AND METER_ID = '{METERID}' 
        #                                                 AND METER_STREAM_NO = '{run}'"""
        #                 billing_NotMatched = fetch_data(sql_text_billing_NotMatched)
        #                 if len(billing_NotMatched) > 0:
        #                         print("มีข้อมูล ใน error")
        #                         sql_text_billing_NotMatched_delete= f"""DELETE FROM AMR_BILLING_DATA 
        #                                                         WHERE DATA_DATE = TO_DATE('{date_formatted}', 'DD-MM-YYYY') 
        #                                                         AND METER_ID = '{METERID}' 
        #                                                         AND METER_STREAM_NO = '{run}'"""
        #                         print(sql_text_billing_NotMatched_delete)
        #                         with cx_Oracle.connect(username, password, f"{hostname}:{port}/{service_name}") as connection:
        #                                 with connection.cursor() as cursor:
        #                                     cursor.execute(sql_text_billing_NotMatched_delete)
        #                                     connection.commit()
        #                                     print("Deleted 'Not' Matched data from billing successfully")
                                                      
        #                 else:
        #                         print("ไม่มีข้อมูล ใน error ")
        #                         print("insert poll เรียบร้อย")
                                                        
        #             for i in range(0, len(df_billing), 2):
        #                     db_test_matched = df_billing[i:i+2] 
        #                             # print(db_test_matched)
        #                     db_test_matched['DATA_DATE'] = pd.to_datetime(db_test_matched['DATA_DATE']).dt.strftime('%d-%m-%Y')
        #                     if db_test_matched['DATA_DATE'].nunique() == 1 and db_test_matched['CORRECTED_VOL'].nunique() == 1 and db_test_matched['UNCORRECTED_VOL'].nunique() == 1:
        #                                         print("Matched:", db_test_matched)
                                            
        #                                         sql_text_billing_matched_delete= f"""DELETE FROM AMR_BILLING_DATA 
        #                                                                     WHERE DATA_DATE = TO_DATE('{db_test_matched['DATA_DATE'].iloc[0]}', 'DD-MM-YYYY') 
        #                                                                     AND CORRECTED_VOL = {db_test_matched['CORRECTED_VOL'].iloc[0]} 
        #                                                                     AND UNCORRECTED_VOL = {db_test_matched['UNCORRECTED_VOL'].iloc[0]} 
        #                                                                     AND METER_ID = '{METERID}' 
        #                                                                     AND METER_STREAM_NO = '{run}'
        #                                                                     AND ROWNUM = 1"""
        #                                         # print(sql_text_billing_matched_delete)
        #                                         with cx_Oracle.connect(username, password, f"{hostname}:{port}/{service_name}") as connection:
        #                                             with connection.cursor() as cursor:
        #                                                 cursor.execute(sql_text_billing_matched_delete)
        #                                                 connection.commit()
        #                                                 print("Deleted matched data from billing successfully")  
                                                                                
                                            
        #                     else:
        #                             print("Not Matched:", db_test_matched)
        #                             query = f"""SELECT   DATA_DATE, CORRECTED_VOL, UNCORRECTED_VOL, AVR_PF, AVR_TF 
        #                                         FROM amr_billing_data 
        #                                         WHERE DATA_DATE = TO_DATE('{db_test_matched['DATA_DATE'].iloc[0]}', 'DD-MM-YYYY') 
        #                                         AND meter_id = '{METERID}' 
        #                                         AND meter_stream_no = '{run}' 
        #                                         ORDER BY DATA_DATE DESC"""
                                    
        #                             results_billing = fetch_data(query)
        #                             for row in results_billing:
        #                                     print(row) 
                                
        #                             sql_texts = []
                                    
        #                             for row in results_billing:
        #                                 formatted_date = row[0].strftime('%d-%m-%Y')  
        #                                 sql_text_billing_insert = f"INSERT INTO AMR_BILLING_DATA_ERROR (METER_ID, METER_STREAM_NO, DATA_DATE, CORRECTED_VOL, UNCORRECTED_VOL, AVR_PE, AVR_TF) VALUES "
        #                                 sql_text_billing_insert += f"('{METERID}', '{run}', TO_DATE('{formatted_date}', 'DD-MM-YYYY')"
        #                                 sql_text_billing_insert += f", '{row[1]}', '{row[2]}', '{row[3]}', '{row[4]}');"
        #                                 sql_texts.append(sql_text_billing_insert)

        #                             full_sql_text = "\n".join(sql_texts)
        #                             with cx_Oracle.connect(username, password, f"{hostname}:{port}/{service_name}") as connection:
        #                                 with connection.cursor() as cursor:
        #                                     for sql_statement in full_sql_text.split(";"):
        #                                         if sql_statement.strip():
        #                                             cursor.execute(sql_statement.strip())
        #                                     connection.commit()
        #                                     print("Insert data ERROR successful")
                                    
        #                             sql_text_billing_NotMatched_delete= f"""DELETE FROM AMR_BILLING_DATA 
        #                                                         WHERE DATA_DATE = TO_DATE('{db_test_matched['DATA_DATE'].iloc[0]}', 'DD-MM-YYYY') 
        #                                                         AND METER_ID = '{METERID}' 
        #                                                         AND METER_STREAM_NO = '{run}'
        #                                                         """
        #                             with cx_Oracle.connect(username, password, f"{hostname}:{port}/{service_name}") as connection:
        #                                 with connection.cursor() as cursor:
        #                                     cursor.execute(sql_text_billing_NotMatched_delete)
        #                                     connection.commit()
        #                                     print("Deleted 'Not' Matched data from billing successfully")  
                                    
        #     else:
        #                 for i in range(0, len(df_billing), 2):
        #                     db_test_matched = df_billing[i:i+2] 
        #                             # print(db_test_matched)
        #                     db_test_matched['DATA_DATE'] = pd.to_datetime(db_test_matched['DATA_DATE']).dt.strftime('%d-%m-%Y')
        #                     if db_test_matched['DATA_DATE'].nunique() == 1 and db_test_matched['CORRECTED_VOL'].nunique() == 1 and db_test_matched['UNCORRECTED_VOL'].nunique() == 1:
        #                                         print("Matched:", db_test_matched)
                                            
        #                                         sql_text_billing_matched_delete= f"""DELETE FROM AMR_BILLING_DATA 
        #                                                                     WHERE DATA_DATE = TO_DATE('{db_test_matched['DATA_DATE'].iloc[0]}', 'DD-MM-YYYY') 
        #                                                                     AND CORRECTED_VOL = {db_test_matched['CORRECTED_VOL'].iloc[0]} 
        #                                                                     AND UNCORRECTED_VOL = {db_test_matched['UNCORRECTED_VOL'].iloc[0]} 
        #                                                                     AND METER_ID = '{METERID}' 
        #                                                                     AND METER_STREAM_NO = '{run}'
        #                                                                     AND ROWNUM = 1"""
        #                                         # print(sql_text_billing_matched_delete)
        #                                         with cx_Oracle.connect(username, password, f"{hostname}:{port}/{service_name}") as connection:
        #                                             with connection.cursor() as cursor:
        #                                                 cursor.execute(sql_text_billing_matched_delete)
        #                                                 connection.commit()
        #                                                 print("Deleted matched data from billing successfully")  
                                            
                                            
                                            
        #                     else:
        #                             print("Not Matched:", db_test_matched)
        #                             query = f"""SELECT   DATA_DATE, CORRECTED_VOL, UNCORRECTED_VOL, AVR_PF, AVR_TF 
        #                                         FROM amr_billing_data 
        #                                         WHERE DATA_DATE = TO_DATE('{db_test_matched['DATA_DATE'].iloc[0]}', 'DD-MM-YYYY') 
        #                                         AND meter_id = '{METERID}' 
        #                                         AND meter_stream_no = '{run}' 
        #                                         ORDER BY DATA_DATE DESC"""
                                    
        #                             results_billing = fetch_data(query)
        #                             for row in results_billing:
        #                                     print(row) 
                                
        #                             sql_texts = []
                                    
        #                             for row in results_billing:
        #                                 formatted_date = row[0].strftime('%d-%m-%Y')  
        #                                 sql_text_billing_insert = f"INSERT INTO AMR_BILLING_DATA_ERROR (METER_ID, METER_STREAM_NO, DATA_DATE, CORRECTED_VOL, UNCORRECTED_VOL, AVR_PE, AVR_TF) VALUES "
        #                                 sql_text_billing_insert += f"('{METERID}', '{run}', TO_DATE('{formatted_date}', 'DD-MM-YYYY')"
        #                                 sql_text_billing_insert += f", '{row[1]}', '{row[2]}', '{row[3]}', '{row[4]}');"
        #                                 sql_texts.append(sql_text_billing_insert)

        #                             full_sql_text = "\n".join(sql_texts)
        #                             with cx_Oracle.connect(username, password, f"{hostname}:{port}/{service_name}") as connection:
        #                                 with connection.cursor() as cursor:
        #                                     for sql_statement in full_sql_text.split(";"):
        #                                         if sql_statement.strip():
        #                                             cursor.execute(sql_statement.strip())
        #                                     connection.commit()
        #                                     print("Insert data ERROR successful")
                                    
         
                                    
        #                             sql_text_billing_NotMatched_delete= f"""DELETE FROM AMR_BILLING_DATA 
        #                                                         WHERE DATA_DATE = TO_DATE('{db_test_matched['DATA_DATE'].iloc[0]}', 'DD-MM-YYYY') 
        #                                                         AND METER_ID = '{METERID}' 
        #                                                         AND METER_STREAM_NO = '{run}'
        #                                                         """
        #                             with cx_Oracle.connect(username, password, f"{hostname}:{port}/{service_name}") as connection:
        #                                 with connection.cursor() as cursor:
        #                                     cursor.execute(sql_text_billing_NotMatched_delete)
        #                                     connection.commit()
        #                                     print("Deleted 'Not' Matched data from billing successfully")

   
        response = {"status": "success", "message": "Data updated successfully"}
    except ValueError as ve:
        response = {"status": "error", "message": str(ve)}
    except cx_Oracle.DatabaseError as e:
        (error,) = e.args
        print(f"Oracle Database Error {error.code}: {error.message}")
        traceback.print_exc() 
        response = {
            "status": "error",
            "message": f"Database Error: {error.code} - {error.message}",
        }
    except Exception as e:
        print(f"Error: {e}")
        traceback.print_exc()  
        response = {
            "status": "error",
            "message": f"An error occurred while updating data: {str(e)}",
        }
    return jsonify(response)
    
def handle_actaris_action(i, address):
    return address
def handle_action_configuration(i, value, address):
    return value, address
 
@app.route("/process_selected_rows", methods=["POST"])
def process_selected_rows():
    selected_rows = request.form.getlist("selected_rows")
    return "Selected rows processed successfully"
     
if __name__ == "__main__":
    app.run(debug=True)
