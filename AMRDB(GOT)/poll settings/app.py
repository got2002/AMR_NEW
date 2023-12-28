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

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/save_to_oracle', methods=['POST'])
def save_to_oracle():
    poll_config_value = None  # Define the variable outside the try block

    try:
        data = request.get_json()

        # Create a list of addresses
        addresses = [
            str(data.get('start', '')),
            str(data.get('end', '')),
            # ... (add more addresses as needed)
        ]

        # Remove empty strings from the list
        addresses = [address for address in addresses if address]

        # Convert the list of addresses to a JSON array string
        poll_config_values = json.dumps(addresses)

        dsn = cx_Oracle.makedsn(oracle_host, oracle_port, service_name=oracle_service)

        with cx_Oracle.connect(user=oracle_username, password=oracle_password, dsn=dsn) as connection:
            # Insert data into Oracle table for all addresses using batch insert
            sql = "INSERT INTO AMR_POLL_RANGE (POLL_CONFIG) VALUES (:poll_config_value)"
            with connection.cursor() as cursor:
                cursor.execute(sql, {'poll_config_value': poll_config_values})

            connection.commit()

        response = {'message': 'Data saved successfully'}
    except cx_Oracle.DatabaseError as e:
        response = {'message': f'Database Error: {e}'}
        print(f'Database Error: {e}')  # Print the error for debugging
    except Exception as e:
        response = {'message': f'Error: {e}'}
        print(f'Error: {e}')  # Print the error for debugging

    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
