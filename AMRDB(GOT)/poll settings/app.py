from flask import Flask, render_template, request, jsonify
import cx_Oracle
import json

app = Flask(__name__)

# Replace these values with your Oracle credentials
oracle_username = "root"
oracle_password = "root"
oracle_host = "192.168.102.192"
oracle_port = "1521"
oracle_service = "orcl"

def generate_address_range(start, end):
    # Generate a range of addresses from start to end
    address_range = list(range(int(start), int(end) + 1))
    return address_range

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/save_to_oracle', methods=['POST'])
def save_to_oracle():
    try:
        data = request.get_json()

        # Extract start and end addresses from the JSON data
        start_address = data.get('start', '')
        end_address = data.get('end', '')

        # Generate the address range as a list of integers
        address_range = generate_address_range(start_address, end_address)

        # Convert the list of addresses to a JSON array string
        poll_config_values = json.dumps(address_range)

        dsn = cx_Oracle.makedsn(oracle_host, oracle_port, service_name=oracle_service)

        with cx_Oracle.connect(user=oracle_username, password=oracle_password, dsn=dsn) as connection:
            # Insert data into Oracle table for the address range using batch insert
            sql = "INSERT INTO AMR_POLL_RANGE (POLL_CONFIG) VALUES (:poll_config_value)"
            with connection.cursor() as cursor:
                cursor.execute(sql, {'poll_config_value': poll_config_values})

            connection.commit()

        response = {'status': 'success', 'message': 'Data saved successfully'}
    except cx_Oracle.DatabaseError as e:
        response = {'status': 'error', 'message': f'Database Error: {e}'}
    except Exception as e:
        response = {'status': 'error', 'message': f'Error: {e}'}

    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
