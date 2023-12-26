from flask import Flask, render_template, request, jsonify
import pandas as pd
import cx_Oracle

app = Flask(__name__)

# กำหนดการเชื่อมต่อฐานข้อมูล
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

# Define your route function
@app.route("/")
def render_template_function():
    # Access request.args and other request-related objects here
    selected_date = request.args.get("date_dropdown")
    selected_tag = request.args.get("tag_dropdown")
    selected_region = request.args.get("region_dropdown")

    # ... (other code)

    return render_template(
        "billingdata.html",
        tables=[df1.to_html(classes="data1"), df2.to_html(classes="data2")],
        titles=[df1.columns.values, df2.columns.values],
        selected_date=selected_date,
        selected_tag=selected_tag,
        selected_region=selected_region,
        region_options=region_options,
        tag_options=tag_options,
    )
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


# SQL query for main data
config1 = """
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

config2 = """
    SELECT 
        amr_configured_data.*, AMR_VC_CONFIGURED_INFO.*
    FROM 
        amr_configured_data
    JOIN 
        AMR_VC_CONFIGURED_INFO ON amr_configured_data.amr_vc_type = AMR_VC_CONFIGURED_INFO.vc_type
    WHERE 
        amr_configured_data.amr_vc_type = 5
        {date_condition}
        {tag_condition}
        {region_condition}
"""

date_condition = ""  # Set a default value or leave it as an empty string
tag_condition = ""
region_condition = ""



# Modify the query with the selected conditions
query1 = config1.format(
    date_condition=date_condition,
    tag_condition=tag_condition,
    region_condition=region_condition,
)
query2 = config2.format(
    date_condition=date_condition,
    tag_condition=tag_condition,
    region_condition=region_condition,
)

selected_date = request.args.get("date_dropdown")
selected_tag = request.args.get("tag_dropdown")
selected_region = request.args.get("region_dropdown")

# Update conditions based on selected values
if selected_date:
    date_condition = (
        f"AND TO_CHAR(AMR_BILLING_DATA.DATA_DATE, 'MM/YYYY') = '{selected_date}'"
    )

if selected_tag:
    tag_condition = f"AND AMR_FIELD_ID.TAG_ID = '{selected_tag}'"

if selected_region:
    region_condition = f"AND amr_pl_group.pl_region_id = '{selected_region}'"
if selected_region:
    # ใช้ fetch_data function ในการดึงข้อมูล
    results1 = fetch_data(query1)
    results2 = fetch_data(query2)

    # ใช้ pandas ในการสร้าง DataFrame
    df1 = pd.DataFrame(
        results1,
        columns=[
            "PL_REGION_ID",
            "TAG_ID",
            "METER_ID",
            "DATA_DATE",
            "CORRECTED",
            "UNCORRECTED",
            "Pressure",
            "Temperature",
        ],
    )

    df2 = pd.DataFrame(
        results2,
        columns=[
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
        ],
    )

    # ลบคอลัมน์ที่ไม่ต้องการ
    df1 = df1.drop(["PL_REGION_ID", "TAG_ID", "METER_ID"], axis=1)
    df2 = df2.drop(["amr_vc_type"], axis=1)  # Assuming 'amr_vc_type' is not needed

    df1 = df1.applymap(lambda x: x.replace("\n", "") if isinstance(x, str) else x)
    df2 = df2.applymap(lambda x: x.replace("\n", "") if isinstance(x, str) else x)

    region_options = []  # Define a default value if not retrieved from the database
    tag_options = []  # Define a default value if not retrieved from the database
    tag_query = """
        SELECT DISTINCT TAG_ID
        FROM AMR_FIELD_ID
        JOIN AMR_PL_GROUP ON AMR_FIELD_ID.FIELD_ID = AMR_PL_GROUP.FIELD_ID 
        WHERE AMR_PL_GROUP.PL_REGION_ID = :region_id
    """
    # Retrieve region and tag options if selected_region is not None
    if selected_region:
        region_results = fetch_data(tag_query, params={"region_id": selected_region})
        region_options = [str(region[0]) for region in region_results]

        tag_results = fetch_data(tag_query, params={"region_id": selected_region})
        tag_options = [str(tag[0]) for tag in tag_results]
if __name__ == "__main__":
    app.run(debug=True)
