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
import numpy as np

app = Flask(__name__)

#### Global Variable 
#For specific configuration data per day 
QUANTITY_CONFIG_DATA = 20  #ค่า config มี 20 ค่า
#For specific quantity of poll range 
QUANTITY_RANGE_CONFIG_LIST = 10  # poll range ทำเป็น list จะมี 10 element

app.secret_key = "your_secret_key_here"

# Replace these values with your actual database credentials
communication_traffic = []
change_to_32bit_counter = 0  # Initialize the counter to 2
def build_request_message(slave_id, function_code, starting_address, quantity):
    request_message = bytearray([
        slave_id,
        function_code,
        starting_address >> 8,
        starting_address & 0xFF,
        quantity >> 8,
        quantity & 0xFF,
    ])

    crc = computeCRC(request_message)
    request_message += crc
    return request_message

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
# active_connection = None  # Global variable to track the active connection

# def connect_to_amr_db():
#     global active_connection
#     username = "AMR_DB"
#     password = "AMR_DB"
#     hostname = "10.104.240.26"
#     port = "1521"
#     sid = "AMR"

#     try:
#         dsn = cx_Oracle.makedsn(hostname, port, sid)
#         connection = cx_Oracle.connect(username, password, dsn)
#         active_connection = "AMR_DB"
#         print("Connected to AMR database")
#         return connection
#     except cx_Oracle.Error as e:
#         (error,) = e.args
#         print("Oracle Error:", error)
#         return None

# def connect_to_ptt_pivot_db():
#     global active_connection
#     username = "PTT_PIVOT"
#     password = "PTT_PIVOT"
#     hostname = "10.100.56.3"
#     port = "1521"
#     service_name = "PTTAMR_MST"

#     try:
#         dsn = cx_Oracle.makedsn(hostname, port, service_name=service_name)
#         connection = cx_Oracle.connect(username, password, dsn)
#         active_connection = "PTT_PIVOT"
#         print("Connected to PTT PIVOT database")
#         return connection
#     except cx_Oracle.Error as e:
#         (error,) = e.args
#         print("Oracle Error:", error)
#         return None

def fetch_data(query, params=None):
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
    

############  /connect database  #####################

######################### connection AMR_DB ###############################
# amr_db_params = {
#     "username": 'AMR_DB',
#     "password": 'AMR_DB',
#     "hostname": '10.104.240.26',
#     "port": '1521',
#     "sid": "AMR"
# }

# # Choose the database connection parameters based on your requirements
# selected_params = amr_db_params  # Change this to switch between databases
# # print("aaaa", selected_params)

# dsn = cx_Oracle.makedsn(selected_params["hostname"], selected_params["port"], selected_params["sid"])

# try:
#     connection_info = {
#         "user": selected_params["username"],
#         "password": selected_params["password"],
#         "dsn": dsn,
#         "min": 1,
#         "max": 5,
#         "increment": 1,
#         "threaded": True
#     }

#     connection_pool = cx_Oracle.SessionPool(**connection_info)
#     connection = connection_pool.acquire()
#     print("Connection to AMR_DB successful.")
# except cx_Oracle.Error as e:
#     (error,) = e.args
#     print("Oracle Error:", error)

######################### connection AMR_DB ###############################

######################### connection AMR_NEW ###############################

# root_params = {
#     "username": 'root',
#     "password": 'root',
#     "hostname": '192.168.102.192',
#     "port": '1521',
#     "service_name": "orcl"
# }

# # Choose the database connection parameters based on your requirements
# selected_params = root_params  # Change this to switch between databases
# # print("aaaa", selected_params)

# dsn = cx_Oracle.makedsn(selected_params["hostname"], selected_params["port"], selected_params["service_name"])

# try:
#     connection_info = {
#         "user": selected_params["username"],
#         "password": selected_params["password"],
#         "dsn": dsn,
#         "min": 1,
#         "max": 5,
#         "increment": 1,
#         "threaded": True
#     }

#     connection_pool = cx_Oracle.SessionPool(**connection_info)
#     connection = connection_pool.acquire()
#     print("Connection to AMR_NEW successful.")
# except cx_Oracle.Error as e:
#     (error,) = e.args
#     print("Oracle Error:", error)

######################### connection AMR_ ###############################


######################### connection PTT_PIVOT ###############################
ptt_pivot_params = {
    "username": "PTT_PIVOT",
    "password": "PTT_PIVOT",
    "hostname": "10.100.56.3",
    "port": "1521",
    "service_name": "PTTAMR_MST"
}

dsn = cx_Oracle.makedsn(ptt_pivot_params["hostname"], ptt_pivot_params["port"], service_name=ptt_pivot_params["service_name"])

try:
    connection_info = {
        "user": ptt_pivot_params["username"],
        "password": ptt_pivot_params["password"],
        "dsn": dsn,
        "min": 1,
        "max": 5,
        "increment": 1,
        "threaded": True
    }

    connection_pool = cx_Oracle.SessionPool(**connection_info)
    connection = connection_pool.acquire()
    print("Connection to PTT_PIVOT successful.")
    
except cx_Oracle.Error as e:
    (error,) = e.args
    print("Oracle Error:", error)

######################### connection PTT_PIVOT ###############################

def fetch_user_data(username):
    query = """
        SELECT "USER_NAME", "PASSWORD", "DESCRIPTION", "USER_LEVEL", "USER_GROUP"
        FROM AMR_USER
        WHERE "USER_NAME" = :username
    """
    params = {'username': username}
    user_data = fetch_data( query, params)
    
    if user_data:
        username, password, description, user_level, user_group = user_data[0]
        return {'password': password, 'description': description, 'user_level': int(user_level), 'user_group': user_group}
    
    return None


users = {}

@app.route('/login', methods=['GET', 'POST'])
def login():
    
    error_message = None  
    
    if request.method == 'POST':
        entered_username = request.form['username']
        entered_password = request.form['password']

        # Query to fetch user data from the database
        query = """
            SELECT "USER_NAME", "PASSWORD", "DESCRIPTION", "USER_LEVEL", "USER_GROUP"
            FROM AMR_USER
            WHERE "USER_NAME" = :entered_username
            AND AMR_USER.user_enable like '1'
        """

        params = {'entered_username': entered_username}
        user_data = fetch_data( query, params)
        # print("login:", user_data)

        if user_data:
            stored_password, description, user_level, user_group = user_data[0][1:]

            if entered_password == stored_password:
                session['username'] = entered_username
                users[entered_username] = {'password': stored_password, 'description': description, 'user_level': user_level, 'user_group': user_group}
                if user_level == '1' or user_level == '4' or user_level == '5':
                    return redirect(url_for('home_amr'))
                elif user_level == '2':
                    return redirect(url_for('home_user_group'))
                elif user_level == '3':
                    return redirect(url_for('home_user'))
            else:
                error_message = 'Incorrect password'
        else:
            error_message = 'User not found'

    return render_template('login.html', error_message=error_message)


@app.route('/')
def home_amr():  
    if 'username' in session:
        username = session['username']
        user = users.get(username)  # Using get method to handle KeyError
        if user:
            return render_template('home.html', username=username, description=user['description'], user_level=user['user_level'])
        else:
            # Handle the case where the user is not in the users dictionary
            flash('User information not found. Please log in again.', 'error')
            return redirect(url_for('login'))
    else:
        flash('Please log in to access this page.', 'error')
        return redirect(url_for('login'))

@app.route('/home_user_group')
def home_user_group():  
    if 'username' in session:
        username = session['username']
        user = users.get(username)  # Using get method to handle KeyError
        if user:
            return render_template('home_user_group.html', username=username, description=user['description'], user_level=user['user_level'])
        else:
            # Handle the case where the user is not in the users dictionary
            flash('User information not found. Please log in again.', 'error')
            return redirect(url_for('login'))
    else:
        flash('Please log in to access this page.', 'error')
        return redirect(url_for('login'))
        
@app.route('/home_user')
def home_user():  
    if 'username' in session:
        username = session['username']
        user = users.get(username)  # Using get method to handle KeyError
        if user:
            return render_template('home_user.html', username=username, description=user['description'], user_level=user['user_level'])
        else:
            # Handle the case where the user is not in the users dictionary
            flash('User information not found. Please log in again.', 'error')
            return redirect(url_for('login'))
    else:
        flash('Please log in to access this page.', 'error')
        return redirect(url_for('login'))
############  Home page  #####################
# @app.route("/")
# def home_amr():
#     return render_template("home.html")
############ / Home page  #####################

@app.route("/ASGS")
def ASGS():
    return render_template("ASGS.html")


############  View Billing Data   #####################


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
    tag_options.sort()
    return jsonify({"tag_options": tag_options})


@app.route("/billing_data")
def billing_data(): 
    query_type = request.args.get("query_type")


    # SQL query to fetch unique PL_REGION_ID values
    region_query = """
    SELECT * FROM AMR_REGION 
    """


    tag_query = """
    SELECT DISTINCT TAG_ID
    FROM AMR_FIELD_ID
    JOIN AMR_PL_GROUP ON AMR_FIELD_ID.FIELD_ID = AMR_PL_GROUP.FIELD_ID 
    WHERE AMR_PL_GROUP.PL_REGION_ID = :region_id
    """

    # Fetch unique region values
    region_results = fetch_data(region_query)
    region_options = [str(region[0]) for region in region_results]
    
    

    query = ""
    print(query)
    if query_type == "daily_data":
        # SQL query for main data
        query = """
        SELECT DISTINCT
            AMR_PL_GROUP.PL_REGION_ID,
            AMR_FIELD_ID.TAG_ID,
            AMR_FIELD_ID.METER_ID,
            TO_CHAR(AMR_BILLING_DATA.DATA_DATE),
            
            AMR_BILLING_DATA.CORRECTED_VOL as CORRECTED,
            AMR_BILLING_DATA.UNCORRECTED_VOL as UNCORRECTED,
            AMR_BILLING_DATA.AVR_PF as Pressure,
            AMR_BILLING_DATA.AVR_TF as Temperature,
            AMR_BILLING_DATA.METER_STREAM_NO  -- Add this line to include METER_STREAM_NO in the SELECT clause
        FROM
            AMR_FIELD_ID, AMR_PL_group, AMR_BILLING_DATA
        WHERE
            AMR_PL_GROUP.FIELD_ID = AMR_FIELD_ID.FIELD_ID 
            AND AMR_BILLING_DATA.METER_ID = AMR_FIELD_ID.METER_ID
            AND AMR_BILLING_DATA.METER_STREAM_NO IS NOT NULL
            {billing_date_condition}
            {tag_condition}
            {region_condition}
        """
        print(query)

        # Return the template with the DataFrame

    elif query_type == "config_data":
        query = """
        SELECT
            AMR_PL_GROUP.PL_REGION_ID,
            AMR_FIELD_ID.TAG_ID,
            amr_field_id.meter_id,
            TO_CHAR(AMR_CONFIGURED_DATA.DATA_DATE),
            
            amr_configured_data.amr_config1,
            amr_configured_data.amr_config2,
            amr_configured_data.amr_config3,
            amr_configured_data.amr_config4,
            amr_configured_data.amr_config5,
            amr_configured_data.amr_config6,
            amr_configured_data.amr_config7,
            amr_configured_data.amr_config8,
            amr_configured_data.amr_config9,
            amr_configured_data.amr_config10,
            amr_configured_data.amr_config11,
            amr_configured_data.amr_config12,
            amr_configured_data.amr_config13,
            amr_configured_data.amr_config14,
            amr_configured_data.amr_config15,
            amr_configured_data.amr_config16,
            amr_configured_data.amr_config17,
            amr_configured_data.amr_config18,
            amr_configured_data.amr_config19,
            amr_configured_data.amr_config20,
            
            
            AMR_VC_CONFIGURED_INFO.config1,
            AMR_VC_CONFIGURED_INFO.config2,
            AMR_VC_CONFIGURED_INFO.config3,
            AMR_VC_CONFIGURED_INFO.config4,
            AMR_VC_CONFIGURED_INFO.config5,
            AMR_VC_CONFIGURED_INFO.config6,
            AMR_VC_CONFIGURED_INFO.config7,
            AMR_VC_CONFIGURED_INFO.config8,
            AMR_VC_CONFIGURED_INFO.config9,
            AMR_VC_CONFIGURED_INFO.config10,
            AMR_VC_CONFIGURED_INFO.config11,
            AMR_VC_CONFIGURED_INFO.config12,
            AMR_VC_CONFIGURED_INFO.config13,
            AMR_VC_CONFIGURED_INFO.config14,
            AMR_VC_CONFIGURED_INFO.config15,
            AMR_VC_CONFIGURED_INFO.config16,
            AMR_VC_CONFIGURED_INFO.config17,
            AMR_VC_CONFIGURED_INFO.config18,
            AMR_VC_CONFIGURED_INFO.config19,
            AMR_VC_CONFIGURED_INFO.config20,
            AMR_CONFIGURED_DATA.METER_STREAM_NO
            
        FROM
            AMR_FIELD_ID, AMR_PL_group, AMR_CONFIGURED_DATA
        JOIN AMR_VC_CONFIGURED_INFO ON amr_configured_data.amr_vc_type = AMR_VC_CONFIGURED_INFO.vc_type
        WHERE
            AMR_PL_GROUP.FIELD_ID = AMR_FIELD_ID.FIELD_ID 
            AND AMR_CONFIGURED_DATA.METER_ID = AMR_FIELD_ID.METER_ID
            AND AMR_CONFIGURED_DATA.METER_STREAM_NO is not null
            
            {configured_date_condition}
            {tag_condition}
            {region_condition}
        """
        print(query)
    # Get selected values from the dropdowns
    billing_date_condition = "AND AMR_BILLING_DATA.DATA_DATE IS NOT NULL"
    configured_date_condition = "AND AMR_CONFIGURED_DATA.DATA_DATE IS NOT NULL"
    tag_condition = "AND AMR_FIELD_ID.TAG_ID IS NOT NULL"
    region_condition = "AND amr_pl_group.pl_region_id IS NOT NULL"

    selected_date = request.args.get("date_dropdown")
    selected_tag = request.args.get("tag_dropdown")
    selected_region = request.args.get("region_dropdown")

    # Fetch unique region values
    region_results = fetch_data(region_query)
    region_options = [str(region[0]) for region in region_results]

    # Fetch tag options based on the selected region
    tag_results = fetch_data(tag_query, params={"region_id": selected_region})
    tag_options = [str(tag[0]) for tag in tag_results]

    if selected_date:
        billing_date_condition = (
            f"AND TO_CHAR(AMR_BILLING_DATA.DATA_DATE, 'MM/YYYY') = '{selected_date}'"
        )
        configured_date_condition = (
            f"AND TO_CHAR(AMR_CONFIGURED_DATA.DATA_DATE, 'MM/YYYY') = '{selected_date}'"
        )
    if selected_tag:
        tag_condition = f"AND AMR_FIELD_ID.TAG_ID = '{selected_tag}'"

    if selected_region:
        region_condition = f"AND amr_pl_group.pl_region_id = '{selected_region}'"

    # Modify the query with the selected conditions
    query = query.format(
        billing_date_condition=billing_date_condition,
        configured_date_condition=configured_date_condition,
        tag_condition=tag_condition,
        region_condition=region_condition,
    )

    if selected_region:
        # Use fetch_data function to retrieve data
        results = fetch_data(query)

        if query_type == "daily_data":
            # Use pandas to create a DataFrame for daily_data
            df = pd.DataFrame(
                results,
                columns=[
                    "PL_REGION_ID",
                    "TAG_ID",
                    "METER_ID",
                    "DATA_DATE",
                    "CORRECTED",
                    "UNCORRECTED",
                    "Pressure",
                    "Temperature",
                    "METER_STREAM_NO",
                ],
            )
            # Get the selected Meter ID before removing it from the DataFrame
            # selected_meter_id = df["METER_ID"].iloc[0]
            selected_meter_id = None

            # Check if 'METER_ID' column exists and the DataFrame is not empty
            if not df.empty and 'METER_ID' in df.columns and len(df['METER_ID']) > 0:
                selected_meter_id = df['METER_ID'].iloc[0]
                print(f"Selected Meter ID: {selected_meter_id}")
            else:
                print("DataFrame is empty or 'METER_ID' column doesn't exist.")

            # Now, remove the "METER_ID" column from the DataFrame
            df = df.drop(["PL_REGION_ID", "TAG_ID", "METER_ID"], axis=1)

            # Remove newline characters
            df = df.apply(lambda x: x.str.replace("\n", "") if x.dtype == "object" else x)

            df = df.drop_duplicates(subset=["DATA_DATE", "METER_STREAM_NO"], keep="first")
            # Sort DataFrame by 'DATA_DATE'
            df = df.sort_values(by="DATA_DATE")

            # Assuming 'df' is the DataFrame created from the query results
            num_streams = 6
            df_runs = {}

            # Loop to create DataFrames for each METER_STREAM_NO
            for i in range(1, num_streams + 1):
                df_runs[f'df_run{i}'] = df[df['METER_STREAM_NO'] == str(i)]

            # Check if each DataFrame has data before including in the tables dictionary
            tables = {
                "config_data": None,
            }

            graphs = {
                "corrected": None,
                "uncorrected": None,
                "pressure": None,
                "temperature": None
            }
            
            selected_date = request.args.get("date_dropdown")
            print("date1:", selected_date)

            # Initialize df_month_list outside the if statement
            df_month_list = pd.DataFrame(columns=['DATA_DATE'])

            # Check if 'selected_date' is available
            if selected_date:
                # Convert selected_date to 'YYYY-MM' format for consistency
                selected_date_formatted = pd.to_datetime(selected_date, format='%m/%Y').strftime('%Y-%m')
                print("date2:", selected_date_formatted)

                # Get the current month and year
                current_month_year = datetime.now().strftime('%Y-%m')

                # Determine if the selected date is in the current month
                is_current_month = selected_date_formatted == current_month_year

                # Update the query to use the selected date
                if is_current_month:
                    # If the selected date is in the current month, show all days up to the current date
                    query_day = f"""
                        SELECT TO_CHAR(TRUNC(LEVEL - 1) + TO_DATE('{current_month_year}-01', 'YYYY-MM-DD')) AS Date1
                        FROM DUAL
                        CONNECT BY LEVEL <= TO_DATE('{datetime.now().strftime('%Y-%m-%d')}', 'YYYY-MM-DD') - TO_DATE('{current_month_year}-01', 'YYYY-MM-DD') + 1
                    """
                else:
                    # If the selected date is in a previous month, show all days of the selected month
                    query_day = f"""
                        SELECT TO_CHAR(TRUNC(LEVEL - 1) + TO_DATE('{selected_date_formatted}-01', 'YYYY-MM-DD')) AS Date1
                        FROM DUAL
                        CONNECT BY LEVEL <= LAST_DAY(TO_DATE('{selected_date_formatted}-01', 'YYYY-MM-DD')) - TO_DATE('{selected_date_formatted}-01', 'YYYY-MM-DD') + 1
                    """

                # Fetch data for the month list
                query_day_result = fetch_data(query_day)
                df_month_list = pd.DataFrame(query_day_result, columns=['DATA_DATE'])
            
             # Merge DataFrames using a loop
            for i in range(1, num_streams + 1):
                df_run = df_runs[f'df_run{i}']
                
                if not df_run.empty:
                    merged_df = pd.merge(df_month_list, df_run, on='DATA_DATE', how='outer')
                    df_runs[f'df_run{i}'] = merged_df

            for i in range(1, num_streams + 1):
                df_run = df_runs[f'df_run{i}']
                if not df_run.empty:
                    df_run = df_run.drop('METER_STREAM_NO', axis=1, errors='ignore')
                    df_run = df_run.fillna("N/A")
                    tables[f"daily_data_run{i}"] = df_run.to_html(classes="data", index=False, na_rep="N/A")
                            
            # common_table_properties = {"classes": "data", "index": False,"header":None}
            
            # Create graphs for each METER_STREAM_NO
            for i in range(1, 7):
                df_run = df[df['METER_STREAM_NO'] == str(i)]

                # Create traces for each graph
                trace_corrected = go.Scatter(
                    x=df_run["DATA_DATE"],
                    y=df_run["CORRECTED"],
                    mode="lines+markers",
                    name=f"Run {i} - Corrected",
                    line=dict(color="blue", width=2),
                )

                trace_uncorrected = go.Scatter(
                    x=df_run["DATA_DATE"],
                    y=df_run["UNCORRECTED"],
                    mode="lines+markers",
                    name=f"Run {i} - Uncorrected",
                    line=dict(color="red", width=2),
                )

                trace_pressure = go.Scatter(
                    x=df_run["DATA_DATE"],
                    y=df_run["Pressure"],
                    mode="lines+markers",
                    name=f"Run {i} - Pressure",
                    line=dict(color="orange", width=2),
                )

                trace_temperature = go.Scatter(
                    x=df_run["DATA_DATE"],
                    y=df_run["Temperature"],
                    mode="lines+markers",
                    name=f"Run {i} - Temperature",
                    line=dict(color="green", width=2),
                )

                # Create subplot for each graph
                fig_corrected = sp.make_subplots(rows=1, cols=1, subplot_titles=[f"Run {i} - Corrected"])
                fig_uncorrected = sp.make_subplots(rows=1, cols=1, subplot_titles=[f"Run {i} - Uncorrected"])
                fig_pressure = sp.make_subplots(rows=1, cols=1, subplot_titles=[f"Run {i} - Pressure"])
                fig_temperature = sp.make_subplots(rows=1, cols=1, subplot_titles=[f"Run {i} - Temperature"])

                # Add traces to subplots
                fig_corrected.add_trace(trace_corrected)
                fig_uncorrected.add_trace(trace_uncorrected)
                fig_pressure.add_trace(trace_pressure)
                fig_temperature.add_trace(trace_temperature)

                # Update subplot and layout properties
                for fig in [fig_corrected, fig_uncorrected, fig_pressure, fig_temperature]:
                    fig.update_traces(
                        line_shape="linear",
                        marker=dict(symbol="circle", size=6),
                        hoverinfo="text+x+y",
                        hovertext=df_run["DATA_DATE"],
                    )
                    fig.update_layout(
                        legend=dict(x=0.6, y=1.25, orientation="h"),
                        yaxis_title="Values",
                        xaxis_title="Date",
                        hovermode="x unified",
                        yaxis=dict(type="linear", title="Values"),
                    )
                    fig.update_xaxes(title_text="Date", tickformat="%Y-%m-%d")

                # Get HTML for each graph
                graph_corrected = fig_corrected.to_html(full_html=False)
                graph_uncorrected = fig_uncorrected.to_html(full_html=False)
                graph_pressure = fig_pressure.to_html(full_html=False)
                graph_temperature = fig_temperature.to_html(full_html=False)

                # Store HTML in the graphs dictionary
                graphs[f"corrected_run{i}"] = graph_corrected
                graphs[f"uncorrected_run{i}"] = graph_uncorrected
                graphs[f"pressure_run{i}"] = graph_pressure
                graphs[f"temperature_run{i}"] = graph_temperature


                # เพิ่มเนื้อหา HTML สำหรับกราฟ
                df = df.sort_values(by="DATA_DATE", ascending=True)
                # ส่ง graph_html ไปยัง HTML template ของ Flask
                return render_template(
                    "billingdata.html",
                    tables=tables,
                    titles=df.columns.values,
                    selected_date=selected_date,
                    selected_tag=selected_tag,
                    selected_region=selected_region,
                    region_options=region_options,
                    tag_options=tag_options,
                    selected_meter_id=selected_meter_id,
                    graph_corrected=graph_corrected,
                    graph_uncorrected=graph_uncorrected,
                    graph_pressure=graph_pressure,
                    graph_temperature=graph_temperature,

                )


        elif query_type == "config_data":
            # Use pandas to create a DataFrame for config_data
            df = pd.DataFrame(
                results,
                columns=[
                    "PL_REGION_ID",
                    "TAG_ID",
                    "METER_ID",
                    "DATA_DATE",
                    "AMR_CONFIG1",
                    "AMR_CONFIG2",
                    "AMR_CONFIG3",
                    "AMR_CONFIG4",
                    "AMR_CONFIG5",
                    "AMR_CONFIG6",
                    "AMR_CONFIG7",
                    "AMR_CONFIG8",
                    "AMR_CONFIG9",
                    "AMR_CONFIG10",
                    "AMR_CONFIG11",
                    "AMR_CONFIG12",
                    "AMR_CONFIG13",
                    "AMR_CONFIG14",
                    "AMR_CONFIG15",
                    "AMR_CONFIG16",
                    "AMR_CONFIG17",
                    "AMR_CONFIG18",
                    "AMR_CONFIG19",
                    "AMR_CONFIG20",
                    "CONFIG1",
                    "CONFIG2",
                    "CONFIG3",
                    "CONFIG4",
                    "CONFIG5",
                    "CONFIG6",
                    "CONFIG7",
                    "CONFIG8",
                    "CONFIG9",
                    "CONFIG10",
                    "CONFIG11",
                    "CONFIG12",
                    "CONFIG13",
                    "CONFIG14",
                    "CONFIG15",
                    "CONFIG16",
                    "CONFIG17",
                    "CONFIG18",
                    "CONFIG19",
                    "CONFIG20",
                    "METER_STREAM_NO",
                ]
            )
            columns_to_drop = [
                "CONFIG1",
                "CONFIG2",
                "CONFIG3",
                "CONFIG4",
                "CONFIG5",
                "CONFIG6",
                "CONFIG7",
                "CONFIG8",
                "CONFIG9",
                "CONFIG10",
                "CONFIG11",
                "CONFIG12",
                "CONFIG13",
                "CONFIG14",
                "CONFIG15",
                "CONFIG16",
                "CONFIG17",
                "CONFIG18",
                "CONFIG19",
                "CONFIG20",
            ]
            dropped_columns_data = pd.concat(
                [
                    pd.DataFrame(columns=df.columns),
                    pd.DataFrame(columns=columns_to_drop),
                ],
                axis=1,
            )
            dropped_columns_data = df[["DATA_DATE"] + columns_to_drop].head(1)
            dropped_columns_data[
                "DATA_DATE"
            ] = "DATA.DATE"  # Replace actual values with the column name
            dropped_columns_data = dropped_columns_data.to_dict(orient="records")

            df = df.drop(columns=columns_to_drop)  # Drop specified columns
            
            # selected_meter_id = df["METER_ID"].iloc[0]
            # Get the selected Meter ID before removing it from the DataFrame
            ##!!!! Detact if empty 
            
            selected_meter_id = None

            # Check if 'METER_ID' column exists and the DataFrame is not empty
            if not df.empty and 'METER_ID' in df.columns and len(df['METER_ID']) > 0:
                selected_meter_id = df['METER_ID'].iloc[0]
                print(f"Selected Meter ID: {selected_meter_id}")
            else:
                print("DataFrame is empty or 'METER_ID' column doesn't exist.")

            # Now, remove the "METER_ID" column from the DataFrame
            df = df.drop(["PL_REGION_ID", "TAG_ID", "METER_ID"], axis=1)

            # Remove newline characters
            df = df.apply(lambda x: x.str.replace("\n", "") if x.dtype == "object" else x)

            df = df.drop_duplicates(subset=["DATA_DATE", "METER_STREAM_NO"], keep="first")
            # Sort DataFrame by 'DATA_DATE'
            df = df.sort_values(by="DATA_DATE")
            

            num_streams = 6
            df_runs = {}

            # Loop to create DataFrames for each METER_STREAM_NO
            for i in range(1, num_streams + 1):
                df_runs[f'df_run{i}'] = df[df['METER_STREAM_NO'] == str(i)]

            # Check if each DataFrame has data before including in the tables dictionary
            # Create Full table of selectedMonth
            tables = {
                "daily_data": None,
                
            }
            
            selected_date = request.args.get("date_dropdown")
            print("date1:", selected_date)

            # Check if 'selected_date' is available
            if selected_date:
                # Convert selected_date to 'YYYY-MM' format for consistency
                selected_date_formatted = pd.to_datetime(selected_date, format='%m/%Y').strftime('%Y-%m')
                print("date2:", selected_date_formatted)

                # Get the current month and year
                current_month_year = datetime.now().strftime('%Y-%m')

                # Determine if the selected date is in the current month
                is_current_month = selected_date_formatted == current_month_year

                # Update the query to use the selected date
                if is_current_month:
                    # If the selected date is in the current month, show all days up to the current date
                    query_day = f"""
                        SELECT TO_CHAR(TRUNC(LEVEL - 1) + TO_DATE('{current_month_year}-01', 'YYYY-MM-DD')) AS Date1
                        FROM DUAL
                        CONNECT BY LEVEL <= TO_DATE('{datetime.now().strftime('%Y-%m-%d')}', 'YYYY-MM-DD') - TO_DATE('{current_month_year}-01', 'YYYY-MM-DD') + 1
                    """
                else:
                    # If the selected date is in a previous month, show all days of the selected month
                    query_day = f"""
                        SELECT TO_CHAR(TRUNC(LEVEL - 1) + TO_DATE('{selected_date_formatted}-01', 'YYYY-MM-DD')) AS Date1
                        FROM DUAL
                        CONNECT BY LEVEL <= LAST_DAY(TO_DATE('{selected_date_formatted}-01', 'YYYY-MM-DD')) - TO_DATE('{selected_date_formatted}-01', 'YYYY-MM-DD') + 1
                    """

                # Fetch data for the month list
                query_day_result = fetch_data(query_day)
                df_month_list = pd.DataFrame(query_day_result, columns=['DATA_DATE'])

            

            # Merge DataFrames using a loop
            for i in range(1, num_streams + 1):
                df_run = df_runs[f'df_run{i}']
                
                if not df_run.empty:
                    merged_df = pd.merge(df_month_list, df_run, on='DATA_DATE', how='outer')
                    df_runs[f'df_run{i}'] = merged_df
                
            common_table_properties = {"classes": "data", "index": False, "header": None, "na_rep": "N/A"}


            for i in range(1, num_streams + 1):
                df_run = df_runs[f'df_run{i}']
                if not df_run.empty:
                    df_run = df_run.drop('METER_STREAM_NO', axis=1, errors='ignore')
                    df_run = df_run.fillna("N/A")
                    tables[f"config_data_run{i}"] = df_run.to_html(**common_table_properties)
        
            return render_template(
                "billingdata.html",
                tables=tables,
                titles=df.columns.values,
                selected_date=selected_date,
                selected_tag=selected_tag,
                selected_region=selected_region,
                region_options=region_options,
                tag_options=tag_options, 
                dropped_columns_data=dropped_columns_data,
                selected_meter_id=selected_meter_id
            )
    else:
        # Render the template without executing the query
        return render_template(
            "billingdata.html",
            selected_date=selected_date,
            selected_region=selected_region,
            selected_tag=selected_tag,
            region_options=region_options,
            tag_options=tag_options,
            tables={}
        )
            

@app.route("/billing_data_user_group")
def billing_data_user_group():

    query_type = request.args.get("query_type")
    
    if 'username' not in session:
        return redirect(url_for('login'))

    # Fetch user information from the session
    logged_in_user = session['username']
    if logged_in_user not in users:
        return redirect(url_for('login'))
    
    user_info = users[logged_in_user]
    user_level = user_info.get('user_level')
    description = user_info.get('description')
    print("description", description)
    
    logged_in_user = logged_in_user
    print("user:", logged_in_user)


    # SQL query to fetch unique PL_REGION_ID values
    region_query = """
    SELECT amr_user.user_group 
    FROM AMR_user 
    WHERE user_name = :logged_in_user
    AND amr_user.user_enable like '1' 
    """
    print("ree", region_query)
    # Fetch unique region values
    region_results = fetch_data( region_query, params={'logged_in_user': logged_in_user})
    
    
    region_options_tmp = [str(region[0]) for region in region_results]
    # print("des", region_options)
    
    region_options = region_options_tmp[0]


    # tag_query = """
    # SELECT DISTINCT TAG_ID
    # FROM AMR_FIELD_ID
    # JOIN AMR_PL_GROUP ON AMR_FIELD_ID.FIELD_ID = AMR_PL_GROUP.FIELD_ID 
    # WHERE AMR_PL_GROUP.PL_REGION_ID = :region_id
    # """
    
    tag_query = """
    SELECT DISTINCT AMR_FIELD_ID.TAG_ID 
    FROM AMR_FIELD_ID, amr_user, amr_pl_group
    WHERE
        amr_user.user_group = amr_pl_group.pl_region_id
        and AMR_FIELD_ID.FIELD_ID = AMR_PL_GROUP.FIELD_ID
        and AMR_FIELD_ID.tag_id NOT like '%.remove%'
        and amr_pl_group.pl_region_id = :region_options
        ORDER BY AMR_FIELD_ID.TAG_ID
    """
    
    print(tag_query)
    tag_results = fetch_data(tag_query, params={"region_options": region_options})
    tag_options = [str(tag[0]) for tag in tag_results]
    print("tag:", tag_options)
    
    query = ""
    print(query)
    if query_type == "daily_data":
        # SQL query for main data
        query = """
        SELECT DISTINCT
            AMR_PL_GROUP.PL_REGION_ID,
            AMR_FIELD_ID.TAG_ID,
            AMR_FIELD_ID.METER_ID,
            TO_CHAR(AMR_BILLING_DATA.DATA_DATE),
            
            AMR_BILLING_DATA.CORRECTED_VOL as CORRECTED,
            AMR_BILLING_DATA.UNCORRECTED_VOL as UNCORRECTED,
            AMR_BILLING_DATA.AVR_PF as Pressure,
            AMR_BILLING_DATA.AVR_TF as Temperature,
            AMR_BILLING_DATA.METER_STREAM_NO  -- Add this line to include METER_STREAM_NO in the SELECT clause
        FROM
            AMR_FIELD_ID, AMR_PL_group, AMR_BILLING_DATA
        WHERE
            AMR_PL_GROUP.FIELD_ID = AMR_FIELD_ID.FIELD_ID 
            AND AMR_BILLING_DATA.METER_ID = AMR_FIELD_ID.METER_ID
            AND AMR_BILLING_DATA.METER_STREAM_NO IS NOT NULL
            {billing_date_condition}
            {tag_condition}
            {region_condition}
        """
        print(query)

        # Return the template with the DataFrame

    elif query_type == "config_data":
        query = """
        SELECT
            AMR_PL_GROUP.PL_REGION_ID,
            AMR_FIELD_ID.TAG_ID,
            amr_field_id.meter_id,
            TO_CHAR(AMR_CONFIGURED_DATA.DATA_DATE),
            
            amr_configured_data.amr_config1,
            amr_configured_data.amr_config2,
            amr_configured_data.amr_config3,
            amr_configured_data.amr_config4,
            amr_configured_data.amr_config5,
            amr_configured_data.amr_config6,
            amr_configured_data.amr_config7,
            amr_configured_data.amr_config8,
            amr_configured_data.amr_config9,
            amr_configured_data.amr_config10,
            amr_configured_data.amr_config11,
            amr_configured_data.amr_config12,
            amr_configured_data.amr_config13,
            amr_configured_data.amr_config14,
            amr_configured_data.amr_config15,
            amr_configured_data.amr_config16,
            amr_configured_data.amr_config17,
            amr_configured_data.amr_config18,
            amr_configured_data.amr_config19,
            amr_configured_data.amr_config20,
            
            
            AMR_VC_CONFIGURED_INFO.config1,
            AMR_VC_CONFIGURED_INFO.config2,
            AMR_VC_CONFIGURED_INFO.config3,
            AMR_VC_CONFIGURED_INFO.config4,
            AMR_VC_CONFIGURED_INFO.config5,
            AMR_VC_CONFIGURED_INFO.config6,
            AMR_VC_CONFIGURED_INFO.config7,
            AMR_VC_CONFIGURED_INFO.config8,
            AMR_VC_CONFIGURED_INFO.config9,
            AMR_VC_CONFIGURED_INFO.config10,
            AMR_VC_CONFIGURED_INFO.config11,
            AMR_VC_CONFIGURED_INFO.config12,
            AMR_VC_CONFIGURED_INFO.config13,
            AMR_VC_CONFIGURED_INFO.config14,
            AMR_VC_CONFIGURED_INFO.config15,
            AMR_VC_CONFIGURED_INFO.config16,
            AMR_VC_CONFIGURED_INFO.config17,
            AMR_VC_CONFIGURED_INFO.config18,
            AMR_VC_CONFIGURED_INFO.config19,
            AMR_VC_CONFIGURED_INFO.config20,
            AMR_CONFIGURED_DATA.METER_STREAM_NO
            
        FROM
            AMR_FIELD_ID, AMR_PL_group, AMR_CONFIGURED_DATA
        JOIN AMR_VC_CONFIGURED_INFO ON amr_configured_data.amr_vc_type = AMR_VC_CONFIGURED_INFO.vc_type
        WHERE
            AMR_PL_GROUP.FIELD_ID = AMR_FIELD_ID.FIELD_ID 
            AND AMR_CONFIGURED_DATA.METER_ID = AMR_FIELD_ID.METER_ID
            AND AMR_CONFIGURED_DATA.METER_STREAM_NO is not null
            
            {configured_date_condition}
            {tag_condition}
            {region_condition}
        """
        print(query)
    # Get selected values from the dropdowns
    billing_date_condition = "AND AMR_BILLING_DATA.DATA_DATE IS NOT NULL"
    configured_date_condition = "AND AMR_CONFIGURED_DATA.DATA_DATE IS NOT NULL"
    tag_condition = "AND AMR_FIELD_ID.TAG_ID IS NOT NULL"
    region_condition = "AND amr_pl_group.pl_region_id IS NOT NULL"

    selected_date = request.args.get("date_dropdown")
    selected_tag = request.args.get("tag_dropdown")
    selected_region = request.args.get("region_dropdown")

    

    if selected_date:
        billing_date_condition = (
            f"AND TO_CHAR(AMR_BILLING_DATA.DATA_DATE, 'MM/YYYY') = '{selected_date}'"
        )
        configured_date_condition = (
            f"AND TO_CHAR(AMR_CONFIGURED_DATA.DATA_DATE, 'MM/YYYY') = '{selected_date}'"
        )
    if selected_tag:
        tag_condition = f"AND AMR_FIELD_ID.TAG_ID = '{selected_tag}'"

    if selected_region:
        region_condition = f"AND amr_pl_group.pl_region_id = '{selected_region}'"

    # Modify the query with the selected conditions
    query = query.format(
        billing_date_condition=billing_date_condition,
        configured_date_condition=configured_date_condition,
        tag_condition=tag_condition,
        region_condition=region_condition,
    )

    if selected_region:
        # Use fetch_data function to retrieve data
        results = fetch_data(query)

        if query_type == "daily_data":
            # Use pandas to create a DataFrame for daily_data
            df = pd.DataFrame(
                results,
                columns=[
                    "PL_REGION_ID",
                    "TAG_ID",
                    "METER_ID",
                    "DATA_DATE",
                    "CORRECTED",
                    "UNCORRECTED",
                    "Pressure",
                    "Temperature",
                    "METER_STREAM_NO",
                ],
            )
            # Get the selected Meter ID before removing it from the DataFrame
            # selected_meter_id = df["METER_ID"].iloc[0]

            selected_meter_id = None

            # Check if 'METER_ID' column exists and the DataFrame is not empty
            if not df.empty and 'METER_ID' in df.columns and len(df['METER_ID']) > 0:
                selected_meter_id = df['METER_ID'].iloc[0]
                print(f"Selected Meter ID: {selected_meter_id}")
            else:
                print("DataFrame is empty or 'METER_ID' column doesn't exist.")

            # Now, remove the "METER_ID" column from the DataFrame
            df = df.drop(["PL_REGION_ID", "TAG_ID", "METER_ID"], axis=1)

            # Remove newline characters
            df = df.apply(lambda x: x.str.replace("\n", "") if x.dtype == "object" else x)

            df = df.drop_duplicates(subset=["DATA_DATE", "METER_STREAM_NO"], keep="first")
            # Sort DataFrame by 'DATA_DATE'
            df = df.sort_values(by="DATA_DATE")

            # Assuming 'df' is the DataFrame created from the query results
            num_streams = 6
            df_runs = {}

            # Loop to create DataFrames for each METER_STREAM_NO
            for i in range(1, num_streams + 1):
                df_runs[f'df_run{i}'] = df[df['METER_STREAM_NO'] == str(i)]

            # Check if each DataFrame has data before including in the tables dictionary
            tables = {
                "config_data": None,
            }

            graphs = {
                "corrected": None,
                "uncorrected": None,
                "pressure": None,
                "temperature": None
            }
            
            selected_date = request.args.get("date_dropdown")
            print("date1:", selected_date)

            # Initialize df_month_list outside the if statement
            df_month_list = pd.DataFrame(columns=['DATA_DATE'])

            # Check if 'selected_date' is available
            if selected_date:
                # Convert selected_date to 'YYYY-MM' format for consistency
                selected_date_formatted = pd.to_datetime(selected_date, format='%m/%Y').strftime('%Y-%m')
                print("date2:", selected_date_formatted)

                # Get the current month and year
                current_month_year = datetime.now().strftime('%Y-%m')

                # Determine if the selected date is in the current month
                is_current_month = selected_date_formatted == current_month_year

                # Update the query to use the selected date
                if is_current_month:
                    # If the selected date is in the current month, show all days up to the current date
                    query_day = f"""
                        SELECT TO_CHAR(TRUNC(LEVEL - 1) + TO_DATE('{current_month_year}-01', 'YYYY-MM-DD')) AS Date1
                        FROM DUAL
                        CONNECT BY LEVEL <= TO_DATE('{datetime.now().strftime('%Y-%m-%d')}', 'YYYY-MM-DD') - TO_DATE('{current_month_year}-01', 'YYYY-MM-DD') + 1
                    """
                else:
                    # If the selected date is in a previous month, show all days of the selected month
                    query_day = f"""
                        SELECT TO_CHAR(TRUNC(LEVEL - 1) + TO_DATE('{selected_date_formatted}-01', 'YYYY-MM-DD')) AS Date1
                        FROM DUAL
                        CONNECT BY LEVEL <= LAST_DAY(TO_DATE('{selected_date_formatted}-01', 'YYYY-MM-DD')) - TO_DATE('{selected_date_formatted}-01', 'YYYY-MM-DD') + 1
                    """

                # Fetch data for the month list
                query_day_result = fetch_data(query_day)
                df_month_list = pd.DataFrame(query_day_result, columns=['DATA_DATE'])
            
             # Merge DataFrames using a loop
            for i in range(1, num_streams + 1):
                df_run = df_runs[f'df_run{i}']
                
                if not df_run.empty:
                    merged_df = pd.merge(df_month_list, df_run, on='DATA_DATE', how='outer')
                    df_runs[f'df_run{i}'] = merged_df

            for i in range(1, num_streams + 1):
                df_run = df_runs[f'df_run{i}']
                if not df_run.empty:
                    df_run = df_run.drop('METER_STREAM_NO', axis=1, errors='ignore')
                    df_run = df_run.fillna("N/A")
                    tables[f"daily_data_run{i}"] = df_run.to_html(classes="data", index=False, na_rep="N/A")
                            
            # common_table_properties = {"classes": "data", "index": False,"header":None}
            
            # Create graphs for each METER_STREAM_NO
            for i in range(1, 7):
                df_run = df[df['METER_STREAM_NO'] == str(i)]

                # Create traces for each graph
                trace_corrected = go.Scatter(
                    x=df_run["DATA_DATE"],
                    y=df_run["CORRECTED"],
                    mode="lines+markers",
                    name=f"Run {i} - Corrected",
                    line=dict(color="blue", width=2),
                )

                trace_uncorrected = go.Scatter(
                    x=df_run["DATA_DATE"],
                    y=df_run["UNCORRECTED"],
                    mode="lines+markers",
                    name=f"Run {i} - Uncorrected",
                    line=dict(color="red", width=2),
                )

                trace_pressure = go.Scatter(
                    x=df_run["DATA_DATE"],
                    y=df_run["Pressure"],
                    mode="lines+markers",
                    name=f"Run {i} - Pressure",
                    line=dict(color="orange", width=2),
                )

                trace_temperature = go.Scatter(
                    x=df_run["DATA_DATE"],
                    y=df_run["Temperature"],
                    mode="lines+markers",
                    name=f"Run {i} - Temperature",
                    line=dict(color="green", width=2),
                )

                # Create subplot for each graph
                fig_corrected = sp.make_subplots(rows=1, cols=1, subplot_titles=[f"Run {i} - Corrected"])
                fig_uncorrected = sp.make_subplots(rows=1, cols=1, subplot_titles=[f"Run {i} - Uncorrected"])
                fig_pressure = sp.make_subplots(rows=1, cols=1, subplot_titles=[f"Run {i} - Pressure"])
                fig_temperature = sp.make_subplots(rows=1, cols=1, subplot_titles=[f"Run {i} - Temperature"])

                # Add traces to subplots
                fig_corrected.add_trace(trace_corrected)
                fig_uncorrected.add_trace(trace_uncorrected)
                fig_pressure.add_trace(trace_pressure)
                fig_temperature.add_trace(trace_temperature)

                # Update subplot and layout properties
                for fig in [fig_corrected, fig_uncorrected, fig_pressure, fig_temperature]:
                    fig.update_traces(
                        line_shape="linear",
                        marker=dict(symbol="circle", size=6),
                        hoverinfo="text+x+y",
                        hovertext=df_run["DATA_DATE"],
                    )
                    fig.update_layout(
                        legend=dict(x=0.6, y=1.25, orientation="h"),
                        yaxis_title="Values",
                        xaxis_title="Date",
                        hovermode="x unified",
                        yaxis=dict(type="linear", title="Values"),
                    )
                    fig.update_xaxes(title_text="Date", tickformat="%Y-%m-%d")

                # Get HTML for each graph
                graph_corrected = fig_corrected.to_html(full_html=False)
                graph_uncorrected = fig_uncorrected.to_html(full_html=False)
                graph_pressure = fig_pressure.to_html(full_html=False)
                graph_temperature = fig_temperature.to_html(full_html=False)

                # Store HTML in the graphs dictionary
                graphs[f"corrected_run{i}"] = graph_corrected
                graphs[f"uncorrected_run{i}"] = graph_uncorrected
                graphs[f"pressure_run{i}"] = graph_pressure
                graphs[f"temperature_run{i}"] = graph_temperature


                # เพิ่มเนื้อหา HTML สำหรับกราฟ
                df = df.sort_values(by="DATA_DATE", ascending=True)
                # ส่ง graph_html ไปยัง HTML template ของ Flask
                return render_template(
                    "billingdata_user_group.html",
                    tables=tables,
                    titles=df.columns.values,
                    selected_date=selected_date,
                    selected_tag=selected_tag,
                    selected_region=selected_region,
                    region_options=region_options,
                    tag_options=tag_options,
                    selected_meter_id=selected_meter_id,
                    graph_corrected=graph_corrected,
                    graph_uncorrected=graph_uncorrected,
                    graph_pressure=graph_pressure,
                    graph_temperature=graph_temperature,

                )


        elif query_type == "config_data":
            # Use pandas to create a DataFrame for config_data
            df = pd.DataFrame(
                results,
                columns=[
                    "PL_REGION_ID",
                    "TAG_ID",
                    "METER_ID",
                    "DATA_DATE",
                    "AMR_CONFIG1",
                    "AMR_CONFIG2",
                    "AMR_CONFIG3",
                    "AMR_CONFIG4",
                    "AMR_CONFIG5",
                    "AMR_CONFIG6",
                    "AMR_CONFIG7",
                    "AMR_CONFIG8",
                    "AMR_CONFIG9",
                    "AMR_CONFIG10",
                    "AMR_CONFIG11",
                    "AMR_CONFIG12",
                    "AMR_CONFIG13",
                    "AMR_CONFIG14",
                    "AMR_CONFIG15",
                    "AMR_CONFIG16",
                    "AMR_CONFIG17",
                    "AMR_CONFIG18",
                    "AMR_CONFIG19",
                    "AMR_CONFIG20",
                    "CONFIG1",
                    "CONFIG2",
                    "CONFIG3",
                    "CONFIG4",
                    "CONFIG5",
                    "CONFIG6",
                    "CONFIG7",
                    "CONFIG8",
                    "CONFIG9",
                    "CONFIG10",
                    "CONFIG11",
                    "CONFIG12",
                    "CONFIG13",
                    "CONFIG14",
                    "CONFIG15",
                    "CONFIG16",
                    "CONFIG17",
                    "CONFIG18",
                    "CONFIG19",
                    "CONFIG20",
                    "METER_STREAM_NO",
                ]
            )
            columns_to_drop = [
                "CONFIG1",
                "CONFIG2",
                "CONFIG3",
                "CONFIG4",
                "CONFIG5",
                "CONFIG6",
                "CONFIG7",
                "CONFIG8",
                "CONFIG9",
                "CONFIG10",
                "CONFIG11",
                "CONFIG12",
                "CONFIG13",
                "CONFIG14",
                "CONFIG15",
                "CONFIG16",
                "CONFIG17",
                "CONFIG18",
                "CONFIG19",
                "CONFIG20",
            ]
            dropped_columns_data = pd.concat(
                [
                    pd.DataFrame(columns=df.columns),
                    pd.DataFrame(columns=columns_to_drop),
                ],
                axis=1,
            )
            dropped_columns_data = df[["DATA_DATE"] + columns_to_drop].head(1)
            dropped_columns_data[
                "DATA_DATE"
            ] = "DATA.DATE"  # Replace actual values with the column name
            dropped_columns_data = dropped_columns_data.to_dict(orient="records")

            df = df.drop(columns=columns_to_drop)  # Drop specified columns
            
            # selected_meter_id = df["METER_ID"].iloc[0]
            # Get the selected Meter ID before removing it from the DataFrame
            ##!!!! Detact if empty 
            
            selected_meter_id = None

            # Check if 'METER_ID' column exists and the DataFrame is not empty
            if not df.empty and 'METER_ID' in df.columns and len(df['METER_ID']) > 0:
                selected_meter_id = df['METER_ID'].iloc[0]
                print(f"Selected Meter ID: {selected_meter_id}")
            else:
                print("DataFrame is empty or 'METER_ID' column doesn't exist.")

            # Now, remove the "METER_ID" column from the DataFrame
            df = df.drop(["PL_REGION_ID", "TAG_ID", "METER_ID"], axis=1)

            # Remove newline characters
            df = df.apply(lambda x: x.str.replace("\n", "") if x.dtype == "object" else x)

            df = df.drop_duplicates(subset=["DATA_DATE", "METER_STREAM_NO"], keep="first")
            # Sort DataFrame by 'DATA_DATE'
            df = df.sort_values(by="DATA_DATE")
            

            num_streams = 6
            df_runs = {}

            # Loop to create DataFrames for each METER_STREAM_NO
            for i in range(1, num_streams + 1):
                df_runs[f'df_run{i}'] = df[df['METER_STREAM_NO'] == str(i)]

            # Check if each DataFrame has data before including in the tables dictionary
            # Create Full table of selectedMonth
            tables = {
                "daily_data": None,
                
            }
            
            selected_date = request.args.get("date_dropdown")
            print("date1:", selected_date)

            # Check if 'selected_date' is available
            if selected_date:
                # Convert selected_date to 'YYYY-MM' format for consistency
                selected_date_formatted = pd.to_datetime(selected_date, format='%m/%Y').strftime('%Y-%m')
                print("date2:", selected_date_formatted)

                # Get the current month and year
                current_month_year = datetime.now().strftime('%Y-%m')

                # Determine if the selected date is in the current month
                is_current_month = selected_date_formatted == current_month_year

                # Update the query to use the selected date
                if is_current_month:
                    # If the selected date is in the current month, show all days up to the current date
                    query_day = f"""
                        SELECT TO_CHAR(TRUNC(LEVEL - 1) + TO_DATE('{current_month_year}-01', 'YYYY-MM-DD')) AS Date1
                        FROM DUAL
                        CONNECT BY LEVEL <= TO_DATE('{datetime.now().strftime('%Y-%m-%d')}', 'YYYY-MM-DD') - TO_DATE('{current_month_year}-01', 'YYYY-MM-DD') + 1
                    """
                else:
                    # If the selected date is in a previous month, show all days of the selected month
                    query_day = f"""
                        SELECT TO_CHAR(TRUNC(LEVEL - 1) + TO_DATE('{selected_date_formatted}-01', 'YYYY-MM-DD')) AS Date1
                        FROM DUAL
                        CONNECT BY LEVEL <= LAST_DAY(TO_DATE('{selected_date_formatted}-01', 'YYYY-MM-DD')) - TO_DATE('{selected_date_formatted}-01', 'YYYY-MM-DD') + 1
                    """

                # Fetch data for the month list
                query_day_result = fetch_data(query_day)
                df_month_list = pd.DataFrame(query_day_result, columns=['DATA_DATE'])

            

            # Merge DataFrames using a loop
            for i in range(1, num_streams + 1):
                df_run = df_runs[f'df_run{i}']
                
                if not df_run.empty:
                    merged_df = pd.merge(df_month_list, df_run, on='DATA_DATE', how='outer')
                    df_runs[f'df_run{i}'] = merged_df
                
            common_table_properties = {"classes": "data", "index": False, "header": None, "na_rep": "N/A"}


            for i in range(1, num_streams + 1):
                df_run = df_runs[f'df_run{i}']
                if not df_run.empty:
                    df_run = df_run.drop('METER_STREAM_NO', axis=1, errors='ignore')
                    df_run = df_run.fillna("N/A")
                    tables[f"config_data_run{i}"] = df_run.to_html(**common_table_properties)
                    
            return render_template(
                "billingdata_user_group.html",
                
                tables=tables,
                titles=df.columns.values,
                selected_date=selected_date,
                selected_tag=selected_tag,
                selected_region=selected_region,
                region_options=region_options,
                tag_options=tag_options, 
                dropped_columns_data=dropped_columns_data,
                selected_meter_id=selected_meter_id,
                username=logged_in_user,  
                description=description,
                user_level=user_level
            )
    else:
        # Render the template without executing the query
        return render_template(
            "billingdata_user_group.html",
            selected_date=selected_date,
            selected_region=selected_region,
            selected_tag=selected_tag,
            region_options=region_options,
            tag_options=tag_options,
            tables={},
            username=logged_in_user,  
            description=description,
            user_level=user_level
        )
            
            

@app.route("/billing_data_user")
def billing_data_user():
    
    if 'username' not in session:
        return redirect(url_for('login'))

    # Fetch user information from the session
    logged_in_user = session['username']
    if logged_in_user not in users:
        return redirect(url_for('login'))
    
    user_info = users[logged_in_user]
    user_level = user_info.get('user_level')
    description = user_info.get('description')
    print("description", description)
    
    logged_in_user = logged_in_user
    print("user:", logged_in_user)

    query_type = request.args.get("query_type")


    # SQL query to fetch unique PL_REGION_ID values
    region_query = """
    SELECT amr_region.id
    FROM AMR_REGION,AMR_user,amr_field_id,amr_pl_group
    WHERE amr_user.user_group = amr_field_id.meter_id
        AND amr_field_id.field_id = amr_pl_group.field_id
        AND amr_pl_group.pl_region_id = amr_region.id
        AND user_name = :logged_in_user
        AND amr_user.user_enable like '1'
    """

    tag_query = """
    SELECT amr_field_id.tag_id
    FROM AMR_REGION,AMR_user,amr_field_id,amr_pl_group
    WHERE amr_user.user_group = amr_field_id.meter_id
        AND amr_field_id.field_id = amr_pl_group.field_id
        AND amr_pl_group.pl_region_id = amr_region.id
        AND user_name = :logged_in_user
        AND amr_user.user_enable like '1'
        ORDER BY AMR_FIELD_ID.TAG_ID
    """

    # Fetch unique region values
    region_results = fetch_data( region_query, params={'logged_in_user': logged_in_user})
    region_options = [str(region[0]) for region in region_results]

    query = ""
    print(query)
    if query_type == "daily_data":
        # SQL query for main data
        query = """
        SELECT DISTINCT
            AMR_PL_GROUP.PL_REGION_ID,
            AMR_FIELD_ID.TAG_ID,
            AMR_FIELD_ID.METER_ID,
            TO_CHAR(AMR_BILLING_DATA.DATA_DATE),
            
            AMR_BILLING_DATA.CORRECTED_VOL as CORRECTED,
            AMR_BILLING_DATA.UNCORRECTED_VOL as UNCORRECTED,
            AMR_BILLING_DATA.AVR_PF as Pressure,
            AMR_BILLING_DATA.AVR_TF as Temperature,
            AMR_BILLING_DATA.METER_STREAM_NO  -- Add this line to include METER_STREAM_NO in the SELECT clause
        FROM
            AMR_FIELD_ID, AMR_PL_group, AMR_BILLING_DATA
        WHERE
            AMR_PL_GROUP.FIELD_ID = AMR_FIELD_ID.FIELD_ID 
            AND AMR_BILLING_DATA.METER_ID = AMR_FIELD_ID.METER_ID
            AND AMR_BILLING_DATA.METER_STREAM_NO IS NOT NULL
            {billing_date_condition}
            {tag_condition}
            {region_condition}
        """
        print(query)

        # Return the template with the DataFrame

    elif query_type == "config_data":
        query = """
        SELECT
            AMR_PL_GROUP.PL_REGION_ID,
            AMR_FIELD_ID.TAG_ID,
            amr_field_id.meter_id,
            TO_CHAR(AMR_CONFIGURED_DATA.DATA_DATE),
            
            amr_configured_data.amr_config1,
            amr_configured_data.amr_config2,
            amr_configured_data.amr_config3,
            amr_configured_data.amr_config4,
            amr_configured_data.amr_config5,
            amr_configured_data.amr_config6,
            amr_configured_data.amr_config7,
            amr_configured_data.amr_config8,
            amr_configured_data.amr_config9,
            amr_configured_data.amr_config10,
            amr_configured_data.amr_config11,
            amr_configured_data.amr_config12,
            amr_configured_data.amr_config13,
            amr_configured_data.amr_config14,
            amr_configured_data.amr_config15,
            amr_configured_data.amr_config16,
            amr_configured_data.amr_config17,
            amr_configured_data.amr_config18,
            amr_configured_data.amr_config19,
            amr_configured_data.amr_config20,
            
            
            AMR_VC_CONFIGURED_INFO.config1,
            AMR_VC_CONFIGURED_INFO.config2,
            AMR_VC_CONFIGURED_INFO.config3,
            AMR_VC_CONFIGURED_INFO.config4,
            AMR_VC_CONFIGURED_INFO.config5,
            AMR_VC_CONFIGURED_INFO.config6,
            AMR_VC_CONFIGURED_INFO.config7,
            AMR_VC_CONFIGURED_INFO.config8,
            AMR_VC_CONFIGURED_INFO.config9,
            AMR_VC_CONFIGURED_INFO.config10,
            AMR_VC_CONFIGURED_INFO.config11,
            AMR_VC_CONFIGURED_INFO.config12,
            AMR_VC_CONFIGURED_INFO.config13,
            AMR_VC_CONFIGURED_INFO.config14,
            AMR_VC_CONFIGURED_INFO.config15,
            AMR_VC_CONFIGURED_INFO.config16,
            AMR_VC_CONFIGURED_INFO.config17,
            AMR_VC_CONFIGURED_INFO.config18,
            AMR_VC_CONFIGURED_INFO.config19,
            AMR_VC_CONFIGURED_INFO.config20,
            AMR_CONFIGURED_DATA.METER_STREAM_NO
            
        FROM
            AMR_FIELD_ID, AMR_PL_group, AMR_CONFIGURED_DATA
        JOIN AMR_VC_CONFIGURED_INFO ON amr_configured_data.amr_vc_type = AMR_VC_CONFIGURED_INFO.vc_type
        WHERE
            AMR_PL_GROUP.FIELD_ID = AMR_FIELD_ID.FIELD_ID 
            AND AMR_CONFIGURED_DATA.METER_ID = AMR_FIELD_ID.METER_ID
            AND AMR_CONFIGURED_DATA.METER_STREAM_NO is not null
            
            {configured_date_condition}
            {tag_condition}
            {region_condition}
        """
        print(query)
    # Get selected values from the dropdowns
    billing_date_condition = "AND AMR_BILLING_DATA.DATA_DATE IS NOT NULL"
    configured_date_condition = "AND AMR_CONFIGURED_DATA.DATA_DATE IS NOT NULL"
    tag_condition = "AND AMR_FIELD_ID.TAG_ID IS NOT NULL"
    region_condition = "AND amr_pl_group.pl_region_id IS NOT NULL"

    selected_date = request.args.get("date_dropdown")
    selected_tag = request.args.get("tag_dropdown")
    selected_region = request.args.get("region_dropdown")

    # Fetch unique region values
    for region in region_results:
        region_results = fetch_data( region_query, params={'logged_in_user': logged_in_user})
        region_options = str(region[0]) 
        print("region:", region_options)

    # # Fetch tag options based on the selected region
    tag_options = None
    tag_results = fetch_data( tag_query, params={'logged_in_user': logged_in_user})
    for tag in tag_results:
        tag_options = str(tag[0])
        print("site:", tag_options)

    if selected_date:
        billing_date_condition = (
            f"AND TO_CHAR(AMR_BILLING_DATA.DATA_DATE, 'MM/YYYY') = '{selected_date}'"
        )
        configured_date_condition = (
            f"AND TO_CHAR(AMR_CONFIGURED_DATA.DATA_DATE, 'MM/YYYY') = '{selected_date}'"
        )
    if selected_tag:
        tag_condition = f"AND AMR_FIELD_ID.TAG_ID = '{selected_tag}'"

    if selected_region:
        region_condition = f"AND amr_pl_group.pl_region_id = '{selected_region}'"

    # Modify the query with the selected conditions
    query = query.format(
        billing_date_condition=billing_date_condition,
        configured_date_condition=configured_date_condition,
        tag_condition=tag_condition,
        region_condition=region_condition,
    )

    if selected_region:
        # Use fetch_data function to retrieve data
        results = fetch_data(query)

        if query_type == "daily_data":
            # Use pandas to create a DataFrame for daily_data
            df = pd.DataFrame(
                results,
                columns=[
                    "PL_REGION_ID",
                    "TAG_ID",
                    "METER_ID",
                    "DATA_DATE",
                    "CORRECTED",
                    "UNCORRECTED",
                    "Pressure",
                    "Temperature",
                    "METER_STREAM_NO",
                ],
            )
            # Get the selected Meter ID before removing it from the DataFrame
            # selected_meter_id = df["METER_ID"].iloc[0]

            selected_meter_id = None

            # Check if 'METER_ID' column exists and the DataFrame is not empty
            if not df.empty and 'METER_ID' in df.columns and len(df['METER_ID']) > 0:
                selected_meter_id = df['METER_ID'].iloc[0]
                print(f"Selected Meter ID: {selected_meter_id}")
            else:
                print("DataFrame is empty or 'METER_ID' column doesn't exist.")

            # Now, remove the "METER_ID" column from the DataFrame
            df = df.drop(["PL_REGION_ID", "TAG_ID", "METER_ID"], axis=1)

            # Remove newline characters
            df = df.apply(lambda x: x.str.replace("\n", "") if x.dtype == "object" else x)

            df = df.drop_duplicates(subset=["DATA_DATE", "METER_STREAM_NO"], keep="first")
            # Sort DataFrame by 'DATA_DATE'
            df = df.sort_values(by="DATA_DATE")

            # Assuming 'df' is the DataFrame created from the query results
            num_streams = 6
            df_runs = {}

            # Loop to create DataFrames for each METER_STREAM_NO
            for i in range(1, num_streams + 1):
                df_runs[f'df_run{i}'] = df[df['METER_STREAM_NO'] == str(i)]

            # Check if each DataFrame has data before including in the tables dictionary
            tables = {
                "config_data": None,
            }

            graphs = {
                "corrected": None,
                "uncorrected": None,
                "pressure": None,
                "temperature": None
            }
            
            selected_date = request.args.get("date_dropdown")
            print("date1:", selected_date)

            # Initialize df_month_list outside the if statement
            df_month_list = pd.DataFrame(columns=['DATA_DATE'])

            # Check if 'selected_date' is available
            if selected_date:
                # Convert selected_date to 'YYYY-MM' format for consistency
                selected_date_formatted = pd.to_datetime(selected_date, format='%m/%Y').strftime('%Y-%m')
                print("date2:", selected_date_formatted)

                # Get the current month and year
                current_month_year = datetime.now().strftime('%Y-%m')

                # Determine if the selected date is in the current month
                is_current_month = selected_date_formatted == current_month_year

                # Update the query to use the selected date
                if is_current_month:
                    # If the selected date is in the current month, show all days up to the current date
                    query_day = f"""
                        SELECT TO_CHAR(TRUNC(LEVEL - 1) + TO_DATE('{current_month_year}-01', 'YYYY-MM-DD')) AS Date1
                        FROM DUAL
                        CONNECT BY LEVEL <= TO_DATE('{datetime.now().strftime('%Y-%m-%d')}', 'YYYY-MM-DD') - TO_DATE('{current_month_year}-01', 'YYYY-MM-DD') + 1
                    """
                else:
                    # If the selected date is in a previous month, show all days of the selected month
                    query_day = f"""
                        SELECT TO_CHAR(TRUNC(LEVEL - 1) + TO_DATE('{selected_date_formatted}-01', 'YYYY-MM-DD')) AS Date1
                        FROM DUAL
                        CONNECT BY LEVEL <= LAST_DAY(TO_DATE('{selected_date_formatted}-01', 'YYYY-MM-DD')) - TO_DATE('{selected_date_formatted}-01', 'YYYY-MM-DD') + 1
                    """

                # Fetch data for the month list
                query_day_result = fetch_data(query_day)
                df_month_list = pd.DataFrame(query_day_result, columns=['DATA_DATE'])
            
            # Merge DataFrames using a loop
            for i in range(1, num_streams + 1):
                df_run = df_runs[f'df_run{i}']
                
                if not df_run.empty:
                    merged_df = pd.merge(df_month_list, df_run, on='DATA_DATE', how='outer')
                    df_runs[f'df_run{i}'] = merged_df

            for i in range(1, num_streams + 1):
                df_run = df_runs[f'df_run{i}']
                if not df_run.empty:
                    df_run = df_run.drop('METER_STREAM_NO', axis=1, errors='ignore')
                    df_run = df_run.fillna("N/A")
                    tables[f"daily_data_run{i}"] = df_run.to_html(classes="data", index=False, na_rep="N/A")
                            
            # common_table_properties = {"classes": "data", "index": False,"header":None}
            
            # Create graphs for each METER_STREAM_NO
            for i in range(1, 7):
                df_run = df[df['METER_STREAM_NO'] == str(i)]

                # Create traces for each graph
                trace_corrected = go.Scatter(
                    x=df_run["DATA_DATE"],
                    y=df_run["CORRECTED"],
                    mode="lines+markers",
                    name=f"Run {i} - Corrected",
                    line=dict(color="blue", width=2),
                )

                trace_uncorrected = go.Scatter(
                    x=df_run["DATA_DATE"],
                    y=df_run["UNCORRECTED"],
                    mode="lines+markers",
                    name=f"Run {i} - Uncorrected",
                    line=dict(color="red", width=2),
                )

                trace_pressure = go.Scatter(
                    x=df_run["DATA_DATE"],
                    y=df_run["Pressure"],
                    mode="lines+markers",
                    name=f"Run {i} - Pressure",
                    line=dict(color="orange", width=2),
                )

                trace_temperature = go.Scatter(
                    x=df_run["DATA_DATE"],
                    y=df_run["Temperature"],
                    mode="lines+markers",
                    name=f"Run {i} - Temperature",
                    line=dict(color="green", width=2),
                )

                # Create subplot for each graph
                fig_corrected = sp.make_subplots(rows=1, cols=1, subplot_titles=[f"Run {i} - Corrected"])
                fig_uncorrected = sp.make_subplots(rows=1, cols=1, subplot_titles=[f"Run {i} - Uncorrected"])
                fig_pressure = sp.make_subplots(rows=1, cols=1, subplot_titles=[f"Run {i} - Pressure"])
                fig_temperature = sp.make_subplots(rows=1, cols=1, subplot_titles=[f"Run {i} - Temperature"])

                # Add traces to subplots
                fig_corrected.add_trace(trace_corrected)
                fig_uncorrected.add_trace(trace_uncorrected)
                fig_pressure.add_trace(trace_pressure)
                fig_temperature.add_trace(trace_temperature)

                # Update subplot and layout properties
                for fig in [fig_corrected, fig_uncorrected, fig_pressure, fig_temperature]:
                    fig.update_traces(
                        line_shape="linear",
                        marker=dict(symbol="circle", size=6),
                        hoverinfo="text+x+y",
                        hovertext=df_run["DATA_DATE"],
                    )
                    fig.update_layout(
                        legend=dict(x=0.6, y=1.25, orientation="h"),
                        yaxis_title="Values",
                        xaxis_title="Date",
                        hovermode="x unified",
                        yaxis=dict(type="linear", title="Values"),
                    )
                    fig.update_xaxes(title_text="Date", tickformat="%Y-%m-%d")

                # Get HTML for each graph
                graph_corrected = fig_corrected.to_html(full_html=False)
                graph_uncorrected = fig_uncorrected.to_html(full_html=False)
                graph_pressure = fig_pressure.to_html(full_html=False)
                graph_temperature = fig_temperature.to_html(full_html=False)

                # Store HTML in the graphs dictionary
                graphs[f"corrected_run{i}"] = graph_corrected
                graphs[f"uncorrected_run{i}"] = graph_uncorrected
                graphs[f"pressure_run{i}"] = graph_pressure
                graphs[f"temperature_run{i}"] = graph_temperature


                # เพิ่มเนื้อหา HTML สำหรับกราฟ
                df = df.sort_values(by="DATA_DATE", ascending=True)
                # ส่ง graph_html ไปยัง HTML template ของ Flask
                return render_template(
                    "billingdata_user.html",
                    tables=tables,
                    titles=df.columns.values,
                    selected_date=selected_date,
                    selected_tag=selected_tag,
                    selected_region=selected_region,
                    region_options=region_options,
                    tag_options=tag_options,
                    selected_meter_id=selected_meter_id,
                    graph_corrected=graph_corrected,
                    graph_uncorrected=graph_uncorrected,
                    graph_pressure=graph_pressure,
                    graph_temperature=graph_temperature,

                )


        elif query_type == "config_data":
            # Use pandas to create a DataFrame for config_data
            df = pd.DataFrame(
                results,
                columns=[
                    "PL_REGION_ID",
                    "TAG_ID",
                    "METER_ID",
                    "DATA_DATE",
                    "AMR_CONFIG1",
                    "AMR_CONFIG2",
                    "AMR_CONFIG3",
                    "AMR_CONFIG4",
                    "AMR_CONFIG5",
                    "AMR_CONFIG6",
                    "AMR_CONFIG7",
                    "AMR_CONFIG8",
                    "AMR_CONFIG9",
                    "AMR_CONFIG10",
                    "AMR_CONFIG11",
                    "AMR_CONFIG12",
                    "AMR_CONFIG13",
                    "AMR_CONFIG14",
                    "AMR_CONFIG15",
                    "AMR_CONFIG16",
                    "AMR_CONFIG17",
                    "AMR_CONFIG18",
                    "AMR_CONFIG19",
                    "AMR_CONFIG20",
                    "CONFIG1",
                    "CONFIG2",
                    "CONFIG3",
                    "CONFIG4",
                    "CONFIG5",
                    "CONFIG6",
                    "CONFIG7",
                    "CONFIG8",
                    "CONFIG9",
                    "CONFIG10",
                    "CONFIG11",
                    "CONFIG12",
                    "CONFIG13",
                    "CONFIG14",
                    "CONFIG15",
                    "CONFIG16",
                    "CONFIG17",
                    "CONFIG18",
                    "CONFIG19",
                    "CONFIG20",
                    "METER_STREAM_NO",
                ]
            )
            columns_to_drop = [
                "CONFIG1",
                "CONFIG2",
                "CONFIG3",
                "CONFIG4",
                "CONFIG5",
                "CONFIG6",
                "CONFIG7",
                "CONFIG8",
                "CONFIG9",
                "CONFIG10",
                "CONFIG11",
                "CONFIG12",
                "CONFIG13",
                "CONFIG14",
                "CONFIG15",
                "CONFIG16",
                "CONFIG17",
                "CONFIG18",
                "CONFIG19",
                "CONFIG20",
            ]
            dropped_columns_data = pd.concat(
                [
                    pd.DataFrame(columns=df.columns),
                    pd.DataFrame(columns=columns_to_drop),
                ],
                axis=1,
            )
            dropped_columns_data = df[["DATA_DATE"] + columns_to_drop].head(1)
            dropped_columns_data[
                "DATA_DATE"
            ] = "DATA.DATE"  # Replace actual values with the column name
            dropped_columns_data = dropped_columns_data.to_dict(orient="records")

            df = df.drop(columns=columns_to_drop)  # Drop specified columns
            
            # selected_meter_id = df["METER_ID"].iloc[0]
            # Get the selected Meter ID before removing it from the DataFrame
            ##!!!! Detact if empty 
            
            selected_meter_id = None

            # Check if 'METER_ID' column exists and the DataFrame is not empty
            if not df.empty and 'METER_ID' in df.columns and len(df['METER_ID']) > 0:
                selected_meter_id = df['METER_ID'].iloc[0]
                print(f"Selected Meter ID: {selected_meter_id}")
            else:
                print("DataFrame is empty or 'METER_ID' column doesn't exist.")

            # Now, remove the "METER_ID" column from the DataFrame
            df = df.drop(["PL_REGION_ID", "TAG_ID", "METER_ID"], axis=1)

            # Remove newline characters
            df = df.apply(lambda x: x.str.replace("\n", "") if x.dtype == "object" else x)

            df = df.drop_duplicates(subset=["DATA_DATE", "METER_STREAM_NO"], keep="first")
            # Sort DataFrame by 'DATA_DATE'
            df = df.sort_values(by="DATA_DATE")
            

            num_streams = 6
            df_runs = {}

            # Loop to create DataFrames for each METER_STREAM_NO
            for i in range(1, num_streams + 1):
                df_runs[f'df_run{i}'] = df[df['METER_STREAM_NO'] == str(i)]

            # Check if each DataFrame has data before including in the tables dictionary
            # Create Full table of selectedMonth
            tables = {
                "daily_data": None,
                
            }
            
            selected_date = request.args.get("date_dropdown")
            print("date1:", selected_date)

            # Check if 'selected_date' is available
            if selected_date:
                # Convert selected_date to 'YYYY-MM' format for consistency
                selected_date_formatted = pd.to_datetime(selected_date, format='%m/%Y').strftime('%Y-%m')
                print("date2:", selected_date_formatted)

                # Get the current month and year
                current_month_year = datetime.now().strftime('%Y-%m')

                # Determine if the selected date is in the current month
                is_current_month = selected_date_formatted == current_month_year

                # Update the query to use the selected date
                if is_current_month:
                    # If the selected date is in the current month, show all days up to the current date
                    query_day = f"""
                        SELECT TO_CHAR(TRUNC(LEVEL - 1) + TO_DATE('{current_month_year}-01', 'YYYY-MM-DD')) AS Date1
                        FROM DUAL
                        CONNECT BY LEVEL <= TO_DATE('{datetime.now().strftime('%Y-%m-%d')}', 'YYYY-MM-DD') - TO_DATE('{current_month_year}-01', 'YYYY-MM-DD') + 1
                    """
                else:
                    # If the selected date is in a previous month, show all days of the selected month
                    query_day = f"""
                        SELECT TO_CHAR(TRUNC(LEVEL - 1) + TO_DATE('{selected_date_formatted}-01', 'YYYY-MM-DD')) AS Date1
                        FROM DUAL
                        CONNECT BY LEVEL <= LAST_DAY(TO_DATE('{selected_date_formatted}-01', 'YYYY-MM-DD')) - TO_DATE('{selected_date_formatted}-01', 'YYYY-MM-DD') + 1
                    """

                # Fetch data for the month list
                query_day_result = fetch_data(query_day)
                df_month_list = pd.DataFrame(query_day_result, columns=['DATA_DATE'])

            

            # Merge DataFrames using a loop
            for i in range(1, num_streams + 1):
                df_run = df_runs[f'df_run{i}']
                
                if not df_run.empty:
                    merged_df = pd.merge(df_month_list, df_run, on='DATA_DATE', how='outer')
                    df_runs[f'df_run{i}'] = merged_df
                
            common_table_properties = {"classes": "data", "index": False, "header": None, "na_rep": "N/A"}


            for i in range(1, num_streams + 1):
                df_run = df_runs[f'df_run{i}']
                if not df_run.empty:
                    df_run = df_run.drop('METER_STREAM_NO', axis=1, errors='ignore')
                    df_run = df_run.fillna("N/A")
                    tables[f"config_data_run{i}"] = df_run.to_html(**common_table_properties)
                    
            return render_template(
                "billingdata_user.html",               
                tables=tables,
                titles=df.columns.values,
                selected_date=selected_date,
                selected_tag=selected_tag,
                selected_region=selected_region,
                region_options=region_options,
                tag_options=tag_options, dropped_columns_data=dropped_columns_data,
                selected_meter_id=selected_meter_id,
                username=logged_in_user,  
                description=description,
                user_level=user_level
            )
    else:
        # Render the template without executing the query
        return render_template(
            "billingdata_user.html",
            selected_date=selected_date,
            selected_region=selected_region,
            selected_tag=selected_tag,
            region_options=region_options,
            tag_options=tag_options,
            tables={},
            username=logged_in_user,  
            description=description,
            user_level=user_level
        )  
############ / View Billing Data  #####################


############ Daily summary #####################
@app.route("/Daily_summary")
def Daily_summary():
    
       
        # SQL query to fetch unique PL_REGION_ID values
        region_query = """
        SELECT * FROM AMR_REGION 
        """

        # Fetch unique region values
        region_results = fetch_data(region_query)
        region_options = [str(region[0]) for region in region_results]

        # SQL query for main data
        query = """
        SELECT DISTINCT
        amr_field_id.TAG_ID as SITE
    FROM
        AMR_FIELD_ID, AMR_PL_group, AMR_RMIU_TYPE, amr_region
        
    WHERE
        AMR_PL_GROUP.FIELD_ID = AMR_FIELD_ID.FIELD_ID 
    {region_condition}
        """
        # Get selected values from the dropdowns
        selected_region = request.args.get("region_dropdown")


            
        region_results = fetch_data(query=region_query)

        region_options = [str(region[0]) for region in region_results]

        # Initialize the query with a condition that is always true
        region_condition = "AND 1 = 1"

        # Fetch tag options based on the selected region
        if selected_region:
            region_condition = f"AND amr_pl_group.pl_region_id = '{selected_region}'"

        # Modify the query with the selected conditions
        query = query.format(region_condition=region_condition)

        # Check if a region is selected before executing the query
        if selected_region:
            # ใช้ fetch_data function ในการดึงข้อมูล
            results = fetch_data(query)

            # ใช้ pandas ในการสร้าง DataFrame
            df = pd.DataFrame(results, columns=["SITE"])
            # ลบคอลัมน์ที่ไม่ต้องการ
            df = df.applymap(lambda x: x.replace("\n", "") if isinstance(x, str) else x)

            # Sort DataFrame by the 'SITE' column (adjust as needed)
            df = df.sort_values(by="SITE")

            # ส่ง DataFrame ไปยัง HTML template
            return render_template(
                "Daily_summary.html",
                tables=[df.to_html(classes="data", index=False)],
                titles=df.columns.values,
                selected_region=selected_region,
                region_options=region_options,
            )
        else:
            # Render the template without executing the query
            return render_template(
                "Daily_summary.html",
                selected_region=selected_region,
                region_options=region_options,
                tables=[],
            )


############ /Daily summary  #####################


############ sitedetail_data  #####################


@app.route("/sitedetail_data")
def sitedetail_data():
    
        
        # SQL query to fetch unique PL_REGION_ID values
        region_query = """
        SELECT * FROM AMR_REGION 
        """

        # Fetch unique region values
        region_results = fetch_data(region_query)
        region_options = [str(region[0]) for region in region_results]

        # SQL query for main data
        query = """
        SELECT DISTINCT
        AMR_FIELD_ID.ID,
        amr_field_id.TAG_ID as SITE,
        AMR_FIELD_ID.AMR_PHASE as PHASE,
        AMR_FIELD_ID.SIM_IP as IPADDRESS,
        (SELECT rmiu_name FROM AMR_RMIU_TYPE WHERE AMR_RMIU_TYPE.ID = AMR_FIELD_ID.RMIU_TYPE) as TYPE
        
    FROM
        AMR_FIELD_ID, AMR_PL_group, AMR_RMIU_TYPE, amr_region
        
    WHERE
        AMR_PL_GROUP.FIELD_ID = AMR_FIELD_ID.FIELD_ID 
            {region_condition}
        """

        # Get selected values from the dropdowns
        selected_region = request.args.get("region_dropdown")

        # Fetch unique region values
        region_results = fetch_data(region_query)
        region_options = [str(region[0]) for region in region_results]

        # Initialize the query with a condition that is always true
        region_condition = "AND 1 = 1"

        # Fetch tag options based on the selected region
        if selected_region:
            region_condition = f"AND amr_pl_group.pl_region_id = '{selected_region}'"

        # Modify the query with the selected conditions
        query = query.format(region_condition=region_condition)

        # Check if a region is selected before executing the query
        if selected_region:
            # ใช้ fetch_data function ในการดึงข้อมูล
            results = fetch_data(query)

            # ใช้ pandas ในการสร้าง DataFrame
            df = pd.DataFrame(
                results, columns=["ID", "SITE", "PHASE", "IP ADDRESS", "TYPE"]
            )
            # ลบคอลัมน์ที่ไม่ต้องการ
            df = df.applymap(lambda x: x.replace("\n", "") if isinstance(x, str) else x)

            # Sort DataFrame by the 'SITE' column (adjust as needed)
            df = df.sort_values(by="SITE")

            # ส่ง DataFrame ไปยัง HTML template
            return render_template(
                "sitedetail.html",
                tables=[df.to_html(classes="data", index=False)],
                titles=df.columns.values,
                selected_region=selected_region,
                region_options=region_options,
            )
        else:
            # Render the template without executing the query
            return render_template(
                "sitedetail.html",
                selected_region=selected_region,
                region_options=region_options,
                tables=[],
            )


############ /sitedetail_data  #####################


############ Manualpoll_data  #####################
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

        return render_template(
            "Manual poll.html",
            tables=[df.to_html(classes="data")],
            titles=df.columns.values,
            selected_tag=selected_tag,
            selected_region=selected_region,
            region_options=region_options,
            tag_options=tag_options,
            df=df,
        )


@app.route("/Manualpoll_data", methods=["POST"])
def read_data():
    
        
        global change_to_32bit_counter  # Use the global variable

        slave_id = int(request.form["slave_id"])
        function_code = int(request.form["function_code"])
        if request.form["starting_address"] == "custom":
            if "custom_starting_address" in request.form:
                starting_address = int(request.form["custom_starting_address"])
            else:
                starting_address = 0  # หรือใส่ค่าเริ่มต้นที่คุณต้องการ
        else:
            starting_address = int(request.form["starting_address"])
        quantity = int(request.form["quantity"])
        tcp_ip = request.form["tcp_ip"]
        tcp_port = int(request.form["tcp_port"])

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

        if "32bit" in request.form and request.form["32bit"] == "true":
            is_32bit = True
        else:
            is_32bit = False

        data_list = []
        address = starting_address
        value = 0

        for i, value in enumerate(values):
            address = starting_address + i * 2
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
            data_list.append(
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
            # หลังจาก values = [int.from_bytes(data[i:i + bytes_per_value], byteorder='big', signed=False) for i in range(0, len(data), bytes_per_value)]
        # แทนที่ด้วย:

        values = [
            int.from_bytes(data[i : i + bytes_per_value], byteorder="big", signed=False)
            for i in range(0, len(data), bytes_per_value)
        ]

        # หากต้องการแปลงเฉพาะแถวแรก สามารถทำได้เช่นนี้:

        session["tcp_ip"] = tcp_ip
        session["tcp_port"] = tcp_port

        # ตรวจสอบค่า is_16bit เพื่อเพิ่มข้อมูลลงในตาราง 16-bit
        if not is_16bit:
            # เพิ่มข้อมูลลงในตาราง 16-bit โดยเพิ่มค่าลงในตารางเดิมและเพิ่มค่าอีก 1
            data_list_16bit = []
            for data_16bit in data_list:
                address_16bit = data_16bit["address"]
                value_16bit = (
                    data_16bit["value"] * 2
                )  # เพิ่มค่าขึ้นเป็น 2 เท่าเพื่อให้เป็น 1 เท่าของข้อมูลเดิม
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
            # ... (other code)

        return render_template(
            "Manual poll.html",
            df=df,
            data_list=data_list,
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
            tag_options=tag_options,
        )


def handle_actaris_action(i, address):
    return address


def handle_action_configuration(i, value, address):
    return value, address


def get_description_from_database(address):
    
        
        query = "SELECT DESCRIPTION FROM AMR_ADDRESS_MAPPING1 WHERE ADDRESS = :address"
        params = {"address": address}
        result = fetch_data(query, params)
        return result[0][0] if result else None


@app.route("/process_selected_rows", methods=["POST"])
def process_selected_rows():
    selected_rows = request.form.getlist("selected_rows")
    return "Selected rows processed successfully"


def get_type_value_from_database(address):
    
        
        query = "SELECT TYPE_VALUE FROM AMR_ADDRESS_MAPPING1 WHERE ADDRESS = :address"
        result = fetch_data(query, params={"address": address})
        if result:
            return result[0][0]  # Assuming TYPE_VALUE is the first column in the result
        return None


############ /Manualpoll_data  #####################



###############################################








@app.route("/billing_data_asgs")
def billing_data_asgs():
   
    
        
        selected_region = request.args.get('region')
        selected_tag = request.args.get('tag')
        selected_month_year = request.args.get('monthYear')


        # Define your Oracle query to fetch REGION_NAME
        region_query = """
        SELECT DISTINCT REGION_NAME
        FROM VW_ASGS_AMR_BILLING_DATA
        ORDER BY REGION_NAME
        """
        # Fetch REGION_NAME data using your fetch_data function
        region_results = fetch_data(region_query)

        # Define your Oracle query to fetch tag_id based on the selected REGION_NAME
        tag_query = """
        SELECT DISTINCT tag_id
        FROM VW_ASGS_AMR_BILLING_DATA
        WHERE REGION_NAME = :selected_region
        ORDER BY tag_id
        """
        # Fetch tag_id data using your fetch_data function
        tag_results = fetch_data( tag_query, {'selected_region': selected_region})

        # Define your Oracle query to fetch data based on selected criteria
        billing_query = """
            SELECT *
            FROM VW_ASGS_AMR_BILLING_DATA
            WHERE 
                VW_ASGS_AMR_BILLING_DATA.region_name = :selected_region
                AND VW_ASGS_AMR_BILLING_DATA.tag_id = :selected_tag
                AND TO_CHAR(VW_ASGS_AMR_BILLING_DATA.data_date, 'MM/YYYY') = :selected_month_year
                ORDER BY VW_ASGS_AMR_BILLING_DATA.data_date
        """
        # Fetch data using your fetch_data function
        

        results = fetch_data( billing_query, {'selected_region': selected_region, 'selected_tag': selected_tag, 'selected_month_year': selected_month_year})
        print(results)
    # Render the template with the fetched data and selected region
        return render_template(
            "billingdataasgs.html",
            region_results=region_results,
            tag_results=tag_results,
            results=results,
            selected_region=selected_region,
        )


@app.route('/get_tag')
def get_tag():
    
        
    region_name = request.args.get('region')

    # Use the selected REGION_NAME to fetch associated tag_id values
    tag_query = """
    SELECT DISTINCT tag_id
    FROM VW_ASGS_AMR_BILLING_DATA
    WHERE REGION_NAME = :region_name
    ORDER BY tag_id
    """
    tag_results = fetch_data(tag_query, {'region_name': region_name})

    # Return the tag_id values as JSON
    return jsonify(tag_results)
############ / View Billing Data  #####################















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
    request_message += crc

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
        address = starting_address + i * 2
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















@app.route("/write_evc",methods=["GET"])
def Manualpoll_data_write_evc():
    
        
       
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

    region_results = fetch_data(region_query)
    region_options = [str(region[0]) for region in region_results]

    tag_results = fetch_data(tag_query, params={"region_id": selected_region})
    tag_options = [str(tag[0]) for tag in tag_results]

    run_results = fetch_data(run_query, params={"tag_id": selected_tag})
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
        "evc.html",
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


@app.route('/write_evc', methods=['POST'])
def read_data_write_evc():
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

            region_results = fetch_data(region_query)
            region_options = [str(region[0]) for region in region_results]

            tag_results = fetch_data(tag_query, params={"region_id": selected_region})
            tag_options = [str(tag[0]) for tag in tag_results]

            run_results = fetch_data(run_query, params={"tag_id": selected_tag})
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
        

        return render_template('evc.html',   df=df,

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


    






@app.route("/billing_asgs")
def billing_asgs():
   

    
    selected_region1 = request.args.get('region')
    selected_tag = request.args.get('tag')
    selected_month_year = request.args.get('monthYear')


    # Define your Oracle query to fetch REGION_NAME
    region_query = """
    SELECT DISTINCT REGION_NAME
    FROM VW_AMR_BILLING_DATA
    ORDER BY REGION_NAME
    """
    # Fetch REGION_NAME data using your fetch_data function
    region_results1 = fetch_data(region_query)

    # Define your Oracle query to fetch tag_id based on the selected REGION_NAME
    tag_query = """
    SELECT DISTINCT tag_id
    FROM VW_AMR_BILLING_DATA
    WHERE REGION_NAME = :selected_region1
    ORDER BY tag_id
    """
    # Fetch tag_id data using your fetch_data function
    tag_results = fetch_data( tag_query, {'selected_region1': selected_region1})
    
    
        # Define your Oracle query to fetch data based on selected criteria
    billing_query = """
            SELECT *
            FROM VW_AMR_BILLING_DATA
            WHERE 
                VW_AMR_BILLING_DATA.region_name = :selected_region1
                AND VW_AMR_BILLING_DATA.tag_id = :selected_tag
                AND TO_CHAR(VW_AMR_BILLING_DATA.data_date, 'MM/YYYY') = :selected_month_year
                ORDER BY VW_AMR_BILLING_DATA.data_date
        """
    # Fetch data using your fetch_data function
    results = fetch_data( billing_query, {'selected_region1': selected_region1, 'selected_tag': selected_tag, 'selected_month_year': selected_month_year})
        
    # Render the template with the fetched data and selected region
    return render_template(
        "billingdataasgs.html",
        region_results1=region_results1,
        tag_results=tag_results,
        results=results,
        selected_region1=selected_region1,selected_month_year=selected_month_year
    )



@app.route('/get_tag_asgs')
def get_tags_asgs():
    
        
        region_name = request.args.get('region')

        # Use the selected REGION_NAME to fetch associated tag_id values
        tag_query = """
        SELECT DISTINCT tag_id
        FROM VW_AMR_BILLING_DATA
        WHERE REGION_NAME = :region_name
        ORDER BY tag_id
        """
        tag = fetch_data( tag_query, {'region_name': region_name})

        # Return the tag_id values as JSON
        return jsonify(tag)
# @app.route("/get_tags", methods=["GET"])
# def get_tags():
#     
#         
#         selected_region = request.args.get("selected_region")

#         tag_query = """
#                 SELECT DISTINCT TAG_ID
#                 FROM AMR_FIELD_ID, AMR_PL_GROUP
#                 WHERE AMR_FIELD_ID.FIELD_ID = AMR_PL_GROUP.FIELD_ID
#                 AND AMR_PL_GROUP.PL_REGION_ID = :region_id
#             """

#         tag_results = fetch_data(tag_query, params={"region_id": selected_region})
#         tag_options = [str(tag[0]) for tag in tag_results]
#         tag_options.sort()
#         return jsonify({"tag_options": tag_options})
    

@app.route("/get_runs", methods=["GET"])
def get_runs():
    
        
        selected_tag = request.args.get("selected_tag")

        run_query = """
            SELECT DISTINCT METER_STREAM_NO
            FROM AMR_FIELD_ID , amr_field_meter
            WHERE amr_field_id.meter_id = amr_field_meter.meter_id
            AND amr_field_id.tag_id = :tag_id
        """

        run_results = fetch_data(run_query, params={"tag_id": selected_tag})
        run_options = [str(run[0]) for run in run_results]
        run_options.sort()
        return jsonify({"run_options": run_options})
    






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





# update polling

def update_sql(sql_statement):
    with connection.cursor() as cursor:
        
        cursor.execute(sql_statement)
    connection.commit()

def insert_address_range_to_oracle(
    poll_config, poll_billing, enable_config, enable_billing, evc_type
):
    
    with connection.cursor() as cursor:
        sql_insert = """
            INSERT INTO AMR_POLL_RANGE (POLL_CONFIG, POLL_BILLING, POLL_CONFIG_ENABLE, POLL_BILLING_ENABLE, EVC_TYPE)
            VALUES (:1, :2, :3, :4, :5)
        """

        # Convert enable_config and enable_billing to comma-separated strings
        enable_config_str = ",".join(map(str, enable_config))
        enable_billing_str = ",".join(map(str, enable_billing))

        data_to_insert = (
            poll_config,
            poll_billing,
            enable_config_str,
            enable_billing_str,
            evc_type,
        )

        cursor.execute( sql_insert, data_to_insert)

    connection.commit()

@app.route("/polling_route")
def polling_route():
    # Fetch type options for the dropdown
    type_query = "SELECT VC_NAME FROM AMR_VC_TYPE ORDER BY VC_NAME"
    type_results = fetch_data(type_query)
    type_options = [str(type[0]) for type in type_results]
    # print(type_results)

    # Define the base query for fetching polling data
    base_query = """
    SELECT
        apr.evc_type,
        apr.poll_config,
        apr.poll_billing,
        apr.poll_config_enable,
        apr.poll_billing_enable
    FROM
        amr_poll_range apr
    JOIN
        amr_vc_type avt ON apr.evc_type = avt.id
    {type_condition}
    """

    # Get selected type from the dropdown
    selected_type = request.args.get("type_dropdown")

    # Define type condition based on the selected type
    type_condition = f"AND avt.VC_NAME = '{selected_type}'" if selected_type else ""

    # Check if a type is selected before executing the query
    if selected_type:
        # Modify the base query with the selected conditions
        query = base_query.format(type_condition=type_condition)

        # Fetch data using the modified query
        results = fetch_data(query)
        # print(results)

        columns = [
            "evc_type",
            "poll_config",
            "poll_billing",
            "poll_config_enable",
            "poll_billing_enable",
        ]
        df = pd.DataFrame(results, columns=columns)

        
        poll_config_list = df.get(["poll_config"]).values.tolist()
        list_config = str(poll_config_list[0]).strip("[]'").split(",")
        # print("===", poll_config_list)
        
        poll_billing_list = df.get(["poll_billing"]).values.tolist()
        list_billing = str(poll_billing_list[0]).strip("[]'").split(",")
        
        poll_config_enable_list = df.get(["poll_config_enable"]).values.tolist()
        list_enable_config = str(poll_config_enable_list[0]).strip("[]'").split(",")
     
        poll_billing_enable_list = df.get(["poll_billing_enable"]).values.tolist()
        list_enable_billing = str(poll_billing_enable_list[0]).strip("[]'").split(",")
        
        return render_template(
            "polling.html",
            tables=[df.to_html(classes="data", index=False)],
            titles=columns,
            selected_type=selected_type,
            type_options=type_options,
            list_config=list_config,
            list_billing=list_billing,
            list_enable_config=list_enable_config,
            list_enable_billing=list_enable_billing,
        )
    else:
    # Render the HTML template without the table if no type is selected
        return render_template(
            "polling.html",
            tables=[],
            titles=[],
            selected_type=None,
            type_options=type_options,
            list_config=[],
            list_billing=[],
            list_enable_config=[],
            list_enable_billing=[],
        )
    
MAX_ADDRESS_LENGTH = 249

@app.route("/update_polling_data", methods=["POST"])
def update_polling_data(): 
    selected_type = request.form.get("selected_type")

    type_id_query = f"SELECT ID FROM AMR_VC_TYPE WHERE VC_NAME LIKE '{selected_type}'"
    results = fetch_data(type_id_query)
    type_id = str(results[0]).strip("',()")
    print(type_id)
    
    # Update configuration data
    poll_config_all = ""
    enable_config = ""
    for i in range(0, 5):
        start_key = f"start_config{i + 1}"
        end_key = f"end_config{i + 1}"
        enable_key = f"enable_config[{i}]"
        
        start_value = request.form.get(start_key)
        end_value = request.form.get(end_key)
        enable_value = 1 if request.form.get(enable_key) == "on" else 0

        address_range = f"{start_value},{end_value}"
        if len(poll_config_all + address_range) <= MAX_ADDRESS_LENGTH:
            if i > 0:
                poll_config_all += ","
            poll_config_all += address_range

        if i == 0:
            enable_config = str(enable_value)
        else:
            enable_config +=  "," + str(enable_value)
            
    print("poll_config:", poll_config_all)
    print("poll_config_enable:", enable_config)
    
    # Update billing data
    poll_billing_all = ""
    enable_billing = ""
    for i in range(0, 10):
        start_key = f"start{i + 1}"
        end_key = f"end{i + 1}"
        enable_key = f"enable[{i}]"
        
        start_value = request.form.get(start_key)
        end_value = request.form.get(end_key)
        enable_value = 1 if request.form.get(enable_key) == "on" else 0
        
        address_range = f"{start_value},{end_value}"
        if len(poll_billing_all + address_range) <= MAX_ADDRESS_LENGTH:
            if i > 0:
                poll_billing_all += ","
            poll_billing_all += address_range

        if i == 0:
            enable_billing = str(enable_value)
        else:
            enable_billing += "," + str(enable_value)
    
    print("poll_billing:", poll_billing_all)
    print("poll_config_enable:", enable_billing)

    update_query = f"""
    UPDATE amr_poll_range
    SET 
        poll_config = '{poll_config_all}',
        poll_billing = '{poll_billing_all}',
        poll_config_enable = '{enable_config}',
        poll_billing_enable = '{enable_billing}'
    WHERE evc_type = '{type_id}'
    """
    update_sql(update_query)
    print("Update Query:", update_query)
    # After updating the data, you may redirect to the polling route or perform any other necessary actions
    
    return redirect("/polling_route")

@app.route("/add_polling_route")
def add_polling_route():
    return render_template("add_polling.html")

MAX_ADDRESS_LENGTH = 249

@app.route("/save_to_oracle", methods=["POST"])
def save_to_oracle():
    
        
    try:
        data = request.get_json()

        # Add the following line to define 'evc_type'
        evc_type = data.get("evc_type", "")

        def validate_address_range(start_key, end_key):
            start_address = int(data.get(start_key, 0))
            end_address = int(data.get(end_key, 0))

            if end_address - start_address + 1 > MAX_ADDRESS_LENGTH:
                raise ValueError(
                    f"Address range {start_key} - {end_key} exceeds the maximum length of {MAX_ADDRESS_LENGTH}"
                )

            return start_address, end_address

        combined_address_config = ",".join(
            [
                ",".join(map(str, validate_address_range(f"start{i}", f"end{i}")))
                for i in range(1, 6)
                if data.get(f"start{i}")
            ]
        )

        enable_config = [int(data.get(f"enable{i}", 0)) for i in range(1, 6)]

        combined_address_billing = ",".join(
            [
                ",".join(map(str, validate_address_range(f"start{i}", f"end{i}")))
                for i in range(6, 16)
                if data.get(f"start{i}")
            ]
        )

        enable_billing = [int(data.get(f"enable{i}", 0)) for i in range(6, 16)]

        if not combined_address_config or not combined_address_billing:
            response = {
                "status": "error",
                "message": "Please enter at least one valid start or end address for both configurations.",
            }
            return jsonify(response)

        # Add a function to update the existing records in Oracle
        update_address_range_in_oracle(
            combined_address_config,
            combined_address_billing,
            enable_config,
            enable_billing,
            evc_type,
        )

        response = {"status": "success", "message": "Data updated successfully"}
    except ValueError as ve:
        response = {"status": "error", "message": str(ve)}
    except cx_Oracle.DatabaseError as e:
        (error,) = e.args
        print(f"Oracle Database Error {error.code}: {error.message}")
        traceback.print_exc()  # Print detailed traceback information
        response = {
            "status": "error",
            "message": f"Database Error: {error.code} - {error.message}",
        }
    except Exception as e:
        print(f"Error: {e}")
        traceback.print_exc()  # Print detailed traceback information
        response = {
            "status": "error",
            "message": f"An error occurred while updating data: {str(e)}",
        }

    return jsonify(response)

@app.route('/mapping_config')  
def mapping_config_route():
    
        
        # SQL query to fetch options for the dropdown
        type_query = "SELECT VC_NAME FROM AMR_VC_TYPE ORDER BY VC_NAME"
        type_results = fetch_data(type_query)
        type_options = [str(type[0]) for type in type_results]

        # SQL query to fetch data based on selected type
        base_query = """
        SELECT
            TO_CHAR(address),
            description,
            data_type,
            evc_type,
            or_der
            
        FROM
            amr_mapping_config, amr_vc_type
        WHERE
            amr_mapping_config.evc_type = amr_vc_type.id
            AND amr_vc_type.VC_NAME LIKE '{selected_type}'
        """

        selected_type = request.args.get("type_dropdown")
        selected_type = f"{selected_type}" if selected_type else ""

        if selected_type:
            query = base_query.format(selected_type=selected_type)
            results = fetch_data(query)

            columns = [
                "address",
                "description",
                "data_type",
                "evc_type",
                "or_der",
                
            ]
            df = pd.DataFrame(results, columns=columns)

            address_list = df.get(["address"]).values.tolist()
            list_address = str(address_list[0]).strip("[]'").split(",")
            print("map:", df)
                
            description_list = df.get(["description"]).values.tolist()
            list_description = str(description_list[0]).strip("[]'").split(",")
                
            data_type_list = df.get(["data_type"]).values.tolist()
            list_data_type = str(data_type_list[0]).strip("[]'").split(",")       
            
            evc_type_list = df.get(["evc_type"]).values.tolist()
            list_evc_type = str(evc_type_list[0]).strip("[]'").split(",")
            
            or_der_list = df.get(["or_der"]).values.tolist()
            list_or_der = str(or_der_list[0]).strip("[]'").split(",")
                
            

            return render_template(
                'mapping_config.html', 
                type_options=type_options, 
                selected_type=selected_type, 
                table=df.to_html(index=False),
                list_address=df["address"].tolist(),
                list_description=df["description"].tolist(),
                list_data_type=df["data_type"].tolist(),
                list_evc_type=df["evc_type"].tolist(),
                list_or_der=df["or_der"].tolist()
                
            )
        else:
            return render_template('mapping_config.html', type_options=type_options)

def checkStrNone(stringcheck):
    if stringcheck == "None": return ""
    return stringcheck

@app.route('/update_mapping_config_route', methods=['POST'])
def update_mapping_config():
    selected_type = request.form.get('selected_type')

    # Fetch type_id from the database
    type_id_query = f"SELECT ID FROM AMR_VC_TYPE WHERE VC_NAME LIKE '{selected_type}'"
    results = fetch_data(type_id_query)
    type_id = str(results[0]).strip("',()")
    print("type:", type_id)
    
    query = """
        SELECT
            apr.evc_type,
            apr.poll_config


        FROM
            amr_poll_range apr
        JOIN
        amr_vc_type avt ON apr.evc_type = avt.id
        {type_condition}
        """
    type_condition = f"AND avt.VC_NAME = '{selected_type}'" if selected_type else ""
    
    # Check if a type is selected before executing the query
    if type_condition:
        query = query.format(type_condition=type_condition)
        results = fetch_data(query)
        # print(results)

        columns = [
            "evc_type",
            "poll_config",
            
        ]
        df = pd.DataFrame(results, columns=columns)

        
        poll_config_list = df.get(["poll_config"]).values.tolist()
        list_config = str(poll_config_list[0]).strip("[]'").split(",")
        print("start:", list_config)     

    description_VC_TYPE = [] 

    for j in range(0,QUANTITY_CONFIG_DATA):  
        i = f"{j:02d}"
        address_key = f"list_address{i}"
        description_key = f"list_description{i}"
        data_type_key = f"list_data_type{i}"
        evc_type_key = f"list_evc_type{i}"
        or_der_key = f"list_or_der{i}"

        address_value = checkStrNone(request.form.get(address_key))
        description_value = checkStrNone(request.form.get(description_key))
        data_type_value = checkStrNone(request.form.get(data_type_key))
        evc_type_value = request.form.get(evc_type_key)
        or_der_value = request.form.get(or_der_key)

        valid = False
        
        #check config
        print(address_value)
        # if textbox = None ไม่ต้อง check address แต่ต้องappend array ด้วย blank เพราะเดี๋ยวจะไม่ครบใน sql command
        if address_value == "": 
            description_VC_TYPE.append("")
            continue
        k = 0
        for k in range(0,QUANTITY_RANGE_CONFIG_LIST,2):
           
            address_value_int = int(address_value)
            address_check_low = int(list_config[k])
            address_check_high = int(list_config[k+1])
            k+=2
            print("low = ", address_check_low, ", high = ", address_check_high, "; value = ", address_value_int)
            if address_check_low  <= address_value_int :
                if address_value_int <= address_check_high:
                    valid = True; print("Result = True"); break
            print("Result = False")
        
        
        if valid == False:
            print("Error : invalid address ; alert หน้าจอ และ ออกจาก function นี้ได้เลย ")
            
            #error
            return ""
             
    
        description_VC_TYPE.append(checkStrNone(description_value))
        # print("---", description_value)


        # Update SQL query based on your table structure
        update_query = f"""
        UPDATE AMR_MAPPING_CONFIG
        SET
            ADDRESS = '{address_value}',
            DESCRIPTION = '{description_value}',
            DATA_TYPE = '{data_type_value}',
            OR_DER = '{or_der_value}'        
        WHERE evc_type = '{evc_type_value}' and or_der = '{or_der_value}'
        """
        # print("Update Query##################", update_query)
        update_sql(update_query)
        
        
    
    update_vc_info_query = f"""
    UPDATE AMR_VC_CONFIGURED_INFO
    SET
        CONFIG1 = '{description_VC_TYPE[0]}',
        CONFIG2 = '{description_VC_TYPE[1]}',
        CONFIG3 = '{description_VC_TYPE[2]}',
        CONFIG4 = '{description_VC_TYPE[3]}',
        CONFIG5 = '{description_VC_TYPE[4]}',
        CONFIG6 = '{description_VC_TYPE[5]}',
        CONFIG7 = '{description_VC_TYPE[6]}',
        CONFIG8 = '{description_VC_TYPE[7]}',
        CONFIG9 = '{description_VC_TYPE[8]}',
        CONFIG10 = '{description_VC_TYPE[9]}',
        CONFIG11 = '{description_VC_TYPE[10]}',
        CONFIG12 = '{description_VC_TYPE[11]}',
        CONFIG13 = '{description_VC_TYPE[12]}',
        CONFIG14 = '{description_VC_TYPE[13]}',
        CONFIG15 = '{description_VC_TYPE[14]}',
        CONFIG16 = '{description_VC_TYPE[15]}',
        CONFIG17 = '{description_VC_TYPE[16]}',
        CONFIG18 = '{description_VC_TYPE[17]}',
        CONFIG19 = '{description_VC_TYPE[18]}',
        CONFIG20 = '{description_VC_TYPE[19]}'
    
    WHERE 
        VC_TYPE = '{evc_type_value}'
        
    """
    
    update_sql(update_vc_info_query)
    # print(update_vc_info_query)

    return redirect("/mapping_config")


@app.route('/mapping_billing')  
def mapping_billing_route():
    # SQL query to fetch options for the dropdown
    type_query = "SELECT VC_NAME FROM AMR_VC_TYPE"
    type_results = fetch_data(type_query)
    type_options = [str(type[0]) for type in type_results]

    # SQL query to fetch data based on selected type
    base_query = f"""
     SELECT
        address,
        description,
        data_type,
        evc_type,
        or_der,
        daily
        
    FROM
        amr_mapping_billing, amr_vc_type
    WHERE
        amr_mapping_billing.evc_type = amr_vc_type.id
        AND amr_vc_type.VC_NAME LIKE :1
        AND daily = 1
    order by or_der
    """

    selected_type = request.args.get("type_dropdown") or ""
    if selected_type:
        type_id_query = "SELECT ID FROM AMR_VC_TYPE WHERE VC_NAME LIKE :1"
        results = fetch_data(type_id_query, (selected_type,))
        
        interval = request.args.get("interval") or "10"
        
         
        if results:
            type_id = str(results[0][0])

            query = base_query
            results = fetch_data(query, (selected_type,))
            
            print("type:", type_id)
            max_daily_query = "SELECT MAX(daily) FROM amr_mapping_billing WHERE evc_type LIKE :1"
            max_daily_result = fetch_data(max_daily_query, (type_id,))
            max_daily_value = str(max_daily_result[0][0]) if max_daily_result and max_daily_result[0][0] else ""
            print("max_day:", max_daily_value)

            #if max_daily_value <=
            columns = [
                "address",
                "description",
                "data_type",
                "evc_type",
                "or_der",
                "daily",
            ]
            df = pd.DataFrame(results, columns=columns)
            print("dd:", df)
            
            # Extracting lists directly from DataFrame columns
            list_address = df["address"].tolist()
            list_description = df["description"].tolist()
            list_data_type = df["data_type"].tolist()
            list_evc_type = df["evc_type"].tolist()
            list_or_der = df["or_der"].tolist()
            list_daily = df["daily"].tolist()

            return render_template(
                'mapping_billing.html', 
                type_options=type_options, 
                selected_type=selected_type, 
                max_daily_value=max_daily_value,
                table=df.to_html(index=False),
                list_address=list_address,
                list_description=list_description,
                list_data_type=list_data_type,
                list_evc_type=list_evc_type,
                list_or_der=list_or_der,
                list_daily=list_daily,
                interval=interval
            )

    return render_template('mapping_billing.html', type_options=type_options)

    
@app.route('/update_mapping_billing_route', methods=['POST'])
def update_mapping_billing():
    selected_type = request.form.get('selected_type')

    # Fetch type_id from the database
    type_id_query = f"SELECT ID FROM AMR_VC_TYPE WHERE VC_NAME = '{selected_type}'"
    results = fetch_data(type_id_query)
    type_id = str(results[0]).strip("',()")
    
    #max_daily_query = "SELECT MAX(daily),MAX(id),MAX(address),MAX(or_der)  FROM amr_mapping_billing  WHERE evc_type = {}".format(type_id)
    max_daily_query = "SELECT MAX(daily)  FROM amr_mapping_billing  WHERE evc_type = {}".format(type_id)
    max_daily_result = fetch_data(max_daily_query)
    max_daily_query = str(max_daily_result[0]).strip("',()")
    # print("Max:", max_daily_query)
    
    # evc_type = type_id
    # max_daily_query = max day before save 
    
    dataframes = {
                'address':[],
                'description':[],
                'data_type':[],
                'evc_type':[],
                'or_der':[],
                'daily':[],
    }
    df_data = pd.DataFrame(dataframes)
    
    # get max day from text box
    max_daily_new = int(request.form.get('max_day'))
    
    # get information Crete initial dataframe
    
    address_value_array = []
    description_value_array = []
    data_type_value_array = []
    or_der_value_array = []
    
    
    for i in range(0, QUANTITY_BILLING_PER_DAY): 
        i = f"{i:02d}"
        address_key = f"list_address{i}"
        description_key = f"list_description{i}"
        data_type_key = f"list_data_type{i}"
        #evc_type_key = f"list_evc_type{i}"
        or_der_key = f"list_or_der{i}"
        #daily_key = f"list_daily{i}"
                
        address_value = request.form.get(address_key.strip("',()"))
        address_value_array.append(int(address_value))
        
        description_value = request.form.get(description_key.strip("',()"))
        description_value_array.append(description_value)
        
        data_type_value = request.form.get(data_type_key.strip("',()"))
        data_type_value_array.append(data_type_value)
        #evc_type_value = request.form.get(evc_type_key.strip("',()"))
        or_der_value = request.form.get(or_der_key.strip("',()"))
        or_der_value_array.append(or_der_value)

    
    #print("XX", address_value_array, description_value_array, data_type_value_array, or_der_value_array)

    # create Full Data frame
    # Get interval
    interval = request.args.get("interval") or "10"
    # print("interval", interval)
    
    # for j in range(0,max_daily_new):
    #     #daily_value = j+1
    #     for i in range(0, QUANTITY_BILLING_PER_DAY):
             
    #         address_calc = int(address_value_array[i]) + (j*int(interval))
    #         print("")
    #         data = {
    #                 'address': [address_calc], 
    #                 'description': [description_value_array[i]],
    #                 'data_type': [data_type_value_array[i]],
    #                 'evc_type': [type_id],
    #                 'or_der': [int(or_der_value_array[i])],
    #                 'daily': [j+1]
    #         }
            
    #         df2 = pd.DataFrame(data)
    #         df_data = pd.concat([df_data, df2], ignore_index=True)
            
    #     df_data['address'] = df_data['address'].astype(int)
    #     df_data['or_der'] = df_data['or_der'].astype(int)
    #     df_data['daily'] = df_data['daily'].astype(int)      
            
    print("dd4", df_data)
         
       
    if  max_daily_new <= int(max_daily_query) :
        if max_daily_new < int(max_daily_query):
            delete_query = f"""
            DELETE FROM AMR_MAPPING_BILLING
            WHERE evc_type = '{type_id}' AND DAILY > {max_daily_new}
            """
            # print(delete_query)
            update_sql(delete_query)
        
        for j in range(max_daily_new):
            for i in range(QUANTITY_BILLING_PER_DAY):
                update_query = f"""
                UPDATE AMR_MAPPING_BILLING
                SET 
                    ADDRESS = '{int(address_value_array[i]) + (j* int(interval))}',
                    DESCRIPTION = '{description_value_array[i]}',
                    data_type = '{data_type_value_array[i]}'
                WHERE 
                    evc_type = '{type_id}' and 
                    or_der = {i+1} and 
                    daily = {j+1}
                    
                """
                # print("update_query", update_query)
                update_sql(update_query)
        
    else : # max_daily_new > int(max_daily_query):
        # updte 1 to max_daily_query
        for j in range(int(max_daily_query)):
            for i in range(QUANTITY_BILLING_PER_DAY):
                update_billing = f"""
                UPDATE AMR_MAPPING_BILLING
                SET 
                    ADDRESS = '{int(address_value_array[i]) + (j* int(interval))}',
                    DESCRIPTION = '{description_value_array[i]}',
                    data_type = '{data_type_value_array[i]}'
                WHERE 
                    evc_type = '{type_id}' and 
                    or_der = {i+1} and 
                    daily = {j+1}
                """
                # print("update_billing", update_billing)
                update_sql(update_billing)
        
        # Insert max_daily_query to max_daily_new
        
        for j in range(max_daily_new - int(max_daily_query)):
            for i in range(QUANTITY_BILLING_PER_DAY):  # Assuming this is the correct length
                new_address = int(address_value_array[i]) + ((int(max_daily_query) + j) * int(interval))
                new_description = description_value_array[i]
                new_data_type = data_type_value_array[i]
                new_evc_type = type_id
                new_or_der = or_der_value_array[i]
                new_daily = int(max_daily_query) + j + 1

                insert_query = f"""
                INSERT INTO AMR_MAPPING_BILLING (ADDRESS, DESCRIPTION, DATA_TYPE, evc_type, OR_DER, DAILY)
                VALUES ('{new_address}', '{new_description}', '{new_data_type}',  '{new_evc_type}', '{new_or_der}', '{new_daily}')
                """

                update_sql(insert_query)
                # print(insert_query)

    return redirect("/mapping_billing")


@app.route("/add_mapping_route")
def add_mapping_route():
    return render_template("add_mapping.html")


@app.route("/submit_form", methods=["POST"])
def submit_form():
    cursor = None
    connection = None
    
        
    try:
        data_list = []
        for i in range(1, 21):
            address = request.form[f"address{i}"]
            description = request.form[f"description{i}"]
            type_value = request.form.get(f"type_value{i}")
            evc_type = request.form[f"evc_type{i}"]
            or_der = request.form[f"or_der{i}"]
            data_type = request.form[f"data_type{i}"]

            data_list.append(
                (address, description, type_value, evc_type, or_der, data_type)
            )

        dsn_tns = cx_Oracle.makedsn(host, port, service_name=service)
        connection = cx_Oracle.connect(user=username, password=password, dsn=dsn_tns)

        cursor = connection.cursor()

        sql_merge = """
            MERGE INTO AMR_MAPPING_CONFIG dst
            USING (
                SELECT
                    :address as address,
                    :description as description,
                    :type_value as type_value,
                    :evc_type as evc_type,
                    :or_der as or_der,
                    :data_type as data_type
                FROM dual
            ) src
            ON (dst.address = src.address)
            WHEN MATCHED THEN
                UPDATE SET
                    dst.description = src.description,
                    dst.type_value = src.type_value,
                    dst.evc_type = src.evc_type,
                    dst.or_der = src.or_der,
                    dst.data_type = src.data_type
            WHEN NOT MATCHED THEN
                INSERT (
                    address,
                    description,
                    type_value,
                    evc_type,
                    or_der,
                    data_type
                ) VALUES (
                    src.address,
                    src.description,
                    src.type_value,
                    src.evc_type,
                    src.or_der,
                    src.data_type
                )
        """

        cursor.executemany(sql_merge, data_list)

        # Commit the changes to the database
        connection.commit()

        return "Data saved successfully"
    except Exception as e:
        return f"Error occurred: {str(e)}"
    finally:
        if cursor is not None:
        # Close the cursor
            cursor.close()

    if connection is not None:
        # Close the connection
        connection.close()


@app.route("/add_actraris_route")
def add_actraris_route():
    return render_template("add_actraris.html")


@app.route("/new_form", methods=["POST"])
def submit_new_form():
    cursor = None
    connection = None
    
        
    try:
        data_list = []
        for i in range(1, 18):
            address = request.form.get(f"address{i}")
            description = request.form.get(f"description{i}")
            type_value = request.form.get(f"type_value{i}")
            evc_type = request.form.get(f"evc_type{i}")
            or_der = request.form.get(f"or_der{i}")
            data_type = request.form.get(f"data_type{i}")

            data_list.append(
                (address, description, type_value, evc_type, or_der, data_type)
            )

        dsn_tns = cx_Oracle.makedsn(host, port, service_name=service)
        connection = cx_Oracle.connect(user=username, password=password, dsn=dsn_tns)

        cursor = connection.cursor()

        sql_merge = """
            MERGE INTO AMR_ADDRESS_MAPPING1 dst
            USING (
                SELECT
                    :address as address,
                    :description as description,
                    :type_value as type_value,
                    :evc_type as evc_type,
                    :or_der as or_der,
                    :data_type as data_type
                FROM dual
            ) src
            ON (dst.address = src.address)
            WHEN MATCHED THEN
                UPDATE SET
                    dst.description = src.description,
                    dst.type_value = src.type_value,
                    dst.evc_type = src.evc_type,
                    dst.or_der = src.or_der,
                    dst.data_type = src.data_type
            WHEN NOT MATCHED THEN
                INSERT (
                    address,
                    description,
                    type_value,
                    evc_type,
                    or_der,
                    data_type
                ) VALUES (
                    src.address,
                    src.description,
                    src.type_value,
                    src.evc_type,
                    src.or_der,
                    src.data_type
                )
        """

        cursor.executemany(sql_merge, data_list)

        connection.commit()

        # Commit the changes to the database
        connection.commit()

        return "Data saved successfully"
    except Exception as e:
        return f"Error occurred: {str(e)}"
    finally:
        if cursor is not None:
        # Close the cursor
            cursor.close()

    if connection is not None:
        # Close the connection
        connection.close()




@app.route('/add_site', methods=['GET', 'POST'])
def add_site():
    max_id_query = "SELECT MAX(ID) + 1 FROM amr_field_id"
    max_id_result = fetch_data(max_id_query)
    max_id_value = str(max_id_result[0][0]) if max_id_result and max_id_result[0][0] is not None else ""
    
    AMR0 = "AMR0"
    CUST0 = "CUST0"
    MET0 = "MET0"
    PROT0 = "PROT0"
    
    
    sql_commands = []
        
    if request.method == 'POST':
        phase = request.form['phase']
        site_name = request.form['site_name']
        factory_name = request.form['factory_name']
        region = request.form['region']
        rmiu_type = request.form['rmiu_type']
        power_indicator = request.form['power_indicator']
        modbus_id = request.form['modbus_id']
        ip_address = request.form['ip_address']
        ready_to_billing = request.form.get('ready_to_billing')  # Check if the checkbox is checked
        auto_ping = request.form.get('auto_ping')  # Check if the checkbox is checked
        billing_date = request.form['billing_date']
        show_sg_co2_n2 = request.form['show_sg_co2_n2']
        amount_of_meter = request.form['amount_of_meter']
        initial_username = request.form['initial_username']
        initial_password = request.form['initial_password']
        
        port_1 = request.form['port_1']
        port1 = request.form['port1']
        auto_1 = request.form['auto_1']
        
        port_2 = request.form['port_2']
        port2 = request.form['port2']
        auto_2 = request.form['auto_2']
        
        port_3 = request.form['port_3']
        port3 = request.form['port3']
        auto_3 = request.form['auto_3']
        
        port_4 = request.form['port_4']
        port4 = request.form['port4']
        auto_4 = request.form['auto_4']
        
        port_5 = request.form['port_5']
        port5 = request.form['port5']
        auto_5 = request.form['auto_5']
        
        port_6 = request.form['port_6']
        port6 = request.form['port6']
        auto_6 = request.form['auto_6']
        
        # print(f'Phase: {phase}')
        # print(f'Site Name: {site_name}')
        # print(f'Factory Name: {factory_name}')
        # print(f'Region: {region}')
        # print(f'RMIU Type: {rmiu_type}')
        # print(f'Power Indicator: {power_indicator}')
        # print(f'MODBUS ID: {modbus_id}')
        # print(f'IP Address: {ip_address}')
        # print(f'Ready to Billing: {ready_to_billing}')  # Will print '1' if checkbox is checked
        # print(f'Auto Ping: {auto_ping}')  # Will print '1' if checkbox is checked
        # print(f'Billing Date: {billing_date}')
        # print(f'Show SG CO2 N2: {show_sg_co2_n2}')
        # print(f'Amount of Meter: {amount_of_meter}')
        # print(f'Initial Username: {initial_username}')
        # print(f'Initial Password: {initial_password}')
        
        # print(f'port_1: {port_1}')
        # print(f'port1: {port1}')
        # print(f'auto_1: {auto_1}')
        
        # print(f'port_2: {port_2}')
        # print(f'port2: {port2}')
        # print(f'auto_2: {auto_2}')
        
        # print(f'port_3: {port_3}')
        # print(f'port3: {port3}')
        # print(f'auto_3: {auto_3}')
        
        # print(f'port_4: {port_4}')
        # print(f'port4: {port4}')
        # print(f'auto_4: {auto_4}')
        
        # print(f'port_5: {port_5}')
        # print(f'port5: {port5}')
        # print(f'auto_5: {auto_5}')
        
        # print(f'port_6: {port_6}')
        # print(f'port6: {port6}')
        # print(f'auto_6: {auto_6}')

        amr_user = f"""
        INSERT INTO AMR_USER (ID, DESCRIPTION, USER_NAME, PASSWORD, USER_LEVEL, USER_GROUP, USER_ENABLE)
        VALUES ({max_id_value}, '{site_name}', '{initial_username}', '{initial_password}', '3', '{MET0+max_id_value}', '1')
        """
        # update_sql(amr_user)
        
        amr_field_id = f"""
        INSERT INTO AMR_FIELD_ID (
                                ID, 
                                TAG_ID, 
                                FIELD_ID, 
                                CUST_ID, 
                                METER_ID, 
                                PROTOCOL_ID, 
                                RTU_MODBUS_ID,
                                RMIU_AUTO_ENABLE,
                                PING_ENABLE,
                                RMIU_TYPE, 
                                SIM_IP,
                                RMIU_POLL_REPEAT1,
                                RMIU_POLL_REPEAT2,
                                AMR_PHASE
                                )
        VALUES ({max_id_value}, '{site_name}', 
                                '{AMR0+max_id_value}', 
                                '{CUST0+max_id_value}', 
                                '{MET0+max_id_value}', 
                                '{PROT0+max_id_value}', 
                                '{modbus_id}',
                                '{ready_to_billing}',
                                '{auto_ping}',
                                '{rmiu_type}', 
                                '{ip_address}',
                                '{0}',
                                '{0}',
                                '{phase}'
                                )
        """
        update_sql(amr_field_id)
        
        amr_field_customer= f"""
        INSERT INTO AMR_FIELD_CUSTOMER (
                                        ID, 
                                        CUST_ID,
                                        CUST_NAME,
                                        CUST_FACTORY_NAME,
                                        METER_RUN
                                        )
        VALUES ({max_id_value}, '{CUST0+max_id_value}',
                                '{site_name}',
                                '{factory_name}',
                                '{amount_of_meter}'            
                                )
        """
        # update_sql(amr_field_customer)
        
        amr_pl_group = f""" 
        INSERT INTO AMR_PL_GROUP (ID, PL_REGION_ID, FIELD_ID) 
        VALUES ({max_id_value}, '{region}', '{AMR0+max_id_value}')
        """
        update_sql(amr_pl_group)
        
        for i in range(1, int(amount_of_meter) + 1): 
            amr_field_meter = f"""
            INSERT INTO AMR_FIELD_METER (METER_ID, 
                                        METER_STREAM_NO, 
                                        METER_NO_STREAM,
                                        METER_STREAM_TYPE,
                                        METER_PORT_NO,
                                        METER_AUTO_ENABLE,
                                        METER_POLL_REPEAT1,
                                        METER_POLL_REPEAT2,
                                        METER_POLL_REPEAT3,
                                        METER_POLL_REPEAT4,
                                        METER_POLL_REPEAT5,
                                        METER_POLL_REPEAT6,
                                        METER_POLL_REPEAT7 
                                        )
            VALUES ('{MET0+max_id_value}', '{i}',
                                        '{amount_of_meter}',
                                        '{request.form['port_' + str(i)]}',
                                        '{request.form['port' + str(i)]}',
                                        '{request.form['auto_' + str(i)]}',
                                        '{0}',
                                        '{0}',
                                        '{0}',
                                        '{0}',
                                        '{0}',
                                        '{0}',
                                        '{0}'
                                        )         
            """
            # update_sql(amr_field_meter)
            
            amr_field_profile = f"""
            INSERT INTO AMR_FIELD_PROFILE (METER_ID, 
                                            METER_STREAM_NO,
                                            WRITE_CONFIG_ENABLE,
                                            WRITE_CONFIG_REPEAT1,
                                            WRITE_CONFIG_REPEAT2
                                            )
            VALUES ('{MET0+max_id_value}', '{i}',
                                            '{auto_ping}',
                                            '{0}',
                                            '{0}'
                                            )
            """
            # update_sql(amr_field_profile)
            
            amr_field_protocal = f"""
            INSERT INTO AMR_FIELD_PROTOCAL (PROTOCOL_ID, PROTOCOL_STREAM_NO, PROTOCOL_NO_STREAM)
            VALUES ('{PROT0+max_id_value}', '{i}', '{amount_of_meter}')
            """
            # update_sql(amr_field_protocal)
            
        return render_template('home.html',)

        
    return render_template('add_site.html', max_id_value=max_id_value)

@app.route('/edit_site', methods=['GET', 'POST'])
def edit_site():
    query_type = request.args.get("query_type")

    # SQL query to fetch unique PL_REGION_ID values
    region_query = """
    SELECT * FROM AMR_REGION 
    """

    selected_region = request.args.get("region_dropdown")

    # Fetch unique region values
    region_results = fetch_data(region_query)
    region_options = [str(region[0]) for region in region_results]

    tag_query = """
    SELECT DISTINCT TAG_ID
    FROM AMR_FIELD_ID
    JOIN AMR_PL_GROUP ON AMR_FIELD_ID.FIELD_ID = AMR_PL_GROUP.FIELD_ID 
    WHERE AMR_PL_GROUP.PL_REGION_ID = :region_id
    ORDER BY TAG_ID
    """
    
    selected_tag = request.args.get("tag_dropdown")
    
    # Fetch tag options based on the selected region
    tag_results = fetch_data(tag_query, params={"region_id": selected_region})
    tag_options = [str(tag[0]) for tag in tag_results]
    
    show_tag_query = """
    SELECT DISTINCT
        AMR_FIELD_ID.ID,
        AMR_FIELD_ID.TAG_ID,
        AMR_FIELD_ID.SIM_IP,
        AMR_FIELD_ID.RTU_MODBUS_ID,
        AMR_FIELD_ID.AMR_PHASE,
        AMR_FIELD_CUSTOMER.CUST_FACTORY_NAME,
        AMR_USER.USER_NAME,
        AMR_USER.PASSWORD,
        AMR_FIELD_METER.METER_ID,
        AMR_FIELD_METER.METER_STREAM_NO,
        AMR_FIELD_METER.METER_NO_STREAM,
        AMR_FIELD_METER.METER_STREAM_TYPE,
        AMR_FIELD_METER.METER_PORT_NO,
        AMR_FIELD_METER.METER_AUTO_ENABLE,
        AMR_FIELD_PROFILE.METER_ID,
        AMR_FIELD_PROTOCOL.PROTOCOL_ID,
        AMR_FIELD_PROTOCOL.PROTOCOL_NO_STREAM
    FROM 
        AMR_FIELD_ID
        JOIN AMR_FIELD_CUSTOMER ON AMR_FIELD_ID.CUST_ID = AMR_FIELD_CUSTOMER.CUST_ID
        JOIN AMR_USER ON AMR_FIELD_ID.ID = AMR_USER.ID
        JOIN AMR_FIELD_METER ON AMR_FIELD_ID.METER_ID = AMR_FIELD_METER.METER_ID
        JOIN AMR_FIELD_PROFILE ON AMR_FIELD_ID.METER_ID = AMR_FIELD_PROFILE.METER_ID
        JOIN AMR_FIELD_PROTOCOL ON AMR_FIELD_ID.PROTOCOL_ID = AMR_FIELD_PROTOCOL.PROTOCOL_ID
        JOIN AMR_PL_GROUP ON AMR_FIELD_ID.FIELD_ID = AMR_PL_GROUP.FIELD_ID 
        JOIN AMR_REGION ON AMR_PL_GROUP.PL_REGION_ID = AMR_REGION.ID
    WHERE 
        AMR_REGION.ID = :region_id AND
        AMR_FIELD_ID.TAG_ID = :tag_id
    ORDER BY METER_STREAM_NO
    """
    
    data = []
    if selected_region is not None and selected_tag is not None:
        data = fetch_data(show_tag_query, params={"region_id": selected_region, "tag_id": selected_tag})
       

    # Create DataFrame from query results
    columns = [
        'id',
        'tag_id',
        'sim_ip',
        'rtu_modbus_id',
        'amr_phase',
        'cust_factory_name',
        'user_name',
        'password',
        'meter_id',
        'meter_stream_no',
        'meter_no_stream',
        'meter_stream_type',
        'meter_port_no',
        'meter_auto_enable',
        'meter_id',
        'protocol_id',
        'protocol_no_stream'
    ]
    df = pd.DataFrame(data, columns=columns)
    
    
    if not df.empty:
        list_id = df["id"].iloc[0]
        list_tag_id = df["tag_id"].iloc[0]
        list_cust_factory_name = df["cust_factory_name"].iloc[0]
        list_amr_phase = df["amr_phase"].iloc[0]
        list_rtu_modbus_id = df["rtu_modbus_id"].iloc[0]
        list_sim_ip = df["sim_ip"].iloc[0]
        list_user_name = df["user_name"].iloc[0]
        list_password = df["password"].iloc[0]
        list_meter_stream_no = df["meter_stream_no"].tolist()       
        list_meter_port_no = df["meter_port_no"].tolist()
        list_meter_auto_enable = df["meter_auto_enable"].tolist()
        

    
        list_meter_stream_type = []
        for meter_stream_type in df["meter_stream_type"]:
            meter_stream_type_list = f"""SELECT vc_name FROM amr_vc_type WHERE id = '{meter_stream_type}' ORDER BY id"""
            type = fetch_data(meter_stream_type_list)
            if type:
                list_meter_stream_type.append(type[0][0])
            else:
                list_meter_stream_type.append(None)
            print("list_meter_stream_type", list_meter_stream_type)
                
        list_meter_port_no = []
        for meter_port_no in df["meter_port_no"]:
            meter_port_no_list =f"""SELECT port_no FROM amr_port_info WHERE id = '{meter_port_no}' ORDER BY id"""
            port = fetch_data(meter_port_no_list)
            if port:
                list_meter_port_no.append(port[0][0])
            else:
                list_meter_port_no.append(None)
            print("list_meter_port_no", list_meter_port_no)
        
            
    else:
        list_id = None
        list_tag_id = None
        list_cust_factory_name = None
        list_amr_phase = None
        list_rtu_modbus_id = None
        list_sim_ip = None
        list_user_name = None
        list_password = None
        list_meter_stream_no = None
        list_meter_auto_enable = None
        list_meter_stream_type = None
        list_meter_port_no = None
        
    # update_user = f"""
    #         UPDATE AMR_USER 
    #         SET 
    #             user_name = '{list_user_name}',
    #             password = '{list_password}'
    #         WHERE id = '{list_id}'
    #         """
    # print("update_user", update_user)
    # update_sql(update_user)
    

    html_table = df.to_html(index=False)
    
    

    return render_template('edit_site.html', 
                            region_options=region_options, 
                            tag_options=tag_options, 
                            selected_region=selected_region,
                            selected_tag=selected_tag,
                            list_id=list_id,
                            list_tag_id=list_tag_id,
                            list_cust_factory_name=list_cust_factory_name,
                            list_amr_phase=list_amr_phase,
                            list_rtu_modbus_id=list_rtu_modbus_id,
                            list_sim_ip=list_sim_ip,
                            list_user_name=list_user_name,
                            list_password=list_password,
                            list_meter_stream_no=list_meter_stream_no,
                            list_meter_stream_type=list_meter_stream_type,
                            list_meter_port_no=list_meter_port_no,
                            list_meter_auto_enable=list_meter_auto_enable,
                            html_table=html_table)







@app.route("/homeasgs")
def homeasgs():
    return render_template("homeasgs.html")

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == "__main__":
    app.run(debug=True)


# @app.teardown_appcontext
# def close_conn(*args, **kwargs):
#     """This function closes the Oracle connection after each request."""
#     global active_connection
#     if active_connection is not None:
#         active_connection.close()


@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html'), 404

# @app.route('/logout')     
# def logout():
#     session.clear()       # remove the user and auth token from the session if it exists
#     flash('You were logged out', 'info')
#     return redirect(url_for('login'))   # send them back to the sign in page

# def FillFullMonth(df, run_no):
#     pass
    #Get month
    # for 1 to today
    #   if ddf.log['datadate'] ไม่มีข้อมูลวันที่นี้ 
    #       สร้าง series ["DATE", N/A, N/A ,....., runno]
    #       ใส่ เข้าไป 
    #  sort
    #  return df
    #
    