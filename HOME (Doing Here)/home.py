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

def execute_query(query, params=None):
    try:
        dsn = cx_Oracle.makedsn(hostname, port, service_name)
        with cx_Oracle.connect(username, password, dsn) as connection:
            with connection.cursor() as cursor:
                if params:
                    cursor.execute(query, params)
                else:
                    cursor.execute(query)
                connection.commit()
        return True
    except cx_Oracle.Error as e:
        (error,) = e.args
        print("Oracle Error:", error)
        return False
############  /connect database  #####################
############  Home page  #####################
@app.route("/")
def home():
    return render_template("home.html")
############ / Home page  #####################
############  Add User  #####################
@app.route("/add_user", methods=["GET", "POST"])
def add_user_route():
    if request.method == "POST":
        description = request.form["description"]
        user_name = request.form["user_name"]
        password = request.form["password"]
        user_level = request.form["user_level"]
        # เข้ารหัสรหัสผ่านโดยใช้ MD5
        hashed_password = md5_hash(password)
        # แปลงเป็น RAWTOHEX ก่อนที่จะบันทึกลงใน Oracle
        hashed_password_hex = "RAWTOHEX(DBMS_OBFUSCATION_TOOLKIT.MD5(input_string => UTL_I18N.STRING_TO_RAW('{}', 'AL32UTF8')))".format(
            hashed_password
        )
        query = "INSERT INTO AMR_USER_TESTS (description, user_name, password, user_level) VALUES (:1, :2, {}, :4)".format(
            hashed_password_hex
        )
        params = (description, user_name, user_level)
        if execute_query(query, params):
            flash("User added successfully!", "success")
            return render_template("add_user.html")
        else:
            flash("Failed to add user. Please try again.", "error")
    return render_template("add_user.html")
############  /Add User  #####################
############  edit_user   #####################
def get_data(filter_text=None, sort_column=None):
    try:
        connection = cx_Oracle.connect(
            user=username, password=password, dsn=f"{hostname}:{port}/{service_name}"
        )
        cursor = connection.cursor()
        # Base query
        query = (
            "SELECT description, USER_NAME, PASSWORD, USER_LEVEL FROM AMR_User_tests"
        )
        # Apply filtering
        if filter_text:
            query += f" WHERE USER_NAME LIKE '%{filter_text}%'"
        # Apply sorting
        if sort_column:
            query += f" ORDER BY {sort_column}"
        cursor.execute(query)
        # Fetch data in chunks (e.g., 100 rows at a time)
        chunk_size = 100
        data = []
        while True:
            rows = cursor.fetchmany(chunk_size)
            if not rows:
                break
            data.extend(
                [
                    {
                        "description": row[0],
                        "user_name": row[1],
                        "password": row[2],
                        "user_level": row[3],
                    }
                    for row in rows
                ]
            )
        return data
    except cx_Oracle.Error as e:
        (error,) = e.args
        print("Oracle Error:", error)
        return []
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()
# Example usage with filtering and sorting
filter_text = "example"  # Replace with your filter text or None for no filtering
sort_column = "USER_NAME"  # Replace with your desired column or None for no sorting
filtered_and_sorted_data = get_data(filter_text=filter_text, sort_column=sort_column)
@app.route("/get_data")
def get_data_route():
    data = get_data()
    return jsonify(data)
@app.route("/edit_user", methods=["GET", "POST"])
def edit_user_route():
    # ดึงข้อมูลผู้ใช้จากฐานข้อมูล
    query = "SELECT DESCRIPTION, USER_NAME, PASSWORD, USER_LEVEL FROM AMR_User_tests"
    user_data = fetch_data(query)
    if not user_data:
        flash("User not found!", "error")
        return render_template("edit_user.html")
    # ถ้ามีการส่งค่า POST (คือการบันทึกการแก้ไข)
    if request.method == "POST":
        # ดึงข้อมูลจากฟอร์มแก้ไข
        description = request.form["description"]
        user_name = request.form["user_name"]
        password = request.form["password"]
        # user_level = request.form["user_level"]
        # เข้ารหัสรหัสผ่านโดยใช้ MD5
        hashed_password = md5_hash(password)
        # สร้างคำสั่ง SQL สำหรับการแก้ไขข้อมูลผู้ใช้
        update_query = "UPDATE AMR_USER_TESTS SET description = :1, user_name = :2, password = :3 WHERE description = :4"
        update_params = (description, user_name, hashed_password, description)
        # ทำการ execute คำสั่ง SQL และ commit การแก้ไข user_name
        if execute_query(update_query, update_params):
            flash("User updated successfully!", "success")
            return render_template("edit_user.html")
        else:
            flash("Failed to update user. Please try again.", "error")
    # กรณีไม่ใช่การส่งค่า POST ให้ส่งข้อมูลผู้ใช้ไปยัง HTML template หรือทำอย่างอื่นตามที่ต้องการ
    return render_template("edit_user.html", user_data=user_data)
############  /edit_user   #####################
############   /remove_user ###################
@app.route("/remove_user", methods=["GET", "POST"])
def remove_user_route():
    # ดึงข้อมูลผู้ใช้จาก Oracle
    query = "SELECT DESCRIPTION, USER_NAME, USER_LEVEL, USER_ENABLE FROM AMR_USER_TESTS"
    user_data = fetch_data(query)
    if not user_data:
        flash("Users not found!", "error")
        return redirect(url_for("remove_user.html"))
    # ถ้ามีการส่งค่า POST (คือการเปลี่ยนสถานะการเข้าสู่ระบบของผู้ใช้)
    if request.method == "POST":
        # ดึงข้อมูลจากฟอร์มเปลี่ยนสถานะการเข้าสู่ระบบของผู้ใช้
        new_status = request.form.get("status")
        user_name = request.form.get("user_name")  # ดึง user_name จากฟอร์ม
        # ตรวจสอบว่าสถานะที่เลือกถูกต้อง
        if new_status not in ["active", "inactive"]:
            flash("Invalid status selected.", "error")
            return redirect(url_for("remove_user"))
        # แปลงสถานะเป็นเลข (0 หรือ 1) ที่จะบันทึกลงในฐานข้อมูล Oracle
        status_mapping = {"active": 1, "inactive": 0}
        new_status_numeric = status_mapping[new_status]
        # สร้างคำสั่ง SQL สำหรับการอัปเดตสถานะการเข้าสู่ระบบของผู้ใช้
        update_query = "UPDATE AMR_USER_TESTS SET USER_ENABLE = :1 WHERE USER_NAME = :2"
        update_params = (new_status_numeric, user_name)
        # ทำการ execute คำสั่ง SQL และ commit การอัปเดตสถานะการเข้าสู่ระบบของผู้ใช้
        if execute_query(update_query, update_params):
            flash("User status updated successfully!", "success")
            return redirect(url_for("remove_user.html"))
        else:
            flash("Failed to update user status. Please try again.", "error")
    # กรณีไม่ใช่การส่งค่า POST ให้ส่งข้อมูลผู้ใช้ไปยัง HTML template หรือทำอย่างอื่นตามที่ต้องการ
    return render_template("remove_user.html", user_data=user_data)
############   /remove_user ###################
############  View Billing Data   #############
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
    selected_meter_id = None  # or any default value
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
            selected_meter_id = df["METER_ID"].iloc[0]
            # Now, remove the "METER_ID" column from the DataFrame
            df = df.drop(["PL_REGION_ID", "TAG_ID", "METER_ID"], axis=1)
            # Continue with the rest of your DataFrame processing
            df["DATA_DATE"] = pd.to_datetime(df["DATA_DATE"])
            df = df.sort_values(by="DATA_DATE")
            df = df.drop_duplicates(subset=["DATA_DATE", "METER_STREAM_NO"], keep="first")
            df = df.apply(lambda x: x.str.replace("\n", "") if x.dtype == "object" else x)
            # สร้าง subplot และ traces สำหรับแต่ละกราฟ
            fig_corrected = sp.make_subplots(rows=1, cols=1, subplot_titles=["Corrected"])
            fig_uncorrected = sp.make_subplots(rows=1, cols=1, subplot_titles=["Uncorrected"])
            fig_pressure = sp.make_subplots(rows=1, cols=1, subplot_titles=["Pressure"])
            fig_temperature = sp.make_subplots(rows=1, cols=1, subplot_titles=["Temperature"])
            # เรียงลำดับ DataFrame ตาม 'DATA_DATE'
            df = df.sort_values(by="DATA_DATE", ascending=True)
            # สร้าง traces สำหรับแต่ละกราฟ
            trace_corrected = go.Scatter(
                x=df["DATA_DATE"],
                y=df["CORRECTED"],
                mode="lines+markers",
                name="CORRECTED",
                line=dict(color="blue", width=2),
            )
            trace_uncorrected = go.Scatter(
                x=df["DATA_DATE"],
                y=df["UNCORRECTED"],
                mode="lines+markers",
                name="UNCORRECTED",
                line=dict(color="red", width=2),
            )
            trace_pressure = go.Scatter(
                x=df["DATA_DATE"],
                y=df["Pressure"],
                mode="lines+markers",
                name="Pressure",
                line=dict(color="orange", width=2),
            )
            trace_temperature = go.Scatter(
                x=df["DATA_DATE"],
                y=df["Temperature"],
                mode="lines+markers",
                name="Temperature",
                line=dict(color="green", width=2),
            )
            
            fig_corrected.add_trace(trace_corrected)
            fig_uncorrected.add_trace(trace_uncorrected)
            fig_pressure.add_trace(trace_pressure)
            fig_temperature.add_trace(trace_temperature)
            
            for fig in [fig_corrected, fig_uncorrected, fig_pressure, fig_temperature]:
                fig.update_traces(
                    line_shape="linear", 
                    marker=dict(symbol="circle", size=6),
                    hoverinfo="text+x+y",  
                    hovertext=df["DATA_DATE"],  
                )
                fig.update_layout(
                    legend=dict(x=0.6, y=1.25, orientation="h"),
                    yaxis_title="Values",
                    xaxis_title="Date",
                    hovermode="x unified",
                     
                    yaxis=dict(type="linear", title="Values"),
                )
            fig.update_xaxes(title_text="Date", tickformat="%Y-%m-%d")
            
            for trace in fig.data:
                trace.marker.line.color = 'rgba(255,255,255,0)'
           
            graph_corrected = fig_corrected.to_html(full_html=False)
            graph_uncorrected = fig_uncorrected.to_html(full_html=False)
            graph_pressure = fig_pressure.to_html(full_html=False)
            graph_temperature = fig_temperature.to_html(full_html=False)
            
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
            if not df_run1.empty:
               
                df_run1 = df_run1.drop('METER_STREAM_NO', axis=1, errors='ignore')
                tables["daily_data_run1"] = df_run1.to_html(classes="data", index=False)
            if not df_run2.empty:
               
                df_run2 = df_run2.drop('METER_STREAM_NO', axis=1, errors='ignore')
                tables["daily_data_ran2"] = df_run2.to_html(classes="data", index=False)
            if not df_run3.empty:
             
                df_run3 = df_run3.drop('METER_STREAM_NO', axis=1, errors='ignore')
                tables["daily_data_ran3"] = df_run3.to_html(classes="data", index=False)
            if not df_run4.empty:
               
                df_run4 = df_run4.drop('METER_STREAM_NO', axis=1, errors='ignore')
                tables["daily_data_run4"] = df_run4.to_html(classes="data", index=False)
            if not df_run5.empty:
               
                df_run4 = df_run5.drop('METER_STREAM_NO', axis=1, errors='ignore')
                tables["daily_data_run5"] = df_run5.to_html(classes="data", index=False)
            if not df_run6.empty:
               
                df_run4 = df_run6.drop('METER_STREAM_NO', axis=1, errors='ignore')
                tables["daily_data_run6"] = df_run6.to_html(classes="data", index=False)
            
            df = df.sort_values(by="DATA_DATE", ascending=True)
            
            return render_template(
                "billingdata.html",
                tables=tables,
                titles=df.columns.values,
                selected_date=selected_date,
                selected_tag=selected_tag,
                selected_region=selected_region,
                region_options=region_options,
                tag_options=tag_options,
                graph_corrected=graph_corrected,
                graph_uncorrected=graph_uncorrected,
                graph_pressure=graph_pressure,
                graph_temperature=graph_temperature,
                selected_meter_id=selected_meter_id,
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
           
            tables = {}
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
                tables["config_data_run5"] = df_run5.to_html(**common_table_properties)
            if not df_run6.empty:
                df_run6 = df_run6.drop('METER_STREAM_NO', axis=1, errors='ignore')
                tables["config_data_run6"] = df_run6.to_html(**common_table_properties)
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
            selected_meter_id=selected_meter_id,
            tables={},
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
    
    evc_type = int(request.form["evc_type"])
    
    run = int(request.form["run"])
    run = run
    METERID = str(request.form["METERID"])
   
    
    
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
   
    formatted_data = []
    evc_type = evc_type
    for i, value in enumerate(values_1):
        address = starting_address_1 + i * 2
        
       
        
        
        
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

                data_list_1.append(
                    {
                        "description": description,
                        "address": address,
                        "value": value,
                        "hex_value": hex_value,
                        "binary_value": binary_value,
                        "ulong_value": ulong_value,
                        "float_value": float_display_value,
                        "signed_value": signed_value,
                        "is_16bit": is_16bit_value,
                        "float_signed_value": signed_value,
                    }
                )
                
            #     print(data_list_1)
            # if i == len(values_1) - 1:
            #     for float_display_value in data_list_1:
            #             formatted_data.append(float_display_value['address'] )

            #     for item in formatted_data:
                    
            #         # print(item)
            #         test = get_address_test_from_database(evc_type,item)
                    # break
                    # print(test)
                    
                    # insert_data(formatted_data[1],run,evc_type,METERID)
                    
                    # type_value = type_value
                    # run = run
                    # evc_type = evc_type
                    # METERID = METERID
                   
                   
    for i, value in enumerate(values_2):
        
        address = starting_address_2 + i * 2
        type_value = get_type_value_from_database(address,evc_type)
        # print(address, ":" ,evc_type)
        
        if type_value is not None: 
            
            hex_value = hex(value)  
            binary_value = convert_to_binary_string(value, bytes_per_value)
            ulong_value = value 
            float_value = struct.unpack("!f", struct.pack("!I", value))[0]
            description = get_description_from_database(address)
            # print(description)
            if description is None:
                description = f"Address {address}"
                address += 0
                
            if is_16bit:
                
                signed_value = value - 2**16 if value >= 2**15 else value
                is_16bit_value = True
                float_value = value if is_16bit_value else float_value
                float_display_value = f"16-bit signed: {signed_value}, float: {float_value}, ulong: {ulong_value}"  
                
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
                )  
                
                if type_value == "Float":
                    
                    float_display_value = float_value
                    # print(float_display_value)
                elif type_value == "signed":
                    
                    float_display_value = signed_value
                    # print(float_display_value)
                elif type_value == "Ulong":
                    
                    float_display_value = ulong_value
                    # print(float_display_value)
                elif type_value == "Date": 
                   
                    date_value = datetime.datetime.fromtimestamp(value)
                  
                    float_display_value = date_value.strftime("%d-%b-%y")

                    # print(float_display_value)
                else:
                    # Handle other cases or set a default behavior
                    float_display_value = "Undefined"
                    # print(f"Type Value for address {address}: {type_value}")
            data_list_2.append(
                {
                    "description": description,
                    "address": address,
                    "value": value,
                    "hex_value": hex_value,
                    "binary_value": binary_value,
                    "ulong_value": ulong_value,  
                    "float_value": float_display_value,
                    "signed_value": signed_value,
                    "is_16bit": is_16bit_value,
                    "float_signed_value": signed_value,
                    
                }
            )
            if i == len(values_2) - 1:
                
                for float_display_value in data_list_2:
                    formatted_data.append(f"{float_display_value['float_value']}")
                
                
                for data in formatted_data:
                    run = run
                    evc_type = evc_type
                    METERID = METERID
                    
                    
                    break
                
                
        value, updated_address = handle_action_configuration(i, value, address)
    for i, value in enumerate(values_3):
        # print(address, ":" ,evc_type)
        address = starting_address_3 + i * 2
        type_value = get_type_value_from_database(address,evc_type)
        if type_value is not None: 
            
            hex_value = hex(value)  
            binary_value = convert_to_binary_string(value, bytes_per_value)
            ulong_value = value 
            float_value = struct.unpack("!f", struct.pack("!I", value))[0]
            description = get_description_from_database(address)
            # print(description)
            if description is None:
                description = f"Address {address}"
                address += 0
                
            if is_16bit:
                
                signed_value = value - 2**16 if value >= 2**15 else value
                is_16bit_value = True
                float_value = value if is_16bit_value else float_value
                float_display_value = f"16-bit signed: {signed_value}, float: {float_value}, ulong: {ulong_value}"  
                
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
                )  
                
                if type_value == "Float":
                    
                    float_display_value = float_value
                    # print(float_display_value)
                elif type_value == "signed":
                    
                    float_display_value = signed_value
                    # print(float_display_value)
                elif type_value == "Ulong":
                    
                    float_display_value = ulong_value
                    # print(float_display_value)
                elif type_value == "Date": 
                   
                    date_value = datetime.datetime.fromtimestamp(value)
                  
                    float_display_value = date_value.strftime("%d-%b-%y")

                    # print(float_display_value)
                else:
                    # Handle other cases or set a default behavior
                    float_display_value = "Undefined"
                    # print(f"Type Value for address {address}: {type_value}")
            data_list_3.append(
                {
                    "description": description,
                    "address": address,
                    "value": value,
                    "hex_value": hex_value,
                    "binary_value": binary_value,
                    "ulong_value": ulong_value,  
                    "float_value": float_display_value,
                    "signed_value": signed_value,
                    "is_16bit": is_16bit_value,
                    "float_signed_value": signed_value,
                    
                }
            )
            if i == len(values_3) - 1:
                
                for float_display_value in data_list_3:
                    formatted_data.append(f"{float_display_value['float_value']},{float_display_value['address']},{float_display_value['description']}")
                
                
                for data in formatted_data:
                    run = run
                    evc_type = evc_type
                    METERID = METERID
                      
                    
                    break
                
        
        value, updated_address = handle_action_configuration(i, value, address)
    for i, value in enumerate(values_4):
        
        address = starting_address_4 + i * 2
        type_value = get_type_value_from_database(address,evc_type)
        # print(address, ":" ,evc_type)
        if type_value is not None: 
            
            hex_value = hex(value)  
            binary_value = convert_to_binary_string(value, bytes_per_value)
            ulong_value = value 
            float_value = struct.unpack("!f", struct.pack("!I", value))[0]
            description = get_description_from_database(address)
            # print(description)
            if description is None:
                description = f"Address {address}"
                address += 0
                
            if is_16bit:
                
                signed_value = value - 2**16 if value >= 2**15 else value
                is_16bit_value = True
                float_value = value if is_16bit_value else float_value
                float_display_value = f"16-bit signed: {signed_value}, float: {float_value}, ulong: {ulong_value}"  
                
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
                )  
                
                if type_value == "Float":
                    
                    float_display_value = float_value
                    # print(float_display_value)
                elif type_value == "signed":
                    
                    float_display_value = signed_value
                    # print(float_display_value)
                elif type_value == "Ulong":
                    
                    float_display_value = ulong_value
                    # print(float_display_value)
                elif type_value == "Date": 
                   
                    date_value = datetime.datetime.fromtimestamp(value)
                  
                    float_display_value = date_value.strftime("%d-%b-%y")

                    # print(float_display_value)
                else:
                    # Handle other cases or set a default behavior
                    float_display_value = "Undefined"
                    # print(f"Type Value for address {address}: {type_value}")
            data_list_4.append(
                {
                    "description": description,
                    "address": address,
                    "value": value,
                    "hex_value": hex_value,
                    "binary_value": binary_value,
                    "ulong_value": ulong_value,  
                    "float_value": float_display_value,
                    "signed_value": signed_value,
                    "is_16bit": is_16bit_value,
                    "float_signed_value": signed_value,
                    
                }
            )
            if i == len(values_4) - 1:
                
                for float_display_value in data_list_4:
                    formatted_data.append(f"{float_display_value['float_value']}")
                
                
                for data in formatted_data:
                    run = run
                    evc_type = evc_type
                    METERID = METERID
                      
                   
                    break
        value, updated_address = handle_action_configuration(i, value, address)
    for i, value in enumerate(values_5):
        
        address = starting_address_5 + i * 2
        type_value = get_type_value_from_database(address,evc_type)
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
                float_value = value if is_16bit_value else float_value
                float_display_value = f"16-bit signed: {signed_value}, float: {float_value}, ulong: {ulong_value}"  
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
                    
                    
                    float_display_value = date_value_local.strftime("%d-%m-%Y")
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
                    "ulong_value": ulong_value,  # Add ulong value to data dictionary
                    "float_value": float_display_value,
                    "signed_value": signed_value,
                    "is_16bit": is_16bit_value,
                    "float_signed_value": signed_value,
                }
            )
            
            
    for i, value in enumerate(values_6):
        address = starting_address_6 + i * 2
        type_value = get_type_value_from_database_billing(address,evc_type)
        if type_value is not None:  # Check if type_value is not None
            hex_value = hex(value)  # Convert the decimal value to HEX
            binary_value = convert_to_binary_string(value, bytes_per_value)
            ulong_value = value  # Set ulong_value equal to value
            float_value = struct.unpack("!f", struct.pack("!I", value))[0]
            description = get_description_from_database_billing(address)
            if description is None:
                description = f"Address {address}"
                address += 0
            if is_16bit:
                signed_value = value - 2**16 if value >= 2**15 else value
                is_16bit_value = True
                float_value = value if is_16bit_value else float_value
                float_display_value = f"16-bit signed: {signed_value}, float: {float_value}, ulong: {ulong_value}"  
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
                    
                    
                    float_display_value = date_value_local.strftime("%d-%m-%Y")
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
                    "ulong_value": ulong_value,  # Add ulong value to data dictionary
                    "float_value": float_display_value,
                    "signed_value": signed_value,
                    "is_16bit": is_16bit_value,
                    "float_signed_value": signed_value,
                }
            )

        
            
            
    for i, value in enumerate(values_7):
        
            address = starting_address_7 + i * 2
            type_value = get_type_value_from_database_billing(address,evc_type)
            if type_value is not None:  # Check if type_value is not None
                hex_value = hex(value)  # Convert the decimal value to HEX
                binary_value = convert_to_binary_string(value, bytes_per_value)
                ulong_value = value  # Set ulong_value equal to value
                float_value = struct.unpack("!f", struct.pack("!I", value))[0]
                description = get_description_from_database_billing(address)
                if description is None:
                    description = f"Address {address}"
                    address += 0
                if is_16bit:
                    signed_value = value - 2**16 if value >= 2**15 else value
                    is_16bit_value = True
                    float_value = value if is_16bit_value else float_value
                    float_display_value = f"16-bit signed: {signed_value}, float: {float_value}, ulong: {ulong_value}"  # Add ulong to display
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
                    elif type_value == "Ulong":
                        # Set float_display_value to the ulong representation
                        float_display_value = ulong_value
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
                        "ulong_value": ulong_value,  # Add ulong value to data dictionary
                        "float_value": float_display_value,
                        "signed_value": signed_value,
                        "is_16bit": is_16bit_value,
                        "float_signed_value": signed_value,
                    }
                )
    for i, value in enumerate(values_8):
        
            address = starting_address_8 + i * 2
            type_value = get_type_value_from_database_billing(address,evc_type)
            if type_value is not None:  # Check if type_value is not None
                hex_value = hex(value)  # Convert the decimal value to HEX
                binary_value = convert_to_binary_string(value, bytes_per_value)
                ulong_value = value  # Set ulong_value equal to value
                float_value = struct.unpack("!f", struct.pack("!I", value))[0]
                description = get_description_from_database_billing(address)
                if description is None:
                    description = f"Address {address}"
                    address += 0
                if is_16bit:
                    signed_value = value - 2**16 if value >= 2**15 else value
                    is_16bit_value = True
                    float_value = value if is_16bit_value else float_value
                    float_display_value = f"16-bit signed: {signed_value}, float: {float_value}, ulong: {ulong_value}"  # Add ulong to display
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
                    elif type_value == "Ulong":
                        # Set float_display_value to the ulong representation
                        float_display_value = ulong_value
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
                        "ulong_value": ulong_value,  # Add ulong value to data dictionary
                        "float_value": float_display_value,
                        "signed_value": signed_value,
                        "is_16bit": is_16bit_value,
                        "float_signed_value": signed_value,
                    }
                )
            
    for i, value in enumerate(values_9):
        
            address = starting_address_9 + i * 2
            type_value = get_type_value_from_database_billing(address,evc_type)
            if type_value is not None:  # Check if type_value is not None
                hex_value = hex(value)  # Convert the decimal value to HEX
                binary_value = convert_to_binary_string(value, bytes_per_value)
                ulong_value = value  # Set ulong_value equal to value
                float_value = struct.unpack("!f", struct.pack("!I", value))[0]
                description = get_description_from_database_billing(address)
                if description is None:
                    description = f"Address {address}"
                    address += 0
                if is_16bit:
                    signed_value = value - 2**16 if value >= 2**15 else value
                    is_16bit_value = True
                    float_value = value if is_16bit_value else float_value
                    float_display_value = f"16-bit signed: {signed_value}, float: {float_value}, ulong: {ulong_value}"  # Add ulong to display
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
                    elif type_value == "Ulong":
                        # Set float_display_value to the ulong representation
                        float_display_value = ulong_value
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
                        "ulong_value": ulong_value,  # Add ulong value to data dictionary
                        "float_value": float_display_value,
                        "signed_value": signed_value,
                        "is_16bit": is_16bit_value,
                        "float_signed_value": signed_value,
                    }
                )
    for i, value in enumerate(values_10):
        
            address = starting_address_10 + i * 2
            type_value = get_type_value_from_database_billing(address,evc_type)
            if type_value is not None:  # Check if type_value is not None
                hex_value = hex(value)  # Convert the decimal value to HEX
                binary_value = convert_to_binary_string(value, bytes_per_value)
                ulong_value = value  # Set ulong_value equal to value
                float_value = struct.unpack("!f", struct.pack("!I", value))[0]
                description = get_description_from_database_billing(address)
                if description is None:
                    description = f"Address {address}"
                    address += 0
                if is_16bit:
                    signed_value = value - 2**16 if value >= 2**15 else value
                    is_16bit_value = True
                    float_value = value if is_16bit_value else float_value
                    float_display_value = f"16-bit signed: {signed_value}, float: {float_value}, ulong: {ulong_value}"  # Add ulong to display
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
                    elif type_value == "Ulong":
                        # Set float_display_value to the ulong representation
                        float_display_value = ulong_value
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
                        "ulong_value": ulong_value,  # Add ulong value to data dictionary
                        "float_value": float_display_value,
                        "signed_value": signed_value,
                        "is_16bit": is_16bit_value,
                        "float_signed_value": signed_value,
                    }
                )
    for i, value in enumerate(values_11):
        
            address = starting_address_11 + i * 2
            type_value = get_type_value_from_database_billing(address,evc_type)
            if type_value is not None:  # Check if type_value is not None
                hex_value = hex(value)  # Convert the decimal value to HEX
                binary_value = convert_to_binary_string(value, bytes_per_value)
                ulong_value = value  # Set ulong_value equal to value
                float_value = struct.unpack("!f", struct.pack("!I", value))[0]
                description = get_description_from_database_billing(address)
                if description is None:
                    description = f"Address {address}"
                    address += 0
                if is_16bit:
                    signed_value = value - 2**16 if value >= 2**15 else value
                    is_16bit_value = True
                    float_value = value if is_16bit_value else float_value
                    float_display_value = f"16-bit signed: {signed_value}, float: {float_value}, ulong: {ulong_value}"  # Add ulong to display
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
                    elif type_value == "Ulong":
                        # Set float_display_value to the ulong representation
                        float_display_value = ulong_value
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
                        "ulong_value": ulong_value,  # Add ulong value to data dictionary
                        "float_value": float_display_value,
                        "signed_value": signed_value,
                        "is_16bit": is_16bit_value,
                        "float_signed_value": signed_value,
                    }
                )
        
    for i, value in enumerate(values_12):
        
            address = starting_address_12 + i * 2
            type_value = get_type_value_from_database_billing(address,evc_type)
            if type_value is not None:  # Check if type_value is not None
                hex_value = hex(value)  # Convert the decimal value to HEX
                binary_value = convert_to_binary_string(value, bytes_per_value)
                ulong_value = value  # Set ulong_value equal to value
                float_value = struct.unpack("!f", struct.pack("!I", value))[0]
                description = get_description_from_database_billing(address)
                if description is None:
                    description = f"Address {address}"
                    address += 0
                if is_16bit:
                    signed_value = value - 2**16 if value >= 2**15 else value
                    is_16bit_value = True
                    float_value = value if is_16bit_value else float_value
                    float_display_value = f"16-bit signed: {signed_value}, float: {float_value}, ulong: {ulong_value}"  # Add ulong to display
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
                    elif type_value == "Ulong":
                        # Set float_display_value to the ulong representation
                        float_display_value = ulong_value
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
                        "ulong_value": ulong_value,  # Add ulong value to data dictionary
                        "float_value": float_display_value,
                        "signed_value": signed_value,
                        "is_16bit": is_16bit_value,
                        "float_signed_value": signed_value,
                    }
                )
    for i, value in enumerate(values_13):
        
            address = starting_address_13 + i * 2
            type_value = get_type_value_from_database_billing(address,evc_type)
            if type_value is not None:  # Check if type_value is not None
                hex_value = hex(value)  # Convert the decimal value to HEX
                binary_value = convert_to_binary_string(value, bytes_per_value)
                ulong_value = value  # Set ulong_value equal to value
                float_value = struct.unpack("!f", struct.pack("!I", value))[0]
                description = get_description_from_database_billing(address)
                if description is None:
                    description = f"Address {address}"
                    address += 0
                if is_16bit:
                    signed_value = value - 2**16 if value >= 2**15 else value
                    is_16bit_value = True
                    float_value = value if is_16bit_value else float_value
                    float_display_value = f"16-bit signed: {signed_value}, float: {float_value}, ulong: {ulong_value}"  # Add ulong to display
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
                    elif type_value == "Ulong":
                        # Set float_display_value to the ulong representation
                        float_display_value = ulong_value
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
                        "ulong_value": ulong_value,  # Add ulong value to data dictionary
                        "float_value": float_display_value,
                        "signed_value": signed_value,
                        "is_16bit": is_16bit_value,
                        "float_signed_value": signed_value,
                    }
                )
    for i, value in enumerate(values_14):
        
            address = starting_address_14 + i * 2
            type_value = get_type_value_from_database_billing(address,evc_type)
            if type_value is not None:  # Check if type_value is not None
                hex_value = hex(value)  # Convert the decimal value to HEX
                binary_value = convert_to_binary_string(value, bytes_per_value)
                ulong_value = value  # Set ulong_value equal to value
                float_value = struct.unpack("!f", struct.pack("!I", value))[0]
                description = get_description_from_database_billing(address)
                if description is None:
                    description = f"Address {address}"
                    address += 0
                if is_16bit:
                    signed_value = value - 2**16 if value >= 2**15 else value
                    is_16bit_value = True
                    float_value = value if is_16bit_value else float_value
                    float_display_value = f"16-bit signed: {signed_value}, float: {float_value}, ulong: {ulong_value}"  # Add ulong to display
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
                    elif type_value == "Ulong":
                        # Set float_display_value to the ulong representation
                        float_display_value = ulong_value
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
                        "ulong_value": ulong_value,  # Add ulong value to data dictionary
                        "float_value": float_display_value,
                        "signed_value": signed_value,
                        "is_16bit": is_16bit_value,
                        "float_signed_value": signed_value,
                    }
                )
    for i, value in enumerate(values_15):
        
            address = starting_address_15 + i * 2
            type_value = get_type_value_from_database_billing(address,evc_type)
            if type_value is not None:  # Check if type_value is not None
                hex_value = hex(value)  # Convert the decimal value to HEX
                binary_value = convert_to_binary_string(value, bytes_per_value)
                ulong_value = value  # Set ulong_value equal to value
                float_value = struct.unpack("!f", struct.pack("!I", value))[0]
                description = get_description_from_database_billing(address)
                if description is None:
                    description = f"Address {address}"
                    address += 0
                if is_16bit:
                    signed_value = value - 2**16 if value >= 2**15 else value
                    is_16bit_value = True
                    float_value = value if is_16bit_value else float_value
                    float_display_value = f"16-bit signed: {signed_value}, float: {float_value}, ulong: {ulong_value}"  # Add ulong to display
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
                    elif type_value == "Ulong":
                        # Set float_display_value to the ulong representation
                        float_display_value = ulong_value
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
                        "ulong_value": ulong_value,  # Add ulong value to data dictionary
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
        # print(poll_config_enable_list)
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
        df=df,METERID=METERID,
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


def get_address_from_database(evc_type, address):
    query = "SELECT address, or_der FROM AMR_MAPPING_CONFIG WHERE evc_type = :evc_type AND ADDRESS = :address  ORDER BY or_der "
    params = {"evc_type": evc_type, "address": address}
    
    result = fetch_data(query, params)
    
    return result[0][0] if result else None


def get_address_test_from_database(evc_type,item):
    query = "SELECT address FROM AMR_MAPPING_CONFIG WHERE evc_type = :evc_type  ORDER BY or_der "
    params = {"evc_type": evc_type}
    
    result = fetch_data(query, params)
    # print(result)
    for item in result:
        test = str(item)
        cleaned_test = test.replace(',', '').replace("'", "").replace("(", "").replace(")", "")
        # print(cleaned_test)

    return result[0][0] if result else None

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

        






############ /Manualpoll_data  #####################
@app.route("/logout")
def logout():
    # ล้าง session หรือทำงานอื่น ๆ ที่คุณต้องการเมื่อลงชื่อออก
    session.clear()
    # ส่งไปยังหน้าลงชื่อเข้าใช้หลังจากลงชื่อออก
    return redirect(url_for("login"))
###############################################
def insert_address_range_to_oracle(
    poll_config, poll_billing, enable_config, enable_billing, evc_type
):
    dsn = cx_Oracle.makedsn(hostname, port, service_name)
    with cx_Oracle.connect(
        user=username, password=password, dsn=dsn
    ) as connection:
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
            cursor.execute(sql_insert, data_to_insert)
        connection.commit()

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
        insert_address_range_to_oracle(
            combined_address_config,
            combined_address_billing,
            enable_config,
            enable_billing,
            evc_type,
        )
        response = {"status": "success", "message": "Data saved successfully"}
    except ValueError as ve:
        response = {"status": "error", "message": str(ve)}
    except cx_Oracle.DatabaseError as e:
        response = {"status": "error", "message": f"Database Error: {e}"}
    except Exception as e:
        response = {"status": "error", "message": f"Error: {e}"}
    return jsonify(response)
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
        dsn_tns = cx_Oracle.makedsn(
            hostname, port, service_name
        )
        connection = cx_Oracle.connect(
            user=username, password=password, dsn=dsn_tns
        )
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
        return "บันทึกข้อมูลสำเร็จ"
    except Exception as e:
        return f"เกิดข้อผิดพลาด: {str(e)}"
    finally:
        if cursor is not None:
            # ปิด cursor
            cursor.close()
        if connection is not None:
            # ปิด connection
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
        dsn_tns = cx_Oracle.makedsn(
            hostname, port, service_name
        )
        connection = cx_Oracle.connect(
            user=username, password=password, dsn=dsn_tns
        )
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
        return "บันทึกข้อมูลสำเร็จ"
    except Exception as e:
        return f"เกิดข้อผิดพลาด: {str(e)}"
    finally:
        if cursor is not None:
            # ปิด cursor
            cursor.close()
        if connection is not None:
            # ปิด connection
            connection.close()
####################################################
if __name__ == "__main__":
    app.run(debug=True)

