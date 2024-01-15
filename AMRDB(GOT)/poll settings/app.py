from flask import Flask, render_template, request, jsonify
import cx_Oracle

app = Flask(__name__)

# Replace these values with your Oracle credentials
oracle_username = "root"
oracle_password = "root"
oracle_host = "192.168.102.192"
oracle_port = "1521"
oracle_service = "orcl"


def insert_address_range_to_oracle(
    poll_config, poll_billing, enable_config, enable_billing
):
    dsn = cx_Oracle.makedsn(oracle_host, oracle_port, service_name=oracle_service)

    with cx_Oracle.connect(
        user=oracle_username, password=oracle_password, dsn=dsn
    ) as connection:
        with connection.cursor() as cursor:
            sql_insert = """
                INSERT INTO AMR_POLL_RANGE (POLL_CONFIG, POLL_BILLING, POLL_CONFIG_ENABLE, POLL_BILLING_ENABLE)
                VALUES (:1, :2, :3, :4)
            """

            # Convert enable_config and enable_billing to comma-separated strings
            enable_config_str = ",".join(map(str, enable_config))
            enable_billing_str = ",".join(map(str, enable_billing))

            data_to_insert = (
                poll_config,
                poll_billing,
                enable_config_str,
                enable_billing_str,
            )

            cursor.execute(sql_insert, data_to_insert)

        connection.commit()


@app.route("/")
def index():
    return render_template("index.html")


MAX_ADDRESS_LENGTH = 249


@app.route("/save_to_oracle", methods=["POST"])
def save_to_oracle():
    try:
        data = request.get_json()

        def validate_address_range(start_key, end_key):
            start_address = int(data.get(start_key, 0))
            end_address = int(data.get(end_key, 0))

            if end_address - start_address + 1 > MAX_ADDRESS_LENGTH:
                raise ValueError(
                    f"Address range {start_key} - {end_key} exceeds the maximum length of {MAX_ADDRESS_LENGTH}"
                )

            return start_address, end_address

        combined_address_config = ",".join(
            [
                ",".join(map(str, validate_address_range(f"start{i}", f"end{i}")))
                for i in range(1, 6)
                if data.get(f"start{i}")
            ]
        )

        enable_config = [int(data.get(f"enable{i}", 0)) for i in range(1, 6)]

        combined_address_billing = ",".join(
            [
                ",".join(map(str, validate_address_range(f"start{i}", f"end{i}")))
                for i in range(6, 16)
                if data.get(f"start{i}")
            ]
        )

        enable_billing = [int(data.get(f"enable{i}", 0)) for i in range(6, 16)]

        if not combined_address_config or not combined_address_billing:
            response = {
                "status": "error",
                "message": "Please enter at least one valid start or end address for both configurations.",
            }
            return jsonify(response)

        insert_address_range_to_oracle(
            combined_address_config,
            combined_address_billing,
            enable_config,
            enable_billing,
        )

        response = {"status": "success", "message": "Data saved successfully"}
    except ValueError as ve:
        response = {"status": "error", "message": str(ve)}
    except cx_Oracle.DatabaseError as e:
        response = {"status": "error", "message": f"Database Error: {e}"}
    except Exception as e:
        response = {"status": "error", "message": f"Error: {e}"}

    return jsonify(response)


if __name__ == "__main__":
    app.run(debug=True)
