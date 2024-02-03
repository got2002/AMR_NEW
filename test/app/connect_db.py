from flask import Blueprint
import cx_Oracle

connect_db = Blueprint('connect_db', __name__)




username = "root"
password = "root"
hostname = "192.168.102.192"
port = "1521"
service_name = "orcl"
pool_min = 1
pool_max = 5
pool_inc = 1
pool_gmd = 0
connection_pool = cx_Oracle.SessionPool(
    user=username,
    password=password,
    dsn=cx_Oracle.makedsn(hostname, port, service_name),
    min=pool_min,
    max=pool_max,
    increment=pool_inc,
    getmode=pool_gmd
)
def fetch_data(query, params=None):
    try:
        # Acquire a connection from the pool
        connection = connection_pool.acquire()
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
    finally:
        # Release the connection back to the pool
        connection_pool.release(connection)
