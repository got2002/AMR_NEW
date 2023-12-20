from flask import Flask, render_template, request, redirect, url_for, flash
import os
import cx_Oracle

app = Flask(__name__)

# Database connection details
username = 'root'
password = 'root'
hostname = '192.168.102.192'
port = '1521'
service_name = 'orcl'

# Set the Flask secret key from the environment variable
app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'fallback_secret_key')

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

        query = 'INSERT INTO AMR_USER (description, user_name, password, user_level) VALUES (:1, :2, :3, :4)'
        params = (description, user_name, password, user_level)

        if execute_query(query, params):
            flash('User added successfully!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Failed to add user. Please try again.', 'error')

    return render_template('add_user.html')

if __name__ == '__main__':
    app.run(debug=True)
