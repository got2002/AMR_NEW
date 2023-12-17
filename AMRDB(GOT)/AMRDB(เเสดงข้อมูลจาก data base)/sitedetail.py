from flask import Flask, render_template, request, jsonify
import pandas as pd
import cx_Oracle

app = Flask(__name__)

# กำหนดการเชื่อมต่อฐานข้อมูล
username = 'root'
password = 'root'
hostname = 'localhost'
port = '1521'
service_name = 'orcl'

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

@app.route('/')
def index():
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
    
    region_condition = "AND amr_pl_group.pl_region_id IS NOT NULL"
    
    
    selected_region = request.args.get('region_dropdown')

    # Fetch unique region values
    region_results = fetch_data(region_query)
    region_options = [str(region[0]) for region in region_results]

    # Fetch tag options based on the selected region
    

   
    if selected_region:
        region_condition = f"AND amr_pl_group.pl_region_id = '{selected_region}'"

    # Modify the query with the selected conditions
    query = query.format( region_condition=region_condition)

    # ใช้ fetch_data function ในการดึงข้อมูล
    results = fetch_data(query)

    # ใช้ pandas ในการสร้าง DataFrame
    df = pd.DataFrame(results, columns=[
        'ID', 'SITE', 'PHASE', 'IP ADDRESS', 'TYPE'

    ])
    # ลบคอลัมน์ที่ไม่ต้องการ
    
    df = df.applymap(lambda x: x.replace('\n', '') if isinstance(x, str) else x)

    # ส่ง DataFrame ไปยัง HTML template
    return render_template('sitedetail.html', tables=[df.to_html(classes='data')],
                       titles=df.columns.values,
                       selected_region=selected_region,
                       region_options=region_options,
                       )
if __name__ == '__main__':
    app.run(debug=True)
