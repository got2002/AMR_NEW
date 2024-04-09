from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
import pandas as pd
import cx_Oracle
import sqlite3


app = Flask(__name__)
app.secret_key = 'your_secret_key'

######################### connection AMR_DB ###############################
# amr_db_params = {
#     "username": 'AMR_DB',
#     "password": 'AMR_DB',
#     "hostname": '10.104.240.26',
#     "port": '1521',
#     "sid": "AMR"
# }

# # Choose the database connection parameters based on your requirements
# selected_params = amr_db_params  # Change this to switch between databases
# print("aaaa", selected_params)

# dsn = cx_Oracle.makedsn(selected_params["hostname"], selected_params["port"], selected_params["sid"])

# try:
#     connection_info = {
#         "user": selected_params["username"],
#         "password": selected_params["password"],
#         "dsn": dsn,
#         "min": 1,
#         "max": 5,
#         "increment": 1,
#         "threaded": True
#     }

#     connection_pool = cx_Oracle.SessionPool(**connection_info)
#     connection = connection_pool.acquire()
#     print("Connection to AMR_DB successful.")
# except cx_Oracle.Error as e:
#     (error,) = e.args
#     print("Oracle Error:", error)

######################### connection AMR_DB ###############################

######################### connection AMR_NEW ###############################

root_params = {
    "username": 'root',
    "password": 'root',
    "hostname": '192.168.102.192',
    "port": '1521',
    "service_name": "orcl"
}

# Choose the database connection parameters based on your requirements
selected_params = root_params  # Change this to switch between databases
# print("aaaa", selected_params)

dsn = cx_Oracle.makedsn(selected_params["hostname"], selected_params["port"], selected_params["service_name"])

try:
    connection_info = {
        "user": selected_params["username"],
        "password": selected_params["password"],
        "dsn": dsn,
        "min": 1,
        "max": 5,
        "increment": 1,
        "threaded": True
    }

    connection_pool = cx_Oracle.SessionPool(**connection_info)
    connection = connection_pool.acquire()
    print("Connection to AMR_NEW successful.")
except cx_Oracle.Error as e:
    (error,) = e.args
    print("Oracle Error:", error)

######################### connection AMR_ ###############################


######################### connection PTT_PIVOT ###############################
# ptt_pivot_params = {
#     "username": "PTT_PIVOT",
#     "password": "PTT_PIVOT",
#     "hostname": "10.100.56.3",
#     "port": "1521",
#     "service_name": "PTTAMR_MST"
# }

# dsn = cx_Oracle.makedsn(ptt_pivot_params["hostname"], ptt_pivot_params["port"], service_name=ptt_pivot_params["service_name"])

# try:
#     connection_info = {
#         "user": ptt_pivot_params["username"],
#         "password": ptt_pivot_params["password"],
#         "dsn": dsn,
#         "min": 1,
#         "max": 5,
#         "increment": 1,
#         "threaded": True
#     }

#     connection_pool = cx_Oracle.SessionPool(**connection_info)
#     connection = connection_pool.acquire()
#     print("Connection to PTT_PIVOT successful.")
    
# except cx_Oracle.Error as e:
#     (error,) = e.args
#     print("Oracle Error:", error)

######################### connection PTT_PIVOT ###############################

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
        (error,) = e.args
        print("Oracle Error:", error)
        return []
    
# update polling
def update_sql(sql_statement):
    with connection.cursor() as cursor:

        cursor.execute(sql_statement)
    connection.commit()

def fetch_user_data(username):
    query = """
        SELECT "USER_NAME", "PASSWORD", "DESCRIPTION", "USER_LEVEL"
        FROM AMR_USER
        WHERE "USER_NAME" = :username
    """
    params = {'username': username}
    user_data = fetch_data(query, params)
    
    
    if user_data:
        username, password, description, user_level = user_data[0]
        return {'password': password, 'description': description, 'user_level': int(user_level)}
    
    return None

users = {}

@app.route('/login', methods=['GET', 'POST'])
def login():
    error_message = None  
    
    if request.method == 'POST':
        entered_username = request.form['username']
        entered_password = request.form['password']

        # Query to fetch user data from the database
        query = """
            SELECT "USER_NAME", "PASSWORD", "DESCRIPTION", "USER_LEVEL"
            FROM AMR_USER
            WHERE "USER_NAME" = :entered_username
            AND amr_user.user_enable like '1'
        """
        params = {'entered_username': entered_username}
        user_data = fetch_data(query, params)
        # print("login:", user_data)

        if user_data:
            stored_password, description, user_level = user_data[0][1:]

            if entered_password == stored_password:
                session['username'] = entered_username
                users[entered_username] = {'password': stored_password, 'description': description, 'user_level': user_level}
                if user_level == '1' or user_level == '4' or user_level == '5':
                    return redirect(url_for('home'))
                elif user_level == '2':
                    return redirect(url_for('home_user_group'))
                elif user_level == '3':
                    return redirect(url_for('home_user'))
            else:
                error_message = 'Incorrect password'
        else:
            error_message = 'User not found'

    return render_template('login.html', error_message=error_message)



@app.route('/')
def home():
    if 'username' in session:
        username = session['username']
        user = users.get(username)  # Using get method to handle KeyError
        if user:
            return render_template('home.html', username=username, description=user['description'], user_level=user['user_level'])
        else:
            # Handle the case where the user is not in the users dictionary
            flash('User information not found. Please log in again.', 'error')
            return redirect(url_for('login'))
    else:
        flash('Please log in to access this page.', 'error')
        return redirect(url_for('login'))


@app.route('/homr_user')
def home_user():
    if 'username' in session:
        username = session['username']
        user = users.get(username)  # Using get method to handle KeyError
        if user:
            return render_template('home_user.html', username=username, description=user['description'], user_level=user['user_level'])
        else:
            # Handle the case where the user is not in the users dictionary
            flash('User information not found. Please log in again.', 'error')
            return redirect(url_for('login'))
    else:
        flash('Please log in to access this page.', 'error')
        return redirect(url_for('login'))
    
@app.route('/home_user_group')
def home_user_group():
    if 'username' in session:
        username = session['username']
        user = users.get(username)  # Using get method to handle KeyError
        if user:
            return render_template('home_user_group.html', username=username, description=user['description'], user_level=user['user_level'])
        else:
            # Handle the case where the user is not in the users dictionary
            flash('User information not found. Please log in again.', 'error')
            return redirect(url_for('login'))
    else:
        flash('Please log in to access this page.', 'error')
        return redirect(url_for('login'))

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

@app.route("/billingdata")
def billingdata():
    
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
    
    
    # Get selected values from the text inputs
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
        return render_template('billingdata.html',
                               selected_date=selected_date,
                               selected_region=selected_region,
                               selected_tag=selected_tag,
                               region_options=region_options,
                               tag_options=tag_options,
                               tables=[])

@app.route("/billingdata_user_group")
def billingdata_user_group():
    if 'username' not in session:
        return redirect(url_for('login'))

    # Fetch user information from the session
    logged_in_user = session['username']
    if logged_in_user not in users:
        return redirect(url_for('login'))
    
    user_info = users[logged_in_user]
    user_level = user_info.get('user_level')
    description = user_info.get('description')
    # print("description", description)
    
    logged_in_user = logged_in_user
    print("user:", logged_in_user)
    
    region_query = """
    SELECT amr_user.user_group 
    FROM AMR_user 
    WHERE user_name = :logged_in_user
    AND amr_user.user_enable like '1' 
    """
    tag_query = """
    SELECT DISTINCT TAG_ID
    FROM AMR_FIELD_ID
    JOIN AMR_PL_GROUP ON AMR_FIELD_ID.FIELD_ID = AMR_PL_GROUP.FIELD_ID 
    WHERE AMR_PL_GROUP.PL_REGION_ID = :region_id
    """
    

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
    
    
    # Get selected values from the text inputs
    selected_date = request.args.get('date_dropdown')
    selected_tag = request.args.get('tag_dropdown')
    selected_region = request.args.get('region_dropdown')
    
    # Fetch unique region values
    region_results = fetch_data(region_query, params={'logged_in_user': logged_in_user})
    region_options = [str(region[0]) for region in region_results]
    # print("des", region_options)

    for region in region_results:
        region_results = fetch_data(region_query, params={'logged_in_user': logged_in_user})
        region_options = str(region[0]) 
        print("region:", region_options)

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
        return render_template('billingdata_user_group.html', tables=[df.to_html(classes='data')],
                        titles=df.columns.values,
                        selected_date=selected_date,
                        selected_tag=selected_tag,
                        selected_region=selected_region,
                        region_options=region_options,
                        tag_options=tag_options,
                        username=logged_in_user,
                        description=description,  
                        user_level=user_level)


    else:
                # Render the template without executing the query
        return render_template('billingdata_user_group.html',
                               selected_date=selected_date,
                               selected_region=selected_region,
                               selected_tag=selected_tag,
                               region_options=region_options,
                               tag_options=tag_options,
                               tables=[],
                               username=logged_in_user,
                               description=description,  
                               user_level=user_level)
              
@app.route("/billingdata_user")
def billingdata_user():
    if 'username' not in session:
        return redirect(url_for('login'))

    # Fetch user information from the session
    logged_in_user = session['username']
    if logged_in_user not in users:
        return redirect(url_for('login'))
    
    user_info = users[logged_in_user]
    user_level = user_info.get('user_level')
    description = user_info.get('description')
    # print("description", description)
    
    logged_in_user = logged_in_user
    print("user:", logged_in_user)

    region_query = """
    SELECT amr_region.id
    FROM AMR_REGION,AMR_user,amr_field_id,amr_pl_group
    WHERE amr_user.user_group = amr_field_id.meter_id
        AND amr_field_id.field_id = amr_pl_group.field_id
        AND amr_pl_group.pl_region_id = amr_region.id
        AND user_name = :logged_in_user
        AND amr_user.user_enable like '1'
    """

    # Fetch unique tag values based on the description
    tag_query = """
        SELECT amr_field_id.tag_id
        FROM AMR_REGION,AMR_user,amr_field_id,amr_pl_group
        WHERE amr_user.user_group = amr_field_id.meter_id
            AND amr_field_id.field_id = amr_pl_group.field_id
            AND amr_pl_group.pl_region_id = amr_region.id
            AND user_name = :logged_in_user
            AND amr_user.user_enable like '1'
    """
    
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
    
    
    # Get selected values from the text inputs
    selected_date = request.args.get('date_dropdown')
    selected_tag = request.args.get('tag_dropdown')
    selected_region = request.args.get('region_dropdown')
    
    # Fetch unique region values
    region_results = fetch_data(region_query, params={'logged_in_user': logged_in_user})
    region_options = [str(region[0]) for region in region_results]
    # print("des", region_options)

    for region in region_results:
        region_results = fetch_data(region_query, params={'logged_in_user': logged_in_user})
        region_options = str(region[0]) 
        print("region:", region_options)

    # # Fetch tag options based on the selected region
    tag_options = None
    tag_results = fetch_data(tag_query, params={'logged_in_user': logged_in_user})
    for tag in tag_results:
        tag_options = str(tag[0])
        print("site:", tag_options)
           
    if selected_date:
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
        return render_template('billingdata_user.html', tables=[df.to_html(classes='data')],
                               titles=df.columns.values,
                               selected_date=selected_date,
                               selected_tag=selected_tag,
                               selected_region=selected_region,
                               region_options=region_options,
                               tag_options=tag_options,
                               username=logged_in_user,
                               description=description,  
                               user_level=user_level) 

    else:
        # Render the template without executing the query
        return render_template('billingdata_user.html',
                               selected_date=selected_date,
                               selected_region=selected_region,
                               selected_tag=selected_tag,
                               region_options=region_options,
                               tag_options=tag_options,
                               tables=[],
                               username=logged_in_user,  
                               description=description,
                               user_level=user_level)  


@app.route('/add_site', methods=['GET', 'POST'])
def add_site():
    max_id_query = "SELECT MAX(ID) + 1 FROM amr_field_id"
    max_id_result = fetch_data(max_id_query)
    max_id_value = str(max_id_result[0][0]) if max_id_result and max_id_result[0][0] is not None else ""
    
    AMR0 = "AMR0"
    CUST0 = "CUST0"
    MET0 = "MET0"
    PROT0 = "PROT0"
    
    
    sql_commands = []
        
    if request.method == 'POST':
        phase = request.form['phase']
        site_name = request.form['site_name']
        factory_name = request.form['factory_name']
        region = request.form['region']
        rmiu_type = request.form['rmiu_type']
        power_indicator = request.form['power_indicator']
        modbus_id = request.form['modbus_id']
        ip_address = request.form['ip_address']
        ready_to_billing = request.form.get('ready_to_billing')  # Check if the checkbox is checked
        auto_ping = request.form.get('auto_ping')  # Check if the checkbox is checked
        billing_date = request.form['billing_date']
        show_sg_co2_n2 = request.form['show_sg_co2_n2']
        amount_of_meter = request.form['amount_of_meter']
        initial_username = request.form['initial_username']
        initial_password = request.form['initial_password']
        
        port_1 = request.form['port_1']
        port1 = request.form['port1']
        auto_1 = request.form['auto_1']
        
        port_2 = request.form['port_2']
        port2 = request.form['port2']
        auto_2 = request.form['auto_2']
        
        port_3 = request.form['port_3']
        port3 = request.form['port3']
        auto_3 = request.form['auto_3']
        
        port_4 = request.form['port_4']
        port4 = request.form['port4']
        auto_4 = request.form['auto_4']
        
        port_5 = request.form['port_5']
        port5 = request.form['port5']
        auto_5 = request.form['auto_5']
        
        port_6 = request.form['port_6']
        port6 = request.form['port6']
        auto_6 = request.form['auto_6']
        
        # print(f'Phase: {phase}')
        # print(f'Site Name: {site_name}')
        # print(f'Factory Name: {factory_name}')
        # print(f'Region: {region}')
        # print(f'RMIU Type: {rmiu_type}')
        # print(f'Power Indicator: {power_indicator}')
        # print(f'MODBUS ID: {modbus_id}')
        # print(f'IP Address: {ip_address}')
        # print(f'Ready to Billing: {ready_to_billing}')  # Will print '1' if checkbox is checked
        # print(f'Auto Ping: {auto_ping}')  # Will print '1' if checkbox is checked
        # print(f'Billing Date: {billing_date}')
        # print(f'Show SG CO2 N2: {show_sg_co2_n2}')
        # print(f'Amount of Meter: {amount_of_meter}')
        # print(f'Initial Username: {initial_username}')
        # print(f'Initial Password: {initial_password}')
        
        # print(f'port_1: {port_1}')
        # print(f'port1: {port1}')
        # print(f'auto_1: {auto_1}')
        
        # print(f'port_2: {port_2}')
        # print(f'port2: {port2}')
        # print(f'auto_2: {auto_2}')
        
        # print(f'port_3: {port_3}')
        # print(f'port3: {port3}')
        # print(f'auto_3: {auto_3}')
        
        # print(f'port_4: {port_4}')
        # print(f'port4: {port4}')
        # print(f'auto_4: {auto_4}')
        
        # print(f'port_5: {port_5}')
        # print(f'port5: {port5}')
        # print(f'auto_5: {auto_5}')
        
        # print(f'port_6: {port_6}')
        # print(f'port6: {port6}')
        # print(f'auto_6: {auto_6}')

        amr_user = f"""
        INSERT INTO AMR_USER (ID, DESCRIPTION, USER_NAME, PASSWORD, USER_LEVEL, USER_GROUP, USER_ENABLE)
        VALUES ({max_id_value}, '{site_name}', '{initial_username}', '{initial_password}', '3', '{MET0+max_id_value}', '1')
        """
        # update_sql(amr_user)
        
        amr_field_id = f"""
        INSERT INTO AMR_FIELD_ID (
                                ID, 
                                TAG_ID, 
                                FIELD_ID, 
                                CUST_ID, 
                                METER_ID, 
                                PROTOCOL_ID, 
                                RTU_MODBUS_ID,
                                RMIU_AUTO_ENABLE,
                                PING_ENABLE,
                                RMIU_TYPE, 
                                SIM_IP,
                                RMIU_POLL_REPEAT1,
                                RMIU_POLL_REPEAT2,
                                AMR_PHASE
                                )
        VALUES ({max_id_value}, '{site_name}', 
                                '{AMR0+max_id_value}', 
                                '{CUST0+max_id_value}', 
                                '{MET0+max_id_value}', 
                                '{PROT0+max_id_value}', 
                                '{modbus_id}',
                                '{ready_to_billing}',
                                '{auto_ping}',
                                '{rmiu_type}', 
                                '{ip_address}',
                                '{0}',
                                '{0}',
                                '{phase}'
                                )
        """
        update_sql(amr_field_id)
        
        amr_field_customer= f"""
        INSERT INTO AMR_FIELD_CUSTOMER (
                                        ID, 
                                        CUST_ID,
                                        CUST_NAME,
                                        CUST_FACTORY_NAME,
                                        METER_RUN
                                        )
        VALUES ({max_id_value}, '{CUST0+max_id_value}',
                                '{site_name}',
                                '{factory_name}',
                                '{amount_of_meter}'            
                                )
        """
        # update_sql(amr_field_customer)
        
        amr_pl_group = f""" 
        INSERT INTO AMR_PL_GROUP (ID, PL_REGION_ID, FIELD_ID) 
        VALUES ({max_id_value}, '{region}', '{AMR0+max_id_value}')
        """
        update_sql(amr_pl_group)
        
        for i in range(1, int(amount_of_meter) + 1): 
            amr_field_meter = f"""
            INSERT INTO AMR_FIELD_METER (METER_ID, 
                                        METER_STREAM_NO, 
                                        METER_NO_STREAM,
                                        METER_STREAM_TYPE,
                                        METER_PORT_NO,
                                        METER_AUTO_ENABLE,
                                        METER_POLL_REPEAT1,
                                        METER_POLL_REPEAT2,
                                        METER_POLL_REPEAT3,
                                        METER_POLL_REPEAT4,
                                        METER_POLL_REPEAT5,
                                        METER_POLL_REPEAT6,
                                        METER_POLL_REPEAT7 
                                        )
            VALUES ('{MET0+max_id_value}', '{i}',
                                        '{amount_of_meter}',
                                        '{request.form['port_' + str(i)]}',
                                        '{request.form['port' + str(i)]}',
                                        '{request.form['auto_' + str(i)]}',
                                        '{0}',
                                        '{0}',
                                        '{0}',
                                        '{0}',
                                        '{0}',
                                        '{0}',
                                        '{0}'
                                        )         
            """
            # update_sql(amr_field_meter)
            
            amr_field_profile = f"""
            INSERT INTO AMR_FIELD_PROFILE (METER_ID, 
                                            METER_STREAM_NO,
                                            WRITE_CONFIG_ENABLE,
                                            WRITE_CONFIG_REPEAT1,
                                            WRITE_CONFIG_REPEAT2
                                            )
            VALUES ('{MET0+max_id_value}', '{i}',
                                            '{auto_ping}',
                                            '{0}',
                                            '{0}'
                                            )
            """
            # update_sql(amr_field_profile)
            
            amr_field_protocal = f"""
            INSERT INTO AMR_FIELD_PROTOCAL (PROTOCOL_ID, PROTOCOL_STREAM_NO, PROTOCOL_NO_STREAM)
            VALUES ('{PROT0+max_id_value}', '{i}', '{amount_of_meter}')
            """
            # update_sql(amr_field_protocal)
            
        return render_template('home.html',)

        
    return render_template('add_site.html', max_id_value=max_id_value)

@app.route('/edit_site', methods=['GET', 'POST'])
def edit_site():
    query_type = request.args.get("query_type")

    # SQL query to fetch unique PL_REGION_ID values
    region_query = """
    SELECT * FROM AMR_REGION 
    """

    selected_region = request.args.get("region_dropdown")

    # Fetch unique region values
    region_results = fetch_data(region_query)
    region_options = [str(region[0]) for region in region_results]

    tag_query = """
    SELECT DISTINCT TAG_ID
    FROM AMR_FIELD_ID
    JOIN AMR_PL_GROUP ON AMR_FIELD_ID.FIELD_ID = AMR_PL_GROUP.FIELD_ID 
    WHERE AMR_PL_GROUP.PL_REGION_ID = :region_id
    ORDER BY TAG_ID
    """
    
    selected_tag = request.args.get("tag_dropdown")
    
    # Fetch tag options based on the selected region
    tag_results = fetch_data(tag_query, params={"region_id": selected_region})
    tag_options = [str(tag[0]) for tag in tag_results]
    
    show_tag_query = """
    SELECT DISTINCT
        AMR_FIELD_ID.ID,
        AMR_FIELD_ID.TAG_ID,
        AMR_FIELD_ID.SIM_IP,
        AMR_FIELD_ID.RTU_MODBUS_ID,
        AMR_FIELD_ID.AMR_PHASE,
        AMR_FIELD_CUSTOMER.CUST_FACTORY_NAME,
        AMR_USER.USER_NAME,
        AMR_USER.PASSWORD,
        AMR_FIELD_METER.METER_ID,
        AMR_FIELD_METER.METER_STREAM_NO,
        AMR_FIELD_METER.METER_NO_STREAM,
        AMR_FIELD_METER.METER_STREAM_TYPE,
        AMR_FIELD_METER.METER_PORT_NO,
        AMR_FIELD_METER.METER_AUTO_ENABLE,
        AMR_FIELD_PROFILE.METER_ID,
        AMR_FIELD_PROTOCAL.PROTOCOL_ID,
        AMR_FIELD_PROTOCAL.PROTOCOL_NO_STREAM
    FROM 
        AMR_FIELD_ID
    JOIN AMR_FIELD_CUSTOMER ON AMR_FIELD_ID.CUST_ID = AMR_FIELD_CUSTOMER.CUST_ID
    JOIN AMR_USER ON AMR_FIELD_ID.ID = AMR_USER.ID
    JOIN AMR_FIELD_METER ON AMR_FIELD_ID.METER_ID = AMR_FIELD_METER.METER_ID
    JOIN AMR_FIELD_PROFILE ON AMR_FIELD_ID.METER_ID = AMR_FIELD_PROFILE.METER_ID
    JOIN AMR_FIELD_PROTOCAL ON AMR_FIELD_ID.PROTOCOL_ID = AMR_FIELD_PROTOCAL.PROTOCOL_ID
    JOIN AMR_PL_GROUP ON AMR_FIELD_ID.FIELD_ID = AMR_PL_GROUP.FIELD_ID 
    JOIN AMR_REGION ON AMR_PL_GROUP.PL_REGION_ID = AMR_REGION.ID
    WHERE 
        AMR_REGION.ID = :region_id AND
        AMR_FIELD_ID.TAG_ID = :tag_id
    ORDER BY METER_STREAM_NO
    """
    
    data = []
    if selected_region is not None and selected_tag is not None:
        data = fetch_data(show_tag_query, params={"region_id": selected_region, "tag_id": selected_tag})
       

    # Create DataFrame from query results
    columns = [
        'id',
        'tag_id',
        'sim_ip',
        'rtu_modbus_id',
        'amr_phase',
        'cust_factory_name',
        'user_name',
        'password',
        'meter_id',
        'meter_stream_no',
        'meter_no_stream',
        'meter_stream_type',
        'meter_port_no',
        'meter_auto_enable',
        'meter_id',
        'protocol_id',
        'protocol_no_stream'
    ]
    df = pd.DataFrame(data, columns=columns)
    
    
    if not df.empty:
        list_id = df["id"].iloc[0]
        list_tag_id = df["tag_id"].iloc[0]
        list_cust_factory_name = df["cust_factory_name"].iloc[0]
        list_amr_phase = df["amr_phase"].iloc[0]
        list_rtu_modbus_id = df["rtu_modbus_id"].iloc[0]
        list_sim_ip = df["sim_ip"].iloc[0]
        list_user_name = df["user_name"].iloc[0]
        list_password = df["password"].iloc[0]
        list_meter_stream_no = df["meter_stream_no"].tolist()       
        list_meter_port_no = df["meter_port_no"].tolist()
        list_meter_auto_enable = df["meter_auto_enable"].tolist()
        
        # update_user = f"""
        #     UPDATE AMR_USER 
        #     SET 
        #         user_name = '{list_user_name}',
        #         password = '{list_password}'
        #     WHERE id = '{list_id}'
        #     """
        # print("update_user", update_user)
        # update_sql(update_user)


            
        
        list_meter_stream_type = []
        for meter_stream_type in df["meter_stream_type"]:
            meter_stream_type_list = f"""SELECT vc_name FROM amr_vc_type WHERE id = '{meter_stream_type}' ORDER BY id"""
            type = fetch_data(meter_stream_type_list)
            if type:
                list_meter_stream_type.append(type[0][0])
            else:
                list_meter_stream_type.append(None)
            print("list_meter_stream_type", list_meter_stream_type)
                
        list_meter_port_no = []
        for meter_port_no in df["meter_port_no"]:
            meter_port_no_list =f"""SELECT port_no FROM amr_port_info WHERE id = '{meter_port_no}' ORDER BY id"""
            port = fetch_data(meter_port_no_list)
            if port:
                list_meter_port_no.append(port[0][0])
            else:
                list_meter_port_no.append(None)
            print("list_meter_port_no", list_meter_port_no)
            
            
    else:
        list_id = None
        list_tag_id = None
        list_cust_factory_name = None
        list_amr_phase = None
        list_rtu_modbus_id = None
        list_sim_ip = None
        list_user_name = None
        list_password = None
        list_meter_stream_no = None
        list_meter_auto_enable = None
        list_meter_stream_type = None
        list_meter_port_no = None
        
    

    html_table = df.to_html(index=False)


    return render_template('edit_site.html', 
                           region_options=region_options, 
                           tag_options=tag_options, 
                           selected_region=selected_region,
                           selected_tag=selected_tag,
                           list_id=list_id,
                           list_tag_id=list_tag_id,
                           list_cust_factory_name=list_cust_factory_name,
                           list_amr_phase=list_amr_phase,
                           list_rtu_modbus_id=list_rtu_modbus_id,
                           list_sim_ip=list_sim_ip,
                           list_user_name=list_user_name,
                           list_password=list_password,
                           list_meter_stream_no=list_meter_stream_no,
                           list_meter_stream_type=list_meter_stream_type,
                           list_meter_port_no=list_meter_port_no,
                           list_meter_auto_enable=list_meter_auto_enable,
                           html_table=html_table)

    


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))



if __name__ == '__main__':
    app.run(debug=True)
    
    
    
        # region_query = """
        # SELECT amr_user.user_group 
        # FROM AMR_user 
        # WHERE user_name = :logged_in_user
        # AND amr_user.user_enable like '1' 
        # """
        # print("ree", region_query)
        # # Fetch unique region values
        # region_results = fetch_data(amr_connection, region_query, params={'logged_in_user': logged_in_user})
        
        
        # region_options_tmp = [str(region[0]) for region in region_results]
        # # print("des", region_options)
        
        # region_options = region_options_tmp[0]


        # tag_query = """
        # SELECT DISTINCT TAG_ID
        # FROM AMR_FIELD_ID
        # JOIN AMR_PL_GROUP ON AMR_FIELD_ID.FIELD_ID = AMR_PL_GROUP.FIELD_ID 
        # WHERE AMR_PL_GROUP.PL_REGION_ID = :region_id
        # """
        
        #         tag_query = """
        # SELECT DISTINCT AMR_FIELD_ID.TAG_ID
        # FROM AMR_FIELD_ID, amr_user, amr_pl_group 
        # WHERE
        #     amr_user.user_group = amr_pl_group.pl_region_id
        #     and AMR_FIELD_ID.FIELD_ID = AMR_PL_GROUP.FIELD_ID
        #     and AMR_FIELD_ID.tag_id NOT like '%.remove%'
        #     and amr_pl_group.pl_region_id = :region_options
        # """
        
        # print(tag_query)
        # tag_results = fetch_data(amr_connection,tag_query, params={"region_options": region_options})
        # tag_options = [str(tag[0]) for tag in tag_results]
        # print("tag:", tag_options)