from flask import Flask, render_template, request, jsonify
import cx_Oracle

app = Flask(__name__)

# Replace these values with your Oracle credentials
oracle_username = "root"
oracle_password = "root"
oracle_host = "192.168.102.192"
oracle_port = "1521"
oracle_service = "orcl"

dsn = cx_Oracle.makedsn(oracle_host, oracle_port, service_name=oracle_service)
connection = cx_Oracle.connect(user=oracle_username, password=oracle_password, dsn=dsn)
cursor = connection.cursor()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/save_to_oracle', methods=['POST'])
def save_to_oracle():
    poll_config_value = None  # Define the variable outside the try block
# Test
    try:
        data = request.get_json()

        # Create a list of addresses
        addresses = [
            str(data.get(7001, '')),
            str(data.get(7005, '')),
            str(data.get(7007, '')),
            str(data.get(7009, '')),
            str(data.get(7011, '')),
            str(data.get(7013, '')),
            str(data.get(7015, '')),
            str(data.get(7017, '')),
            str(data.get(7019, '')),
            str(data.get(7021, '')),
            str(data.get(7023, '')),
            str(data.get(7025, '')),
            str(data.get(7027, '')),
            str(data.get(7065, '')),
        ]

        # Remove empty strings from the list
        addresses = [address for address in addresses if address]

        # Assume that the value you want to add to POLL_CONFIG is the list of addresses
        poll_config_value = addresses

        sql = "INSERT INTO AMR_POLL_RANGE (POLL_CONFIG) VALUES (:poll_config_value)"
        cursor.execute(sql, {'poll_config_value': poll_config_value})
        connection.commit()

        response = {'message': 'Data saved successfully'}
    except Exception as e:
        response = {'message': f'Error: {e}'}
    finally:
        if poll_config_value is not None:
            # Do not close connection and cursor within this block
            pass

    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
