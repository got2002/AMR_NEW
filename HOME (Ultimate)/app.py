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

app = Flask(__name__)

# app.secret_key = "your_secret_key_here"

# Replace these values with your actual database credentials
communication_traffic = []
change_to_32bit_counter = 1  # Initialize the counter to 2


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

pool_min = 1
pool_max = 5
pool_inc = 1
pool_gmd = 0
connection_pool = cx_Oracle.SessionPool(
    user=username,
    password=password,
    dsn=cx_Oracle.makedsn(hostname, port, service_name),
    min=pool_min,
    max=pool_max,
    increment=pool_inc,
    getmode=pool_gmd
)


def fetch_data(query, params=None):
    try:
        # Acquire a connection from the pool
        connection = connection_pool.acquire()

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
    finally:
        # Release the connection back to the pool
        connection_pool.release(connection)


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
            df = df.drop_duplicates(
                subset=["DATA_DATE", "METER_STREAM_NO"], keep="first")
            df = df.apply(lambda x: x.str.replace("\n", "")
                        if x.dtype == "object" else x)

            # 
            fig_corrected = sp.make_subplots(
                rows=1, cols=1, subplot_titles=["Corrected"])
            fig_uncorrected = sp.make_subplots(
                rows=1, cols=1, subplot_titles=["Uncorrected"])
            fig_pressure = sp.make_subplots(
                rows=1, cols=1, subplot_titles=["Pressure"])
            fig_temperature = sp.make_subplots(
                rows=1, cols=1, subplot_titles=["Temperature"])

            # 
            df = df.sort_values(by="DATA_DATE", ascending=True)

            # 
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

            # 
            fig_corrected.add_trace(trace_corrected)
            fig_uncorrected.add_trace(trace_uncorrected)
            fig_pressure.add_trace(trace_pressure)
            fig_temperature.add_trace(trace_temperature)

            # 
            for fig in [fig_corrected, fig_uncorrected, fig_pressure, fig_temperature]:
                fig.update_traces(
                    line_shape="linear",
                    marker=dict(symbol="circle", size=6),
                    hoverinfo="text+x+y",  # 
                    hovertext=df["DATA_DATE"],  # 
                )
                fig.update_layout(
                    legend=dict(x=0.6, y=1.25, orientation="h"),
                    yaxis_title="Values",
                    xaxis_title="Date",
                    hovermode="x unified",
                    # 
                    yaxis=dict(type="linear", title="Values"),
                )
            fig.update_xaxes(title_text="Date", tickformat="%Y-%m-%d")

            # 
            for trace in fig.data:
                trace.marker.line.color = 'rgba(255,255,255,0)'
            #
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

                df_run1 = df_run1.drop(
                    'METER_STREAM_NO', axis=1, errors='ignore')
                tables["daily_data_run1"] = df_run1.to_html(
                    classes="data", index=False)

            if not df_run2.empty:

                df_run2 = df_run2.drop(
                    'METER_STREAM_NO', axis=1, errors='ignore')
                tables["daily_data_ran2"] = df_run2.to_html(
                    classes="data", index=False)

            if not df_run3.empty:

                df_run3 = df_run3.drop(
                    'METER_STREAM_NO', axis=1, errors='ignore')
                tables["daily_data_ran3"] = df_run3.to_html(
                    classes="data", index=False)

            if not df_run4.empty:

                df_run4 = df_run4.drop(
                    'METER_STREAM_NO', axis=1, errors='ignore')
                tables["daily_data_run4"] = df_run4.to_html(
                    classes="data", index=False)
            if not df_run5.empty:

                df_run4 = df_run5.drop(
                    'METER_STREAM_NO', axis=1, errors='ignore')
                tables["daily_data_run5"] = df_run5.to_html(
                    classes="data", index=False)
            if not df_run6.empty:

                df_run4 = df_run6.drop(
                    'METER_STREAM_NO', axis=1, errors='ignore')
                tables["daily_data_run6"] = df_run6.to_html(
                    classes="data", index=False)

            
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
            dropped_columns_data = dropped_columns_data.to_dict(
                orient="records")

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

            df = df.drop_duplicates(
                subset=["DATA_DATE", "METER_STREAM_NO"], keep="first")
            # Sort DataFrame by 'DATA_DATE'
            df = df.sort_values(by="DATA_DATE")

            # Send the DataFrame to the HTML template
            df_run1 = df[df['METER_STREAM_NO'] == '1']
            df_run2 = df[df['METER_STREAM_NO'] == '2']
            df_run3 = df[df['METER_STREAM_NO'] == '3']
            df_run4 = df[df['METER_STREAM_NO'] == '4']
            df_run5 = df[df['METER_STREAM_NO'] == '5']
            df_run6 = df[df['METER_STREAM_NO'] == '6']

            common_table_properties = {
                "classes": "data", "index": False, "header": None}

            if not df_run1.empty:
                df_run1 = df_run1.drop(
                    'METER_STREAM_NO', axis=1, errors='ignore')
                tables["config_data_run1"] = df_run1.to_html(
                    **common_table_properties)
            if not df_run2.empty:
                df_run2 = df_run2.drop(
                    'METER_STREAM_NO', axis=1, errors='ignore')
                tables["config_data_run2"] = df_run2.to_html(
                    **common_table_properties)
            if not df_run3.empty:
                df_run3 = df_run3.drop(
                    'METER_STREAM_NO', axis=1, errors='ignore')
                tables["config_data_run3"] = df_run3.to_html(
                    **common_table_properties)
            if not df_run4.empty:
                df_run4 = df_run4.drop(
                    'METER_STREAM_NO', axis=1, errors='ignore')
                tables["config_data_run4"] = df_run4.to_html(
                    **common_table_properties)
            if not df_run5.empty:
                df_run5 = df_run5.drop(
                    'METER_STREAM_NO', axis=1, errors='ignore')
                tables["config_data_run5"] = df_run5.to_html(
                    **common_table_properties)
            if not df_run6.empty:
                df_run6 = df_run6.drop(
                    'METER_STREAM_NO', axis=1, errors='ignore')
                tables["config_data_run6"] = df_run6.to_html(
                    **common_table_properties)

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


@app.route("/add_mapping_route")
def add_mapping_route():
    return render_template("add_mapping.html")


@app.route("/add_actraris_route")
def add_actraris_route():
    return render_template("add_actraris.html")


####################################################


if __name__ == "__main__":
    app.run(debug=True)
