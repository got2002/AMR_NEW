from flask import Flask, render_template, jsonify, request, flash, redirect, url_for
import cx_Oracle
import hashlib
import os

app = Flask(__name__)

# Database connection details
username = "root"
password = "root"
hostname = "192.168.102.192"
port = "1521"
service_name = "orcl"

# Set the Flask secret key from the environment variable
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "fallback_secret_key")


def md5_hash(input_string):
    # เข้ารหัสรหัสผ่านโดยใช้ MD5
    return hashlib.md5(input_string.encode()).hexdigest()


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
        (error,) = e.args
        print("Oracle Error:", error)
        return False


# Function to connect to Oracle database and fetch data
def get_data(filter_text=None, sort_column=None):
    try:
        connection = cx_Oracle.connect(
            user=username, password=password, dsn=f"{hostname}:{port}/{service_name}"
        )
        cursor = connection.cursor()

        # Base query
        query = (
            "SELECT description, USER_NAME, PASSWORD, USER_LEVEL FROM AMR_User_tests"
        )

        # Apply filtering
        if filter_text:
            query += f" WHERE USER_NAME LIKE '%{filter_text}%'"

        # Apply sorting
        if sort_column:
            query += f" ORDER BY {sort_column}"

        cursor.execute(query)

        # Fetch data in chunks (e.g., 100 rows at a time)
        chunk_size = 100
        data = []
        while True:
            rows = cursor.fetchmany(chunk_size)
            if not rows:
                break
            data.extend(
                [
                    {
                        "description": row[0],
                        "user_name": row[1],
                        "password": row[2],
                        "user_level": row[3],
                    }
                    for row in rows
                ]
            )

        return data
    except cx_Oracle.Error as e:
        (error,) = e.args
        print("Oracle Error:", error)
        return []
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


# Example usage with filtering and sorting
filter_text = "example"  # Replace with your filter text or None for no filtering
sort_column = "USER_NAME"  # Replace with your desired column or None for no sorting
filtered_and_sorted_data = get_data(filter_text=filter_text, sort_column=sort_column)


# User list page
@app.route("/")
def index():
    query = "SELECT * FROM AMR_USER_TESTS"
    users = fetch_data(query)
    return render_template("user.html", users=users)


@app.route("/get_data")
def get_data_route():
    data = get_data()
    return jsonify(data)


# Add user page
@app.route("/add_user", methods=["GET", "POST"])
def add_user_route():
    if request.method == "POST":
        description = request.form["description"]
        user_name = request.form["user_name"]
        password = request.form["password"]
        user_level = request.form["user_level"]

        # เข้ารหัสรหัสผ่านโดยใช้ MD5
        hashed_password = md5_hash(password)

        # แปลงเป็น RAWTOHEX ก่อนที่จะบันทึกลงใน Oracle
        hashed_password_hex = "RAWTOHEX(DBMS_OBFUSCATION_TOOLKIT.MD5(input_string => UTL_I18N.STRING_TO_RAW('{}', 'AL32UTF8')))".format(
            hashed_password
        )

        query = "INSERT INTO AMR_USER_TESTS (description, user_name, password, user_level) VALUES (:1, :2, {}, :4)".format(
            hashed_password_hex
        )
        params = (description, user_name, user_level)

        if execute_query(query, params):
            flash("User added successfully!", "success")
            return redirect(url_for("index"))
        else:
            flash("Failed to add user. Please try again.", "error")

    return render_template("add_user.html")


@app.route("/edit_user", methods=["GET", "POST"])
def edit_user_route():
    # ดึงข้อมูลผู้ใช้จากฐานข้อมูล
    query = "SELECT DESCRIPTION, USER_NAME, PASSWORD, USER_LEVEL FROM AMR_User_tests"
    user_data = fetch_data(query)

    if not user_data:
        flash("User not found!", "error")
        return render_template("edit_user.html")

    # ถ้ามีการส่งค่า POST (คือการบันทึกการแก้ไข)
    if request.method == "POST":
        # ดึงข้อมูลจากฟอร์มแก้ไข
        description = request.form["description"]
        user_name = request.form["user_name"]
        password = request.form["password"]
        user_level = request.form["user_level"]

        # เข้ารหัสรหัสผ่านโดยใช้ MD5
        hashed_password = md5_hash(password)

        # สร้างคำสั่ง SQL สำหรับการแก้ไขข้อมูลผู้ใช้
        update_query = "UPDATE AMR_USER_TESTS SET description = :1, user_name = :2, password = :3, user_level = :4 WHERE description = :5"
        update_params = (
            description,
            user_name,
            hashed_password,
            user_level,
            description,
        )

        # ทำการ execute คำสั่ง SQL และ commit การแก้ไข user_name
        if execute_query(update_query, update_params):
            return render_template("edit_user.html", user_data=user_data)
        else:
            flash("Failed to update user. Please try again.", "error")

    # กรณีไม่ใช่การส่งค่า POST ให้ส่งข้อมูลผู้ใช้ไปยัง HTML template หรือทำอย่างอื่นตามที่ต้องการ
    return render_template("edit_user.html", user_data=user_data)


@app.route("/remove_user", methods=["GET", "POST"])
def remove_user_route():
    # ดึงข้อมูลผู้ใช้จาก Oracle
    query = "SELECT DESCRIPTION, USER_NAME, USER_LEVEL, USER_ENABLE FROM AMR_USER_TESTS"
    user_data = fetch_data(query)

    if not user_data:
        flash("Users not found!", "error")
        return redirect(url_for("index"))

    # ถ้ามีการส่งค่า POST (คือการเปลี่ยนสถานะการเข้าสู่ระบบของผู้ใช้)
    if request.method == "POST":
        # ดึงข้อมูลจากฟอร์มเปลี่ยนสถานะการเข้าสู่ระบบของผู้ใช้
        new_status = request.form.get("status")
        user_name = request.form.get("user_name")  # ดึง user_name จากฟอร์ม

        # ตรวจสอบว่าสถานะที่เลือกถูกต้อง
        if new_status not in ["active", "inactive"]:
            flash("Invalid status selected.", "error")
            return redirect(url_for("remove_user_route"))

        # แปลงสถานะเป็นเลข (0 หรือ 1) ที่จะบันทึกลงในฐานข้อมูล Oracle
        status_mapping = {"active": 1, "inactive": 0}
        new_status_numeric = status_mapping[new_status]

        # สร้างคำสั่ง SQL สำหรับการอัปเดตสถานะการเข้าสู่ระบบของผู้ใช้
        update_query = "UPDATE AMR_USER_TESTS SET USER_ENABLE = :1 WHERE USER_NAME = :2"
        update_params = (new_status_numeric, user_name)

        # ทำการ execute คำสั่ง SQL และ commit การอัปเดตสถานะการเข้าสู่ระบบของผู้ใช้
        if execute_query(update_query, update_params):
            flash("User status updated successfully!", "success")
            return redirect(url_for("index"))
        else:
            flash("Failed to update user status. Please try again.", "error")

    # กรณีไม่ใช่การส่งค่า POST ให้ส่งข้อมูลผู้ใช้ไปยัง HTML template หรือทำอย่างอื่นตามที่ต้องการ
    return render_template("remove_user.html", user_data=user_data)


if __name__ == "__main__":
    app.run(debug=True)
