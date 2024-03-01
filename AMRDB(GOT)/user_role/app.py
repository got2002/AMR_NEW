from flask import Flask, render_template, request, redirect, url_for, session, flash
import pandas as pd
import cx_Oracle
import sqlite3


app = Flask(__name__)
app.secret_key = 'your_secret_key'

######################### connection AMR_DB ###############################
amr_db_params = {
    "username": 'AMR_DB',
    "password": 'AMR_DB',
    "hostname": '10.104.240.26',
    "port": '1521',
    "sid": "AMR"
}

# root_params = {
#     "username": 'root',
#     "password": 'root',
#     "hostname": '192.168.102.192',
#     "port": '1521',
#     "service_name": "orcl"
# }

# Choose the database connection parameters based on your requirements
selected_params = amr_db_params  # Change this to switch between databases
print("aaaa", selected_params)

dsn = cx_Oracle.makedsn(selected_params["hostname"], selected_params["port"], selected_params["sid"])

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
    print("Connection to AMR_DB successful.")
except cx_Oracle.Error as e:
    (error,) = e.args
    print("Oracle Error:", error)
######################### connection AMR_DB ###############################


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