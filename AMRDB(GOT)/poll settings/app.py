from flask import Flask, render_template, request, jsonify
import cx_Oracle

app = Flask(__name__)

# Replace these values with your Oracle credentials
oracle_username = "root"
oracle_password = "root"
oracle_host = "192.168.102.192"
oracle_port = "1521"
oracle_service = "orcl"

def insert_address_range_to_oracle(address_range):
    dsn = cx_Oracle.makedsn(oracle_host, oracle_port, service_name=oracle_service)

    with cx_Oracle.connect(user=oracle_username, password=oracle_password, dsn=dsn) as connection:
        sql = "INSERT INTO AMR_POLL_RANGE (POLL_CONFIG) VALUES (:address_range)"
        with connection.cursor() as cursor:
            cursor.execute(sql, {'address_range': address_range})
            
        connection.commit()   
        
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/save_to_oracle', methods=['POST'])
def save_to_oracle():
    try:
        data = request.get_json()

       # Combine start and end addresses alternately into a single string
        combined_address_range = ",".join(
            [data[f'start{i}'] + ',' + data[f'end{i}'] for i in range(1, 6) if data[f'start{i}']])


        if not combined_address_range:
            response = {'status': 'error', 'message': 'Please enter at least one start or end address.'}
            return jsonify(response)

        # Wrap the combined address range with square brackets to create a JSON array
        combined_address_range = f"[{combined_address_range}]"

        insert_address_range_to_oracle(combined_address_range)

        response = {'status': 'success', 'message': 'Data saved successfully'}
    except cx_Oracle.DatabaseError as e:
        response = {'status': 'error', 'message': f'Database Error: {e}'}
    except Exception as e:
        response = {'status': 'error', 'message': f'Error: {e}'}

    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
