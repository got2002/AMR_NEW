
import pandas as pd
import cx_Oracle
from flask import flash
import traceback
from datetime import datetime
from flask import abort
import socket
import struct
from pymodbus.utilities import computeCRC
import time
import datetime
import logging
communication_traffic = []
change_to_32bit_counter = 0 
def convert_to_binary_string(value, bytes_per_value):
    binary_string = bin(value)[
        2:
    ]  
    return binary_string.zfill(
        bytes_per_value * 8
    )  

def convert_raw_to_value(data_type, raw_data):
    if data_type == "Date":
        raw_data_as_int = int(raw_data, 16)
        date_object = datetime.datetime.fromtimestamp(raw_data_as_int).date()
        
        
        modified_date = date_object - datetime.timedelta(days=1)
        
        formatted_date = modified_date.strftime('%d-%m-%Y') 
        
        return formatted_date
    elif data_type == "Float":
        float_value = struct.unpack('!f', bytes.fromhex(raw_data))[0]
        rounded_float_value = round(float_value, 5)  
        return rounded_float_value
    elif data_type == "Ulong":
        return int(raw_data, 16)
    else:
       
        return raw_data 
############  connect database  #####################

# username = "root"
# password = "root"
# hostname = "192.168.102.192"
# port = "1521"
# service_name = "orcl"


username = "PTT_PIVOT"
password = "PTT_PIVOT"
hostname = "10.100.56.3"
port = "1521"
service_name = "PTTAMR_MST"
dsn = cx_Oracle.makedsn(hostname, port, service_name=service_name)

# สร้าง connection pool ที่ใช้ในการเชื่อมต่อแบบประหยัดทรัพยากร
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

# อ่านข้อมูลจากฐานข้อมูลโดยใช้ connection pool
def fetch_data(query, params=None):
    try:
        with connection_pool.acquire() as connection:
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



logging.basicConfig(filename='C:\\Users\\Administrator\\Desktop\\Autopoll\\Elster EK-280.log', level=logging.ERROR, format='%(asctime)s - %(levelname)s: %(message)s')
query = """
            SELECT
                    AMR_PL_GROUP.PL_REGION_ID as region,
                    AMR_FIELD_ID.TAG_ID as Sitename,
                     AMR_FIELD_METER.METER_NO_STREAM as NoRun,
                    
                    AMR_FIELD_METER.METER_STREAM_NO as RunNo,
                    
                    AMR_FIELD_METER.METER_ID as METERID,
                
                    AMR_VC_TYPE.VC_NAME as VCtype,
                    
                    AMR_FIELD_ID.SIM_IP as IPAddress,
                    AMR_PORT_INFO.PORT_NO as port,
                    AMR_POLL_RANGE.poll_config as poll_config,
                    AMR_POLL_RANGE.poll_billing as poll_billing,
                    AMR_POLL_RANGE.POLL_CONFIG_ENABLE as POLL_CONFIG_ENABLE,
                    AMR_POLL_RANGE.POLL_BILLING_ENABLE as POLL_BILLING_ENABLE,
                    AMR_VC_TYPE.id as evctype
                FROM
                    AMR_POLL_RANGE,
                    AMR_FIELD_ID,
                    AMR_USER,
                    AMR_FIELD_CUSTOMER,
                    AMR_FIELD_METER,
                    AMR_PL_GROUP,
                    AMR_VC_TYPE,
                    AMR_PORT_INFO
                WHERE
                    AMR_FIELD_METER.METER_AUTO_ENABLE=1 AND
                    AMR_FIELD_ID.FIELD_ID = AMR_PL_GROUP.FIELD_ID AND
                    AMR_FIELD_ID.METER_ID = AMR_USER.USER_GROUP AND
                    AMR_FIELD_ID.CUST_ID = AMR_FIELD_CUSTOMER.CUST_ID AND
                    AMR_FIELD_ID.METER_ID = AMR_FIELD_METER.METER_ID AND
                    AMR_VC_TYPE.ID = AMR_FIELD_METER.METER_STREAM_TYPE AND
                    AMR_FIELD_METER.METER_PORT_NO = AMR_PORT_INFO.ID AND
                    amr_poll_range.evc_type = AMR_VC_TYPE.id AND
                    amr_vc_type.id like '13'
                                   
                ORDER BY
                                        
                                        AMR_FIELD_ID.TAG_ID ASC, port
                                        
                
"""



rows =  fetch_data(query)


completed_sets = 0

for row in rows:
    try:
        tcp_ip = row[6]
        tcp_port = row[7]
        run = row[3]
        METERID = row[4]
        poll_config_set = row[8]
        poll_billing_set = row[9]
        CONFIG_ENABLE_set = row[10].replace(',', '')
        BILLING_ENABLE_set = row[11].replace(',', '')
        print("ElsterEK-280")
        print(tcp_ip)
        print(tcp_port)
        evc_type = row[12]
        print(evc_type)
        print(METERID)
        slave_id = 1
        function_code = 3
        completed_sets += 1
        starting_address_config_ = {}
        quantity_config_ = {}
        starting_address_ = {}
        quantity_ = {}
        for i, value in enumerate(poll_config_set.split(',')):
            if i % 2 == 0:
                starting_address_config_[i // 2 + 1] = int(value)
                
            else:
                quantity_config_[i // 2 + 1] = int(value)
                
        for i, value in enumerate(poll_billing_set.split(',')):
            if i % 2 == 0:
                starting_address_[i // 2 + 1] = int(value)
                
                
            else:
                quantity_[i // 2 + 1] = int(value)
        
        
        

        data= {'starting_address_i': [], 
            'quantity_i': [], 
            'adjusted_quantity_i': []}
        df_pollRange = pd.DataFrame(data)
        df_pollBilling = pd.DataFrame(data)
        for i in range(1, 6):
            if CONFIG_ENABLE_set[i-1] == '1':
                starting_address_i = starting_address_config_[i]
                quantity_i = quantity_config_[i]
                adjusted_quantity_i = quantity_i - starting_address_i + 1
                data = {'starting_address_i': [starting_address_i], 
                        'quantity_i': [quantity_i], 
                        'adjusted_quantity_i': [adjusted_quantity_i]}
                df_2 = pd.DataFrame(data)
                
                df_pollRange = pd.concat([df_pollRange,df_2] , ignore_index=True)
        
        for i in range(1, 11): 
            
            if BILLING_ENABLE_set[i-1] == '1': 
                
                starting_address_i = starting_address_[i]
                
                quantity_i =  quantity_[i]
                
                adjusted_quantity_i = quantity_i - starting_address_i + 1
                data= {'starting_address_i': [starting_address_i], 
                    'quantity_i': [quantity_i], 
                    'adjusted_quantity_i': [adjusted_quantity_i]}
                
                df_2 = pd.DataFrame(data)
                df_pollBilling = pd.concat([df_pollBilling,df_2] , ignore_index=True)
    



        sock_i = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock_i.settimeout(15)

        
        sock_i.connect((tcp_ip, int(tcp_port)))
        print("Connected successfully")
        
            
        dataframes = {
                'address_start': [],
                'finish': [],
                'TX': [],
                'RX': []
            }
        df_Modbus = pd.DataFrame(dataframes)
        df_Modbusbilling = pd.DataFrame(dataframes)
        # print(df_data)
        for i in range(0, len(df_pollRange)):
            
            # print(i)
            start_address = int(df_pollRange.loc[i,'starting_address_i'])
            
            adjusted_quantity = int(df_pollRange.loc[i,'adjusted_quantity_i'])
        

        
            
            request_message_i = bytearray(
            [slave_id, function_code, start_address >> 8, start_address & 0xFF, adjusted_quantity >> 8, adjusted_quantity & 0xFF])
            crc_i = computeCRC(request_message_i)
            request_message_i += crc_i.to_bytes(2, byteorder="big")
            
            
            

            communication_traffic_i = []
        
            
            communication_traffic_i.append(request_message_i.hex())
            
            
           
            sock_i.send(request_message_i)
            time.sleep(3)
            response_i = sock_i.recv(4096)
            
            communication_traffic_i.append(response_i.hex())

            if response_i[1:2] != b'\x03':
                    abort(400, f"Error: Unexpected response code from device {communication_traffic_i[1]}!")
            else:
                    pass

            
                        
            data = {
                'address_start': [int(start_address)],
                'finish': [int(start_address+adjusted_quantity)],
                'TX': [communication_traffic_i[0]],
                'RX': [communication_traffic_i[1]]
            }
            
            df_2 = pd.DataFrame(data)
            df_Modbus = pd.concat([df_Modbus, df_2], ignore_index=True)

            



        for i in range(0, len(df_pollBilling)):
            
            start_address = int(df_pollBilling.loc[i,'starting_address_i'])
            adjusted_quantity = int(df_pollBilling.loc[i,'adjusted_quantity_i'])
        
            request_message_i = bytearray(
            [slave_id, function_code, start_address >> 8, start_address & 0xFF, adjusted_quantity >> 8, adjusted_quantity & 0xFF])
            crc_i = computeCRC(request_message_i)
            request_message_i += crc_i.to_bytes(2, byteorder="big")
            
        
            communication_traffic_i = []
            
            communication_traffic_i.append(request_message_i.hex())
            
            
         
            sock_i.send(request_message_i)
            time.sleep(3)
            response_i = sock_i.recv(4096)
            
            communication_traffic_i.append(response_i.hex())

            if response_i[1:2] != b'\x03':
                    abort(400, f"Error: Unexpected response code from device {communication_traffic_i[1]}!")
            else:
                    pass

            
            # print(communication_traffic_i)
            data = {
                'address_start': [int(start_address)],
                'finish': [int(start_address+adjusted_quantity-1)],
                'TX': [communication_traffic_i[0]],
                'RX': [communication_traffic_i[1]]
            }
            # print(data)
            df_2 = pd.DataFrame(data)
            df_Modbusbilling = pd.concat([df_Modbusbilling, df_2], ignore_index=True)
            
            
            # print(df_2)
            
            
            

            
            query = f"select amc.or_der as order1, amc.address as address1, amc.description as desc1, amc.data_type as dtype1 \
            from amr_mapping_config amc \
            where amc.evc_type = '{evc_type}' AND address is not null \
            order by order1"
            
            cursor = fetch_data(query)
            df_mapping = pd.DataFrame(cursor, columns=['order', 'address', 'desc', 'data_type'])
            

            list_of_values_configured = []
            for i in range(0, len(df_mapping)):
                
                address = int(df_mapping.iloc[i,1])
                
                data_type = str(df_mapping.iloc[i,3])
                
                
                for j in range(0,len(df_Modbus)):
                    address_start = int(df_Modbus.iloc[j,0])
                    address_finish = int(df_Modbus.iloc[j,1])
                    #print(address)
                    if address >= address_start and address <= address_finish:
                        # print(address_start, address_finish, df_Modbus.iloc[j,3])
                        location_data = (address - address_start)*int(8/2)
                        frameRx = (df_Modbus.iloc[j,3])
                        #
                        raw_data = frameRx[location_data + 6: location_data + 14]
                        
                    
                        list_of_values_configured.append(convert_raw_to_value(data_type,raw_data))
                        # print(list_of_values_configured)
                        break
            # value_config = pd.DataFrame(list_of_values_configured,columns=['Value'])
            # result_config = pd.concat([df_mapping, value_config], axis=1)
            # print(result_config)


            
            query = f"SELECT amb.daily ,amb.or_der ,amb.address,amb.description,amb.data_type  FROM amr_mapping_billing amb WHERE amb.evc_type = '{evc_type}' AND address is not null order by amb.daily,amb.or_der"
            cursor = fetch_data(query)
            
            df_mappingbilling = pd.DataFrame(cursor, columns=['daily','or_der', 'address', 'description', 'data_type'])

        

            list_of_values_billing = []
            for i in range(0, len(df_mappingbilling)):
                
                address = int(df_mappingbilling.iloc[i,2])
                
                data_type = str(df_mappingbilling.iloc[i,4])
                
                
                for j in range(0,len(df_Modbusbilling)):
                    address_start = int(df_Modbusbilling.iloc[j,0])
                    address_finish = int(df_Modbusbilling.iloc[j,1])
                
                    if address >= address_start and address <= address_finish:
                    
                        location_data = (address - address_start)*int(8/2)
                        
                        frameRx = (df_Modbusbilling.iloc[j,3])
                    
                        raw_data = frameRx[location_data + 6: location_data + 14]
                        
                        
                        list_of_values_billing.append(convert_raw_to_value(data_type,raw_data))   
                        
                        break
            
            

    
        current_datetime = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=7))).strftime('%d-%b-%y %I.%M.%S.%f %p ASIA/BANGKOK')
        current_datetime_upper = current_datetime.upper()
        date_system = datetime.datetime.now().strftime('%d-%m-%Y')   
        sql_text_config_delete = f"""delete from AMR_CONFIGURED_DATA where METER_ID = '{METERID}' AND METER_STREAM_NO = '{run}' AND DATA_DATE = TO_DATE('{date_system}', 'DD-MM-YYYY')"""
        
        sql_text_config_insert = "insert into AMR_CONFIGURED_DATA (DATA_DATE, METER_ID,METER_STREAM_NO, AMR_VC_TYPE,TIME_CREATE, "
        for i in range(0, len(df_mapping)):  
                
            sql_text_config_insert+=f" AMR_CONFIG{i+1},"
        sql_text_config_insert+=" CREATED_BY) values ("
            
        sql_text_config_insert+=f"TO_DATE('{date_system}', 'DD-MM-YYYY'), '{METERID}','{run}','{evc_type}','{current_datetime_upper}',"
        
            
        for i in range(0, len(df_mapping)):
            
                sql_text_config_insert+=f"'{str(list_of_values_configured[i])}',"
                
        sql_text_config_insert+="'')" 
        # print(sql_text_config_insert)

        get_maxdate =f"SELECT MAX(DATA_DATE) FROM amr_configured_data WHERE meter_id = '{METERID}' AND meter_stream_no = '{run}'"
        
        cursor = fetch_data(get_maxdate)
        config_db = pd.DataFrame(cursor,columns=['DATA_DATE'])
            
        config_db['DATA_DATE'] = pd.to_datetime(config_db['DATA_DATE'])

            # Access the first row and format the date
        config_db_1 = config_db.iloc[0]['DATA_DATE'].strftime('%d-%m-%Y')
        # print(date_system , ":",config_db_1)
        if date_system == config_db_1:
                print("config มีข้อมูลของวันนี้เเล้ว")
                
                config_delete = f"DELETE FROM AMR_CONFIGURED_DATA WHERE DATA_DATE = TO_DATE('{date_system}', 'DD-MM-YYYY') AND METER_ID = '{METERID}' AND METER_STREAM_NO = '{run}' AND AMR_VC_TYPE = '{evc_type}'"
                
                with cx_Oracle.connect(username, password, f"{hostname}:{port}/{service_name}") as connection:
                    with connection.cursor() as cursor:
                        cursor.execute(config_delete)  
                    connection.commit()  
                    print("Insert data 'config_delete' successful")
                    
                with cx_Oracle.connect(username, password, f"{hostname}:{port}/{service_name}") as connection:
                    with connection.cursor() as cursor:
                        cursor.execute(sql_text_config_insert)  
                    connection.commit()  
                    print("Insert data 'config' successful")
                
            

        else:
            
                with cx_Oracle.connect(username, password, f"{hostname}:{port}/{service_name}") as connection:
                    with connection.cursor() as cursor:
                        cursor.execute(sql_text_config_insert)  
                    connection.commit()  
                    print("Insert data 'config' successful")
    
    
    
    
        


        
        sql_texts = []
        for i in range(0, len(df_mappingbilling), 5):
            
                
                values_subset = list_of_values_billing[i:i+5]
                # print(values_subset)
                
                # print(sql_text_billing_delete)
                sql_text_billing_insert = f"INSERT INTO AMR_BILLING_DATA (METER_ID, METER_STREAM_NO, DATA_DATE,TIME_CREATE,UNCORRECTED_VOL ,CORRECTED_VOL, AVR_PF, AVR_TF) VALUES ('{METERID}', '{run}', TO_DATE('{values_subset[0]}', 'DD-MM-YYYY'),"
                

                sql_text_billing_insert += f"'{current_datetime_upper}'"

                for value in values_subset[1:]:
                    sql_text_billing_insert += f", {value}"
                
                sql_text_billing_insert += ");"
            
                sql_text_billing_insert = sql_text_billing_insert.rstrip(',')
                
                sql_texts.append(sql_text_billing_insert)

        full_sql_text = "\n".join(sql_texts)
            
        
        print(full_sql_text)

        with cx_Oracle.connect(username, password, f"{hostname}:{port}/{service_name}") as connection:
                with connection.cursor() as cursor:
                    for sql_statement in full_sql_text.split(";"):
                        if sql_statement.strip():
                            cursor.execute(sql_statement.strip())
                    connection.commit()
                    print("Insert data billing successful")







                    
        query_maxdaily = f"SELECT MAX(DAILY)FROM amr_mapping_billing WHERE evc_type = '{evc_type}'"
        result_maxdaily = fetch_data(query_maxdaily) 
        
        max_daily_value = result_maxdaily[0][0]
        
            # print("max_daily_value",":",max_daily_value)
            
            
        query_maxdaily_1 = f"""SELECT MAX(DAILY)-1 FROM amr_mapping_billing WHERE evc_type = '{evc_type}'"""
        result_maxdaily = fetch_data(query_maxdaily_1) 
        max_daily_value_1 = result_maxdaily[0][0]
        
        
        
        values_subset_1 = list_of_values_billing[0]
        query_maxdate = f"""SELECT DATA_DATE 
                            FROM (
                                SELECT DATA_DATE 
                                FROM amr_billing_data 
                                WHERE data_date = TO_DATE('{values_subset_1}', 'DD-MM-YYYY') 
                                AND meter_id = '{METERID}' 
                                AND meter_stream_no = '{run}' 
                            )
                            WHERE ROWNUM <= 1"""
        maxdate_db = fetch_data(query_maxdate) 
        
        maxdate_billing_1 = pd.DataFrame(maxdate_db)
        
        if maxdate_billing_1.empty:
            maxdate_billing_str_1 = "0-0-0"
            
        else:
            maxdate_billing_1 = maxdate_billing_1.iloc[0]
        
            maxdate_billing_str_1 = maxdate_billing_1.iloc[0].strftime('%d-%m-%Y')
            

        
        
        values_subset = list_of_values_billing[5]
        query_maxdate = f"""SELECT DATA_DATE 
                            FROM (
                                SELECT DATA_DATE 
                                FROM amr_billing_data 
                                WHERE data_date = TO_DATE('{values_subset}', 'DD-MM-YYYY') 
                                AND meter_id = '{METERID}' 
                                AND meter_stream_no = '{run}' 
                            )
                            WHERE ROWNUM <= 1
                            """
        maxdate_db = fetch_data(query_maxdate)
    
        maxdate_billing = pd.DataFrame(maxdate_db)
        maxdate_billing = maxdate_billing.iloc[0]
        maxdate_billing_str = maxdate_billing.iloc[0].strftime('%d-%m-%Y')
        # print(maxdate_billing_str)
        
        
        
        
        # print(values_subset_1 ,":",maxdate_billing_str_1)
        # # # ########### เช็คค่า poll ซ้ำ #####################
        if values_subset_1 == maxdate_billing_str_1:
                
                print("poll ซ้ำ")
                
                query = f"""SELECT  DATA_DATE, CORRECTED_VOL, UNCORRECTED_VOL 
                            FROM amr_billing_data 
                            WHERE DATA_DATE BETWEEN TO_DATE('{values_subset_1}', 'DD-MM-YYYY') - INTERVAL '{max_daily_value}' DAY AND TO_DATE('{values_subset_1}', 'DD-MM-YYYY') 
                            AND meter_id = '{METERID}' 
                            AND meter_stream_no = '{run}' 
                            ORDER BY DATA_DATE DESC"""
                # print(query)
                results_billing = fetch_data(query)
                
                df_billing = pd.DataFrame(results_billing , columns=['DATA_DATE','CORRECTED_VOL', 'UNCORRECTED_VOL'])
                df_billing['DATA_DATE'] = df_billing['DATA_DATE'].dt.strftime('%d-%m-%Y')
                # print(df_billing_1)
                df_billing['DATA_DATE'] = pd.to_datetime(df_billing['DATA_DATE'], format='%d-%m-%Y')
                date_counts = df_billing['DATA_DATE'].value_counts()

                
                single_dates = date_counts[date_counts == 1].index.tolist()

                single_dates_formatted = pd.to_datetime(single_dates).strftime('%d-%m-%Y')
                single_date_rows = df_billing[df_billing['DATA_DATE'].isin(single_dates)]

            
                df_billing = df_billing[~df_billing['DATA_DATE'].isin(single_dates)]
               
                if len(single_dates_formatted) > 0:
                
                    for date_formatted in single_dates_formatted:
                    
                        sql_text_billing_NotMatched = f"""SELECT DATA_DATE, METER_ID, METER_STREAM_NO FROM amr_billing_data_error
                                                        WHERE DATA_DATE = TO_DATE('{date_formatted}', 'DD-MM-YYYY')
                                                        AND METER_ID = '{METERID}' 
                                                        AND METER_STREAM_NO = '{run}'"""
                        
                        billing_NotMatched = fetch_data(sql_text_billing_NotMatched)
                        
                        if len(billing_NotMatched) > 0:
                                print("มีข้อมูล ใน error")
                                sql_text_billing_NotMatched_delete= f"""DELETE FROM AMR_BILLING_DATA 
                                                                WHERE DATA_DATE = TO_DATE('{date_formatted}', 'DD-MM-YYYY') 
                                                                AND METER_ID = '{METERID}' 
                                                                AND METER_STREAM_NO = '{run}'"""
                            
                                with cx_Oracle.connect(username, password, f"{hostname}:{port}/{service_name}") as connection:
                                        with connection.cursor() as cursor:
                                            cursor.execute(sql_text_billing_NotMatched_delete)
                                            connection.commit()
                                            print("Deleted 'Not' Matched data from billing successfully")
                                
                                
                        else:
                                print("ไม่มีข้อมูล ใน error ")
                                print("insert poll เรียบร้อย")
                                
                                
                    for i in range(0, len(df_billing), 2):
                            db_test_matched = df_billing[i:i+2] 
                                    # print(db_test_matched)
                            db_test_matched['DATA_DATE'] = pd.to_datetime(db_test_matched['DATA_DATE']).dt.strftime('%d-%m-%Y')
                            if db_test_matched['DATA_DATE'].nunique() == 1 and db_test_matched['CORRECTED_VOL'].nunique() == 1 and db_test_matched['UNCORRECTED_VOL'].nunique() == 1:
                                                print("Matched:", db_test_matched)
                                                TIME_CREATE_MAX = f"""SELECT MAX(TIME_CREATE) AS MAX_TIME_CREATE FROM amr_billing_data WHERE DATA_DATE = TO_DATE('{db_test_matched['DATA_DATE'].iloc[0]}', 'DD-MM-YYYY') 
                                                                            AND CORRECTED_VOL = {db_test_matched['CORRECTED_VOL'].iloc[0]} 
                                                                            AND UNCORRECTED_VOL = {db_test_matched['UNCORRECTED_VOL'].iloc[0]} 
                                                                            AND METER_ID = '{METERID}' 
                                                                            AND METER_STREAM_NO = '{run}'"""
                                                MAX_TIME_CREATE = fetch_data(TIME_CREATE_MAX)
                                                MAX_TIME_CREATE_ALL = MAX_TIME_CREATE[0][0]
                                                
                                                sql_text_billing_matched_delete= f"""DELETE FROM AMR_BILLING_DATA 
                                                                            WHERE DATA_DATE = TO_DATE('{db_test_matched['DATA_DATE'].iloc[0]}', 'DD-MM-YYYY') 
                                                                            AND CORRECTED_VOL = {db_test_matched['CORRECTED_VOL'].iloc[0]} 
                                                                            AND UNCORRECTED_VOL = {db_test_matched['UNCORRECTED_VOL'].iloc[0]} 
                                                                            AND METER_ID = '{METERID}' 
                                                                            AND METER_STREAM_NO = '{run}'
                                                                            AND TIME_CREATE = '{MAX_TIME_CREATE_ALL}'"""
                                                # print(sql_text_billing_matched_delete)
                                                # print(sql_text_billing_matched_delete)
                                                with cx_Oracle.connect(username, password, f"{hostname}:{port}/{service_name}") as connection:
                                                    with connection.cursor() as cursor:
                                                        cursor.execute(sql_text_billing_matched_delete)
                                                        connection.commit()
                                                        print("Deleted matched data from billing successfully")  
                                            
                                            
                                            
                            else:
                                    print("Not Matched:", db_test_matched)
                                    query = f"""SELECT   DATA_DATE, CORRECTED_VOL, UNCORRECTED_VOL, AVR_PF, AVR_TF 
                                                FROM amr_billing_data 
                                                WHERE DATA_DATE = TO_DATE('{db_test_matched['DATA_DATE'].iloc[0]}', 'DD-MM-YYYY') 
                                                AND meter_id = '{METERID}' 
                                                AND meter_stream_no = '{run}' 
                                                ORDER BY DATA_DATE DESC"""
                                    
                                
                                    results_billing = fetch_data(query)
                                    
                                    for row in results_billing:
                                            pass
                                
                                    sql_texts = []
                                    
                                    for row in results_billing:
                                        formatted_date = row[0].strftime('%d-%m-%Y')  
                                        sql_text_billing_insert = f"INSERT INTO AMR_BILLING_DATA_ERROR (METER_ID, METER_STREAM_NO, DATA_DATE, CORRECTED_VOL, UNCORRECTED_VOL, AVR_PF, AVR_TF) VALUES "
                                        sql_text_billing_insert += f"('{METERID}', '{run}', TO_DATE('{formatted_date}', 'DD-MM-YYYY')"
                                        sql_text_billing_insert += f", '{row[1]}', '{row[2]}', '{row[3]}', '{row[4]}');"
                                        sql_texts.append(sql_text_billing_insert)

                                    full_sql_text = "\n".join(sql_texts)
                                    with cx_Oracle.connect(username, password, f"{hostname}:{port}/{service_name}") as connection:
                                        with connection.cursor() as cursor:
                                            for sql_statement in full_sql_text.split(";"):
                                                if sql_statement.strip():
                                                    cursor.execute(sql_statement.strip())
                                            connection.commit()
                                            print("Insert data ERROR successful")
                                    
                                    sql_text_billing_NotMatched_delete= f"""DELETE FROM AMR_BILLING_DATA 
                                                                WHERE DATA_DATE = TO_DATE('{db_test_matched['DATA_DATE'].iloc[0]}', 'DD-MM-YYYY') 
                                                                AND METER_ID = '{METERID}' 
                                                                AND METER_STREAM_NO = '{run}'
                                                                """
                                    with cx_Oracle.connect(username, password, f"{hostname}:{port}/{service_name}") as connection:
                                        with connection.cursor() as cursor:
                                            cursor.execute(sql_text_billing_NotMatched_delete)
                                            connection.commit()
                                            print("Deleted 'Not' Matched data from billing successfully")  
                                    
                else:
                            for i in range(0, len(df_billing), 2):
                                db_test_matched = df_billing[i:i+2] 
                                        # print(db_test_matched)
                                db_test_matched['DATA_DATE'] = pd.to_datetime(db_test_matched['DATA_DATE']).dt.strftime('%d-%m-%Y')
                                if db_test_matched['DATA_DATE'].nunique() == 1 and db_test_matched['CORRECTED_VOL'].nunique() == 1 and db_test_matched['UNCORRECTED_VOL'].nunique() == 1:
                                                    print("Matched:", db_test_matched)
                                                    TIME_CREATE_MAX = f"""SELECT MAX(TIME_CREATE) AS MAX_TIME_CREATE FROM amr_billing_data WHERE DATA_DATE = TO_DATE('{db_test_matched['DATA_DATE'].iloc[0]}', 'DD-MM-YYYY') 
                                                                            AND CORRECTED_VOL = {db_test_matched['CORRECTED_VOL'].iloc[0]} 
                                                                            AND UNCORRECTED_VOL = {db_test_matched['UNCORRECTED_VOL'].iloc[0]} 
                                                                            AND METER_ID = '{METERID}' 
                                                                            AND METER_STREAM_NO = '{run}'"""
                                                    MAX_TIME_CREATE = fetch_data(TIME_CREATE_MAX)
                                                    MAX_TIME_CREATE_ALL = MAX_TIME_CREATE[0][0]
                                                    sql_text_billing_matched_delete= f"""DELETE FROM AMR_BILLING_DATA 
                                                                                WHERE DATA_DATE = TO_DATE('{db_test_matched['DATA_DATE'].iloc[0]}', 'DD-MM-YYYY') 
                                                                                AND CORRECTED_VOL = {db_test_matched['CORRECTED_VOL'].iloc[0]} 
                                                                                AND UNCORRECTED_VOL = {db_test_matched['UNCORRECTED_VOL'].iloc[0]} 
                                                                                AND METER_ID = '{METERID}' 
                                                                                AND METER_STREAM_NO = '{run}'
                                                                                AND TIME_CREATE = '{MAX_TIME_CREATE_ALL}'"""
                                                    # print(sql_text_billing_matched_delete)
                                                    with cx_Oracle.connect(username, password, f"{hostname}:{port}/{service_name}") as connection:
                                                        with connection.cursor() as cursor:
                                                            cursor.execute(sql_text_billing_matched_delete)
                                                            connection.commit()
                                                            print("Deleted matched data from billing successfully")  
                                                
                                                
                                                
                                else:
                                        print("Not Matched:", db_test_matched)
                                        query = f"""SELECT   DATA_DATE, CORRECTED_VOL, UNCORRECTED_VOL, AVR_PF, AVR_TF 
                                                    FROM amr_billing_data 
                                                    WHERE DATA_DATE = TO_DATE('{db_test_matched['DATA_DATE'].iloc[0]}', 'DD-MM-YYYY') 
                                                    AND meter_id = '{METERID}' 
                                                    AND meter_stream_no = '{run}' 
                                                    ORDER BY DATA_DATE DESC"""
                                        
                                        
                                        results_billing = fetch_data(query)
                                    
                                        for row in results_billing:
                                                print(row) 
                                    
                                        sql_texts = []
                                        
                                        for row in results_billing:
                                            formatted_date = row[0].strftime('%d-%m-%Y')  
                                            sql_text_billing_insert = f"INSERT INTO AMR_BILLING_DATA_ERROR (METER_ID, METER_STREAM_NO, DATA_DATE, CORRECTED_VOL, UNCORRECTED_VOL, AVR_PF, AVR_TF) VALUES "
                                            sql_text_billing_insert += f"('{METERID}', '{run}', TO_DATE('{formatted_date}', 'DD-MM-YYYY')"
                                            sql_text_billing_insert += f", '{row[1]}', '{row[2]}', '{row[3]}', '{row[4]}');"
                                            sql_texts.append(sql_text_billing_insert)

                                        full_sql_text = "\n".join(sql_texts)
                                        with cx_Oracle.connect(username, password, f"{hostname}:{port}/{service_name}") as connection:
                                            with connection.cursor() as cursor:
                                                for sql_statement in full_sql_text.split(";"):
                                                    if sql_statement.strip():
                                                        cursor.execute(sql_statement.strip())
                                                connection.commit()
                                                print("Insert data ERROR successful")
                                        
                                        
                                        
                                        
                                        
                                        
                                        
                                        sql_text_billing_NotMatched_delete= f"""DELETE FROM AMR_BILLING_DATA 
                                                                    WHERE DATA_DATE = TO_DATE('{db_test_matched['DATA_DATE'].iloc[0]}', 'DD-MM-YYYY') 
                                                                    AND METER_ID = '{METERID}' 
                                                                    AND METER_STREAM_NO = '{run}'
                                                                    """
                                        with cx_Oracle.connect(username, password, f"{hostname}:{port}/{service_name}") as connection:
                                            with connection.cursor() as cursor:
                                                cursor.execute(sql_text_billing_NotMatched_delete)
                                                connection.commit()
                                                print("Deleted 'Not' Matched data from billing successfully")
            
            
            
            
        
        
        
        
        
        
        
        
        
        # ########### เช็คค่า poll ปกติ #####################
        else:
                    
            if values_subset == maxdate_billing_str:
                print(values_subset ,":",maxdate_billing_str)
                print("ปกติ")
                
                query = f"""SELECT  DATA_DATE, CORRECTED_VOL, UNCORRECTED_VOL 
                            FROM amr_billing_data 
                            WHERE DATA_DATE BETWEEN TO_DATE('{values_subset}', 'DD-MM-YYYY') - INTERVAL '{max_daily_value}' DAY AND TO_DATE('{values_subset}', 'DD-MM-YYYY') 
                            AND meter_id = '{METERID}' 
                            AND meter_stream_no = '{run}' 
                            ORDER BY DATA_DATE DESC"""
            
                
                results_billing = fetch_data(query)
                
                df_billing = pd.DataFrame(results_billing , columns=['DATA_DATE','CORRECTED_VOL', 'UNCORRECTED_VOL'])
                df_billing['DATA_DATE'] = df_billing['DATA_DATE'].dt.strftime('%d-%m-%Y')
                df_billing['DATA_DATE'] = pd.to_datetime(df_billing['DATA_DATE'], format='%d-%m-%Y')
                date_counts = df_billing['DATA_DATE'].value_counts()

                
                single_dates = date_counts[date_counts == 1].index.tolist()

                single_dates_formatted = pd.to_datetime(single_dates).strftime('%d-%m-%Y')
                single_date_rows = df_billing[df_billing['DATA_DATE'].isin(single_dates)]

            
                df_billing = df_billing[~df_billing['DATA_DATE'].isin(single_dates)]
                
                if len(single_dates_formatted) > 0:
                    # print(single_dates_formatted)
                    for date_formatted in single_dates_formatted:
                    
                        sql_text_billing_NotMatched = f"""SELECT DATA_DATE, METER_ID, METER_STREAM_NO FROM amr_billing_data_error
                                                        WHERE DATA_DATE = TO_DATE('{date_formatted}', 'DD-MM-YYYY')
                                                        AND METER_ID = '{METERID}' 
                                                        AND METER_STREAM_NO = '{run}'"""
                        
                        billing_NotMatched = fetch_data(sql_text_billing_NotMatched)
                        
                        if len(billing_NotMatched) > 0:
                                # print("มีข้อมูล ใน error")
                                sql_text_billing_NotMatched_delete= f"""DELETE FROM AMR_BILLING_DATA 
                                                                WHERE DATA_DATE = TO_DATE('{date_formatted}', 'DD-MM-YYYY') 
                                                                AND METER_ID = '{METERID}' 
                                                                AND METER_STREAM_NO = '{run}'"""
                                # print(sql_text_billing_NotMatched_delete)
                                with cx_Oracle.connect(username, password, f"{hostname}:{port}/{service_name}") as connection:
                                        with connection.cursor() as cursor:
                                            cursor.execute(sql_text_billing_NotMatched_delete)
                                            connection.commit()
                                            print("Deleted 'Not' Matched data from billing successfully")
                                
                                
                        else:
                                print("ไม่มีข้อมูล ใน error ")
                                print("insert poll เรียบร้อย")
                                
                                
                    for i in range(0, len(df_billing), 2):
                            db_test_matched = df_billing[i:i+2] 
                                    # print(db_test_matched)
                            db_test_matched['DATA_DATE'] = pd.to_datetime(db_test_matched['DATA_DATE']).dt.strftime('%d-%m-%Y')
                            if db_test_matched['DATA_DATE'].nunique() == 1 and db_test_matched['CORRECTED_VOL'].nunique() == 1 and db_test_matched['UNCORRECTED_VOL'].nunique() == 1:
                                                print("Matched:", db_test_matched)
                                                TIME_CREATE_MAX = f"""SELECT MAX(TIME_CREATE) AS MAX_TIME_CREATE FROM amr_billing_data WHERE DATA_DATE = TO_DATE('{db_test_matched['DATA_DATE'].iloc[0]}', 'DD-MM-YYYY') 
                                                                            AND CORRECTED_VOL = {db_test_matched['CORRECTED_VOL'].iloc[0]} 
                                                                            AND UNCORRECTED_VOL = {db_test_matched['UNCORRECTED_VOL'].iloc[0]} 
                                                                            AND METER_ID = '{METERID}' 
                                                                            AND METER_STREAM_NO = '{run}'"""
                                                MAX_TIME_CREATE = fetch_data(TIME_CREATE_MAX)
                                                MAX_TIME_CREATE_ALL = MAX_TIME_CREATE[0][0]
                                                print(MAX_TIME_CREATE_ALL)
                                                sql_text_billing_matched_delete= f"""DELETE FROM AMR_BILLING_DATA 
                                                                            WHERE DATA_DATE = TO_DATE('{db_test_matched['DATA_DATE'].iloc[0]}', 'DD-MM-YYYY') 
                                                                            AND CORRECTED_VOL = {db_test_matched['CORRECTED_VOL'].iloc[0]} 
                                                                            AND UNCORRECTED_VOL = {db_test_matched['UNCORRECTED_VOL'].iloc[0]} 
                                                                            AND METER_ID = '{METERID}' 
                                                                            AND METER_STREAM_NO = '{run}'
                                                                            
                                                                            AND TIME_CREATE = '{MAX_TIME_CREATE_ALL}'"""
                                                # print(sql_text_billing_matched_delete)
                                                # print(sql_text_billing_matched_delete)
                                                with cx_Oracle.connect(username, password, f"{hostname}:{port}/{service_name}") as connection:
                                                    with connection.cursor() as cursor:
                                                        cursor.execute(sql_text_billing_matched_delete)
                                                        connection.commit()
                                                        print("Deleted matched data from billing successfully")  
                                            
                                            
                                            
                            else:
                                    # print("Not Matched:", db_test_matched)
                                    query = f"""SELECT   DATA_DATE, CORRECTED_VOL, UNCORRECTED_VOL, AVR_PF, AVR_TF 
                                                FROM amr_billing_data 
                                                WHERE DATA_DATE = TO_DATE('{db_test_matched['DATA_DATE'].iloc[0]}', 'DD-MM-YYYY') 
                                                AND meter_id = '{METERID}' 
                                                AND meter_stream_no = '{run}' 
                                                ORDER BY DATA_DATE DESC"""
                                    
                                
                                    results_billing = fetch_data(query)
                                    
                                    for row in results_billing:
                                            print(row) 
                                
                                    sql_texts = []
                                    
                                    for row in results_billing:
                                        formatted_date = row[0].strftime('%d-%m-%Y')  
                                        sql_text_billing_insert = f"INSERT INTO AMR_BILLING_DATA_ERROR (METER_ID, METER_STREAM_NO, DATA_DATE, CORRECTED_VOL, UNCORRECTED_VOL, AVR_PF, AVR_TF) VALUES "
                                        sql_text_billing_insert += f"('{METERID}', '{run}', TO_DATE('{formatted_date}', 'DD-MM-YYYY')"
                                        sql_text_billing_insert += f", '{row[1]}', '{row[2]}', '{row[3]}', '{row[4]}');"
                                        sql_texts.append(sql_text_billing_insert)

                                    full_sql_text = "\n".join(sql_texts)
                                    with cx_Oracle.connect(username, password, f"{hostname}:{port}/{service_name}") as connection:
                                        with connection.cursor() as cursor:
                                            for sql_statement in full_sql_text.split(";"):
                                                if sql_statement.strip():
                                                    cursor.execute(sql_statement.strip())
                                            connection.commit()
                                            print("Insert data ERROR successful")
                                    
                                    sql_text_billing_NotMatched_delete= f"""DELETE FROM AMR_BILLING_DATA 
                                                                WHERE DATA_DATE = TO_DATE('{db_test_matched['DATA_DATE'].iloc[0]}', 'DD-MM-YYYY') 
                                                                AND METER_ID = '{METERID}' 
                                                                AND METER_STREAM_NO = '{run}'
                                                                """
                                    with cx_Oracle.connect(username, password, f"{hostname}:{port}/{service_name}") as connection:
                                        with connection.cursor() as cursor:
                                            cursor.execute(sql_text_billing_NotMatched_delete)
                                            connection.commit()
                                            print("Deleted 'Not' Matched data from billing successfully")  
                                    
            else:
                        
                    for i in range(0, len(df_billing), 2):
                            db_test_matched = df_billing[i:i+2] 
                                    # print(db_test_matched)
                            db_test_matched['DATA_DATE'] = pd.to_datetime(db_test_matched['DATA_DATE']).dt.strftime('%d-%m-%Y')
                            if db_test_matched['DATA_DATE'].nunique() == 1 and db_test_matched['CORRECTED_VOL'].nunique() == 1 and db_test_matched['UNCORRECTED_VOL'].nunique() == 1:
                                                print("Matched:", db_test_matched)
                                                TIME_CREATE_MAX = f"""SELECT MAX(TIME_CREATE) AS MAX_TIME_CREATE FROM amr_billing_data WHERE DATA_DATE = TO_DATE('{db_test_matched['DATA_DATE'].iloc[0]}', 'DD-MM-YYYY') 
                                                                            AND CORRECTED_VOL = {db_test_matched['CORRECTED_VOL'].iloc[0]} 
                                                                            AND UNCORRECTED_VOL = {db_test_matched['UNCORRECTED_VOL'].iloc[0]} 
                                                                            AND METER_ID = '{METERID}' 
                                                                            AND METER_STREAM_NO = '{run}'"""
                                                MAX_TIME_CREATE = fetch_data(TIME_CREATE_MAX)
                                                MAX_TIME_CREATE_ALL = MAX_TIME_CREATE[0][0]
                                                
                                                sql_text_billing_matched_delete= f"""DELETE FROM AMR_BILLING_DATA 
                                                                            WHERE DATA_DATE = TO_DATE('{db_test_matched['DATA_DATE'].iloc[0]}', 'DD-MM-YYYY') 
                                                                            AND CORRECTED_VOL = {db_test_matched['CORRECTED_VOL'].iloc[0]} 
                                                                            AND UNCORRECTED_VOL = {db_test_matched['UNCORRECTED_VOL'].iloc[0]} 
                                                                            AND METER_ID = '{METERID}' 
                                                                            AND METER_STREAM_NO = '{run}'
                                                                            AND TIME_CREATE = '{MAX_TIME_CREATE_ALL}'"""
                                                # print(sql_text_billing_matched_delete)
                                                with cx_Oracle.connect(username, password, f"{hostname}:{port}/{service_name}") as connection:
                                                    with connection.cursor() as cursor:
                                                        cursor.execute(sql_text_billing_matched_delete)
                                                        connection.commit()
                                                        print("Deleted matched data from billing successfully")  
                                            
                                            
                                            
                            else:
                                    print("Not Matched:", db_test_matched)
                                    query = f"""SELECT   DATA_DATE, CORRECTED_VOL, UNCORRECTED_VOL, AVR_PF, AVR_TF 
                                                FROM amr_billing_data 
                                                WHERE DATA_DATE = TO_DATE('{db_test_matched['DATA_DATE'].iloc[0]}', 'DD-MM-YYYY') 
                                                AND meter_id = '{METERID}' 
                                                AND meter_stream_no = '{run}' 
                                                ORDER BY DATA_DATE DESC"""
                                    
                                    
                                    results_billing = fetch_data(query)
                                    
                                    for row in results_billing:
                                            print(row) 
                                
                                    sql_texts = []
                                    
                                    for row in results_billing:
                                        formatted_date = row[0].strftime('%d-%m-%Y')  
                                        sql_text_billing_insert = f"INSERT INTO AMR_BILLING_DATA_ERROR (METER_ID, METER_STREAM_NO, DATA_DATE, CORRECTED_VOL, UNCORRECTED_VOL, AVR_PF, AVR_TF) VALUES "
                                        sql_text_billing_insert += f"('{METERID}', '{run}', TO_DATE('{formatted_date}', 'DD-MM-YYYY')"
                                        sql_text_billing_insert += f", '{row[1]}', '{row[2]}', '{row[3]}', '{row[4]}');"
                                        sql_texts.append(sql_text_billing_insert)

                                    full_sql_text = "\n".join(sql_texts)
                                    with cx_Oracle.connect(username, password, f"{hostname}:{port}/{service_name}") as connection:
                                        with connection.cursor() as cursor:
                                            for sql_statement in full_sql_text.split(";"):
                                                if sql_statement.strip():
                                                    cursor.execute(sql_statement.strip())
                                            connection.commit()
                                            print("Insert data ERROR successful")
                                    
                                    
                                    
                                    
                                    
                                    
                                    
                                    sql_text_billing_NotMatched_delete= f"""DELETE FROM AMR_BILLING_DATA 
                                                                WHERE DATA_DATE = TO_DATE('{db_test_matched['DATA_DATE'].iloc[0]}', 'DD-MM-YYYY') 
                                                                AND METER_ID = '{METERID}' 
                                                                AND METER_STREAM_NO = '{run}'
                                                                """
                                    with cx_Oracle.connect(username, password, f"{hostname}:{port}/{service_name}") as connection:
                                        with connection.cursor() as cursor:
                                            cursor.execute(sql_text_billing_NotMatched_delete)
                                            connection.commit()
                                            print("Deleted 'Not' Matched data from billing successfully")








        
        print(f"ชุดที่ {completed_sets} เสร็จสิ้นแล้ว\n")
    except Exception as e:
        current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        tcp_ip = row[6]
        tcp_port = row[7]
        run = row[3]
        METERID = row[4]
        
        error_message = f"Error occurred at {current_time} - TCP IP: {tcp_ip}, Port: {tcp_port}, Run: {run}, METERID: {METERID}. Error: {e}"
        logging.error(error_message)
        traceback.print_exc()
        continue
    
if __name__ == '__main__':
    
    exit()