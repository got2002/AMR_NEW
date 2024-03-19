from flask import Flask, render_template, request, jsonify, redirect, flash
import cx_Oracle
import pandas as pd
from flask_sqlalchemy import SQLAlchemy

#### Global Variable 
#For specific configuration data per day 
QUANTITY_CONFIG_DATA = 20  #ค่า config มี 20 ค่า
QUANTITY_BILLING_PER_DAY = 5
#For specific quantity of poll range 
QUANTITY_RANGE_CONFIG_LIST = 10  # poll range ทำเป็น list จะมี 10 element

app = Flask(__name__)
app.secret_key = 'your_secret_key'

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

def insert_address_range_to_oracle(
    connection, poll_config, poll_billing, enable_config, enable_billing, evc_type
):
    with connection.cursor() as cursor:
        sql_insert = """
            INSERT INTO AMR_POLL_RANGE (POLL_CONFIG, POLL_BILLING, POLL_CONFIG_ENABLE, POLL_BILLING_ENABLE, EVC_TYPE)
            VALUES (:1, :2, :3, :4, :5)
        """

        # Convert enable_config and enable_billing to comma-separated strings
        enable_config_str = ",".join(map(str, enable_config))
        enable_billing_str = ",".join(map(str, enable_billing))

        data_to_insert = (
            poll_config,
            poll_billing,
            enable_config_str,
            enable_billing_str,
            evc_type,
        )

        cursor.execute(sql_insert, data_to_insert)

    connection.commit()

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/polling_route")
def polling_route():
    # Fetch type options for the dropdown
    type_query = "SELECT VC_NAME FROM AMR_VC_TYPE"
    type_results = fetch_data(type_query)
    type_options = [str(type[0]) for type in type_results]
    # print(type_results)

    # Define the base query for fetching polling data
    base_query = """
    SELECT
        apr.evc_type,
        apr.poll_config,
        apr.poll_billing,
        apr.poll_config_enable,
        apr.poll_billing_enable
    FROM
        amr_poll_range apr
    JOIN
        amr_vc_type avt ON apr.evc_type = avt.id
    {type_condition}
    """

    # Get selected type from the dropdown
    selected_type = request.args.get("type_dropdown")

    # Define type condition based on the selected type
    type_condition = f"AND avt.VC_NAME = '{selected_type}'" if selected_type else ""

    # Check if a type is selected before executing the query
    if selected_type:
        # Modify the base query with the selected conditions
        query = base_query.format(type_condition=type_condition)

        # Fetch data using the modified query
        results = fetch_data(query)
        # print(results)

        columns = [
            "evc_type",
            "poll_config",
            "poll_billing",
            "poll_config_enable",
            "poll_billing_enable",
        ]
        df = pd.DataFrame(results, columns=columns)

        
        poll_config_list = df.get(["poll_config"]).values.tolist()
        list_config = str(poll_config_list[0]).strip("[]'").split(",")
        # print("===", poll_config_list)
        
        poll_billing_list = df.get(["poll_billing"]).values.tolist()
        list_billing = str(poll_billing_list[0]).strip("[]'").split(",")
        
        poll_config_enable_list = df.get(["poll_config_enable"]).values.tolist()
        list_enable_config = str(poll_config_enable_list[0]).strip("[]'").split(",")
     
        poll_billing_enable_list = df.get(["poll_billing_enable"]).values.tolist()
        list_enable_billing = str(poll_billing_enable_list[0]).strip("[]'").split(",")
        
        return render_template(
            "polling.html",
            tables=[df.to_html(classes="data", index=False)],
            titles=columns,
            selected_type=selected_type,
            type_options=type_options,
            list_config=list_config,
            list_billing=list_billing,
            list_enable_config=list_enable_config,
            list_enable_billing=list_enable_billing,
        )
    else:
    # Render the HTML template without the table if no type is selected
        return render_template(
            "polling.html",
            tables=[],
            titles=[],
            selected_type=None,
            type_options=type_options,
            list_config=[],
            list_billing=[],
            list_enable_config=[],
            list_enable_billing=[],
        )
    
MAX_ADDRESS_LENGTH = 249

@app.route("/update_polling_data", methods=["POST"])
def update_polling_data(): 
    selected_type = request.form.get("selected_type")

    type_id_query = f"SELECT ID FROM AMR_VC_TYPE WHERE VC_NAME LIKE '{selected_type}'"
    results = fetch_data(type_id_query)
    type_id = str(results[0]).strip("',()")
    print(type_id)
    
    # Update configuration data
    poll_config_all = ""
    enable_config = ""
    for i in range(0, 5):
        start_key = f"start_config{i + 1}"
        end_key = f"end_config{i + 1}"
        enable_key = f"enable_config[{i}]"
        
        start_value = request.form.get(start_key)
        end_value = request.form.get(end_key)
        enable_value = 1 if request.form.get(enable_key) == "on" else 0

        address_range = f"{start_value},{end_value}"
        if len(poll_config_all + address_range) <= MAX_ADDRESS_LENGTH:
            if i > 0:
                poll_config_all += ","
            poll_config_all += address_range

        if i == 0:
            enable_config = str(enable_value)
        else:
            enable_config +=  "," + str(enable_value)
            
    print("poll_config:", poll_config_all)
    print("poll_config_enable:", enable_config)
    
    # Update billing data
    poll_billing_all = ""
    enable_billing = ""
    for i in range(0, 10):
        start_key = f"start{i + 1}"
        end_key = f"end{i + 1}"
        enable_key = f"enable[{i}]"
        
        start_value = request.form.get(start_key)
        end_value = request.form.get(end_key)
        enable_value = 1 if request.form.get(enable_key) == "on" else 0
        
        address_range = f"{start_value},{end_value}"
        if len(poll_billing_all + address_range) <= MAX_ADDRESS_LENGTH:
            if i > 0:
                poll_billing_all += ","
            poll_billing_all += address_range

        if i == 0:
            enable_billing = str(enable_value)
        else:
            enable_billing += "," + str(enable_value)
    
    print("poll_billing:", poll_billing_all)
    print("poll_config_enable:", enable_billing)

    update_query = f"""
    UPDATE amr_poll_range
    SET 
        poll_config = '{poll_config_all}',
        poll_billing = '{poll_billing_all}',
        poll_config_enable = '{enable_config}',
        poll_billing_enable = '{enable_billing}'
    WHERE evc_type = '{type_id}'
    """
    update_sql(update_query)
    print("Update Query:", update_query)
    # After updating the data, you may redirect to the polling route or perform any other necessary actions
    
    return redirect("/polling_route")

@app.route("/add_polling_route")
def add_polling_route():
    return render_template("add_polling.html")

MAX_ADDRESS_LENGTH = 249

@app.route("/save_to_oracle", methods=["POST"])
def save_to_oracle():
    try:
        data = request.get_json()

        # Add the following line to define 'evc_type'
        evc_type = data.get("evc_type", "")

        def validate_address_range(start_key, end_key):
            start_address = int(data.get(start_key, 0))
            end_address = int(data.get(end_key, 0))

            if end_address - start_address + 1 > MAX_ADDRESS_LENGTH:
                raise ValueError(
                    f"Address range {start_key} - {end_key} exceeds the maximum length of {MAX_ADDRESS_LENGTH}"
                )

            return start_address, end_address

        combined_address_config = ",".join(
            [
                ",".join(map(str, validate_address_range(f"start{i}", f"end{i}")))
                for i in range(1, 6)
                if data.get(f"start{i}")
            ]
        )

        enable_config = [int(data.get(f"enable{i}", 0)) for i in range(1, 6)]

        combined_address_billing = ",".join(
            [
                ",".join(map(str, validate_address_range(f"start{i}", f"end{i}")))
                for i in range(6, 16)
                if data.get(f"start{i}")
            ]
        )

        enable_billing = [int(data.get(f"enable{i}", 0)) for i in range(6, 16)]

        if not combined_address_config or not combined_address_billing:
            response = {
                "status": "error",
                "message": "Please enter at least one valid start or end address for both configurations.",
            }
            return jsonify(response)

        # Add a function to update the existing records in Oracle
        update_address_range_in_oracle(
            combined_address_config,
            combined_address_billing,
            enable_config,
            enable_billing,
            evc_type,
        )

        response = {"status": "success", "message": "Data updated successfully"}
    except ValueError as ve:
        response = {"status": "error", "message": str(ve)}
    except cx_Oracle.DatabaseError as e:
        (error,) = e.args
        print(f"Oracle Database Error {error.code}: {error.message}")
        traceback.print_exc()  # Print detailed traceback information
        response = {
            "status": "error",
            "message": f"Database Error: {error.code} - {error.message}",
        }
    except Exception as e:
        print(f"Error: {e}")
        traceback.print_exc()  # Print detailed traceback information
        response = {
            "status": "error",
            "message": f"An error occurred while updating data: {str(e)}",
        }

    return jsonify(response)

@app.route('/mapping_config')  
def mapping_config_route():
    # SQL query to fetch options for the dropdown
    type_query = "SELECT VC_NAME FROM AMR_VC_TYPE ORDER BY VC_NAME"
    type_results = fetch_data(type_query)
    type_options = [str(type[0]) for type in type_results]

    # SQL query to fetch data based on selected type
    base_query = """
     SELECT
        address,
        description,
        data_type,
        evc_type,
        or_der
        
    FROM
        amr_mapping_config, amr_vc_type
    WHERE
        amr_mapping_config.evc_type = amr_vc_type.id
        AND amr_vc_type.VC_NAME LIKE '{selected_type}'
    ORDER BY or_der
    """
    
    selected_type = request.args.get("type_dropdown")
    selected_type = f"{selected_type}" if selected_type else ""

    if selected_type:
        query = base_query.format(selected_type=selected_type)
        results = fetch_data(query)

        columns = [
            "address",
            "description",
            "data_type",
            "evc_type",
            "or_der",
            
        ]
        df = pd.DataFrame(results, columns=columns)

        address_list = df.get(["address"]).values.tolist()
        list_address = str(address_list[0]).strip("[]'").split(",")
        print("map:", df)
               
        description_list = df.get(["description"]).values.tolist()
        list_description = str(description_list[0]).strip("[]'").split(",")
               
        data_type_list = df.get(["data_type"]).values.tolist()
        list_data_type = str(data_type_list[0]).strip("[]'").split(",")       
        
        evc_type_list = df.get(["evc_type"]).values.tolist()
        list_evc_type = str(evc_type_list[0]).strip("[]'").split(",")
        
        or_der_list = df.get(["or_der"]).values.tolist()
        list_or_der = str(or_der_list[0]).strip("[]'").split(",")
               
        

        return render_template(
            'mapping_config.html', 
            type_options=type_options, 
            selected_type=selected_type, 
            table=df.to_html(index=False),
            list_address=df["address"].tolist(),
            list_description=df["description"].tolist(),
            list_data_type=df["data_type"].tolist(),
            list_evc_type=df["evc_type"].tolist(),
            list_or_der=df["or_der"].tolist()
            
        )
    else:
        return render_template('mapping_config.html', type_options=type_options)

def checkStrNone(stringcheck):
    if stringcheck == "None": return ""
    return stringcheck
    
@app.route('/update_mapping_config_route', methods=['POST'])
def update_mapping_config():
    selected_type = request.form.get('selected_type')

    # Fetch type_id from the database
    type_id_query = f"SELECT ID FROM AMR_VC_TYPE WHERE VC_NAME LIKE '{selected_type}'"
    results = fetch_data(type_id_query)
    type_id = str(results[0]).strip("',()")
    print("type:", type_id)
    
    query = """
        SELECT
            apr.evc_type,
            apr.poll_config


        FROM
            amr_poll_range apr
        JOIN
        amr_vc_type avt ON apr.evc_type = avt.id
        {type_condition}
        """
    type_condition = f"AND avt.VC_NAME = '{selected_type}'" if selected_type else ""
    
    # Check if a type is selected before executing the query
    if type_condition:
        query = query.format(type_condition=type_condition)
        results = fetch_data(query)
        # print(results)

        columns = [
            "evc_type",
            "poll_config",
            
        ]
        df = pd.DataFrame(results, columns=columns)

        
        poll_config_list = df.get(["poll_config"]).values.tolist()
        list_config = str(poll_config_list[0]).strip("[]'").split(",")
        print("start:", list_config)     

    description_VC_TYPE = [] 

    for j in range(0,QUANTITY_CONFIG_DATA):  
        i = f"{j:02d}"
        address_key = f"list_address{i}"
        description_key = f"list_description{i}"
        data_type_key = f"list_data_type{i}"
        evc_type_key = f"list_evc_type{i}"
        or_der_key = f"list_or_der{i}"

        address_value = checkStrNone(request.form.get(address_key))
        description_value = checkStrNone(request.form.get(description_key))
        data_type_value = checkStrNone(request.form.get(data_type_key))
        evc_type_value = request.form.get(evc_type_key)
        or_der_value = request.form.get(or_der_key)

        valid = False
        
        #check config
        print(address_value)
        # if textbox = None ไม่ต้อง check address แต่ต้องappend array ด้วย blank เพราะเดี๋ยวจะไม่ครบใน sql command
        if address_value == "": 
            description_VC_TYPE.append("")
            continue
        k = 0
        for k in range(0,QUANTITY_RANGE_CONFIG_LIST,2):
           
            address_value_int = int(address_value)
            address_check_low = int(list_config[k])
            address_check_high = int(list_config[k+1])
            k+=2
            print("low = ", address_check_low, ", high = ", address_check_high, "; value = ", address_value_int)
            if address_check_low  <= address_value_int :
                if address_value_int <= address_check_high:
                    valid = True; print("Result = True"); break
            print("Result = False")
        
        
        if valid == False:
            print("Error : invalid address ; alert หน้าจอ และ ออกจาก function นี้ได้เลย ")
            
            #error
            return ""
             
    
        description_VC_TYPE.append(checkStrNone(description_value))
        # print("---", description_value)


        # Update SQL query based on your table structure
        update_query = f"""
        UPDATE AMR_MAPPING_CONFIG
        SET
            ADDRESS = '{address_value}',
            DESCRIPTION = '{description_value}',
            DATA_TYPE = '{data_type_value}',
            OR_DER = '{or_der_value}'        
        WHERE evc_type = '{evc_type_value}' and or_der = '{or_der_value}'
        """
        # print("Update Query##################", update_query)
        update_sql(update_query)
        
        
    
    update_vc_info_query = f"""
    UPDATE AMR_VC_CONFIGURED_INFO
    SET
        CONFIG1 = '{description_VC_TYPE[0]}',
        CONFIG2 = '{description_VC_TYPE[1]}',
        CONFIG3 = '{description_VC_TYPE[2]}',
        CONFIG4 = '{description_VC_TYPE[3]}',
        CONFIG5 = '{description_VC_TYPE[4]}',
        CONFIG6 = '{description_VC_TYPE[5]}',
        CONFIG7 = '{description_VC_TYPE[6]}',
        CONFIG8 = '{description_VC_TYPE[7]}',
        CONFIG9 = '{description_VC_TYPE[8]}',
        CONFIG10 = '{description_VC_TYPE[9]}',
        CONFIG11 = '{description_VC_TYPE[10]}',
        CONFIG12 = '{description_VC_TYPE[11]}',
        CONFIG13 = '{description_VC_TYPE[12]}',
        CONFIG14 = '{description_VC_TYPE[13]}',
        CONFIG15 = '{description_VC_TYPE[14]}',
        CONFIG16 = '{description_VC_TYPE[15]}',
        CONFIG17 = '{description_VC_TYPE[16]}',
        CONFIG18 = '{description_VC_TYPE[17]}',
        CONFIG19 = '{description_VC_TYPE[18]}',
        CONFIG20 = '{description_VC_TYPE[19]}'
    
    WHERE 
        VC_TYPE = '{evc_type_value}'
        
    """
    
    update_sql(update_vc_info_query)
    # print(update_vc_info_query)

    return redirect("/mapping_config")


@app.route('/mapping_billing')  
def mapping_billing_route():
    # SQL query to fetch options for the dropdown
    type_query = "SELECT VC_NAME FROM AMR_VC_TYPE"
    type_results = fetch_data(type_query)
    type_options = [str(type[0]) for type in type_results]

    # SQL query to fetch data based on selected type
    base_query = f"""
     SELECT
        address,
        description,
        data_type,
        evc_type,
        or_der,
        daily
        
    FROM
        amr_mapping_billing, amr_vc_type
    WHERE
        amr_mapping_billing.evc_type = amr_vc_type.id
        AND amr_vc_type.VC_NAME LIKE :1
        AND daily = 1
    order by or_der
    """

    selected_type = request.args.get("type_dropdown") or ""
    if selected_type:
        type_id_query = "SELECT ID FROM AMR_VC_TYPE WHERE VC_NAME LIKE :1"
        results = fetch_data(type_id_query, (selected_type,))
        
        interval = request.args.get("interval") or "10"
        
         
        if results:
            type_id = str(results[0][0])

            query = base_query
            results = fetch_data(query, (selected_type,))
            
            print("type:", type_id)
            max_daily_query = "SELECT MAX(daily) FROM amr_mapping_billing WHERE evc_type LIKE :1"
            max_daily_result = fetch_data(max_daily_query, (type_id,))
            max_daily_value = str(max_daily_result[0][0]) if max_daily_result and max_daily_result[0][0] else ""
            print("max_day:", max_daily_value)

            #if max_daily_value <=
            columns = [
                "address",
                "description",
                "data_type",
                "evc_type",
                "or_der",
                "daily",
            ]
            df = pd.DataFrame(results, columns=columns)
            print("dd:", df)
            
            # Extracting lists directly from DataFrame columns
            list_address = df["address"].tolist()
            list_description = df["description"].tolist()
            list_data_type = df["data_type"].tolist()
            list_evc_type = df["evc_type"].tolist()
            list_or_der = df["or_der"].tolist()
            list_daily = df["daily"].tolist()

            return render_template(
                'mapping_billing.html', 
                type_options=type_options, 
                selected_type=selected_type, 
                max_daily_value=max_daily_value,
                table=df.to_html(index=False),
                list_address=list_address,
                list_description=list_description,
                list_data_type=list_data_type,
                list_evc_type=list_evc_type,
                list_or_der=list_or_der,
                list_daily=list_daily,
                interval=interval
            )

    return render_template('mapping_billing.html', type_options=type_options)

    
@app.route('/update_mapping_billing_route', methods=['POST'])
def update_mapping_billing():
    selected_type = request.form.get('selected_type')

    # Fetch type_id from the database
    type_id_query = f"SELECT ID FROM AMR_VC_TYPE WHERE VC_NAME = '{selected_type}'"
    results = fetch_data(type_id_query)
    type_id = str(results[0]).strip("',()")
    
    #max_daily_query = "SELECT MAX(daily),MAX(id),MAX(address),MAX(or_der)  FROM amr_mapping_billing  WHERE evc_type = {}".format(type_id)
    max_daily_query = "SELECT MAX(daily)  FROM amr_mapping_billing  WHERE evc_type = {}".format(type_id)
    max_daily_result = fetch_data(max_daily_query)
    max_daily_query = str(max_daily_result[0]).strip("',()")
    print("Max:", max_daily_query)
    
    # evc_type = type_id
    # max_daily_query = max day before save 
    
    dataframes = {
                'address':[],
                'description':[],
                'data_type':[],
                'evc_type':[],
                'or_der':[],
                'daily':[],
    }
    df_data = pd.DataFrame(dataframes)
    
    # get max day from text box
    max_daily_new = int(request.form.get('max_day'))
    
    # get information Crete initial dataframe
    
    address_value_array = []
    description_value_array = []
    data_type_value_array = []
    or_der_value_array = []
    
    
    for i in range(0, QUANTITY_BILLING_PER_DAY): 
        i = f"{i:02d}"
        address_key = f"list_address{i}"
        description_key = f"list_description{i}"
        data_type_key = f"list_data_type{i}"
        #evc_type_key = f"list_evc_type{i}"
        or_der_key = f"list_or_der{i}"
        #daily_key = f"list_daily{i}"
                
        address_value = request.form.get(address_key.strip("',()"))
        address_value_array.append(int(address_value))
        
        description_value = request.form.get(description_key.strip("',()"))
        description_value_array.append(description_value)
        
        data_type_value = request.form.get(data_type_key.strip("',()"))
        data_type_value_array.append(data_type_value)
        #evc_type_value = request.form.get(evc_type_key.strip("',()"))
        or_der_value = request.form.get(or_der_key.strip("',()"))
        or_der_value_array.append(or_der_value)

    
    #print("XX", address_value_array, description_value_array, data_type_value_array, or_der_value_array)

    # create Full Data frame
    # Get interval
    interval = request.args.get("interval") or "10"
    print("interval", interval)
    
    for j in range(0,max_daily_new):
        #daily_value = j+1
        for i in range(0, QUANTITY_BILLING_PER_DAY):
             
            address_calc = int(address_value_array[i]) + (j*int(interval))
            print("")
            data = {
                    'address': [address_calc], 
                    'description': [description_value_array[i]],
                    'data_type': [data_type_value_array[i]],
                    'evc_type': [type_id],
                    'or_der': [int(or_der_value_array[i])],
                    'daily': [j+1]
            }
            
            df2 = pd.DataFrame(data)
            df_data = pd.concat([df_data, df2], ignore_index=True)
            
        df_data['address'] = df_data['address'].astype(int)
        df_data['or_der'] = df_data['or_der'].astype(int)
        df_data['daily'] = df_data['daily'].astype(int)      
            
    print("dd4", df_data)
         
       
    if  max_daily_new <= int(max_daily_query) :
        print("EEEE", max_daily_new, max_daily_query)
        if max_daily_new < int(max_daily_query):
            delete_query = f"""
            DELETE FROM AMR_MAPPING_BILLING
            WHERE evc_type = '{type_id}' AND DAILY > {max_daily_new}
            """
            print(delete_query)
            update_sql(delete_query)
        
        for j in range(max_daily_new):
            for i in range(QUANTITY_BILLING_PER_DAY):
                update_query = f"""
                UPDATE AMR_MAPPING_BILLING
                SET 
                    ADDRESS = '{int(address_value_array[i]) + (j* int(interval))}',
                    DESCRIPTION = '{description_value_array[i]}',
                    data_type = '{data_type_value_array[i]}'
                WHERE 
                    evc_type = '{type_id}' and 
                    or_der = {i+1} and 
                    daily = {j+1}
                    
                """
                print("update_query", update_query)

                update_sql(update_query)
        
    else : # max_daily_new > int(max_daily_query):
        # updte 1 to max_daily_query
        for j in range(0, int(max_daily_query)):
            for i in range(QUANTITY_BILLING_PER_DAY):
                update_billing = f"""
                UPDATE AMR_MAPPING_BILLING
                SET 
                    ADDRESS = '{int(address_value_array[i]) + (j* int(interval))}',
                    DESCRIPTION = '{description_value_array[i]}',
                    data_type = '{data_type_value_array[i]}'
                WHERE 
                    evc_type = '{type_id}' and 
                    or_der = {i+1} and 
                    daily = {j+1}
                """
                print("update_billing", update_billing)

                update_sql(update_billing)
        
        # Insert max_daily_query to max_daily_new
        
        for j in range(max_daily_new - int(max_daily_query)):
            for i in range(QUANTITY_BILLING_PER_DAY):  # Assuming this is the correct length
                new_address = int(address_value_array[i]) + ((int(max_daily_query) + j) * int(interval))
                new_description = description_value_array[i]
                new_data_type = data_type_value_array[i]
                new_evc_type = type_id
                new_or_der = or_der_value_array[i]
                new_daily = int(max_daily_query) + j + 1

                insert_query = f"""
                INSERT INTO AMR_MAPPING_BILLING (ADDRESS, DESCRIPTION, DATA_TYPE, evc_type, OR_DER, DAILY)
                VALUES ('{new_address}', '{new_description}', '{new_data_type}',  '{new_evc_type}', '{new_or_der}', '{new_daily}')
                """

                update_sql(insert_query)
                print(insert_query)
    
    
    # Update SQL query based on your table structure
    
        # update_query = f"""
        # UPDATE AMR_MAPPING_BILLING
        # SET
        #     ADDRESS = '{address_value}',
        #     DESCRIPTION = '{description_value}',
        #     DATA_TYPE = '{data_type_value}',
        #     OR_DER = '{or_der_value}',
        #     DAILY = '{daily_value}'        
        # WHERE evc_type = '{evc_type_value}' and or_der = '{or_der_value}'
        # """

        # update_sql(update_query)
        # print(update_query)

    return redirect("/mapping_billing")


@app.route("/add_mapping_route")
def add_mapping_route():
    return render_template("add_mapping.html")


@app.route("/submit_form", methods=["POST"])
def submit_form():
    cursor = None
    connection = None

    try:
        data_list = []
        for i in range(1, 21):
            address = request.form[f"address{i}"]
            description = request.form[f"description{i}"]
            type_value = request.form.get(f"type_value{i}")
            evc_type = request.form[f"evc_type{i}"]
            or_der = request.form[f"or_der{i}"]
            data_type = request.form[f"data_type{i}"]

            data_list.append(
                (address, description, type_value, evc_type, or_der, data_type)
            )

        dsn_tns = cx_Oracle.makedsn(host, port, service_name=service)
        connection = cx_Oracle.connect(user=username, password=password, dsn=dsn_tns)

        cursor = connection.cursor()

        sql_merge = """
            MERGE INTO AMR_MAPPING_CONFIG dst
            USING (
                SELECT
                    :address as address,
                    :description as description,
                    :type_value as type_value,
                    :evc_type as evc_type,
                    :or_der as or_der,
                    :data_type as data_type
                FROM dual
            ) src
            ON (dst.address = src.address)
            WHEN MATCHED THEN
                UPDATE SET
                    dst.description = src.description,
                    dst.type_value = src.type_value,
                    dst.evc_type = src.evc_type,
                    dst.or_der = src.or_der,
                    dst.data_type = src.data_type
            WHEN NOT MATCHED THEN
                INSERT (
                    address,
                    description,
                    type_value,
                    evc_type,
                    or_der,
                    data_type
                ) VALUES (
                    src.address,
                    src.description,
                    src.type_value,
                    src.evc_type,
                    src.or_der,
                    src.data_type
                )
        """

        cursor.executemany(sql_merge, data_list)

        # Commit the changes to the database
        connection.commit()

        return "Data saved successfully"
    except Exception as e:
        return f"Error occurred: {str(e)}"
    finally:
        if cursor is not None:
        # Close the cursor
            cursor.close()

    if connection is not None:
        # Close the connection
        connection.close()


@app.route("/add_actraris_route")
def add_actraris_route():
    return render_template("add_actraris.html")


@app.route("/new_form", methods=["POST"])
def submit_new_form():
    cursor = None
    connection = None

    try:
        data_list = []
        for i in range(1, 18):
            address = request.form.get(f"address{i}")
            description = request.form.get(f"description{i}")
            type_value = request.form.get(f"type_value{i}")
            evc_type = request.form.get(f"evc_type{i}")
            or_der = request.form.get(f"or_der{i}")
            data_type = request.form.get(f"data_type{i}")

            data_list.append(
                (address, description, type_value, evc_type, or_der, data_type)
            )

        dsn_tns = cx_Oracle.makedsn(host, port, service_name=service)
        connection = cx_Oracle.connect(user=username, password=password, dsn=dsn_tns)

        cursor = connection.cursor()

        sql_merge = """
            MERGE INTO AMR_ADDRESS_MAPPING1 dst
            USING (
                SELECT
                    :address as address,
                    :description as description,
                    :type_value as type_value,
                    :evc_type as evc_type,
                    :or_der as or_der,
                    :data_type as data_type
                FROM dual
            ) src
            ON (dst.address = src.address)
            WHEN MATCHED THEN
                UPDATE SET
                    dst.description = src.description,
                    dst.type_value = src.type_value,
                    dst.evc_type = src.evc_type,
                    dst.or_der = src.or_der,
                    dst.data_type = src.data_type
            WHEN NOT MATCHED THEN
                INSERT (
                    address,
                    description,
                    type_value,
                    evc_type,
                    or_der,
                    data_type
                ) VALUES (
                    src.address,
                    src.description,
                    src.type_value,
                    src.evc_type,
                    src.or_der,
                    src.data_type
                )
        """

        cursor.executemany(sql_merge, data_list)

        connection.commit()

        # Commit the changes to the database
        connection.commit()

        return "Data saved successfully"
    except Exception as e:
        return f"Error occurred: {str(e)}"
    finally:
        if cursor is not None:
        # Close the cursor
            cursor.close()

    if connection is not None:
        # Close the connection
        connection.close()

if __name__ == "__main__":
    app.run(debug=True)
