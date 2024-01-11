import sys
from PyQt5 import QtWidgets
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QIntValidator
from PyQt5.QtWidgets import (
    QApplication,
    QHeaderView,
    QMainWindow,
    QScrollArea,
    QSizePolicy,
    QTextEdit,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QFormLayout,
    QTableWidget,
    QTableWidgetItem,
    QListWidget,
    QStackedWidget,
    QListWidgetItem,
)
import mysql.connector

class SideNavigationMenu(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Side Navigation Menu")
        self.setGeometry(100, 100, 800, 500)
        self.db_connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='MySql@12345',
            database='test'
        )
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.fetch_vendor_data)
        self.timer.start(1000)  # Update data every 5000 milliseconds (5 seconds)
        print("Timer started.")
        self.cursor = self.db_connection.cursor()  # Define the cursor here
        self.initUI()
        # Add a flag to indicate whether the form is in "Add" or "Edit" mode
        self.edit_mode = False
        self.submit_button1.clicked.connect(self.add_data_to_table)
        self.toggle_button_state()  # Call the toggle_button_state method here

    def initUI(self):
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        central_layout = QHBoxLayout(central_widget)

        menu_widget = QListWidget()
        menu_widget.setMaximumWidth(150)
        menu_widget.addItem("Home")
        menu_widget.addItem("Vendor Details")
        menu_widget.setStyleSheet("background-color: grey")
        menu_widget.itemClicked.connect(self.displayContent)
        central_layout.addWidget(menu_widget)

        self.stacked_widget = QStackedWidget()
        central_layout.addWidget(self.stacked_widget)

        home_widget = QWidget()
        home_layout = QVBoxLayout(home_widget)
        home_label = QLabel("Welcome to the Home Page")
        home_layout.addWidget(home_label)
        self.stacked_widget.addWidget(home_widget)

        vendor_details_widget = QWidget()
        vendor_details_layout = QHBoxLayout(vendor_details_widget)
        self.stacked_widget.addWidget(vendor_details_widget)
        self.Vendor_Details(vendor_details_layout)

    def displayContent(self, item):
        selected_item_text = item.text()
        if selected_item_text == "Home":
            self.stacked_widget.setCurrentIndex(0)
        elif selected_item_text == "Vendor Details":
            self.stacked_widget.setCurrentIndex(1)

    def Vendor_Details(self, layout1):
        vendor_form_widget = QWidget()
        table_widget = QWidget()
        table_widget = QScrollArea()

        vendor_form_layout = QVBoxLayout(vendor_form_widget)
        table_layout = QVBoxLayout(table_widget)

        vendor_form_layout.setAlignment(Qt.AlignTop)

        vendor_form_layout.addWidget(QLabel("Vendor Details"))

        vendor_form_widget.setMinimumSize(300, 0)
        vendor_form_widget.setMaximumSize(300, 800)
        table_widget.setMinimumSize(300, 0)

        form_layout1 = QFormLayout()

        labels1 = [
            "Vendor Name:",
            "GSTIN:",
            "Phone No:",
            "E-Mail:",
            "State:",
        ]

        self.vendor_entry_fields = {}

        for label_text in labels1:
            label1 = QLabel(label_text)

            # Integer validator for Phone Number
            if label_text == "Phone No:":
                entry1 = QLineEdit()
                onlyInt = QIntValidator()
                entry1.setValidator(onlyInt)
            else:
                entry1 = QLineEdit()

            # Set placeholders for specific fields
            if label_text == "Vendor Name:":
                entry1.setPlaceholderText("Enter Vendor Name")
            elif label_text == "GSTIN:":
                entry1.setPlaceholderText("Enter GSTIN")
            elif label_text == "Phone No:":
                entry1.setPlaceholderText("Enter Phone No")
            elif label_text == "E-Mail:":
                entry1.setPlaceholderText("Enter E-Mail ID")
            elif label_text == "State:":
                entry1.setPlaceholderText("Enter State")

            form_layout1.addRow(label1, entry1)
            self.vendor_entry_fields[label_text] = entry1

        # Address field
        address_label = QLabel("Address:")
        address_entry = QTextEdit()  # Use QTextEdit instead of QLineEdit
        address_entry.setPlaceholderText("Enter Address")

        # You can use the following line to make the address input box expand horizontally
        address_entry.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        form_layout1.addRow(address_label, address_entry)
        self.vendor_entry_fields["Address:"] = address_entry

        self.submit_button1 = QPushButton("Save")
        self.submit_button1.clicked.connect(self.add_data_to_table)
        self.submit_button1.setStyleSheet("background-color: Cyan")

        back_button = QPushButton("Back")
        back_button.clicked.connect(lambda: self.displayContent(QListWidgetItem("Home")))
        back_button.setStyleSheet("background-color: silver")

        vendor_form_layout.addLayout(form_layout1)
        vendor_form_layout.addWidget(self.submit_button1)
        vendor_form_layout.addWidget(back_button)

        # table_layout.addWidget(QLabel("Vendor Details"))
        self.vendor_table = QTableWidget()
        self.vendor_table.setColumnCount(8)
        self.vendor_table.setHorizontalHeaderLabels(
            ["Vendor Name", "GSTIN", "Phone No", "E-Mail", "State", "Address", "", ""]
        )
        table_layout.addWidget(self.vendor_table)

        # Set the table to resize horizontally based on the available space
        self.vendor_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        table_widget.setWidget(self.vendor_table)
        table_widget.setWidgetResizable(True)  # Allow the table to be scrollable if it doesn't fit

        layout1.addWidget(vendor_form_widget)
        layout1.addWidget(table_widget)

        	
        # Connect the "Edit" and "Delete" buttons to their respective functions
        self.vendor_table.cellClicked.connect(self.cell_clicked)

        # Fetch and display data
        self.fetch_vendor_data()

    
    def cell_clicked(self, row, col):
        if col == self.vendor_table.columnCount() - 3:  # "Edit" button column
            self.edit_row(row)
        elif col == self.vendor_table.columnCount() - 2:  # "Delete" button column
            self.delete_row(row)

    def edit_row(self, row):
        # Get the data from the selected row
        vendor_data = []
        for col in range(self.vendor_table.columnCount() - 2):  # Exclude the "Edit" and "Delete" columns
            item = self.vendor_table.item(row, col)
            vendor_data.append(item.text())

        # Populate the form fields with the data from the selected row
        for label, entry in self.vendor_entry_fields.items():
            if label == "Address:":
                entry.setPlainText(vendor_data.pop(0))
            else:
                entry.setText(vendor_data.pop(0))
        # Set up the form for editing
        self.edit_mode = True
        self.submit_button1.setText("Update")
        #self.submit_button1.clicked.disconnect(self.add_data_to_table)
        self.submit_button1.clicked.disconnect()
        self.submit_button1.clicked.connect(lambda: self.update_data_in_table(row))

    """def toggle_button_state(self):
        if self.edit_mode:
            self.submit_button1.setText("Update")
            self.submit_button1.setEnabled(True)  # Enable the "Update" button in edit mode
        else:
            self.submit_button1.setText("Save")
            self.submit_button1.setEnabled(
                not all(
                    entry.toPlainText() == "" if isinstance(entry, QTextEdit) else entry.text() == ""
                    for entry in self.vendor_entry_fields.values()
                )
            )  # Enable the "Save" button if any field is non-empty
        if self.vendor_table.rowCount() == 0:
            self.submit_button1.setDisabled(True)
        else:
            self.submit_button1.setDisabled(False)
        #self.submit_button1.setDisabled(self.vendor_table.rowCount() == 0)"""
    """def toggle_button_state(self):
        if self.edit_mode:
            self.submit_button1.setText("Update")
            self.submit_button1.setEnabled(True)
        else:
            empty_fields = all(
                entry.toPlainText() == "" if isinstance(entry, QTextEdit) else entry.text() == ""
                for entry in self.vendor_entry_fields.values()
            )
            self.submit_button1.setEnabled(not empty_fields)

        if self.vendor_table.rowCount() == 0:
            self.submit_button1.setDisabled(True)
        else:
            self.submit_button1.setDisabled(False)"""

    def toggle_button_state(self):
        if self.edit_mode:
            self.submit_button1.setText("Update")
            self.submit_button1.setEnabled(True)
        else:
            
            self.submit_button1.setText("Save")
            self.submit_button1.setEnabled(
                not all(
                    entry.toPlainText() == "" if isinstance(entry, QTextEdit) else entry.text() == ""
                    for entry in self.vendor_entry_fields.values()
                )
            ) 
        if self.vendor_table.rowCount() == 0:
            self.submit_button1.setDisabled(True)
        else:
            self.submit_button1.setDisabled(False)

        # Connect the appropriate function based on the edit mode
        if self.edit_mode:
            self.submit_button1.clicked.disconnect()
            self.submit_button1.clicked.connect(lambda: self.update_data_in_table(self.current_edit_row))
        else:
            self.submit_button1.clicked.disconnect()
            self.submit_button1.clicked.connect(self.add_data_to_table)



    def update_data_in_table(self, row):
        mandatory_fields = ["Vendor Name:", "GSTIN:", "Phone No:", "E-Mail:", "State:"]
        for field in mandatory_fields:
            if not self.vendor_entry_fields[field].text():
                QtWidgets.QMessageBox.warning(self, "Error", f"{field} is mandatory.")
                return
        """vendor_data = [
            str(self.vendor_entry_fields[label].toPlainText()) if label == "Address:" else str(
                self.vendor_entry_fields[label].text())
            for label in self.vendor_entry_fields
        ]"""
        vendor_data = [
            str(self.vendor_entry_fields[label].toPlainText()) if label == "Address:" else str(
                self.vendor_entry_fields[label].text())
            for label in self.vendor_entry_fields if label != "Address:"
        ]
        vendor_data.append(self.vendor_entry_fields["Address:"].toPlainText())


        try:
            # Your update query for the Vendor table
            update_vendor_query = "UPDATE Vendor SET VendorName = %s, GSTIN = %s, PhoneNo = %s, Email = %s, State = %s, Address = %s WHERE VendorName = %s"

            # Append the VendorName to the vendor_data for the WHERE clause
            vendor_data.append(self.vendor_table.item(row, 0).text())

            # Update the data in the table using the class cursor attribute
            self.cursor.execute(update_vendor_query, vendor_data)
            self.db_connection.commit()

        except mysql.connector.Error as error:
            print(f"Failed to update MySQL table: {error}")
        finally:
            # Refresh the entire form immediately after updating the data
            self.refresh_form()

            # Set the form back to "Add" mode
            self.edit_mode = False
            #self.toggle_button_state()

            # Clear the input fields after updating data in the table
            for entry in self.vendor_entry_fields.values():
                if isinstance(entry, QLineEdit):
                    entry.clear()  # Clear QLineEdit widgets
                elif isinstance(entry, QTextEdit):
                    entry.setPlainText("")  # Clear QTextEdit widgets

            # Add the vendor data to the table, excluding the last element (ID)
            for col, data in enumerate(vendor_data[:-1]):  # Exclude the last element (ID)
                item = QTableWidgetItem(str(data))
                item.setFlags(item.flags() & ~Qt.ItemIsEditable)  # Make the item non-editable
                self.vendor_table.setItem(row, col, item)

            # Connect the lambda function after performing the update
            self.submit_button1.clicked.connect(lambda: self.update_data_in_table(row))

        # Call toggle_button_state after the update is completed
        self.toggle_button_state()



    def refresh_form(self):
        # Clear the input fields
        for entry in self.vendor_entry_fields.values():
            if isinstance(entry, QLineEdit):
                entry.clear()
            elif isinstance(entry, QTextEdit):
                entry.setPlainText("")

        # Clear the table
        self.vendor_table.clearContents()
        self.vendor_table.setRowCount(0)

        # Fetch and display fresh data
        self.fetch_vendor_data()
        # Disable the "Update" button when there is no data in the table
        if self.vendor_table.rowCount() == 0:
            self.edit_mode = False
            self.submit_button1.setText("Save")
            self.submit_button1.setDisabled(True)
            self.submit_button1.clicked.disconnect()  # Disconnect all connected slots
            self.submit_button1.clicked.connect(self.add_data_to_table)

    def add_data_to_table(self):
        #print("Save button clicked")
        mandatory_fields = ["Vendor Name:", "GSTIN:", "Phone No:", "E-Mail:", "State:","Address:"]
        for field in mandatory_fields:
            entry = self.vendor_entry_fields[field]
            if isinstance(entry, QTextEdit) and not entry.toPlainText():
                QtWidgets.QMessageBox.warning(self, "Error", f"{field} is mandatory.")
                return
            elif isinstance(entry, QLineEdit) and not entry.text():
                QtWidgets.QMessageBox.warning(self, "Error", f"{field} is mandatory.")
                return

        vendor_data = [
            str(entry.toPlainText()) if isinstance(entry, QTextEdit) else str(entry.text())
            for field, entry in self.vendor_entry_fields.items()
        ]

        try:
            #print("Inside try block")
            # Your insert query for the Vendor table
            add_vendor_query = "INSERT INTO Vendor (VendorName, GSTIN, PhoneNo, Email, State, Address) VALUES (%s, %s, %s, %s, %s, %s)"

            # Insert the data into the table using the class cursor attribute
            self.cursor.execute(add_vendor_query, vendor_data)
            self.db_connection.commit()

        except mysql.connector.Error as error:
            print(f"Failed to insert into MySQL table: {error}")
        finally:
            #print("Inside finally block")
            row_position = self.vendor_table.rowCount()
            self.vendor_table.insertRow(row_position)

            # Clear the input fields after adding data to the table
            for entry in self.vendor_entry_fields.values():
                if isinstance(entry, QLineEdit):
                    entry.clear()  # Clear QLineEdit widgets
                # Do not clear QTextEdit widgets
                elif isinstance(entry, QTextEdit):
                    entry.setPlainText("")  # Clear QTextEdit widgets

            # Add the vendor data to the table, excluding the last element (ID)
            for col, data in enumerate(vendor_data[:-1]):  # Exclude the last element (ID)
                item = QTableWidgetItem(str(data))
                item.setFlags(item.flags() & ~Qt.ItemIsEditable)  # Make the item non-editable
                self.vendor_table.setItem(row_position, col, item)

            # Add the "Edit" button to the new row
            edit_button = QPushButton("Edit")
            edit_button.clicked.connect(lambda state, row=row_position: self.edit_row(row))
            self.vendor_table.setCellWidget(row_position, 6, edit_button)
            # Add the "Delete" button to the new row
            delete_button = QPushButton("Delete")
            delete_button.clicked.connect(lambda state, row=row_position: self.delete_row(row))
            self.vendor_table.setCellWidget(row_position, 7, delete_button)

            self.vendor_table.resizeColumnsToContents()
            self.vendor_table.resizeRowsToContents()

            # Toggle the button state after adding data to the table
            self.toggle_button_state()




    def delete_row(self, row):
        try:
            # Get the VendorID from the database for the selected row
            select_query = "SELECT VendorName FROM Vendor LIMIT 1 OFFSET %s"
            self.cursor.execute(select_query, (row,))
            vendor_id = self.cursor.fetchone()[0]

            # Perform the deletion
            delete_query = "DELETE FROM Vendor WHERE VendorName = %s"
            self.cursor.execute(delete_query, (vendor_id,))
            self.db_connection.commit()

        except mysql.connector.Error as error:
            print(f"Failed to delete row from MySQL table: {error}")
        finally:
            self.vendor_table.removeRow(row)

    def fetch_vendor_data(self):
        try:
            # Your select query to fetch data from the Vendor table
            select_query = "SELECT * FROM Vendor"
            self.cursor.execute(select_query)

            # Fetch all the results from the cursor
            records = self.cursor.fetchall()

            column_map = {
                0: "VendorName",
                1: "GSTIN",
                2: "PhoneNo",
                3: "Email",
                4: "State",
                5: "Address",
            }

            # Iterate over the records and populate the QTableWidget
            self.vendor_table.setRowCount(len(records))
            for row, record in enumerate(records):
                for col, data in enumerate(record):
                    column_name = column_map.get(col)
                    if column_name is None:
                        # Hide the ID data by not adding it to the table
                        continue
                    item = QTableWidgetItem(str(data))
                    item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                    self.vendor_table.setItem(row, col, item)

                # Add the "Edit" button to each row
                edit_button = QPushButton("Edit")
                edit_button.clicked.connect(lambda state, row=row: self.edit_row(row))
                self.vendor_table.setCellWidget(row, 6, edit_button)
                # Add the "Delete" button to each row
                delete_button = QPushButton("Delete")
                delete_button.clicked.connect(lambda state, row=row: self.delete_row(row))
                self.vendor_table.setCellWidget(row, 7, delete_button)

        except mysql.connector.Error as error:
            print(f"Failed to fetch data from MySQL table: {error}")


    # Don't forget to close the database connection
    def closeEvent(self, event):
        self.db_connection.close()
        super().closeEvent(event)()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SideNavigationMenu()
    window.show()
    sys.exit(app.exec_())
