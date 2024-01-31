import mysql.connector

class DatabaseOperations:
    def __init__(self, host, user, password, database):
        self.connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        self.cursor = self.connection.cursor()

    def insert_data(self, data):
        query = "INSERT INTO your_table_name (vendor_name, gstin, phone_no, email, state, address) VALUES (%s, %s, %s, %s, %s, %s)"
        self.cursor.execute(query, data)
        self.connection.commit()

    def get_all_data(self):
        query = "SELECT * FROM your_table_name"
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def delete_data(self, vendor_name, gstin):
        query = "DELETE FROM your_table_name WHERE vendor_name = %s AND gstin = %s"
        self.cursor.execute(query, (vendor_name, gstin))
        self.connection.commit()

    def close_connection(self):
        self.cursor.close()
        self.connection.close()
