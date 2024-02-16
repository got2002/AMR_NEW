from flask import Flask, render_template, request, redirect, url_for
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

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    if username == '1' and password == '1':
        return render_template('dashboard.html')
    else:
        return 'Login failed'

@app.route('/dashboard')
def dashboard_page():
    # นี่คือหน้าหลักหลัง login
    return render_template('dashboard.html')

if __name__ == '__main__':
    app.run(debug=True)