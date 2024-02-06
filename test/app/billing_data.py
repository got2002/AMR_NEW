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

from .connect_db import fetch_data,connect_to_amr_db,connect_to_ptt_pivot_db,active_connection
billing_data = Blueprint('billing', __name__)



@billing_data.route("/get_tags", methods=["GET"])
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
    
@billing_data.route("/billing_data")
def billing():
    with connect_to_amr_db() as amr_connection:
        print("Active Connection:", active_connection)
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
        tables = {}
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