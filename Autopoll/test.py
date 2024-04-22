
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
    start_time = time.time()
        
    run = row[3]
    METERID = row[4]
    print(METERID)
    deleted_rows = []

    delete_DB = f"""DELETE FROM amr_billing_data
                    WHERE ROWID IN (
                        SELECT rid FROM (
                            SELECT ROWID rid,
                                ROW_NUMBER() OVER (PARTITION BY DATA_DATE ORDER BY DATA_DATE) AS RowNumber
                            FROM amr_billing_data 
                            WHERE meter_id = '{METERID}' AND meter_stream_no = '{run}'
                        ) WHERE RowNumber > 1
                    )"""
                    
    try:
        with cx_Oracle.connect(username, password, f"{hostname}:{port}/{service_name}") as connection:
            with connection.cursor() as cursor:
                cursor.execute(delete_DB)
                deleted_rows = cursor.rowcount 
                connection.commit()
        
        print(f"จำนวนแถวที่ถูกลบ: {deleted_rows} rows")
        
      
        
    except Exception as e:
        print(f"เกิดข้อผิดพลาดในการลบข้อมูล: {e}")
        continue  
    

if __name__ == '__main__':
    
    exit()