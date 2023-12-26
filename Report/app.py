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


@app.route('/get_tags', methods=['GET'])
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
    return jsonify({'tag_options': tag_options})















@app.route('/')
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
        AMR_CONFIGURED_DATA.DATA_DATE,
        amr_configured_data.amr_vc_type,
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
        amr_configured_data.DATE_CREATED,
        amr_configured_data.TIME_CREATE,
        amr_configured_data.status,
        amr_configured_data.created_by,
        amr_configured_data.updated_by,
        amr_configured_data.updated_time,
        amr_configured_data.amr_config17,
        amr_configured_data.amr_config18,
        amr_configured_data.amr_config19,
        amr_configured_data.amr_config20,
        
        AMR_VC_CONFIGURED_INFO.vc_type,
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
        AMR_VC_CONFIGURED_INFO.config20
        
       
    FROM
        AMR_FIELD_ID, AMR_PL_group, AMR_CONFIGURED_DATA
    JOIN AMR_VC_CONFIGURED_INFO ON amr_configured_data.amr_vc_type = AMR_VC_CONFIGURED_INFO.vc_type
    WHERE
        AMR_PL_GROUP.FIELD_ID = AMR_FIELD_ID.FIELD_ID 
        AND AMR_CONFIGURED_DATA.METER_ID = AMR_FIELD_ID.METER_ID
        AND AMR_CONFIGURED_DATA.METER_STREAM_NO like '1'
        
        {date_condition}
        {tag_condition}
        {region_condition}
    """

    # Get selected values from the dropdowns
    date_condition = "AND AMR_CONFIGURED_DATA.DATA_DATE IS NOT NULL"
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
            f"AND TO_CHAR(AMR_CONFIGURED_DATA.DATA_DATE, 'MM/YYYY') = '{selected_date}'"
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
            "AMR_VC_TYPE",
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
            "DATE_CREATED",
            "TIME_CREATE",
            "STATUS",
            "CREATED_BY",
            "UPDATED_BY",
            "UPDATED_TIME",
            "AMR_CONFIG17",
            "AMR_CONFIG18",
            "AMR_CONFIG19",
            "AMR_CONFIG20",
            "VC_TYPE",
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
    )

        df = df.apply(lambda x: x.apply(lambda y: y.replace("\n", "") if isinstance(y, str) else y) if x.dtype == 'O' else x)
        # สลับแถวกับคอลัมน์ (Transpose) เพื่อทำให้ CONFIG1 เป็นหัวตาราง
        df_transposed = df.T

        # ให้ CONFIG1 เป็นหัวตาราง
        df_transposed.columns = df_transposed.iloc[6]

        # ลบแถวที่ไม่ต้องการ
        df_transposed = df_transposed.drop(["PL_REGION_ID", "TAG_ID", "METER_ID", "DATA_DATE", "AMR_VC_TYPE"])

        # ลบข้อมูลที่ซ้ำ
        df_transposed = df_transposed.drop(df_transposed.index[6])
        df = df.sort_values(by='DATA_DATE')
        
        print(df)
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
                # Render the template without executing the query
        return render_template('billingdata.html', selected_date=selected_date,selected_region=selected_region,selected_tag=selected_tag, region_options=region_options, tag_options=tag_options, tables=[])

if __name__ == '__main__':
    app.run(debug=True)
