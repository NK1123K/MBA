import mysql.connector
# from common_database_config import common_database_config

class VendorDBOperations:
    def __init__(self):
        self.connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='root',
            database='ims'
        )
        self.cursor = self.connection.cursor()
        # self.config = common_database_config()
        # self.connection = mysql.connector.connect(**self.config)
        self.create_table_if_not_exists()

    def create_table_if_not_exists(self):
        create_table_query = """
        CREATE TABLE IF NOT EXISTS vendors (
            id INT AUTO_INCREMENT PRIMARY KEY,
            vendor_name VARCHAR(255),
            gstin VARCHAR(255),
            phone_no VARCHAR(255),
            email VARCHAR(255),
            state VARCHAR(255),
            address VARCHAR(255)
        )
        """
        self.cursor.execute(create_table_query)
        self.connection.commit()

    def insert_vendor(self, vendor_data):
        sql = "INSERT INTO vendors (vendor_name, gstin, phone_no, email, state, address) VALUES (%s, %s, %s, %s, %s, %s)"
        self.cursor.execute(sql, vendor_data)
        self.connection.commit()

    def delete_vendor(self, vendor_id):
        sql = "DELETE FROM vendors WHERE id = %s"
        self.cursor.execute(sql, (vendor_id,))
        self.connection.commit()

    # Other database operations like update, select, etc. can be added here
    def get_all_vendors(self, search_text=None):  # Accept search_text parameter
        if search_text is not None and search_text.strip():  # Check if search_text is not empty
            sql = "SELECT * FROM vendors WHERE vendor_name LIKE %s"  # Use LIKE for partial search
            self.cursor.execute(sql, ('%' + search_text + '%',))
        else:
            sql = "SELECT * FROM vendors"
            self.cursor.execute(sql)
        return self.cursor.fetchall()



    def __del__(self):
        self.cursor.close()
        self.connection.close()
