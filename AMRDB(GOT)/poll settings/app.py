from flask import Flask, render_template, request, jsonify
import cx_Oracle
import pandas as pd
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# กำหนดการเชื่อมต่อฐานข้อมูล
username = "root"
password = "root"
hostname = "192.168.102.192"
port = "1521"
service_name = "orcl"


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
        (error,) = e.args
        print("Oracle Error:", error)
        return []


def insert_address_range_to_oracle(
    poll_config, poll_billing, enable_config, enable_billing, evc_type
):
    dsn = cx_Oracle.makedsn(host, port, service_name=service)

    with cx_Oracle.connect(user=username, password=password, dsn=dsn) as connection:
        with connection.cursor() as cursor:
            sql_insert = """
                INSERT INTO AMR_POLL_RANGE (POLL_CONFIG, POLL_BILLING, POLL_CONFIG_ENABLE, POLL_BILLING_ENABLE, EVC_TYPE)
                VALUES (:1, :2, :3, :4, :5)
            """

            # Convert enable_config and enable_billing to comma-separated strings
            enable_config_str = ",".join(map(str, enable_config))
            enable_billing_str = ",".join(map(str, enable_billing))

            data_to_insert = (
                poll_config,
                poll_billing,
                enable_config_str,
                enable_billing_str,
                evc_type,
            )

            cursor.execute(sql_insert, data_to_insert)

        connection.commit()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/polling_route")
def polling_route():
    # Fetch type options for the dropdown
    type_query = "SELECT VC_NAME FROM AMR_VC_TYPE"
    type_results = fetch_data(type_query)
    type_options = [str(type[0]) for type in type_results]
    # print(type_results)

    # Define the base query for fetching polling data
    base_query = """
    SELECT
        apr.evc_type,
        apr.poll_config,
        apr.poll_billing,
        apr.poll_config_enable,
        apr.poll_billing_enable
    FROM
        amr_poll_range apr
    JOIN
        amr_vc_type avt ON apr.evc_type = avt.id
    {type_condition}
    """

    # Get selected type from the dropdown
    selected_type = request.args.get("type_dropdown")

    # Define type condition based on the selected type
    type_condition = f"AND avt.VC_NAME = '{selected_type}'" if selected_type else ""

    # Check if a type is selected before executing the query
    if selected_type:
        # Modify the base query with the selected conditions
        query = base_query.format(type_condition=type_condition)

        # Fetch data using the modified query
        results = fetch_data(query)
        # print(results)
        # Create a DataFrame from the results
        columns = [
            "evc_type",
            "poll_config",
            "poll_billing",
            "poll_config_enable",
            "poll_billing_enable",
        ]
        df = pd.DataFrame(results, columns=columns)

        poll_config_list = df.get(["poll_config"]).values.tolist()
        list_config = str(poll_config_list[0]).strip("[]'").split(",")

        poll_billing_list = df.get(["poll_billing"]).values.tolist()
        list_billing = str(poll_billing_list[0]).strip("[]'").split(",")
        
        poll_config_enable_list = df.get(["poll_config_enable"]).values.tolist()
        list_enable_config = str(poll_config_enable_list[0]).strip("[]'").split(",")
     
        poll_billing_enable_list = df.get(["poll_billing_enable"]).values.tolist()
        list_enable_billing = str(poll_billing_enable_list[0]).strip("[]'").split(",")
               
        return render_template(
            "polling.html",
            tables=[df.to_html(classes="data", index=False)],
            titles=columns,
            selected_type=selected_type,
            type_options=type_options,
            list_config=list_config,  # Pass the list_str to the template
            list_billing=list_billing,
            list_enable_config=list_enable_config,
            #list_enable_billing=list_enable_blling,
        )

    # Render the HTML template without the table if no type is selected
    return render_template(
        "polling.html",
        tables=[],
        titles=[],
        selected_type=None,
        type_options=type_options,
        list_config=[],  # Pass an empty list_str to the template
        list_billing=[],
        list_enable_config=[],
       # list_enable_billing=[],
    )


MAX_ADDRESS_LENGTH = 249


@app.route("/add_polling_route")
def add_polling_route():
    return render_template("add_polling.html")


@app.route("/save_to_oracle", methods=["POST"])
def save_to_oracle():
    try:
        data = request.get_json()

        # Add the following line to define 'evc_type'
        evc_type = data.get("evc_type", "")

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
            evc_type,  # Add 'evc_type' as an argument here
        )

        response = {"status": "success", "message": "Data saved successfully"}
    except ValueError as ve:
        response = {"status": "error", "message": str(ve)}
    except cx_Oracle.DatabaseError as e:
        (error,) = e.args
        print(f"Oracle Database Error {error.code}: {error.message}")
        traceback.print_exc()  # Print detailed traceback information
        response = {
            "status": "error",
            "message": f"Database Error: {error.code} - {error.message}",
        }
    except Exception as e:
        print(f"Error: {e}")
        traceback.print_exc()  # Print detailed traceback information
        response = {
            "status": "error",
            "message": f"An error occurred while saving data: {str(e)}",
        }

    return jsonify(response)


@app.route("/edit_polling_route")
def edit_polling_route():
    return render_template("edit_polling.html")


@app.route("/save_edited_to_oracle", methods=["POST"])
def save_edited_to_oracle():
    try:
        data = request.get_json()

        # Add the following line to define 'evc_type'
        evc_type = data.get("evc_type", "")

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

        # Add a function to update the existing records in Oracle
        update_address_range_in_oracle(
            combined_address_config,
            combined_address_billing,
            enable_config,
            enable_billing,
            evc_type,
        )

        response = {"status": "success", "message": "Data updated successfully"}
    except ValueError as ve:
        response = {"status": "error", "message": str(ve)}
    except cx_Oracle.DatabaseError as e:
        (error,) = e.args
        print(f"Oracle Database Error {error.code}: {error.message}")
        traceback.print_exc()  # Print detailed traceback information
        response = {
            "status": "error",
            "message": f"Database Error: {error.code} - {error.message}",
        }
    except Exception as e:
        print(f"Error: {e}")
        traceback.print_exc()  # Print detailed traceback information
        response = {
            "status": "error",
            "message": f"An error occurred while updating data: {str(e)}",
        }

    return jsonify(response)


@app.route("/add_mapping_route")
def add_mapping_route():
    return render_template("add_mapping.html")


@app.route("/submit_form", methods=["POST"])
def submit_form():
    cursor = None
    connection = None

    try:
        data_list = []
        for i in range(1, 21):
            address = request.form[f"address{i}"]
            description = request.form[f"description{i}"]
            type_value = request.form.get(f"type_value{i}")
            evc_type = request.form[f"evc_type{i}"]
            or_der = request.form[f"or_der{i}"]
            data_type = request.form[f"data_type{i}"]

            data_list.append(
                (address, description, type_value, evc_type, or_der, data_type)
            )

        dsn_tns = cx_Oracle.makedsn(host, port, service_name=service)
        connection = cx_Oracle.connect(user=username, password=password, dsn=dsn_tns)

        cursor = connection.cursor()

        sql_merge = """
            MERGE INTO AMR_ADDRESS_MAPPING1 dst
            USING (
                SELECT
                    :address as address,
                    :description as description,
                    :type_value as type_value,
                    :evc_type as evc_type,
                    :or_der as or_der,
                    :data_type as data_type
                FROM dual
            ) src
            ON (dst.address = src.address)
            WHEN MATCHED THEN
                UPDATE SET
                    dst.description = src.description,
                    dst.type_value = src.type_value,
                    dst.evc_type = src.evc_type,
                    dst.or_der = src.or_der,
                    dst.data_type = src.data_type
            WHEN NOT MATCHED THEN
                INSERT (
                    address,
                    description,
                    type_value,
                    evc_type,
                    or_der,
                    data_type
                ) VALUES (
                    src.address,
                    src.description,
                    src.type_value,
                    src.evc_type,
                    src.or_der,
                    src.data_type
                )
        """

        cursor.executemany(sql_merge, data_list)

        # Commit the changes to the database
        connection.commit()

        return "Data saved successfully"
    except Exception as e:
        return f"Error occurred: {str(e)}"
    finally:
        if cursor is not None:
        # Close the cursor
            cursor.close()

    if connection is not None:
        # Close the connection
        connection.close()


@app.route("/add_actraris_route")
def add_actraris_route():
    return render_template("add_actraris.html")


@app.route("/new_form", methods=["POST"])
def submit_new_form():
    cursor = None
    connection = None

    try:
        data_list = []
        for i in range(1, 18):
            address = request.form.get(f"address{i}")
            description = request.form.get(f"description{i}")
            type_value = request.form.get(f"type_value{i}")
            evc_type = request.form.get(f"evc_type{i}")
            or_der = request.form.get(f"or_der{i}")
            data_type = request.form.get(f"data_type{i}")

            data_list.append(
                (address, description, type_value, evc_type, or_der, data_type)
            )

        dsn_tns = cx_Oracle.makedsn(host, port, service_name=service)
        connection = cx_Oracle.connect(user=username, password=password, dsn=dsn_tns)

        cursor = connection.cursor()

        sql_merge = """
            MERGE INTO AMR_ADDRESS_MAPPING1 dst
            USING (
                SELECT
                    :address as address,
                    :description as description,
                    :type_value as type_value,
                    :evc_type as evc_type,
                    :or_der as or_der,
                    :data_type as data_type
                FROM dual
            ) src
            ON (dst.address = src.address)
            WHEN MATCHED THEN
                UPDATE SET
                    dst.description = src.description,
                    dst.type_value = src.type_value,
                    dst.evc_type = src.evc_type,
                    dst.or_der = src.or_der,
                    dst.data_type = src.data_type
            WHEN NOT MATCHED THEN
                INSERT (
                    address,
                    description,
                    type_value,
                    evc_type,
                    or_der,
                    data_type
                ) VALUES (
                    src.address,
                    src.description,
                    src.type_value,
                    src.evc_type,
                    src.or_der,
                    src.data_type
                )
        """

        cursor.executemany(sql_merge, data_list)

        connection.commit()

        # Commit the changes to the database
        connection.commit()

        return "Data saved successfully"
    except Exception as e:
        return f"Error occurred: {str(e)}"
    finally:
        if cursor is not None:
        # Close the cursor
            cursor.close()

    if connection is not None:
        # Close the connection
        connection.close()


if __name__ == "__main__":
    app.run(debug=True)
