from flask import Flask, render_template, request, redirect, url_for
from database import init_db
from data_processing import process_data, generate_plot
from forms import RegistrationForm
from api import process_api_data
from database import db  
from data_processing import process_data, generate_plot
from forms import RegistrationForm
from api import process_api_data

app = Flask(__name__)

# Configure the database
# app.config['SQLALCHEMY_DATABASE_URI'] = 'your_database_uri'
# app.config['SECRET_KEY'] = 'your_secret_key'

# Initialize the database
# init_db(app)

# Replace these values with your actual database credentials
communication_traffic = []
change_to_32bit_counter = 1  # Initialize the counter to 2


def convert_to_binary_string(value, bytes_per_value):
    binary_string = bin(value)[
        2:
    ]  # Convert the value to binary string excluding the '0b' prefix
    return binary_string.zfill(
        bytes_per_value * 8
    )  # Zero-fill to fit the number of bits based on bytes_per_value


# Set the Flask secret key from the environment variable
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "fallback_secret_key")


def md5_hash(input_string):
    # เข้ารหัสรหัสผ่านโดยใช้ MD5
    return hashlib.md5(input_string.encode()).hexdigest()





############  Home page  #####################
@app.route("/")
def home():
    return render_template("home.html")


############ / Home page  #####################


############  Add User  #####################
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
            return render_template("add_user.html")
        else:
            flash("Failed to add user. Please try again.", "error")

    return render_template("add_user.html")


############  /Add User  #####################



############  edit_user   #####################


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


@app.route("/get_data")
def get_data_route():
    data = get_data()
    return jsonify(data)


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
        # user_level = request.form["user_level"]

        # เข้ารหัสรหัสผ่านโดยใช้ MD5
        hashed_password = md5_hash(password)

        # สร้างคำสั่ง SQL สำหรับการแก้ไขข้อมูลผู้ใช้
        update_query = "UPDATE AMR_USER_TESTS SET description = :1, user_name = :2, password = :3 WHERE description = :4"
        update_params = (description, user_name, hashed_password, description)

        # ทำการ execute คำสั่ง SQL และ commit การแก้ไข user_name
        if execute_query(update_query, update_params):
            flash("User updated successfully!", "success")
            return render_template("edit_user.html")
        else:
            flash("Failed to update user. Please try again.", "error")

    # กรณีไม่ใช่การส่งค่า POST ให้ส่งข้อมูลผู้ใช้ไปยัง HTML template หรือทำอย่างอื่นตามที่ต้องการ
    return render_template("edit_user.html", user_data=user_data)


############  /edit_user   #####################


############   /remove_user ###################
@app.route("/remove_user", methods=["GET", "POST"])
def remove_user_route():
    # ดึงข้อมูลผู้ใช้จาก Oracle
    query = "SELECT DESCRIPTION, USER_NAME, USER_LEVEL, USER_ENABLE FROM AMR_USER_TESTS"
    user_data = fetch_data(query)

    if not user_data:
        flash("Users not found!", "error")
        return redirect(url_for("remove_user.html"))

    # ถ้ามีการส่งค่า POST (คือการเปลี่ยนสถานะการเข้าสู่ระบบของผู้ใช้)
    if request.method == "POST":
        # ดึงข้อมูลจากฟอร์มเปลี่ยนสถานะการเข้าสู่ระบบของผู้ใช้
        new_status = request.form.get("status")
        user_name = request.form.get("user_name")  # ดึง user_name จากฟอร์ม

        # ตรวจสอบว่าสถานะที่เลือกถูกต้อง
        if new_status not in ["active", "inactive"]:
            flash("Invalid status selected.", "error")
            return redirect(url_for("remove_user"))

        # แปลงสถานะเป็นเลข (0 หรือ 1) ที่จะบันทึกลงในฐานข้อมูล Oracle
        status_mapping = {"active": 1, "inactive": 0}
        new_status_numeric = status_mapping[new_status]

        # สร้างคำสั่ง SQL สำหรับการอัปเดตสถานะการเข้าสู่ระบบของผู้ใช้
        update_query = "UPDATE AMR_USER_TESTS SET USER_ENABLE = :1 WHERE USER_NAME = :2"
        update_params = (new_status_numeric, user_name)

        # ทำการ execute คำสั่ง SQL และ commit การอัปเดตสถานะการเข้าสู่ระบบของผู้ใช้
        if execute_query(update_query, update_params):
            flash("User status updated successfully!", "success")
            return redirect(url_for("remove_user.html"))
        else:
            flash("Failed to update user status. Please try again.", "error")

    # กรณีไม่ใช่การส่งค่า POST ให้ส่งข้อมูลผู้ใช้ไปยัง HTML template หรือทำอย่างอื่นตามที่ต้องการ
    return render_template("remove_user.html", user_data=user_data)


############   /remove_user ###################


############  View Billing Data   #####################


@app.route("/get_tags", methods=["GET"])
def get_tags():
    selected_region = request.args.get("selected_region")

    tag_query = """
    SELECT DISTINCT TAG_ID
    FROM AMR_FIELD_ID
    JOIN AMR_PL_GROUP ON AMR_FIELD_ID.FIELD_ID = AMR_PL_GROUP.FIELD_ID 
    WHERE AMR_PL_GROUP.PL_REGION_ID = :region_id
    """

    tag_results = fetch_data(tag_query, params={"region_id": selected_region})
    tag_options = [str(tag[0]) for tag in tag_results]
    tag_options.sort()
    return jsonify({"tag_options": tag_options})


@app.route("/billing_data")
def billing_data():
    query_type = request.args.get("query_type")

    # SQL query to fetch unique PL_REGION_ID values
    region_query = """
    SELECT * FROM AMR_REGION 
    """

    tag_query = """
    SELECT DISTINCT TAG_ID
    FROM AMR_FIELD_ID
    JOIN AMR_PL_GROUP ON AMR_FIELD_ID.FIELD_ID = AMR_PL_GROUP.FIELD_ID 
    WHERE AMR_PL_GROUP.PL_REGION_ID = :region_id
    """

    # Fetch unique region values
    region_results = fetch_data(region_query)
    region_options = [str(region[0]) for region in region_results]

    query = ""
    print(query)
    if query_type == "daily_data":
        # SQL query for main data
        query = """
        SELECT DISTINCT
            AMR_PL_GROUP.PL_REGION_ID,
            AMR_FIELD_ID.TAG_ID,
            AMR_FIELD_ID.METER_ID,
            AMR_BILLING_DATA.DATA_DATE,
            AMR_BILLING_DATA.CORRECTED_VOL as CORRECTED,
            AMR_BILLING_DATA.UNCORRECTED_VOL as UNCORRECTED,
            AMR_BILLING_DATA.AVR_PF as Pressure,
            AMR_BILLING_DATA.AVR_TF as Temperature,
            AMR_BILLING_DATA.METER_STREAM_NO  -- Add this line to include METER_STREAM_NO in the SELECT clause
        FROM
            AMR_FIELD_ID, AMR_PL_group, AMR_BILLING_DATA
        WHERE
            AMR_PL_GROUP.FIELD_ID = AMR_FIELD_ID.FIELD_ID 
            AND AMR_BILLING_DATA.METER_ID = AMR_FIELD_ID.METER_ID
            AND AMR_BILLING_DATA.METER_STREAM_NO IS NOT NULL
            {billing_date_condition}
            {tag_condition}
            {region_condition}
        """


        # Return the template with the DataFrame

    elif query_type == "config_data":
        query = """
        SELECT
            AMR_PL_GROUP.PL_REGION_ID,
            AMR_FIELD_ID.TAG_ID,
            amr_field_id.meter_id,
            AMR_CONFIGURED_DATA.DATA_DATE,
            
            amr_configured_data.amr_config1,
            amr_configured_data.amr_config2,
            amr_configured_data.amr_config3,
            amr_configured_data.amr_config4,
            amr_configured_data.amr_config5,
            amr_configured_data.amr_config6,
            amr_configured_data.amr_config7,
            amr_configured_data.amr_config8,
            amr_configured_data.amr_config9,
            amr_configured_data.amr_config10,
            amr_configured_data.amr_config11,
            amr_configured_data.amr_config12,
            amr_configured_data.amr_config13,
            amr_configured_data.amr_config14,
            amr_configured_data.amr_config15,
            amr_configured_data.amr_config16,
            amr_configured_data.amr_config17,
            amr_configured_data.amr_config18,
            amr_configured_data.amr_config19,
            amr_configured_data.amr_config20,
            
            
            AMR_VC_CONFIGURED_INFO.config1,
            AMR_VC_CONFIGURED_INFO.config2,
            AMR_VC_CONFIGURED_INFO.config3,
            AMR_VC_CONFIGURED_INFO.config4,
            AMR_VC_CONFIGURED_INFO.config5,
            AMR_VC_CONFIGURED_INFO.config6,
            AMR_VC_CONFIGURED_INFO.config7,
            AMR_VC_CONFIGURED_INFO.config8,
            AMR_VC_CONFIGURED_INFO.config9,
            AMR_VC_CONFIGURED_INFO.config10,
            AMR_VC_CONFIGURED_INFO.config11,
            AMR_VC_CONFIGURED_INFO.config12,
            AMR_VC_CONFIGURED_INFO.config13,
            AMR_VC_CONFIGURED_INFO.config14,
            AMR_VC_CONFIGURED_INFO.config15,
            AMR_VC_CONFIGURED_INFO.config16,
            AMR_VC_CONFIGURED_INFO.config17,
            AMR_VC_CONFIGURED_INFO.config18,
            AMR_VC_CONFIGURED_INFO.config19,
            AMR_VC_CONFIGURED_INFO.config20,
            AMR_CONFIGURED_DATA.METER_STREAM_NO
            
        FROM
            AMR_FIELD_ID, AMR_PL_group, AMR_CONFIGURED_DATA
        JOIN AMR_VC_CONFIGURED_INFO ON amr_configured_data.amr_vc_type = AMR_VC_CONFIGURED_INFO.vc_type
        WHERE
            AMR_PL_GROUP.FIELD_ID = AMR_FIELD_ID.FIELD_ID 
            AND AMR_CONFIGURED_DATA.METER_ID = AMR_FIELD_ID.METER_ID
            AND AMR_CONFIGURED_DATA.METER_STREAM_NO is not null
            
            {configured_date_condition}
            {tag_condition}
            {region_condition}
        """


    # Get selected values from the dropdowns
    billing_date_condition = "AND AMR_BILLING_DATA.DATA_DATE IS NOT NULL"
    configured_date_condition = "AND AMR_CONFIGURED_DATA.DATA_DATE IS NOT NULL"
    tag_condition = "AND AMR_FIELD_ID.TAG_ID IS NOT NULL"
    region_condition = "AND amr_pl_group.pl_region_id IS NOT NULL"

    selected_date = request.args.get("date_dropdown")
    selected_tag = request.args.get("tag_dropdown")
    selected_region = request.args.get("region_dropdown")

    # Fetch unique region values
    region_results = fetch_data(region_query)
    region_options = [str(region[0]) for region in region_results]

    # Fetch tag options based on the selected region
    tag_results = fetch_data(tag_query, params={"region_id": selected_region})
    tag_options = [str(tag[0]) for tag in tag_results]

    if selected_date:
        billing_date_condition = (
            f"AND TO_CHAR(AMR_BILLING_DATA.DATA_DATE, 'MM/YYYY') = '{selected_date}'"
        )
        configured_date_condition = (
            f"AND TO_CHAR(AMR_CONFIGURED_DATA.DATA_DATE, 'MM/YYYY') = '{selected_date}'"
        )
    if selected_tag:
        tag_condition = f"AND AMR_FIELD_ID.TAG_ID = '{selected_tag}'"

    if selected_region:
        region_condition = f"AND amr_pl_group.pl_region_id = '{selected_region}'"

    # Modify the query with the selected conditions
    query = query.format(
        billing_date_condition=billing_date_condition,
        configured_date_condition=configured_date_condition,
        tag_condition=tag_condition,
        region_condition=region_condition,
    )

    if selected_region:
        # Use fetch_data function to retrieve data
        results = fetch_data(query)

        if query_type == "daily_data":
            # Use pandas to create a DataFrame for daily_data
            df = pd.DataFrame(
                results,
                columns=[
                    "PL_REGION_ID",
                    "TAG_ID",
                    "METER_ID",
                    "DATA_DATE",
                    "CORRECTED",
                    "UNCORRECTED",
                    "Pressure",
                    "Temperature",
                    "METER_STREAM_NO",
                ],
            )
            df = df.drop(["PL_REGION_ID", "TAG_ID", "METER_ID"], axis=1)
            df["DATA_DATE"] = pd.to_datetime(df["DATA_DATE"])

            # Sort DataFrame by 'DATA_DATE'
            df = df.sort_values(by="DATA_DATE")

            df = df.drop_duplicates(subset=["DATA_DATE", "METER_STREAM_NO"], keep="first")
            # Remove newline characters
            df = df.apply(
                lambda x: x.str.replace("\n", "") if x.dtype == "object" else x
            )


            # สร้าง subplot และ traces สำหรับแต่ละกราฟ
            fig_corrected = sp.make_subplots(rows=1, cols=1, subplot_titles=["Corrected"])
            fig_uncorrected = sp.make_subplots(rows=1, cols=1, subplot_titles=["Uncorrected"])
            fig_pressure = sp.make_subplots(rows=1, cols=1, subplot_titles=["Pressure"])
            fig_temperature = sp.make_subplots(rows=1, cols=1, subplot_titles=["Temperature"])

            # เรียงลำดับ DataFrame ตาม 'DATA_DATE'
            df = df.sort_values(by="DATA_DATE", ascending=True)

            # สร้าง traces สำหรับแต่ละกราฟ
            trace_corrected = go.Scatter(
                x=df["DATA_DATE"],
                y=df["CORRECTED"],
                mode="lines+markers",
                name="CORRECTED",
                line=dict(color="blue", width=2),
            )

            trace_uncorrected = go.Scatter(
                x=df["DATA_DATE"],
                y=df["UNCORRECTED"],
                mode="lines+markers",
                name="UNCORRECTED",
                line=dict(color="red", width=2),
            )

            trace_pressure = go.Scatter(
                x=df["DATA_DATE"],
                y=df["Pressure"],
                mode="lines+markers",
                name="Pressure",
                line=dict(color="orange", width=2),
            )

            trace_temperature = go.Scatter(
                x=df["DATA_DATE"],
                y=df["Temperature"],
                mode="lines+markers",
                name="Temperature",
                line=dict(color="green", width=2),
            )

            # เพิ่ม traces ลงใน subplot
            fig_corrected.add_trace(trace_corrected)
            fig_uncorrected.add_trace(trace_uncorrected)
            fig_pressure.add_trace(trace_pressure)
            fig_temperature.add_trace(trace_temperature)

            # ปรับปรุงลักษณะและรายละเอียดของกราฟ
            for fig in [fig_corrected, fig_uncorrected, fig_pressure, fig_temperature]:
                fig.update_traces(
                    line_shape="linear", 
                    marker=dict(symbol="circle", size=6),
                    hoverinfo="text+x+y",  # แสดงข้อมูล tooltip
                    hovertext=df["DATA_DATE"],  # ข้อมูลที่แสดงใน tooltip
                )
                fig.update_layout(
                    legend=dict(x=0.6, y=1.25, orientation="h"),
                    yaxis_title="Values",
                    xaxis_title="Date",
                    hovermode="x unified",
                     # ใช้ template dark
                    yaxis=dict(type="linear", title="Values"),
                )
            fig.update_xaxes(title_text="Date", tickformat="%Y-%m-%d")


            # เพิ่มเติม: ปรับสีของแต่ละ trace
            for trace in fig.data:
                trace.marker.line.color = 'rgba(255,255,255,0)'
            # แสดงกราฟ
            graph_corrected = fig_corrected.to_html(full_html=False)
            graph_uncorrected = fig_uncorrected.to_html(full_html=False)
            graph_pressure = fig_pressure.to_html(full_html=False)
            graph_temperature = fig_temperature.to_html(full_html=False)
            # Assuming 'df' is the DataFrame created from the query results
            df_run1 = df[df['METER_STREAM_NO'] == '1']
            df_run2 = df[df['METER_STREAM_NO'] == '2']
            df_run3 = df[df['METER_STREAM_NO'] == '3']
            df_run4 = df[df['METER_STREAM_NO'] == '4']
            df_run5 = df[df['METER_STREAM_NO'] == '5']
            df_run6 = df[df['METER_STREAM_NO'] == '6']

            # Check if each DataFrame has data before including in the tables dictionary
            tables = {
                "config_data": None,
            }

            if not df_run1.empty:
               
                df_run1 = df_run1.drop('METER_STREAM_NO', axis=1, errors='ignore')
                tables["daily_data_run1"] = df_run1.to_html(classes="data", index=False)

            if not df_run2.empty:
               
                df_run2 = df_run2.drop('METER_STREAM_NO', axis=1, errors='ignore')
                tables["daily_data_ran2"] = df_run2.to_html(classes="data", index=False)

            if not df_run3.empty:
             
                df_run3 = df_run3.drop('METER_STREAM_NO', axis=1, errors='ignore')
                tables["daily_data_ran3"] = df_run3.to_html(classes="data", index=False)

            if not df_run4.empty:
               
                df_run4 = df_run4.drop('METER_STREAM_NO', axis=1, errors='ignore')
                tables["daily_data_run4"] = df_run4.to_html(classes="data", index=False)
            if not df_run5.empty:
               
                df_run4 = df_run5.drop('METER_STREAM_NO', axis=1, errors='ignore')
                tables["daily_data_run5"] = df_run5.to_html(classes="data", index=False)
            if not df_run6.empty:
               
                df_run4 = df_run6.drop('METER_STREAM_NO', axis=1, errors='ignore')
                tables["daily_data_run6"] = df_run6.to_html(classes="data", index=False)

            # เพิ่มเนื้อหา HTML สำหรับกราฟ
            df = df.sort_values(by="DATA_DATE", ascending=True)
            # ส่ง graph_html ไปยัง HTML template ของ Flask
            return render_template(
                "billingdata.html",
                tables=tables,

                titles=df.columns.values,
                selected_date=selected_date,
                selected_tag=selected_tag,
                selected_region=selected_region,
                region_options=region_options,
                tag_options=tag_options,
                graph_corrected=graph_corrected,
                graph_uncorrected=graph_uncorrected,
                graph_pressure=graph_pressure,
                graph_temperature=graph_temperature,
            )


        elif query_type == "config_data":
            # Use pandas to create a DataFrame for config_data
            df = pd.DataFrame(
                results,
                columns=[
                    "PL_REGION_ID",
                    "TAG_ID",
                    "METER_ID",
                    "DATA_DATE",
                    "AMR_CONFIG1",
                    "AMR_CONFIG2",
                    "AMR_CONFIG3",
                    "AMR_CONFIG4",
                    "AMR_CONFIG5",
                    "AMR_CONFIG6",
                    "AMR_CONFIG7",
                    "AMR_CONFIG8",
                    "AMR_CONFIG9",
                    "AMR_CONFIG10",
                    "AMR_CONFIG11",
                    "AMR_CONFIG12",
                    "AMR_CONFIG13",
                    "AMR_CONFIG14",
                    "AMR_CONFIG15",
                    "AMR_CONFIG16",
                    "AMR_CONFIG17",
                    "AMR_CONFIG18",
                    "AMR_CONFIG19",
                    "AMR_CONFIG20",
                    "CONFIG1",
                    "CONFIG2",
                    "CONFIG3",
                    "CONFIG4",
                    "CONFIG5",
                    "CONFIG6",
                    "CONFIG7",
                    "CONFIG8",
                    "CONFIG9",
                    "CONFIG10",
                    "CONFIG11",
                    "CONFIG12",
                    "CONFIG13",
                    "CONFIG14",
                    "CONFIG15",
                    "CONFIG16",
                    "CONFIG17",
                    "CONFIG18",
                    "CONFIG19",
                    "CONFIG20",
                    "METER_STREAM_NO",
                ]
            )
            columns_to_drop = [
                "CONFIG1",
                "CONFIG2",
                "CONFIG3",
                "CONFIG4",
                "CONFIG5",
                "CONFIG6",
                "CONFIG7",
                "CONFIG8",
                "CONFIG9",
                "CONFIG10",
                "CONFIG11",
                "CONFIG12",
                "CONFIG13",
                "CONFIG14",
                "CONFIG15",
                "CONFIG16",
                "CONFIG17",
                "CONFIG18",
                "CONFIG19",
                "CONFIG20",
            ]
            dropped_columns_data = pd.concat(
                [
                    pd.DataFrame(columns=df.columns),
                    pd.DataFrame(columns=columns_to_drop),
                ],
                axis=1,
            )
            dropped_columns_data = df[["DATA_DATE"] + columns_to_drop].head(1)
            dropped_columns_data[
                "DATA_DATE"
            ] = "DATA.DATE"  # Replace actual values with the column name
            dropped_columns_data = dropped_columns_data.to_dict(orient="records")

            df = df.drop(columns=columns_to_drop)  # Drop specified columns

            print(df.columns)
            df = df.drop(["PL_REGION_ID", "TAG_ID", "METER_ID"], axis=1)

            # Remove newline characters
            df = df.apply(
                lambda x: x.str.replace("\n", "") if x.dtype == "object" else x
            )
            df["DATA_DATE"] = pd.to_datetime(df["DATA_DATE"])

            df = df.drop_duplicates(subset=["DATA_DATE", "METER_STREAM_NO"], keep="first")
            # Sort DataFrame by 'DATA_DATE'
            df = df.sort_values(by="DATA_DATE")
            # Send the DataFrame to the HTML template
            df_run1 = df[df['METER_STREAM_NO'] == '1']
            df_run2 = df[df['METER_STREAM_NO'] == '2']
            df_run3 = df[df['METER_STREAM_NO'] == '3']
            df_run4 = df[df['METER_STREAM_NO'] == '4']
            df_run5 = df[df['METER_STREAM_NO'] == '5']
            df_run6 = df[df['METER_STREAM_NO'] == '6']

            # Check if each DataFrame has data before including in the tables dictionary
            tables = {
                "daily_data": None,
                
            }

            common_table_properties = {"classes": "data", "index": False,"header":None}

            if not df_run1.empty:
                df_run1 = df_run1.drop('METER_STREAM_NO', axis=1, errors='ignore')
                tables["config_data_run1"] = df_run1.to_html(**common_table_properties)
            if not df_run2.empty:
                df_run2 = df_run2.drop('METER_STREAM_NO', axis=1, errors='ignore')
                tables["config_data_run2"] = df_run2.to_html(**common_table_properties)
            if not df_run3.empty:
                df_run3 = df_run3.drop('METER_STREAM_NO', axis=1, errors='ignore')
                tables["config_data_run3"] = df_run3.to_html(**common_table_properties)
            if not df_run4.empty:
                df_run4 = df_run4.drop('METER_STREAM_NO', axis=1, errors='ignore')
                tables["config_data_run4"] = df_run4.to_html(**common_table_properties)
            if not df_run5.empty:
                df_run5 = df_run5.drop('METER_STREAM_NO', axis=1, errors='ignore')
                tables["config_data_run5"] = df_run4.to_html(**common_table_properties)
            if not df_run6.empty:
                df_run6 = df_run6.drop('METER_STREAM_NO', axis=1, errors='ignore')
                tables["config_data_run6"] = df_run4.to_html(**common_table_properties)
            return render_template(
                "billingdata.html",
                
                tables=tables,
                titles=df.columns.values,
                selected_date=selected_date,
                selected_tag=selected_tag,
                selected_region=selected_region,
                region_options=region_options,
                tag_options=tag_options, dropped_columns_data=dropped_columns_data
            )

    else:
        # Render the template without executing the query
        return render_template(
            "billingdata.html",
            selected_date=selected_date,
            selected_region=selected_region,
            selected_tag=selected_tag,
            region_options=region_options,
            tag_options=tag_options,
            tables={},
        )


############ / View Billing Data  #####################


############ Daily summary #####################
@app.route("/Daily_summary")
def Daily_summary():
    # SQL query to fetch unique PL_REGION_ID values
    region_query = """
    SELECT * FROM AMR_REGION 
    """

    # Fetch unique region values
    region_results = fetch_data(region_query)
    region_options = [str(region[0]) for region in region_results]

    # SQL query for main data
    query = """
    SELECT DISTINCT
    amr_field_id.TAG_ID as SITE
FROM
    AMR_FIELD_ID, AMR_PL_group, AMR_RMIU_TYPE, amr_region
    
WHERE
    AMR_PL_GROUP.FIELD_ID = AMR_FIELD_ID.FIELD_ID 
  {region_condition}
    """
    # Get selected values from the dropdowns
    selected_region = request.args.get("region_dropdown")

    # Fetch unique region values
    region_results = fetch_data(region_query)
    region_options = [str(region[0]) for region in region_results]

    # Initialize the query with a condition that is always true
    region_condition = "AND 1 = 1"

    # Fetch tag options based on the selected region
    if selected_region:
        region_condition = f"AND amr_pl_group.pl_region_id = '{selected_region}'"

    # Modify the query with the selected conditions
    query = query.format(region_condition=region_condition)

    # Check if a region is selected before executing the query
    if selected_region:
        # ใช้ fetch_data function ในการดึงข้อมูล
        results = fetch_data(query)

        # ใช้ pandas ในการสร้าง DataFrame
        df = pd.DataFrame(results, columns=["SITE"])
        # ลบคอลัมน์ที่ไม่ต้องการ
        df = df.applymap(lambda x: x.replace("\n", "") if isinstance(x, str) else x)

        # Sort DataFrame by the 'SITE' column (adjust as needed)
        df = df.sort_values(by="SITE")

        # ส่ง DataFrame ไปยัง HTML template
        return render_template(
            "Daily_summary.html",
            tables=[df.to_html(classes="data", index=False)],
            titles=df.columns.values,
            selected_region=selected_region,
            region_options=region_options,
        )
    else:
        # Render the template without executing the query
        return render_template(
            "Daily_summary.html",
            selected_region=selected_region,
            region_options=region_options,
            tables=[],
        )


############ /Daily summary  #####################


############ sitedetail_data  #####################


@app.route("/sitedetail_data")
def sitedetail_data():
    # SQL query to fetch unique PL_REGION_ID values
    region_query = """
    SELECT * FROM AMR_REGION 
    """

    # Fetch unique region values
    region_results = fetch_data(region_query)
    region_options = [str(region[0]) for region in region_results]

    # SQL query for main data
    query = """
    SELECT DISTINCT
    AMR_FIELD_ID.ID,
    amr_field_id.TAG_ID as SITE,
    AMR_FIELD_ID.AMR_PHASE as PHASE,
    AMR_FIELD_ID.SIM_IP as IPADDRESS,
    (SELECT rmiu_name FROM AMR_RMIU_TYPE WHERE AMR_RMIU_TYPE.ID = AMR_FIELD_ID.RMIU_TYPE) as TYPE
    
FROM
    AMR_FIELD_ID, AMR_PL_group, AMR_RMIU_TYPE, amr_region
    
WHERE
    AMR_PL_GROUP.FIELD_ID = AMR_FIELD_ID.FIELD_ID 
        {region_condition}
    """

    # Get selected values from the dropdowns
    selected_region = request.args.get("region_dropdown")

    # Fetch unique region values
    region_results = fetch_data(region_query)
    region_options = [str(region[0]) for region in region_results]

    # Initialize the query with a condition that is always true
    region_condition = "AND 1 = 1"

    # Fetch tag options based on the selected region
    if selected_region:
        region_condition = f"AND amr_pl_group.pl_region_id = '{selected_region}'"

    # Modify the query with the selected conditions
    query = query.format(region_condition=region_condition)

    # Check if a region is selected before executing the query
    if selected_region:
        # ใช้ fetch_data function ในการดึงข้อมูล
        results = fetch_data(query)

        # ใช้ pandas ในการสร้าง DataFrame
        df = pd.DataFrame(
            results, columns=["ID", "SITE", "PHASE", "IP ADDRESS", "TYPE"]
        )
        # ลบคอลัมน์ที่ไม่ต้องการ
        df = df.applymap(lambda x: x.replace("\n", "") if isinstance(x, str) else x)

        # Sort DataFrame by the 'SITE' column (adjust as needed)
        df = df.sort_values(by="SITE")

        # ส่ง DataFrame ไปยัง HTML template
        return render_template(
            "sitedetail.html",
            tables=[df.to_html(classes="data", index=False)],
            titles=df.columns.values,
            selected_region=selected_region,
            region_options=region_options,
        )
    else:
        # Render the template without executing the query
        return render_template(
            "sitedetail.html",
            selected_region=selected_region,
            region_options=region_options,
            tables=[],
        )


############ /sitedetail_data  #####################


############ Manualpoll_data  #####################
@app.route("/Manualpoll_data")
def Manualpoll_data():
    region_query = """
        SELECT * FROM AMR_REGION 
        """
    tag_query = """
        SELECT DISTINCT TAG_ID
        FROM AMR_FIELD_ID
        JOIN AMR_PL_GROUP ON AMR_FIELD_ID.FIELD_ID = AMR_PL_GROUP.FIELD_ID 
        WHERE AMR_PL_GROUP.PL_REGION_ID = :region_id
        """

    region_results = fetch_data(region_query)
    region_options = [str(region[0]) for region in region_results]

    query = """
        SELECT
            AMR_FIELD_METER.METER_STREAM_NO as RunNo,
            AMR_PL_GROUP.PL_REGION_ID as region,
            AMR_FIELD_ID.TAG_ID as Sitename,
            AMR_FIELD_METER.METER_NO_STREAM as NoRun,
            AMR_FIELD_METER.METER_ID as METERID,
            AMR_VC_TYPE.VC_NAME as VCtype,
            AMR_FIELD_ID.SIM_IP as IPAddress,
            
             AMR_PORT_INFO.PORT_NO as port,
            amr_poll_range.evc_type as evc_type,
    
   amr_vc_type.vc_name as vc_name ,
   amr_poll_range.poll_billing as poll_billing ,
    amr_poll_range.poll_config as poll_config,
    amr_poll_range.poll_billing_enable as poll_billing_enable ,
   amr_poll_range.poll_config_enable as poll_config_enable
        FROM
            AMR_FIELD_ID,
            AMR_USER,
            AMR_FIELD_CUSTOMER,
            AMR_FIELD_METER,
            AMR_PL_GROUP,
            AMR_VC_TYPE,
            AMR_PORT_INFO,
            amr_poll_range
        WHERE
            AMR_USER.USER_ENABLE=1 AND
            amr_vc_type.id=amr_poll_range.evc_type AND
            AMR_FIELD_ID.FIELD_ID = AMR_PL_GROUP.FIELD_ID AND
            AMR_FIELD_ID.METER_ID = AMR_USER.USER_GROUP AND
            AMR_FIELD_ID.CUST_ID = AMR_FIELD_CUSTOMER.CUST_ID AND
            AMR_FIELD_ID.METER_ID = AMR_FIELD_METER.METER_ID AND
            AMR_VC_TYPE.ID = AMR_FIELD_METER.METER_STREAM_TYPE AND
            AMR_FIELD_METER.METER_PORT_NO = AMR_PORT_INFO.ID
            {tag_condition}
            {region_condition}
        """

    tag_condition = "AND AMR_FIELD_ID.TAG_ID IS NOT NULL"
    region_condition = "AND amr_pl_group.pl_region_id = 'default_region_id'"

    selected_tag = request.args.get("tag_dropdown")
    selected_region = request.args.get("region_dropdown")

    region_results = fetch_data(region_query)
    region_options = [str(region[0]) for region in region_results]

    tag_results = fetch_data(tag_query, params={"region_id": selected_region})
    tag_options = [str(tag[0]) for tag in tag_results]

    # Sort the tag options alphabetically
    tag_options.sort()

    if selected_tag:
        tag_condition = f"AND AMR_FIELD_ID.TAG_ID = '{selected_tag}'"
    if selected_region:
        region_condition = f"AND amr_pl_group.pl_region_id = '{selected_region}'"

    query = query.format(tag_condition=tag_condition, region_condition=region_condition)

    results = fetch_data(query)
    df = pd.DataFrame(
        results,
        columns=[
            "RUN",
            "Region",
            "Sitename",
            "NoRun",
            "METERID",
            "VCtype",
            "IPAddress",
            "Port",
            "evc_type",
            "vc_name",
            "poll_billing",
            "poll_config",
            "poll_billing_enable",
            "poll_config_enable",
        ],
    )

    return render_template(
        "Manual_poll.html",
        tables=[df.to_html(classes="data")],
        titles=df.columns.values,
        selected_tag=selected_tag,
        selected_region=selected_region,
        region_options=region_options,
        tag_options=tag_options,
        df=df,
    )


@app.route("/Manualpoll_data", methods=["POST"])
def read_data():
    global change_to_32bit_counter  # Use the global variable

    slave_id = int(request.form["slave_id"])
    function_code = int(request.form["function_code"])
    if request.form["starting_address"] == "custom":
        if "custom_starting_address" in request.form:
            starting_address = int(request.form["custom_starting_address"])
        else:
            starting_address = 0  # หรือใส่ค่าเริ่มต้นที่คุณต้องการ
    else:
        starting_address = int(request.form["starting_address"])
    quantity = int(request.form["quantity"])
    tcp_ip = request.form["tcp_ip"]
    tcp_port = int(request.form["tcp_port"])

    # Check if the data should be displayed in 16-bit format or 32-bit format
    is_16bit = request.form.get("is_16bit") == "true"

    if is_16bit:
        bytes_per_value = 2
    else:
        bytes_per_value = 4
        if change_to_32bit_counter > 0:
            quantity *= 2
            change_to_32bit_counter -= 1

    # Build the request message
    request_message = bytearray(
        [
            slave_id,
            function_code,
            starting_address >> 8,
            starting_address & 0xFF,
            quantity >> 8,
            quantity & 0xFF,
        ]
    )

    crc = computeCRC(request_message)
    request_message += crc.to_bytes(2, byteorder="big")

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((tcp_ip, tcp_port))

    # Store the TX message in communication_traffic
    communication_traffic.append({"direction": "TX", "data": request_message.hex()})

    sock.send(request_message)

    response = sock.recv(1024)

    # Store the RX message in communication_traffic
    communication_traffic.append({"direction": "RX", "data": response.hex()})

    sock.close()

    data = response[3:]

    values = [
        int.from_bytes(data[i : i + bytes_per_value], byteorder="big", signed=False)
        for i in range(0, len(data), bytes_per_value)
    ]

    if "32bit" in request.form and request.form["32bit"] == "true":
        is_32bit = True
    else:
        is_32bit = False

    data_list = []
    address = starting_address
    value = 0

    for i, value in enumerate(values):
        address = starting_address + i * 2
        type_value = get_type_value_from_database(address)
        hex_value = hex(value)  # Convert the decimal value to HEX
        binary_value = convert_to_binary_string(value, bytes_per_value)
        float_value = struct.unpack("!f", struct.pack("!I", value))[0]
        description = get_description_from_database(address)

        if description is None:
            description = f"Address {address}"
            address += 0

        if is_16bit:
            signed_value = value - 2**16 if value >= 2**15 else value
            is_16bit_value = True
            float_value = value if is_16bit_value else float_value
            float_display_value = f"16-bit signed: {signed_value}, float: {float_value}"
        else:
            signed_value = value - 2**32 if value >= 2**31 else value
            is_16bit_value = False
            float_value = (
                float_value
                if is_16bit_value
                else struct.unpack("!f", struct.pack("!I", value))[0]
            )
            float_signed_value = (
                signed_value if is_16bit_value else None
            )  # Set signed_value to None for 32-bit

            # Apply type_value check after determining 16-bit or 32-bit format
            if type_value == "Float":
                # Set float_display_value to the float representation
                float_display_value = float_value
            elif type_value == "signed":
                # Set float_display_value to the signed representation
                float_display_value = signed_value
            else:
                # Handle other cases or set a default behavior
                float_display_value = "Undefined"
                print(f"Type Value for address {address}: {type_value}")
        data_list.append(
            {
                "description": description,
                "address": address,
                "value": value,
                "hex_value": hex_value,
                "binary_value": binary_value,
                "float_value": float_display_value,
                "signed_value": signed_value,
                "is_16bit": is_16bit_value,
                "float_signed_value": signed_value,
            }
        )

        value, updated_address = handle_action_configuration(i, value, address)
        # หลังจาก values = [int.from_bytes(data[i:i + bytes_per_value], byteorder='big', signed=False) for i in range(0, len(data), bytes_per_value)]
    # แทนที่ด้วย:

    values = [
        int.from_bytes(data[i : i + bytes_per_value], byteorder="big", signed=False)
        for i in range(0, len(data), bytes_per_value)
    ]

    # หากต้องการแปลงเฉพาะแถวแรก สามารถทำได้เช่นนี้:

    session["tcp_ip"] = tcp_ip
    session["tcp_port"] = tcp_port

    # ตรวจสอบค่า is_16bit เพื่อเพิ่มข้อมูลลงในตาราง 16-bit
    if not is_16bit:
        # เพิ่มข้อมูลลงในตาราง 16-bit โดยเพิ่มค่าลงในตารางเดิมและเพิ่มค่าอีก 1
        data_list_16bit = []
        for data_16bit in data_list:
            address_16bit = data_16bit["address"]
            value_16bit = (
                data_16bit["value"] * 2
            )  # เพิ่มค่าขึ้นเป็น 2 เท่าเพื่อให้เป็น 1 เท่าของข้อมูลเดิม
            data_list_16bit.append({"address": address_16bit, "value": value_16bit})

    region_query = """
        SELECT * FROM AMR_REGION 
        """
    tag_query = """
        SELECT DISTINCT TAG_ID
        FROM AMR_FIELD_ID
        JOIN AMR_PL_GROUP ON AMR_FIELD_ID.FIELD_ID = AMR_PL_GROUP.FIELD_ID 
        WHERE AMR_PL_GROUP.PL_REGION_ID = :region_id
        """

    region_results = fetch_data(region_query)
    region_options = [str(region[0]) for region in region_results]

    query = """
        SELECT
            AMR_FIELD_METER.METER_STREAM_NO as RunNo,
            AMR_PL_GROUP.PL_REGION_ID as region,
            AMR_FIELD_ID.TAG_ID as Sitename,
            AMR_FIELD_METER.METER_NO_STREAM as NoRun,
            AMR_FIELD_METER.METER_ID as METERID,
            AMR_VC_TYPE.VC_NAME as VCtype,
            AMR_FIELD_ID.SIM_IP as IPAddress,
            
             AMR_PORT_INFO.PORT_NO as port,
            amr_poll_range.evc_type as evc_type,
    
   amr_vc_type.vc_name as vc_name ,
   amr_poll_range.poll_billing as poll_billing ,
    amr_poll_range.poll_config as poll_config,
    amr_poll_range.poll_billing_enable as poll_billing_enable ,
   amr_poll_range.poll_config_enable as poll_config_enable
        FROM
            AMR_FIELD_ID,
            AMR_USER,
            AMR_FIELD_CUSTOMER,
            AMR_FIELD_METER,
            AMR_PL_GROUP,
            AMR_VC_TYPE,
            AMR_PORT_INFO,
            amr_poll_range
        WHERE
            AMR_USER.USER_ENABLE=1 AND
            amr_vc_type.id=amr_poll_range.evc_type AND
            AMR_FIELD_ID.FIELD_ID = AMR_PL_GROUP.FIELD_ID AND
            AMR_FIELD_ID.METER_ID = AMR_USER.USER_GROUP AND
            AMR_FIELD_ID.CUST_ID = AMR_FIELD_CUSTOMER.CUST_ID AND
            AMR_FIELD_ID.METER_ID = AMR_FIELD_METER.METER_ID AND
            AMR_VC_TYPE.ID = AMR_FIELD_METER.METER_STREAM_TYPE AND
            AMR_FIELD_METER.METER_PORT_NO = AMR_PORT_INFO.ID
            {tag_condition}
            {region_condition}
        """

    tag_condition = "AND AMR_FIELD_ID.TAG_ID IS NOT NULL"
    region_condition = "AND amr_pl_group.pl_region_id IS NOT NULL"

    selected_tag = request.args.get("tag_dropdown")
    selected_region = request.args.get("region_dropdown")

    region_results = fetch_data(region_query)
    region_options = [str(region[0]) for region in region_results]

    tag_results = fetch_data(tag_query, params={"region_id": selected_region})
    tag_options = [str(tag[0]) for tag in tag_results]

    # Sort the tag options alphabetically
    tag_options.sort()

    if selected_tag:
        tag_condition = f"AND AMR_FIELD_ID.TAG_ID = '{selected_tag}'"
    if selected_region:
        region_condition = f"AND amr_pl_group.pl_region_id = '{selected_region}'"

    query = query.format(tag_condition=tag_condition, region_condition=region_condition)
    df = pd.DataFrame(
        columns=[
            "RUN",
            "Region",
            "Sitename",
            "NoRun",
            "METERID",
            "VCtype",
            "IPAddress",
            "Port",
            "evc_type",
            "vc_name",
            "poll_billing",
            "poll_config",
            "poll_billing_enable",
            "poll_config_enable",
        ]
    )
    if selected_region:
        results = fetch_data(query)
        df = pd.DataFrame(
            results,
            columns=[
                "RUN",
                "Region",
                "Sitename",
                "NoRun",
                "METERID",
                "VCtype",
                "IPAddress",
                "Port",
                "evc_type",
                "vc_name",
                "poll_billing",
                "poll_config",
                "poll_billing_enable",
                "poll_config_enable",
            ],
        )
        # ... (other code)

    return render_template(
        "Manual_poll.html",
        df=df,
        data_list=data_list,
        slave_id=slave_id,
        function_code=function_code,
        starting_address=starting_address,
        quantity=quantity,
        is_16bit=is_16bit,
        communication_traffic=communication_traffic,
        data=data,
        tables=[df.to_html(classes="data")],
        titles=df.columns.values,
        selected_tag=selected_tag,
        selected_region=selected_region,
        region_options=region_options,
        tag_options=tag_options,
    )


def handle_actaris_action(i, address):
    return address


def handle_action_configuration(i, value, address):
    return value, address


def get_description_from_database(address):
    query = "SELECT DESCRIPTION FROM AMR_ADDRESS_MAPPING1 WHERE ADDRESS = :address"
    params = {"address": address}
    result = fetch_data(query, params)
    return result[0][0] if result else None


@app.route("/process_selected_rows", methods=["POST"])
def process_selected_rows():
    selected_rows = request.form.getlist("selected_rows")
    return "Selected rows processed successfully"


def get_type_value_from_database(address):
    query = "SELECT TYPE_VALUE FROM AMR_ADDRESS_MAPPING1 WHERE ADDRESS = :address"
    result = fetch_data(query, params={"address": address})
    if result:
        return result[0][0]  # Assuming TYPE_VALUE is the first column in the result
    return None


############ /Manualpoll_data  #####################
@app.route("/logout")
def logout():
    # ล้าง session หรือทำงานอื่น ๆ ที่คุณต้องการเมื่อลงชื่อออก
    session.clear()
    # ส่งไปยังหน้าลงชื่อเข้าใช้หลังจากลงชื่อออก
    return redirect(url_for("login"))


###############################################


def insert_address_range_to_oracle(
    poll_config, poll_billing, enable_config, enable_billing, evc_type
):
    dsn = cx_Oracle.makedsn(hostname, port, service_name)

    with cx_Oracle.connect(
        user=username, password=password, dsn=dsn
    ) as connection:
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


@app.route("/add_polling_route")
def add_polling_route():
    return render_template("add_polling.html")


MAX_ADDRESS_LENGTH = 249


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
            evc_type,
        )

        response = {"status": "success", "message": "Data saved successfully"}
    except ValueError as ve:
        response = {"status": "error", "message": str(ve)}
    except cx_Oracle.DatabaseError as e:
        response = {"status": "error", "message": f"Database Error: {e}"}
    except Exception as e:
        response = {"status": "error", "message": f"Error: {e}"}

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

        dsn_tns = cx_Oracle.makedsn(
            hostname, port, service_name
        )
        connection = cx_Oracle.connect(
            user=username, password=password, dsn=dsn_tns
        )

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

        dsn_tns = cx_Oracle.makedsn(
            hostname, port, service_name
        )
        connection = cx_Oracle.connect(
            user=username, password=password, dsn=dsn_tns
        )

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


####################################################


if __name__ == "__main__":
    app.run(debug=True)
