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

username = "PTT_PIVOT"
password = "PTT_PIVOT"
hostname = "10.100.56.3"
port = "1521"
service_name = "PTTAMR_MST"

def fetch_data(query, params=None):
    try:
        connection_string = f"{username}/{password}@{hostname}:{port}/{service_name}"
        with cx_Oracle.connect(connection_string) as connection:
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

    



@app.route("/")
def billing_data():
    selected_region = request.args.get('region')
    selected_tag = request.args.get('tag')
    selected_month_year = request.args.get('monthYear')

    # Define your Oracle query to fetch REGION_NAME
    region_query = """
    SELECT DISTINCT REGION_NAME
    FROM VW_AMR_BILLING_DATA
    ORDER BY REGION_NAME
    """
    # Fetch REGION_NAME data using your fetch_data function
    region_results = fetch_data(region_query)

    # Define your Oracle query to fetch tag_id based on the selected REGION_NAME
    tag_query = """
    SELECT DISTINCT tag_id
    FROM VW_AMR_BILLING_DATA
    WHERE REGION_NAME = :selected_region
    ORDER BY tag_id
    """
    # Fetch tag_id data using your fetch_data function
    tag_results = fetch_data(tag_query, {'selected_region': selected_region})

    # Define your Oracle query to fetch data based on selected criteria
    billing_query = """
        SELECT *
        FROM VW_AMR_BILLING_DATA
        WHERE 
            VW_AMR_BILLING_DATA.region_name = :selected_region
            AND VW_AMR_BILLING_DATA.tag_id = :selected_tag
            AND TO_CHAR(VW_AMR_BILLING_DATA.data_date, 'MM/YYYY') = :selected_month_year
            ORDER BY VW_AMR_BILLING_DATA.data_date
    """
    # Fetch data using your fetch_data function
    results = fetch_data(billing_query, {'selected_region': selected_region, 'selected_tag': selected_tag, 'selected_month_year': selected_month_year})
    print(results)
    # Render the template with the fetched data and selected region
    return render_template(
        "billingdata.html",
        region_results=region_results,
        tag_results=tag_results,
        results=results,
        selected_region=selected_region,
    )





@app.route('/get_tags')
def get_tags():
    region_name = request.args.get('region')

    # Use the selected REGION_NAME to fetch associated tag_id values
    tag_query = """
    SELECT DISTINCT tag_id
    FROM VW_AMR_BILLING_DATA
    WHERE REGION_NAME = :region_name
    ORDER BY tag_id
    """
    tag_results = fetch_data(tag_query, {'region_name': region_name})

    # Return the tag_id values as JSON
    return jsonify(tag_results)



    
          

    
if __name__ == "__main__":
    app.run(debug=True)