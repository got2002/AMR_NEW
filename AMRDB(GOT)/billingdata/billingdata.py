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
<<<<<<< HEAD


@app.route("/get_tags", methods=["GET"])
=======
@app.route('/get_tags', methods=['GET'])
>>>>>>> 0422056793ba8b88f7241bf046e2a7fd47135730
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
<<<<<<< HEAD
    return jsonify({"tag_options": tag_options})


@app.route("/")
=======
    return jsonify({'tag_options': tag_options})
@app.route('/')
>>>>>>> 0422056793ba8b88f7241bf046e2a7fd47135730
def index():
    results = []  # Initialize results to an empty list
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
        # ปรับ format ใน date_condition เพื่อให้ตรงกับรูปแบบที่ datepicker กำหนด
        date_condition = (
            f"AND TO_CHAR(AMR_BILLING_DATA.DATA_DATE, 'MM/YYYY') = '{selected_date}'"
        )

    if selected_tag:
        tag_condition = f"AND AMR_FIELD_ID.TAG_ID = '{selected_tag}'"
    if selected_region:
        region_condition = f"AND amr_pl_group.pl_region_id = '{selected_region}'"
    region_condition = "AND 1 = 1"
    # Modify the query with the selected conditions
    query = query.format(
        date_condition=date_condition,
        tag_condition=tag_condition,
        region_condition=region_condition,
    )

    if selected_region:
        # ใช้ fetch_data function ในการดึงข้อมูล
        results = fetch_data(query)

    # ใช้ pandas ในการสร้าง DataFrame
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
        ],
    )

    # ลบคอลัมน์ที่ไม่ต้องการ
    df = df.drop(["PL_REGION_ID", "TAG_ID", "METER_ID"], axis=1)
    df = df.applymap(lambda x: x.replace("\n", "") if isinstance(x, str) else x)
    # แปลง 'DATA_DATE' เป็น datetime object
    df['DATA_DATE'] = pd.to_datetime(df['DATA_DATE'])
    # เรียงลำดับตาม 'DATA_DATE'
    df = df.sort_values(by='DATA_DATE')
    if not df.empty:
        return render_template(
            "billingdata.html",
            titles=df.columns,
            tables=df.to_dict("records"),
            selected_date=selected_date,
            selected_tag=selected_tag,
            selected_region=selected_region,
            region_options=region_options,
            tag_options=tag_options,
        )
    else:
<<<<<<< HEAD
        return render_template(
            "billingdata.html",
            titles=[],
            tables=[],
            selected_date=selected_date,
            selected_tag=selected_tag,
            selected_region=selected_region,
            region_options=region_options,
            )

if __name__ == "__main__":
=======
                # Render the template without executing the query
        return render_template('billingdata.html', selected_date=selected_date,selected_region=selected_region,selected_tag=selected_tag, region_options=region_options, tag_options=tag_options, tables=[])
if __name__ == '__main__':
>>>>>>> 0422056793ba8b88f7241bf046e2a7fd47135730
    app.run(debug=True)
