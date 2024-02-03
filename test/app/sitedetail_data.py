
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
from connect_db import  fetch_data

sitedetail_data = Blueprint('sitedetail', __name__)






@sitedetail_data.route("/sitedetail_data")
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