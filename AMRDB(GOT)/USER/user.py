from flask import Flask, render_template, request, redirect, url_for, flash
import os
import cx_Oracle
import hashlib

app = Flask(__name__)

# Database connection details
username = 'root'
password = 'root'
hostname = '192.168.102.192'
port = '1521'
service_name = 'orcl'

# Set the Flask secret key from the environment variable
app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'fallback_secret_key')

def md5_hash(input_string):
    # เข้ารหัสรหัสผ่านโดยใช้ MD5
    return hashlib.md5(input_string.encode()).hexdigest()

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

def execute_query(query, params=None):
    try:
        dsn = cx_Oracle.makedsn(hostname, port, service_name)
        with cx_Oracle.connect(username, password, dsn) as connection:
            with connection.cursor() as cursor:
                if params:
                    cursor.execute(query, params)
                else:
                    cursor.execute(query)
                connection.commit()
        return True
    except cx_Oracle.Error as e:
        error, = e.args
        print("Oracle Error:", error)
        return False

# User list page
@app.route('/')
def index():
    query = 'SELECT * FROM AMR_USER'
    users = fetch_data(query)
    return render_template('user.html', users=users)

# Add user page
@app.route('/add_user', methods=['GET', 'POST'])
def add_user_route():
    if request.method == 'POST':
        description = request.form['description']
        user_name = request.form['user_name']
        password = request.form['password']
        user_level = request.form['user_level']

        # เข้ารหัสรหัสผ่านโดยใช้ MD5
        hashed_password = md5_hash(password)

        # แปลงเป็น RAWTOHEX ก่อนที่จะบันทึกลงใน Oracle
        hashed_password_hex = "RAWTOHEX(DBMS_OBFUSCATION_TOOLKIT.MD5(input_string => UTL_I18N.STRING_TO_RAW('{}', 'AL32UTF8')))".format(hashed_password)

        query = 'INSERT INTO AMR_USER (description, user_name, password, user_level) VALUES (:1, :2, {}, :4)'.format(hashed_password_hex)
        params = (description, user_name, user_level)

        if execute_query(query, params):
            flash('User added successfully!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Failed to add user. Please try again.', 'error')

    return render_template('add_user.html')

# Edit user page
@app.route('/edit_user', methods=['GET', 'POST'])
def edit_user_route():
    # ดึงข้อมูลผู้ใช้จากฐานข้อมูลตาม user_id
    query = 'SELECT * FROM AMR_USER'
    user_data = fetch_data(query, ())

    if not user_data:
        flash('User not found!', 'error')
        return redirect(url_for('index'))

    # ถ้ามีการส่งค่า POST (คือการบันทึกการแก้ไข)
    if request.method == 'POST':
        # ดึงข้อมูลจากฟอร์มแก้ไข
        description = request.form['description']
        user_name = request.form['user_name']
        password = request.form['password']
        user_level = request.form['user_level']

        # เข้ารหัสรหัสผ่านโดยใช้ MD5
        hashed_password = md5_hash(password)

        # แปลงเป็น RAWTOHEX ก่อนที่จะบันทึกลงใน Oracle
        hashed_password_hex = "RAWTOHEX(DBMS_OBFUSCATION_TOOLKIT.MD5(input_string => UTL_I18N.STRING_TO_RAW('{}', 'AL32UTF8')))".format(hashed_password)

        # สร้างคำสั่ง SQL สำหรับการแก้ไขข้อมูลผู้ใช้
        update_query = 'UPDATE AMR_USER SET description = :1, user_name = :2, password = {}, user_level = :4 WHERE user_id = :5'.format(hashed_password_hex)
        update_params = (description, user_name, user_level, user_id)

        # ทำการ execute คำสั่ง SQL และ commit การแก้ไข
        if execute_query(update_query, update_params):
            flash('User updated successfully!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Failed to update user. Please try again.', 'error')

    # ถ้าไม่มีการส่งค่า POST (แสดงหน้าแก้ไข)
    return render_template('edit_user.html', user=user_data[0])


if __name__ == '__main__':
    app.run(debug=True)
