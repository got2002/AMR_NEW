from flask import Flask, render_template, request, jsonify
import cx_Oracle
import pandas as pd
from flask_sqlalchemy import SQLAlchemy

region_query = """
        SELECT
            EVC_TYPE,
            POLL_CONFIG,
            POLL_BILLING,
            POLL_CONFIG_ENABLE,
            POLL_BILLING_ENABLE
        FROM
            AMR_POLL_RANGE
    """

address_mapping_query = """
        SELECT
            ADDRESS,
            DESCRIPTION,
            TYPE_VALUE,
            EVC_TYPE,
            OR_DER,
            DATA_TYPE
        FROM
            AMR_ADDRESS_MAPPING1
    """

# Fetch data for both queries
region_data = fetch_data(region_query)
address_mapping_data = fetch_data(address_mapping_query)

# Convert the result to Pandas DataFrames for easier manipulation (optional)
region_column_names = [
    "EVC Type",
    "Poll Config",
    "Poll Billing",
    "Poll Config Enable",
    "Poll Billing Enable",
]
region_df = pd.DataFrame(region_data, columns=region_column_names)

address_mapping_column_names = [
    "ADDRESS",
    "DESCRIPTION",
    "TYPE_VALUE",
    "EVC_TYPE",
    "OR_DER",
    "DATA_TYPE",
]
address_mapping_df = pd.DataFrame(
    address_mapping_data, columns=address_mapping_column_names
)

# Pass the DataFrames to the HTML template
if __name__ == "__main__":
    app.run(debug=True)
