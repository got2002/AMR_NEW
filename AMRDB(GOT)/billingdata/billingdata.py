from flask import Flask, render_template, request, jsonify
import pandas as pd
import cx_Oracle

app = Flask(__name__)

# กำหนดการเชื่อมต่อฐานข้อมูล
# username = 'AMR_DB'
# password = 'AMR_DB'
# hostname = '10.104.240.26'
# port = '1521'
# sid = "AMR"

username = "root"
password = "root"
hostname = "192.168.102.192"
port = "1521"
service_name = "orcl"

dsn = cx_Oracle.makedsn(hostname, port, service_name)

try:
    connection_info = {
        "user": username,
        "password": password,
        "dsn": dsn,
        "min": 1,
        "max": 5,
        "increment": 1,
        "threaded": True
    }

    connection_pool = cx_Oracle.SessionPool(**connection_info)
    connection = connection_pool.acquire()
    print("Success")
except cx_Oracle.Error as e:
    (error,) = e.args
    print("Oracle Error:", error)

def fetch_data(query, params=None):
    try:
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

@app.route("/")
def billingdata():
    # SQL query to fetch unique PL_REGION_ID values
    # user_name_query = "SELECT user_name FROM amr_user_tests ORDER BY user_name"
    # user_name_results = fetch_data(user_name_query)
    # user_name_options = [str(user_name[0]) for user_name in user_name_results]
    
    # password_query = "SELECT password FROM amr_user_tests ORDER BY password"
    # password_results = fetch_data(password_query)
    # password_options = [str(password[0]) for password in password_results]
    
    user_name_query = """
    SELECT amr_region.id,amr_user_tests.description 
    FROM AMR_REGION,amr_user_tests,amr_field_id,amr_pl_group
    WHERE amr_user_tests.user_group = amr_field_id.meter_id
        AND amr_field_id.field_id = amr_pl_group.field_id
        AND amr_pl_group.pl_region_id = amr_region.id
        AND amr_user_tests.user_name = amr_user_tests.user_name
        AND amr_user_tests.password = amr_user_tests.password
        AND amr_user_tests.user_enable like '1'
        {user_name_condition}
        {password_condition}
        
    """
    # selected_user_name = request.args.get("user_name_dropdown")
    # user_name_condition = f"AND amr_user_tests.user_name = '{selected_user_name}'" if selected_user_name else ""
    # print("===:", selected_user_name)
    
    # selected_password = request.args.get("password_dropdown")
    # password_condition = f"AND amr_user_tests.password = '{selected_password}'" if selected_password else ""
    # print("=", password_condition)

    
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
    user_name_condition = "AND amr_user_tests.user_name IS NOT NULL"
    password_condition = "AND amr_user_tests.password IS NOT NULL"
    date_condition = "AND AMR_BILLING_DATA.DATA_DATE IS NOT NULL"
    tag_condition = "AND AMR_FIELD_ID.TAG_ID IS NOT NULL"
    region_condition = "AND amr_pl_group.pl_region_id IS NOT NULL"
    
    
    # Get selected values from the text inputs
    selected_user_name = request.form.get('user_name')
    selected_password = request.form.get('password')
    selected_date = request.args.get('date_dropdown')
    selected_tag = request.args.get('tag_dropdown')
    selected_region = request.args.get('region_dropdown')
   
    region_results = fetch_data(region_query)
    region_options = [str(region[0]) for region in region_results]

    # Fetch tag options based on the selected region
    tag_results = fetch_data(tag_query, params={'region_id': selected_region})
    tag_options = [str(tag[0]) for tag in tag_results]
    
           
    if selected_date:
        date_condition = f"AND TO_CHAR(AMR_BILLING_DATA.DATA_DATE, 'MM/YYYY') = '{selected_date}'"

    if selected_tag:
        tag_condition = f"AND AMR_FIELD_ID.TAG_ID = '{selected_tag}'"
        
    if selected_region:
        region_condition = f"AND amr_pl_group.pl_region_id = '{selected_region}'"
    region_condition = "AND 1 = 1"
    # Modify the query with the selected conditions
    query = query.format(user_name_condition=user_name_condition, password_condition=password_condition, date_condition=date_condition, tag_condition=tag_condition, region_condition=region_condition)
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
                        selected_user_name=selected_user_name,
                        selected_password=selected_password,
                        selected_date=selected_date,
                        selected_tag=selected_tag,
                        selected_region=selected_region,
                        # user_name_options=user_name_options,
                        # password_options=password_options,
                        region_options=region_options,
                        tag_options=tag_options)


    else:
                # Render the template without executing the query
        return render_template('billingdata.html',
                               selected_user_name=selected_user_name,
                               selected_password=selected_password,
                               selected_date=selected_date,
                               selected_region=selected_region,
                               selected_tag=selected_tag,
                            #    user_name_options=user_name_options,
                            #    password_options=password_options,
                               region_options=region_options,
                               tag_options=tag_options,
                               tables=[])

if __name__ == '__main__':
    app.run(debug=True)
