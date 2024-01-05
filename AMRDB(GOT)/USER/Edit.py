import tkinter as tk
import cx_Oracle
import numpy as np

# Global variable to store the addresses
addresses = []


def on_save_button_click():
    start_address = start_entry.get()
    end_address = end_entry.get()

    # Check if start and end addresses are provided
    if start_address and end_address:
        # Convert start and end addresses to integers
        start_address = int(start_address)
        end_address = int(end_address)

        # Generate a range of addresses from start to end
        address_range = list(range(start_address, end_address + 1))

        # Extend the global addresses list with the generated range
        addresses.extend(address_range)

        print("Addresses:", addresses)

        # Call a function to handle the database connection
        save_to_csv()


def save_to_csv():
    try:
        # Replace these values with your Oracle credentials
        oracle_username = "root"
        oracle_password = "root"
        oracle_host = "192.168.102.192"
        oracle_port = "1521"
        oracle_service = "orcl"

        # Construct the connection string
        dsn = cx_Oracle.makedsn(oracle_host, oracle_port, service_name=oracle_service)
        connection = cx_Oracle.connect(
            user=oracle_username, password=oracle_password, dsn=dsn
        )

        # Perform database operations here
        # Example: execute a query using the addresses
        cursor = connection.cursor()

        # Create an empty list to store the results
        poll_config_results = []

        for address in addresses:
            cursor.execute(
                "SELECT POLL_CONFIG FROM AMR_POLL_RANGE WHERE ADDRESS = :address",
                {"address": address},
            )
            rows = cursor.fetchall()
            for row in rows:
                # Append the result to the list
                poll_config_results.append(row[0])

        # Display the results
        print("Poll Config Results:", poll_config_results)

        # Convert the list to a numpy array
        poll_config_array = np.array(poll_config_results)

        # Save the array to a file (e.g., CSV)
        np.savetxt("poll_config_array.csv", poll_config_array, delimiter=",")

        print("Data saved to poll_config_array.csv")

        # Close the cursor and connection when done
        cursor.close()
        connection.close()

    except cx_Oracle.Error as error:
        print("Oracle Error:", error)


# Create the GUI
root = tk.Tk()
root.title("Polling Configuration")

# Labels and Textboxes for entering start and end addresses
start_label = tk.Label(root, text="Start Address:")
start_label.pack(pady=5)
start_entry = tk.Entry(root)
start_entry.pack(pady=5)

end_label = tk.Label(root, text="End Address:")
end_label.pack(pady=5)
end_entry = tk.Entry(root)
end_entry.pack(pady=5)

# Button to trigger save and database connection
save_button = tk.Button(root, text="Save", command=on_save_button_click)
save_button.pack(pady=10)

# Run the GUI loop
root.mainloop()


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
