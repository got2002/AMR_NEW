from flask import Flask, render_template, request, jsonify
import pandas as pd
import cx_Oracle
from flask import flash
from datetime import datetime
import pandas as pd
import sqlite3
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
from wtforms import StringField, PasswordField, SubmitField, validators
from werkzeug.security import generate_password_hash
from sqlalchemy import desc
from flask import Flask, send_from_directory
from flask_migrate import Migrate

import cx_Oracle


app = Flask(__name__)

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
############  /connect database  #####################



############  Home page  #####################
@app.route("/")
def home():
    return render_template("home.html")
############ / Home page  #####################





############  View Billing Data   #####################

@app.route('/get_tags', methods=['GET'])
def get_tags():
    selected_region = request.args.get('selected_region')
    
    tag_query = """
    SELECT DISTINCT TAG_ID
    FROM AMR_FIELD_ID
    JOIN AMR_PL_GROUP ON AMR_FIELD_ID.FIELD_ID = AMR_PL_GROUP.FIELD_ID 
    WHERE AMR_PL_GROUP.PL_REGION_ID = :region_id
    """
    
    tag_results = fetch_data(tag_query, params={'region_id': selected_region})
    tag_options = [str(tag[0]) for tag in tag_results]
    tag_options.sort()
    return jsonify({'tag_options': tag_options})

@app.route('/billing_data')
def billing_data():
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

    # SQL query for main data
    query = """
    SELECT
        AMR_PL_GROUP.PL_REGION_ID,
        AMR_FIELD_ID.TAG_ID,
        amr_field_id.meter_id,
        AMR_BILLING_DATA.DATA_DATE as DATA_DATE,
        AMR_BILLING_DATA.CORRECTED_VOL as CORRECTED,
        AMR_BILLING_DATA.UNCORRECTED_VOL as UNCORRECTED,
        AMR_BILLING_DATA.AVR_PF as Pressure,
        AMR_BILLING_DATA.AVR_TF as Temperature
    FROM
        AMR_FIELD_ID, AMR_PL_group, AMR_BILLING_DATA
    WHERE
        AMR_PL_GROUP.FIELD_ID = AMR_FIELD_ID.FIELD_ID 
        AND AMR_BILLING_DATA.METER_ID = AMR_FIELD_ID.METER_ID
        AND AMR_BILLING_DATA.METER_STREAM_NO like '1'
        {date_condition}
        {tag_condition}
        {region_condition}
    """

    # Get selected values from the dropdowns
    date_condition = "AND AMR_BILLING_DATA.DATA_DATE IS NOT NULL"
    tag_condition = "AND AMR_FIELD_ID.TAG_ID IS NOT NULL"
    region_condition = "AND amr_pl_group.pl_region_id IS NOT NULL"
    
    selected_date = request.args.get('date_dropdown')
    selected_tag = request.args.get('tag_dropdown')
    selected_region = request.args.get('region_dropdown')

    # Fetch unique region values
    region_results = fetch_data(region_query)
    region_options = [str(region[0]) for region in region_results]

    # Fetch tag options based on the selected region
    tag_results = fetch_data(tag_query, params={'region_id': selected_region})
    tag_options = [str(tag[0]) for tag in tag_results]


    if selected_date:
        # ปรับ format ใน date_condition เพื่อให้ตรงกับรูปแบบที่ datepicker กำหนด
        date_condition = f"AND TO_CHAR(AMR_BILLING_DATA.DATA_DATE, 'MM/YYYY') = '{selected_date}'"

    if selected_tag:
        tag_condition = f"AND AMR_FIELD_ID.TAG_ID = '{selected_tag}'"
    if selected_region:
        region_condition = f"AND amr_pl_group.pl_region_id = '{selected_region}'"
    region_condition = "AND 1 = 1"
    # Modify the query with the selected conditions
    query = query.format(date_condition=date_condition, tag_condition=tag_condition, region_condition=region_condition)
    if selected_region:
    # ใช้ fetch_data function ในการดึงข้อมูล
        results = fetch_data(query)

        # ใช้ pandas ในการสร้าง DataFrame
        df = pd.DataFrame(results, columns=[
            'PL_REGION_ID', 'TAG_ID', 'METER_ID', 'DATA_DATE', 'CORRECTED', 'UNCORRECTED', 'Pressure', 'Temperature'
        ])
        
        # ลบคอลัมน์ที่ไม่ต้องการ
        df = df.drop(['PL_REGION_ID', 'TAG_ID', 'METER_ID'], axis=1)
        df = df.applymap(lambda x: x.replace('\n', '') if isinstance(x, str) else x)


        # ส่ง DataFrame ไปยัง HTML template
        return render_template('billingdata.html', tables=[df.to_html(classes='data')],
                        titles=df.columns.values,
                        selected_date=selected_date,
                        selected_tag=selected_tag,
                        selected_region=selected_region,
                        region_options=region_options,
                        tag_options=tag_options)


    else:
                # Render the template without executing the query
        return render_template('billingdata.html', selected_date=selected_date,selected_region=selected_region,selected_tag=selected_tag, region_options=region_options, tag_options=tag_options, tables=[])

############ / View Billing Data  #####################



@app.route('/sitedetail_data')
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
    selected_region = request.args.get('region_dropdown')

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
        df = pd.DataFrame(results, columns=[
            'ID', 'SITE', 'PHASE', 'IP ADDRESS', 'TYPE'
        ])
        # ลบคอลัมน์ที่ไม่ต้องการ
        df = df.applymap(lambda x: x.replace('\n', '') if isinstance(x, str) else x)

        # Sort DataFrame by the 'SITE' column (adjust as needed)
        df = df.sort_values(by='SITE')

        # ส่ง DataFrame ไปยัง HTML template
        return render_template('sitedetail.html', tables=[df.to_html(classes='data')],
                            titles=df.columns.values,
                            selected_region=selected_region,
                            region_options=region_options)
    else:
        # Render the template without executing the query
        return render_template('sitedetail.html', selected_region=selected_region, region_options=region_options, tables=[])


if __name__ == "__main__":
    app.run(debug=True)