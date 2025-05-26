import mysql.connector

try:
    db = mysql.connector.connect(
        host="localhost",
        user="root",  # Replace with your username
        password="Nakara",  # Replace with your password
        database="healthtech"
    )
    print("Connection successful!")
    db.close()
except mysql.connector.Error as err:
    print(f"Error: {err}")