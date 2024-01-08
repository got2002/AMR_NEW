from flask import Flask, render_template, request, jsonify
import cx_Oracle

app = Flask(__name__)

# Replace these values with your Oracle credentials
oracle_username = "root"
oracle_password = "root"
oracle_host = "192.168.102.192"
oracle_port = "1521"
oracle_service = "orcl"


def insert_address_range_to_oracle(data_to_insert):
    dsn = cx_Oracle.makedsn(oracle_host, oracle_port, service_name=oracle_service)

    with cx_Oracle.connect(
        user=oracle_username, password=oracle_password, dsn=dsn
    ) as connection:
        with connection.cursor() as cursor:
            sql_insert = """
                INSERT INTO AMR_POLL_RANGE_config (
                    config1, config2, config3, config4, config5,
                    config6, config7, config8, config9, config10,
                    config11, config12, config13, config14, config15,
                    config16, config17, config18, config19, config20
                )
                VALUES (
                    :1, :2, :3, :4, :5,
                    :6, :7, :8, :9, :10,
                    :11, :12, :13, :14, :15,
                    :16, :17, :18, :19, :20
                )
            """

            cursor.execute(
                sql_insert,
                (
                    data_to_insert["config1"],
                    data_to_insert["config2"],
                    data_to_insert["config3"],
                    data_to_insert["config4"],
                    data_to_insert["config5"],
                    data_to_insert["config6"],
                    data_to_insert["config7"],
                    data_to_insert["config8"],
                    data_to_insert["config9"],
                    data_to_insert["config10"],
                    data_to_insert["config11"],
                    data_to_insert["config12"],
                    data_to_insert["config13"],
                    data_to_insert["config14"],
                    data_to_insert["config15"],
                    data_to_insert["config16"],
                    data_to_insert["config17"],
                    data_to_insert["config18"],
                    data_to_insert["config19"],
                    data_to_insert["config20"],
                ),
            )

        connection.commit()


@app.route("/")
def index():
    return render_template("indexx.html")


@app.route("/save_to_oracle", methods=["POST"])
def save_to_oracle():
    try:
        data = request.json
        # Call the function to insert data into Oracle
        insert_address_range_to_oracle(data)

        response_data = {"message": "Data saved successfully."}
        return jsonify(response_data), 200
    except Exception as e:
        print("Error:", e)
        response_data = {"message": "Error saving data to Oracle."}
        return jsonify(response_data), 500


if __name__ == "__main__":
    app.run(debug=True)
