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
active_connection = None  # Global variable to track the active connection

def connect_to_amr_db():
    global active_connection
    username = "AMR_DB"
    password = "AMR_DB"
    hostname = "10.104.240.26"
    port = "1521"
    sid = "AMR"

    try:
        dsn = cx_Oracle.makedsn(hostname, port, sid)
        connection = cx_Oracle.connect(username, password, dsn)
        active_connection = "AMR_DB"
        print("Connected to AMR database")
        return connection
    except cx_Oracle.Error as e:
        (error,) = e.args
        print("Oracle Error:", error)
        return None

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




############  /connect database  #####################


############  Home page  #####################
@app.route("/")
def home_amr():
    return render_template("home.html")
############ / Home page  #####################

@app.route("/ASGS")
def ASGS():
    return render_template("ASGS.html")


# ############  Add User  #####################
@app.route("/add_user")
def add_user_route():
    return render_template("add_user.html")
# @app.route("/add_user", methods=["GET", "POST"])
# def add_user_route():
#     if request.method == "POST":
#         description = request.form["description"]
#         user_name = request.form["user_name"]
#         password = request.form["password"]
#         user_level = request.form["user_level"]

#         # เข้ารหัสรหัสผ่านโดยใช้ MD5
#         hashed_password = md5_hash(password)

#         # แปลงเป็น RAWTOHEX ก่อนที่จะบันทึกลงใน Oracle
#         hashed_password_hex = "RAWTOHEX(DBMS_OBFUSCATION_TOOLKIT.MD5(input_string => UTL_I18N.STRING_TO_RAW('{}', 'AL32UTF8')))".format(
#             hashed_password
#         )

#         query = "INSERT INTO AMR_USER_TESTS (description, user_name, password, user_level) VALUES (:1, :2, {}, :4)".format(
#             hashed_password_hex
#         )
#         params = (description, user_name, user_level)

#         if execute_query(query, params):
#             flash("User added successfully!", "success")
#             return render_template("add_user.html")
#         else:
#             flash("Failed to add user. Please try again.", "error")

#     return render_template("add_user.html")


# ############  /Add User  #####################



# ############  edit_user   #####################
@app.route("/edit_user")
def edit_user_route():
    return render_template("edit_user.html")

# def get_data(filter_text=None, sort_column=None):
#     # try:
#         connection = cx_Oracle.connect(
#             user=username, password=password, dsn=f"{hostname}:{port}/{sid}"
#         )
#         cursor = connection.cursor()

#         # Base query
#         query = (
#             "SELECT description, USER_NAME, PASSWORD, USER_LEVEL FROM AMR_User_tests"
#         )

#         # Apply filtering
#         if filter_text:
#             query += f" WHERE USER_NAME LIKE '%{filter_text}%'"

#         # Apply sorting
#         if sort_column:
#             query += f" ORDER BY {sort_column}"

#         cursor.execute(query)

#         # Fetch data in chunks (e.g., 100 rows at a time)
#         chunk_size = 100
#         data = []
#         while True:
#             rows = cursor.fetchmany(chunk_size)
#             if not rows:
#                 break
#             data.extend(
#                 [
#                     {
#                         "description": row[0],
#                         "user_name": row[1],
#                         "password": row[2],
#                         "user_level": row[3],
#                     }
#                     for row in rows
#                 ]
#             )

#         return data
#     except cx_Oracle.Error as e:
#         (error,) = e.args
#         print("Oracle Error:", error)
#         return []
#     finally:
#         if cursor:
#             cursor.close()
#         if connection:
#             connection.close()


# # Example usage with filtering and sorting
# filter_text = "example"  # Replace with your filter text or None for no filtering
# sort_column = "USER_NAME"  # Replace with your desired column or None for no sorting
# filtered_and_sorted_data = get_data(filter_text=filter_text, sort_column=sort_column)


# @app.route("/get_data")
# def get_data_route():
#     data = get_data()
#     return jsonify(data)


# @app.route("/edit_user", methods=["GET", "POST"])
# def edit_user_route():
#     # ดึงข้อมูลผู้ใช้จากฐานข้อมูล
#     query = "SELECT DESCRIPTION, USER_NAME, PASSWORD, USER_LEVEL FROM AMR_User_tests"
#     user_data = fetch_data(query)

#     if not user_data:
#         flash("User not found!", "error")
#         return render_template("edit_user.html")

#     # ถ้ามีการส่งค่า POST (คือการบันทึกการแก้ไข)
#     if request.method == "POST":
#         # ดึงข้อมูลจากฟอร์มแก้ไข
#         description = request.form["description"]
#         user_name = request.form["user_name"]
#         password = request.form["password"]
#         # user_level = request.form["user_level"]

#         # เข้ารหัสรหัสผ่านโดยใช้ MD5
#         hashed_password = md5_hash(password)

#         # สร้างคำสั่ง SQL สำหรับการแก้ไขข้อมูลผู้ใช้
#         update_query = "UPDATE AMR_USER_TESTS SET description = :1, user_name = :2, password = :3 WHERE description = :4"
#         update_params = (description, user_name, hashed_password, description)

#         # ทำการ execute คำสั่ง SQL และ commit การแก้ไข user_name
#         if execute_query(update_query, update_params):
#             flash("User updated successfully!", "success")
#             return render_template("edit_user.html")
#         else:
#             flash("Failed to update user. Please try again.", "error")

#     # กรณีไม่ใช่การส่งค่า POST ให้ส่งข้อมูลผู้ใช้ไปยัง HTML template หรือทำอย่างอื่นตามที่ต้องการ
#     return render_template("edit_user.html", user_data=user_data)


# ############  /edit_user   #####################


# ############   /remove_user ###################

@app.route("/remove_user")
def remove_user_route():
    return render_template("remove_user.html")

# @app.route("/remove_user", methods=["GET", "POST"])
# def remove_user_route():
#     # ดึงข้อมูลผู้ใช้จาก Oracle
#     query = "SELECT DESCRIPTION, USER_NAME, USER_LEVEL, USER_ENABLE FROM AMR_USER_TESTS"
#     user_data = fetch_data(query)

#     if not user_data:
#         flash("Users not found!", "error")
#         return redirect(url_for("remove_user.html"))

#     # ถ้ามีการส่งค่า POST (คือการเปลี่ยนสถานะการเข้าสู่ระบบของผู้ใช้)
#     if request.method == "POST":
#         # ดึงข้อมูลจากฟอร์มเปลี่ยนสถานะการเข้าสู่ระบบของผู้ใช้
#         new_status = request.form.get("status")
#         user_name = request.form.get("user_name")  # ดึง user_name จากฟอร์ม

#         # ตรวจสอบว่าสถานะที่เลือกถูกต้อง
#         if new_status not in ["active", "inactive"]:
#             flash("Invalid status selected.", "error")
#             return redirect(url_for("remove_user"))

#         # แปลงสถานะเป็นเลข (0 หรือ 1) ที่จะบันทึกลงในฐานข้อมูล Oracle
#         status_mapping = {"active": 1, "inactive": 0}
#         new_status_numeric = status_mapping[new_status]

#         # สร้างคำสั่ง SQL สำหรับการอัปเดตสถานะการเข้าสู่ระบบของผู้ใช้
#         update_query = "UPDATE AMR_USER_TESTS SET USER_ENABLE = :1 WHERE USER_NAME = :2"
#         update_params = (new_status_numeric, user_name)

#         # ทำการ execute คำสั่ง SQL และ commit การอัปเดตสถานะการเข้าสู่ระบบของผู้ใช้
#         if execute_query(update_query, update_params):
#             flash("User status updated successfully!", "success")
#             return redirect(url_for("remove_user.html"))
#         else:
#             flash("Failed to update user status. Please try again.", "error")

#     # กรณีไม่ใช่การส่งค่า POST ให้ส่งข้อมูลผู้ใช้ไปยัง HTML template หรือทำอย่างอื่นตามที่ต้องการ
#     return render_template("remove_user.html", user_data=user_data)


# ############   /remove_user ###################


############  View Billing Data   #####################


@app.route("/get_tags", methods=["GET"])
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

        tag_results = fetch_data(amr_connection,tag_query, params={"region_id": selected_region})
        tag_options = [str(tag[0]) for tag in tag_results]
        tag_options.sort()
        return jsonify({"tag_options": tag_options})


@app.route("/billing_data")
def billing_data():
    print("Active Connection:", active_connection)
    with connect_to_amr_db() as amr_connection:
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
        region_results = fetch_data(amr_connection,region_query)
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
                AMR_BILLING_DATA.DATA_DATE,
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
                AMR_CONFIGURED_DATA.DATA_DATE,
                
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
        region_results = fetch_data(amr_connection,region_query)
        region_options = [str(region[0]) for region in region_results]

        # Fetch tag options based on the selected region
        tag_results = fetch_data(amr_connection,tag_query, params={"region_id": selected_region})
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
            results = fetch_data(amr_connection,query)

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
                selected_meter_id = df["METER_ID"].iloc[0]

                # Now, remove the "METER_ID" column from the DataFrame
                df = df.drop(["PL_REGION_ID", "TAG_ID", "METER_ID"], axis=1)

                # Continue with the rest of your DataFrame processing
                df["DATA_DATE"] = pd.to_datetime(df["DATA_DATE"])
                df = df.sort_values(by="DATA_DATE")
                df = df.drop_duplicates(subset=["DATA_DATE", "METER_STREAM_NO"], keep="first")
                df = df.apply(lambda x: x.str.replace("\n", "") if x.dtype == "object" else x)

                # Assuming 'df' is the DataFrame created from the query results
                df_run1 = df[df['METER_STREAM_NO'] == '1']
                df_run2 = df[df['METER_STREAM_NO'] == '2']
                df_run3 = df[df['METER_STREAM_NO'] == '3']
                df_run4 = df[df['METER_STREAM_NO'] == '4']
                df_run5 = df[df['METER_STREAM_NO'] == '5']
                df_run6 = df[df['METER_STREAM_NO'] == '6']

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

                if not df_run1.empty:
                    df_run1 = df_run1.drop('METER_STREAM_NO', axis=1, errors='ignore')
                    tables["daily_data_run1"] = df_run1.to_html(classes="data", index=False)

                if not df_run2.empty:
                    df_run2 = df_run2.drop('METER_STREAM_NO', axis=1, errors='ignore')
                    tables["daily_data_run2"] = df_run2.to_html(classes="data", index=False)

                if not df_run3.empty:
                    df_run3 = df_run3.drop('METER_STREAM_NO', axis=1, errors='ignore')
                    tables["daily_data_run3"] = df_run3.to_html(classes="data", index=False)

                if not df_run4.empty:
                    df_run4 = df_run4.drop('METER_STREAM_NO', axis=1, errors='ignore')
                    tables["daily_data_run4"] = df_run4.to_html(classes="data", index=False)

                if not df_run5.empty:
                    df_run5 = df_run5.drop('METER_STREAM_NO', axis=1, errors='ignore')
                    tables["daily_data_run5"] = df_run5.to_html(classes="data", index=False)

                if not df_run6.empty:
                    df_run6 = df_run6.drop('METER_STREAM_NO', axis=1, errors='ignore')
                    tables["daily_data_run6"] = df_run6.to_html(classes="data", index=False)

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

                print(df.columns)
                # Get the selected Meter ID before removing it from the DataFrame
                selected_meter_id = df["METER_ID"].iloc[0]

                # Now, remove the "METER_ID" column from the DataFrame
                df = df.drop(["PL_REGION_ID", "TAG_ID", "METER_ID"], axis=1)

                # Remove newline characters
                df = df.apply(
                    lambda x: x.str.replace("\n", "") if x.dtype == "object" else x
                )
                df["DATA_DATE"] = pd.to_datetime(df["DATA_DATE"])

                df = df.drop_duplicates(subset=["DATA_DATE", "METER_STREAM_NO"], keep="first")
                # Sort DataFrame by 'DATA_DATE'
                df = df.sort_values(by="DATA_DATE")
                # Send the DataFrame to the HTML template
                df_run1 = df[df['METER_STREAM_NO'] == '1']
                df_run2 = df[df['METER_STREAM_NO'] == '2']
                df_run3 = df[df['METER_STREAM_NO'] == '3']
                df_run4 = df[df['METER_STREAM_NO'] == '4']
                df_run5 = df[df['METER_STREAM_NO'] == '5']
                df_run6 = df[df['METER_STREAM_NO'] == '6']

                # Check if each DataFrame has data before including in the tables dictionary
                tables = {
                    "daily_data": None,
                    
                }

                common_table_properties = {"classes": "data", "index": False,"header":None}

                if not df_run1.empty:
                    df_run1 = df_run1.drop('METER_STREAM_NO', axis=1, errors='ignore')
                    tables["config_data_run1"] = df_run1.to_html(**common_table_properties)
                if not df_run2.empty:
                    df_run2 = df_run2.drop('METER_STREAM_NO', axis=1, errors='ignore')
                    tables["config_data_run2"] = df_run2.to_html(**common_table_properties)
                if not df_run3.empty:
                    df_run3 = df_run3.drop('METER_STREAM_NO', axis=1, errors='ignore')
                    tables["config_data_run3"] = df_run3.to_html(**common_table_properties)
                if not df_run4.empty:
                    df_run4 = df_run4.drop('METER_STREAM_NO', axis=1, errors='ignore')
                    tables["config_data_run4"] = df_run4.to_html(**common_table_properties)
                if not df_run5.empty:
                    df_run5 = df_run5.drop('METER_STREAM_NO', axis=1, errors='ignore')
                    tables["config_data_run5"] = df_run4.to_html(**common_table_properties)
                if not df_run6.empty:
                    df_run6 = df_run6.drop('METER_STREAM_NO', axis=1, errors='ignore')
                    tables["config_data_run6"] = df_run4.to_html(**common_table_properties)
                return render_template(
                    "billingdata.html",
                    
                    tables=tables,
                    titles=df.columns.values,
                    selected_date=selected_date,
                    selected_tag=selected_tag,
                    selected_region=selected_region,
                    region_options=region_options,
                    tag_options=tag_options, dropped_columns_data=dropped_columns_data,
                    selected_meter_id=selected_meter_id,
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
                tables={},
            )


############ / View Billing Data  #####################


############ Daily summary #####################
@app.route("/Daily_summary")
def Daily_summary():
    with connect_to_amr_db() as amr_connection:
        print("Active Connection:", active_connection)
        # SQL query to fetch unique PL_REGION_ID values
        region_query = """
        SELECT * FROM AMR_REGION 
        """

        # Fetch unique region values
        region_results = fetch_data(amr_connection,region_query)
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
            results = fetch_data(amr_connection,query)

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
    with connect_to_amr_db() as amr_connection:
        print("Active Connection:", active_connection)
        # SQL query to fetch unique PL_REGION_ID values
        region_query = """
        SELECT * FROM AMR_REGION 
        """

        # Fetch unique region values
        region_results = fetch_data(amr_connection,region_query)
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
        region_results = fetch_data(amr_connection,region_query)
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
            results = fetch_data(amr_connection,query)

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
    with connect_to_amr_db() as amr_connection:
        print("Active Connection:", active_connection)
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
    with connect_to_amr_db() as amr_connection:
        print("Active Connection:", active_connection)
        query = "SELECT DESCRIPTION FROM AMR_ADDRESS_MAPPING1 WHERE ADDRESS = :address"
        params = {"address": address}
        result = fetch_data(amr_connection,query, params)
        return result[0][0] if result else None


@app.route("/process_selected_rows", methods=["POST"])
def process_selected_rows():
    selected_rows = request.form.getlist("selected_rows")
    return "Selected rows processed successfully"


def get_type_value_from_database(address):
    with connect_to_amr_db() as amr_connection:
        print("Active Connection:", active_connection)
        query = "SELECT TYPE_VALUE FROM AMR_ADDRESS_MAPPING1 WHERE ADDRESS = :address"
        result = fetch_data(amr_connection,query, params={"address": address})
        if result:
            return result[0][0]  # Assuming TYPE_VALUE is the first column in the result
        return None


############ /Manualpoll_data  #####################
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login.html"))


###############################################








@app.route("/billing_data_asgs")
def billing_data_asgs():
   
    with connect_to_ptt_pivot_db() as ptt_pivot_connection:
        print("Active Connection:", active_connection)
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
        region_results = fetch_data(ptt_pivot_connection,region_query)

        # Define your Oracle query to fetch tag_id based on the selected REGION_NAME
        tag_query = """
        SELECT DISTINCT tag_id
        FROM VW_ASGS_AMR_BILLING_DATA
        WHERE REGION_NAME = :selected_region
        ORDER BY tag_id
        """
        # Fetch tag_id data using your fetch_data function
        tag_results = fetch_data(ptt_pivot_connection, tag_query, {'selected_region': selected_region})

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
        

        results = fetch_data(ptt_pivot_connection, billing_query, {'selected_region': selected_region, 'selected_tag': selected_tag, 'selected_month_year': selected_month_year})
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
    with connect_to_ptt_pivot_db() as ptt_pivot_connection:
        print("Active Connection:", active_connection)
    region_name = request.args.get('region')

    # Use the selected REGION_NAME to fetch associated tag_id values
    tag_query = """
    SELECT DISTINCT tag_id
    FROM VW_ASGS_AMR_BILLING_DATA
    WHERE REGION_NAME = :region_name
    ORDER BY tag_id
    """
    tag_results = fetch_data(ptt_pivot_connection,tag_query, {'region_name': region_name})

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
   
    with connect_to_ptt_pivot_db() as ptt_pivot_connection:
        print("Active Connection:", active_connection)
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
        region_results1 = fetch_data(ptt_pivot_connection,region_query)

        # Define your Oracle query to fetch tag_id based on the selected REGION_NAME
        tag_query = """
        SELECT DISTINCT tag_id
        FROM VW_AMR_BILLING_DATA
        WHERE REGION_NAME = :selected_region1
        ORDER BY tag_id
        """
        # Fetch tag_id data using your fetch_data function
        tag_results = fetch_data(ptt_pivot_connection, tag_query, {'selected_region1': selected_region1})
        
        
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
        results = fetch_data(ptt_pivot_connection, billing_query, {'selected_region1': selected_region1, 'selected_tag': selected_tag, 'selected_month_year': selected_month_year})
        
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
    with connect_to_ptt_pivot_db() as ptt_pivot_connection:
        print("Active Connection:", active_connection)
        region_name = request.args.get('region')

        # Use the selected REGION_NAME to fetch associated tag_id values
        tag_query = """
        SELECT DISTINCT tag_id
        FROM VW_AMR_BILLING_DATA
        WHERE REGION_NAME = :region_name
        ORDER BY tag_id
        """
        tag = fetch_data(ptt_pivot_connection, tag_query, {'region_name': region_name})

        # Return the tag_id values as JSON
        return jsonify(tag)
# @app.route("/get_tags", methods=["GET"])
# def get_tags():
#     with connect_to_ptt_pivot_db() as ptt_pivot_connection:
#         print("Active Connection:", active_connection)
#         selected_region = request.args.get("selected_region")

#         tag_query = """
#                 SELECT DISTINCT TAG_ID
#                 FROM AMR_FIELD_ID, AMR_PL_GROUP
#                 WHERE AMR_FIELD_ID.FIELD_ID = AMR_PL_GROUP.FIELD_ID
#                 AND AMR_PL_GROUP.PL_REGION_ID = :region_id
#             """

#         tag_results = fetch_data(ptt_pivot_connection,tag_query, params={"region_id": selected_region})
#         tag_options = [str(tag[0]) for tag in tag_results]
#         tag_options.sort()
#         return jsonify({"tag_options": tag_options})
    

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
def update_sql(connection, sql_statement):
    with connection.cursor() as cursor:
        
        cursor.execute(sql_statement)
    connection.commit()

def insert_address_range_to_oracle(
    connection, poll_config, poll_billing, enable_config, enable_billing, evc_type
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

        cursor.execute(ptt_pivot_connection, sql_insert, data_to_insert)

    connection.commit()



@app.route("/polling_route")
def polling_route():
    with connect_to_ptt_pivot_db() as ptt_pivot_connection:
        print("Active Connection:", active_connection)
        # Fetch type options for the dropdown
        type_query = "SELECT VC_NAME FROM AMR_VC_TYPE ORDER BY VC_NAME"
        type_results = fetch_data(ptt_pivot_connection,type_query)
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
            print("Query : ", query)
            # Fetch data using the modified query
            results = fetch_data(ptt_pivot_connection,query)
            # print(results)

            columns = [
                "evc_type",
                "poll_config",
                "poll_billing",
                "poll_config_enable",
                "poll_billing_enable",
            ]
            df = pd.DataFrame(results, columns=columns)

            print(results)
            poll_config_list = df.get(["poll_config"]).values.tolist()
            list_config = str(poll_config_list[0]).strip("[]'").split(",")
            
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
    with connect_to_ptt_pivot_db() as ptt_pivot_connection:
        print("Active Connection:", active_connection)
        selected_type = request.form.get("selected_type")

        type_id_query = f"SELECT ID FROM AMR_VC_TYPE WHERE VC_NAME LIKE '{selected_type}'"
        results = fetch_data(ptt_pivot_connection,type_id_query)
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
        print("Update Query:", update_query)
        
        update_sql(ptt_pivot_connection, update_query)
        # with connection.cursor() as cursor:
        
        #     cursor.execute(update_query)
        # connection.commit()
        # After updating the data, you may redirect to the polling route or perform any other necessary actions
    
    return redirect("/polling_route")

@app.route("/add_polling_route")
def add_polling_route():
    return render_template("add_polling.html")

MAX_ADDRESS_LENGTH = 249

@app.route("/save_to_oracle", methods=["POST"])
def save_to_oracle():
    with connect_to_ptt_pivot_db() as ptt_pivot_connection:
        print("Active Connection:", active_connection)
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
    with connect_to_ptt_pivot_db() as ptt_pivot_connection:
        print("Active Connection:", active_connection)
        # SQL query to fetch options for the dropdown
        type_query = "SELECT VC_NAME FROM AMR_VC_TYPE ORDER BY VC_NAME"
        type_results = fetch_data(ptt_pivot_connection,type_query)
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
            results = fetch_data(ptt_pivot_connection,query)

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
    with connect_to_ptt_pivot_db() as ptt_pivot_connection:
        print("Active Connection:", active_connection)
        selected_type = request.form.get('selected_type')

        # Fetch type_id from the database
        type_id_query = f"SELECT ID FROM AMR_VC_TYPE WHERE VC_NAME LIKE '{selected_type}'"
        results = fetch_data(ptt_pivot_connection,type_id_query)
        type_id = str(results[0]).strip("',()")
        print("type:", type_id)

        description_VC_TYPE = []
        
        for j in range(0, 20):  # Start from 1 and end at 20
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
            
            # if description_value == "None":
            #     description_value = ""
            
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
            update_sql(ptt_pivot_connection, update_query)
            
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
        
        update_sql(ptt_pivot_connection, update_vc_info_query)
        print(update_vc_info_query)

        return redirect("/mapping_config")


@app.route('/mapping_billing')  
def mapping_billing_route():
    with connect_to_ptt_pivot_db() as ptt_pivot_connection:
        print("Active Connection:", active_connection)
        # SQL query to fetch options for the dropdown
        type_query = "SELECT VC_NAME FROM AMR_VC_TYPE ORDER BY VC_NAME"
        type_results = fetch_data(ptt_pivot_connection,type_query)
        type_options = [str(type[0]) for type in type_results]

        # SQL query to fetch data based on selected type
        base_query = """
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
        """

        selected_type = request.args.get("type_dropdown") or ""
        if selected_type:
            type_id_query = "SELECT ID FROM AMR_VC_TYPE WHERE VC_NAME LIKE :1"
            results = fetch_data(ptt_pivot_connection,type_id_query, (selected_type,))
            
            interval = request.args.get("interval") or "10"
            
            if results:
                type_id = str(results[0][0])

                query = base_query
                results = fetch_data(ptt_pivot_connection,query, (selected_type,))
                
                print("type:", type_id)
                max_daily_query = "SELECT MAX(daily) FROM amr_mapping_billing WHERE evc_type LIKE :1"
                max_daily_result = fetch_data(ptt_pivot_connection,max_daily_query, (type_id,))
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
                print("dd", df)
                
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
    with connect_to_ptt_pivot_db() as ptt_pivot_connection:
        print("Active Connection:", active_connection)
        type_name_value = ["Time Stamp","Converted Index (VbA)","Unconverted Index (VmA)","Pressure Daily Average","Temperature Daily Average"]
        unit_type_name_value = ["Ulong","Ulong","Ulong","float","float"]
        selected_type = request.form.get('selected_type')

        # Fetch type_id from the database
        type_id_query = f"SELECT ID FROM AMR_VC_TYPE WHERE VC_NAME = '{selected_type}'"
        results = fetch_data(ptt_pivot_connection,type_id_query)
        type_id = str(results[0]).strip("',()")
        
        max_daily_query = "SELECT MAX(daily),MAX(id),MAX(address),MAX(or_der)  FROM amr_mapping_billing  WHERE evc_type = {}".format(type_id)
        max_daily_result = fetch_data(ptt_pivot_connection,max_daily_query)
        current_id = 0
        current_address = 0
        current_order = 0
        for row in max_daily_result:
            if len(row) >= 3:
                max_daily_value = int(row[0])
                current_id = int(row[1])   
                current_address = int(row[2]) 
                current_order = int(row[3])
                
        if current_id == 0 or current_address == 0 or current_order == 0:
            return redirect('/') # TODO : handler an errors and alert it.
        
        
        max_daily_new = int(request.form.get('max_day'))
        
        interval = request.args.get("interval") or "10"
        if  max_daily_new <= max_daily_value :
            # Delete excess rows from max_daily_new + 1 to max_daily_value
            for i in range(max_daily_value, max_daily_new, -1):
                delete_query = f"""
                DELETE FROM AMR_MAPPING_BILLING
                WHERE evc_type = '{type_id}' AND DAILY = {i}
                """
                update_sql(ptt_pivot_connection, delete_query)

        elif max_daily_new > max_daily_value:
            # Update existing rows from 1 to max_daily_value
            for i in range(max_daily_new - max_daily_value):
                for x,y in zip(type_name_value,unit_type_name_value):
                    # Adjust the values as needed from your form input or other sources
                    new_address = current_address = current_address + 2
                    new_description = x
                    new_data_type = y
                    new_evc_type = type_id
                    new_or_der = current_order = current_order + 1
                    new_daily = i + 1 + max_daily_value
                
                    insert_query = f"""
                    INSERT INTO AMR_MAPPING_BILLING (ADDRESS, DESCRIPTION, DATA_TYPE, evc_type, OR_DER, DAILY)
                    VALUES ('{new_address}', '{new_description}', '{new_data_type}',  '{new_evc_type}', '{new_or_der}', '{new_daily}')
                    """

                    update_sql(ptt_pivot_connection, insert_query)
                    # print(insert_query)
        
        # Update SQL query based on your table structure
        for i in range(0, 5): 
            i = f"{i:02d}"
            address_key = f"list_address{i}"
            description_key = f"list_description{i}"
            data_type_key = f"list_data_type{i}"
            evc_type_key = f"list_evc_type{i}"
            or_der_key = f"list_or_der{i}"
            daily_key = f"list_daily{i}"
                    
            address_value = request.form.get(address_key.strip("',()"))
            description_value = request.form.get(description_key.strip("',()"))
            data_type_value = request.form.get(data_type_key.strip("',()"))
            evc_type_value = request.form.get(evc_type_key.strip("',()"))
            or_der_value = request.form.get(or_der_key.strip("',()"))
            daily_value = request.form.get(daily_key.strip("',()"))
            # print("address:", address_value)
            
            # Update SQL query based on your table structure
            update_query = f"""
            UPDATE AMR_MAPPING_BILLING
            SET
                ADDRESS = '{address_value}',
                DESCRIPTION = '{description_value}',
                DATA_TYPE = '{data_type_value}',
                OR_DER = '{or_der_value}',
                DAILY = '{daily_value}'        
            WHERE evc_type = '{evc_type_value}' and or_der = '{or_der_value}'
        """

            update_sql(ptt_pivot_connection, update_query)
            print(update_query)

        return redirect("/mapping_billing")


@app.route("/add_mapping_route")
def add_mapping_route():
    return render_template("add_mapping.html")


@app.route("/submit_form", methods=["POST"])
def submit_form():
    cursor = None
    connection = None
    with connect_to_ptt_pivot_db() as ptt_pivot_connection:
        print("Active Connection:", active_connection)
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
    with connect_to_ptt_pivot_db() as ptt_pivot_connection:
        print("Active Connection:", active_connection)
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












@app.route("/homeasgs")
def homeasgs():
    return render_template("homeasgs.html")


@app.route("/login")
def login():
    return render_template("login.html")

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
