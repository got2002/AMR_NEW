from flask import Flask, render_template, request, jsonify
import cx_Oracle

app = Flask(__name__)

# Replace these values with your Oracle credentials
oracle_username = "root"
oracle_password = "root"
oracle_host = "192.168.102.192"
oracle_port = "1521"
oracle_service = "orcl"


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/submit_form", methods=["POST"])
def submit_form():
    cursor = None
    connection = None

    try:
        # รับข้อมูลจากฟอร์ม
        address = request.form["address"]
        description = request.form["description"]
        type_value = request.form.get("type_value")
        evc_type = request.form["evc_type"]  # เพิ่มการรับข้อมูล EVC_TYPE
        or_der = request.form["or_der"]  # เพิ่มการรับข้อมูล OR_DER
        data_type = request.form["data_type"]  # เพิ่มการรับข้อมูล DATA_TYPE

        # เชื่อมต่อกับ Oracle Database
        dsn_tns = cx_Oracle.makedsn(
            oracle_host, oracle_port, service_name=oracle_service
        )
        connection = cx_Oracle.connect(
            user=oracle_username, password=oracle_password, dsn=dsn_tns
        )

        # สร้าง cursor
        cursor = connection.cursor()

        # ทำคำสั่ง SQL เพื่อเพิ่มข้อมูล
        sql_merge = """
            MERGE INTO ADDRESS_MAPPING dst
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
            ON (dst.data_type = src.data_type)
            WHEN MATCHED THEN
                UPDATE SET
                    dst.address = src.address,
                    dst.description = src.description,
                    dst.type_value = src.type_value,
                    dst.evc_type = src.evc_type,
                    dst.or_der = src.or_der
                    
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

        # ให้ข้อมูลเข้าไปในคำสั่ง SQL
        cursor.execute(
            sql_merge,
            {
                "address": address,
                "description": description,
                "type_value": type_value,
                "evc_type": evc_type,
                "or_der": or_der,
                "data_type": data_type,
            },
        )

        # ยืนยันการบันทึก
        connection.commit()

        return "บันทึกข้อมูลสำเร็จ"
    except Exception as e:
        return f"เกิดข้อผิดพลาด: {str(e)}"
    finally:
        if cursor is not None:
            # ปิด cursor
            cursor.close()

        if connection is not None:
            # ปิด connection
            connection.close()


if __name__ == "__main__":
    app.run(debug=True)
