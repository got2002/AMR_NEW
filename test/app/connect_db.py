from flask import Blueprint
import cx_Oracle

connect_db = Blueprint('connect_db', __name__)


active_connection = None  # Global variable to track the active connection

def connect_to_amr_db():
    global active_connection
    username = "AMR_DB"
    password = "AMR_DB"
    hostname = "10.104.240.26"
    port = "1521"
    sid = "AMR"

    try:
        dsn = cx_Oracle.makedsn(hostname, port, sid)
        connection = cx_Oracle.connect(username, password, dsn)
        active_connection = "AMR_DB"
        print("Connected to AMR database")
        return connection
    except cx_Oracle.Error as e:
        (error,) = e.args
        print("Oracle Error:", error)
        return None

def connect_to_ptt_pivot_db():
    global active_connection
    username = "PTT_PIVOT"
    password = "PTT_PIVOT"
    hostname = "10.100.56.3"
    port = "1521"
    service_name = "PTTAMR_MST"

    try:
        dsn = cx_Oracle.makedsn(hostname, port, service_name=service_name)
        connection = cx_Oracle.connect(username, password, dsn)
        active_connection = "PTT_PIVOT"
        print("Connected to PTT PIVOT database")
        return connection
    except cx_Oracle.Error as e:
        (error,) = e.args
        print("Oracle Error:", error)
        return None

def fetch_data(connection, query, params=None):
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