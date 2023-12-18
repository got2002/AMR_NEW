from flask import Flask, render_template
from io import BytesIO
import base64
import matplotlib.pyplot as plt
import numpy as np

# from flask_mail import Mail, Message
from flask import Flask, render_template, request, flash, redirect, url_for, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
# from wtforms.validators import DataRequired, Email, EqualTo, Length
# from werkzeug.security import generate_password_hash, check_password_hash
# from models import User  # Import the User model from models.py
# from forms import LoginForm, RegisterForm, EditUserForm  # Import the forms

import cx_Oracle
import pandas as pd
import random
import string

app = Flask(__name__)

hostname = 'localhost'
port = '1521'
service_name = 'orcl'
username = 'root'
password = 'root'


@app.route('/')
def home():
    return render_template('Search.html')

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
        error, = e.args
        print("Oracle Error:", error)
        return []

# ส่วนที่ขาดหายไปใน get_tags


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

    return jsonify({'tag_options': tag_options})

# ปรับแต่งส่วนที่ขาดหายไปใน index


@app.route('/')
def Search():
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

    # Modify the query with the selected conditions
    query = query.format(date_condition=date_condition,
                         tag_condition=tag_condition, region_condition=region_condition)

    # ใช้ fetch_data function ในการดึงข้อมูล
    results = fetch_data(query)

    # ใช้ pandas ในการสร้าง DataFrame
    df = pd.DataFrame(results, columns=[
        'PL_REGION_ID', 'TAG_ID', 'METER_ID', 'DATA_DATE', 'CORRECTED', 'UNCORRECTED', 'Pressure', 'Temperature'
    ])
    # ลบคอลัมน์ที่ไม่ต้องการ
    df = df.drop(['PL_REGION_ID', 'TAG_ID', 'METER_ID'], axis=1)
    df = df.applymap(lambda x: x.replace('\n', '')
                     if isinstance(x, str) else x)

    # ส่ง DataFrame ไปยัง HTML template
    return render_template('Search.html', tables=[df.to_html(classes='data')],
                           titles=df.columns.values,
                           selected_date=selected_date,
                           selected_tag=selected_tag,
                           selected_region=selected_region,
                           region_options=region_options,
                           tag_options=tag_options)


@app.route('/your_api_endpoint')
def your_api_endpoint():
    # ตัวอย่างข้อมูลที่จะส่งกลับในรูปแบบ JSON
    tag_options = ['tag1', 'tag2', 'tag3']

    # ส่ง JSON response กลับไปยัง client
    return jsonify({'tag_options': tag_options})


@app.route('/')
def home():
    # ข้อมูลสำหรับกราฟเส้นที่แยกกัน
    x_data = np.array(range(1, 32))

    y_data_1 = np.random.randint(1, 10, size=(31,))
    y_data_2 = np.random.randint(1, 10, size=(31,))
    y_data_3 = np.random.randint(1, 10, size=(31,))

    # สร้างกราฟเส้นที่ 1
    plt.plot(x_data, y_data_1, marker='o', linestyle='-', color='blue', label='Graph 1')

    # กำหนดชื่อแกน x และ y
    plt.xlabel('Days')
    plt.ylabel('Values')

    # กำหนดชื่อกราฟ
    plt.title('Graph 1')

    # เพิ่มตำแหน่งของ legend
    plt.legend(loc='upper left')

    # แปลงกราฟเป็นรูปภาพและเก็บไว้ใน BytesIO
    img_1 = BytesIO()
    plt.savefig(img_1, format='png')
    img_1.seek(0)
    plt.close()

    # แปลงรูปภาพเป็น base64
    graph_url_1 = base64.b64encode(img_1.getvalue()).decode('utf8')

    # สร้างกราฟเส้นที่ 2
    plt.plot(x_data, y_data_2, marker='s', linestyle='--', color='green', label='Graph 2')

    # กำหนดชื่อแกน x และ y
    plt.xlabel('Days')
    plt.ylabel('Values')

    # กำหนดชื่อกราฟ
    plt.title('Graph 2')

    # เพิ่มตำแหน่งของ legend
    plt.legend(loc='upper left')

    # แปลงกราฟเป็นรูปภาพและเก็บไว้ใน BytesIO
    img_2 = BytesIO()
    plt.savefig(img_2, format='png')
    img_2.seek(0)
    plt.close()

    # แปลงรูปภาพเป็น base64
    graph_url_2 = base64.b64encode(img_2.getvalue()).decode('utf8')

    # สร้างกราฟเส้นที่ 3
    plt.plot(x_data, y_data_3, marker='^', linestyle='-.', color='red', label='Graph 3')

    # กำหนดชื่อแกน x และ y
    plt.xlabel('Days')
    plt.ylabel('Values')

    # กำหนดชื่อกราฟ
    plt.title('Graph 3')

    # เพิ่มตำแหน่งของ legend
    plt.legend(loc='upper left')

    # แปลงกราฟเป็นรูปภาพและเก็บไว้ใน BytesIO
    img_3 = BytesIO()
    plt.savefig(img_3, format='png')
    img_3.seek(0)
    plt.close()

    # แปลงรูปภาพเป็น base64
    graph_url_3 = base64.b64encode(img_3.getvalue()).decode('utf8')

    return render_template('index.html', graph_url_1=graph_url_1, graph_url_2=graph_url_2, graph_url_3=graph_url_3)


if __name__ == '__main__':
    app.run(debug=True)
