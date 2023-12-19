from flask import Flask, render_template
import cx_Oracle

app = Flask(__name__)

# Database connection information
username = 'root'
password = 'root'
hostname = 'localhost'
port = '1521'
service_name = 'orcl'


def fetch_data(query):
    try:
        dsn = cx_Oracle.makedsn(hostname, port, service_name)
        with cx_Oracle.connect(username, password, dsn) as connection:
            with connection.cursor() as cursor:
                cursor.execute(query)
                results = cursor.fetchall()
        return results
    except cx_Oracle.Error as e:
        error, = e.args
        print("Oracle Error:", error)
        return []


@app.route('/')
def index():
    try:
        # Create connection
        dsn = cx_Oracle.makedsn(hostname, port, service_name)

        with cx_Oracle.connect(username, password, dsn) as connection:
            # Create cursor
            with connection.cursor() as cursor:
                # Execute SQL query
                cursor.execute("SELECT * FROM AMR_REGION")

                # Fetch all rows
                results = cursor.fetchall()

                # Execute SQL query to fetch data for the "SITE" dropdown
                cursor.execute("SELECT * FROM AMR_FIELD_ID")

                # Fetch all rows for "SITE"
                site_results = cursor.fetchall()
                cursor.execute("SELECT * FROM AMR_BILLING_DATA FETCH FIRST 10 ROWS ONLY")
                data = cursor.fetchall()
                column_names = [desc[0] for desc in cursor.description]
    # ดึงชื่อคอลัมน์
                


    except cx_Oracle.Error as e:
        error, = e.args
        print("Oracle Error:", error)
        results = []
        site_results = []
        data = []
        column_names = []


    # Render the HTML template with the retrieved data
    return render_template('index.html', results=results, site_results=site_results, data=data, column_names=column_names)


if __name__ == '__main__':
    app.run(debug=True)
