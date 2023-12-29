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
        connection = cx_Oracle.connect(user=oracle_username, password=oracle_password, dsn=dsn)

        # Perform database operations here
        # Example: execute a query using the addresses
        cursor = connection.cursor()

        # Create an empty list to store the results
        poll_config_results = []

        for address in addresses:
            cursor.execute("SELECT POLL_CONFIG FROM AMR_POLL_RANGE WHERE ADDRESS = :address", {'address': address})
            rows = cursor.fetchall()
            for row in rows:
                # Append the result to the list
                poll_config_results.append(row[0])

        # Display the results
        print("Poll Config Results:", poll_config_results)

        # Convert the list to a numpy array
        poll_config_array = np.array(poll_config_results)

        # Save the array to a file (e.g., CSV)
        np.savetxt('poll_config_array.csv', poll_config_array, delimiter=',')

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
