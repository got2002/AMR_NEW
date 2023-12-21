from flask import Flask, render_template, request, jsonify
import pandas as pd
import cx_Oracle

app = Flask(__name__)

# Replace these values with your actual database credentials
username = 'root'
password = 'root'
hostname = '192.168.102.192'
port = '1521'
service_name = 'orcl'

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
        error, = e.args
        print("Oracle Error:", error)
        return []

@app.route('/get_tags', methods=['GET'])
def get_tags():
    selected_region = request.args.get('selected_region')

    tag_query = """
    SELECT DISTINCT TAG_ID
    FROM AMR_FIELD_ID
    JOIN AMR_PL_GROUP ON AMR_FIELD_ID.FIELD_ID = AMR_PL_GROUP.FIELD_ID 
    WHERE AMR_PL_GROUP.PL_REGION_ID = :region_id
    """

    tag_results = fetch_data(tag_query, params={'region_id': selected_region})
    tag_options = [str(tag[0]) for tag in tag_results]

    # Sort the tag options alphabetically
    tag_options.sort()

    return jsonify({'tag_options': tag_options})

@app.route('/')
def index():
    try:
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
            AMR_PORT_INFO.PORT_NO as port
        FROM
            AMR_FIELD_ID,
            AMR_USER,
            AMR_FIELD_CUSTOMER,
            AMR_FIELD_METER,
            AMR_PL_GROUP,
            AMR_VC_TYPE,
            AMR_PORT_INFO
        WHERE
            AMR_USER.USER_ENABLE=1 AND
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

        selected_tag = request.args.get('tag_dropdown')
        selected_region = request.args.get('region_dropdown')

        region_results = fetch_data(region_query)
        region_options = [str(region[0]) for region in region_results]

        tag_results = fetch_data(tag_query, params={'region_id': selected_region})
        tag_options = [str(tag[0]) for tag in tag_results]

        # Sort the tag options alphabetically
        tag_options.sort()

        if selected_tag:
            tag_condition = f"AND AMR_FIELD_ID.TAG_ID = '{selected_tag}'"
        if selected_region:
            region_condition = f"AND amr_pl_group.pl_region_id = '{selected_region}'"

        query = query.format(tag_condition=tag_condition, region_condition=region_condition)

        results = fetch_data(query)

        df = pd.DataFrame(results, columns=[
            'RUN', 'Region', 'Sitename', 'NoRun', 'METERID', 'VCtype', 'IPAddress', 'Port'
        ])
        
        return render_template('billingdata.html', tables=[df.to_html(classes='data')],
                               titles=df.columns.values,
                               selected_tag=selected_tag,
                               selected_region=selected_region,
                               region_options=region_options,
                               tag_options=tag_options)
    except Exception as e:
        # Log the error for debugging purposes
        print("Error:", str(e))
        return "An error occurred."
if __name__ == '__main__':
    app.run(debug=True)
