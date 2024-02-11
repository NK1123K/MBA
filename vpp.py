from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QFormLayout, QLineEdit, QTextEdit, \
    QPushButton, QTableWidget, QTableWidgetItem, QHeaderView, QScrollArea, QHBoxLayout,QSizePolicy
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIntValidator
from PyQt5 import QtWidgets
import mysql.connector

class Vendor_Page(QWidget):
    def __init__(self):
        super().__init__()
        self.edit_mode = False
        self.db_connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='MySql@12345',
            database='test'
        )
        self.cursor = self.db_connection.cursor()

        # Create a QVBoxLayout for the main layout
        main_layout = QVBoxLayout(self)

        # Add vendor form, search bar, and table to the main layout
        self.Vendor_Details(main_layout)

    def Vendor_Details(self, layout1):
        vendor_form_widget = QWidget()
        table_widget = QScrollArea()

        vendor_form_layout = QVBoxLayout(vendor_form_widget)
        table_layout = QVBoxLayout(table_widget)

        vendor_form_layout.setAlignment(Qt.AlignTop)

        # Create the search bar
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Search...")
        self.search_bar.textChanged.connect(self.filter_vendor_data)

        # Add the search bar to the main layout
        vendor_form_layout.addWidget(self.search_bar)

        # To add space between search bar and Vendor Details
        vendor_form_layout.addWidget(QLabel(""))
        vendor_form_layout.addWidget(QLabel(""))

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

        self.clear_button = QPushButton("Clear")
        self.clear_button.clicked.connect(self.clear_form)
        self.clear_button.setStyleSheet("background-color: LightGray")

        # Connect the button state to a method to enable/disable it based on form data
        self.clear_button.setEnabled(False)
        self.check_form_data()
        for entry_field in self.vendor_entry_fields.values():
            if isinstance(entry_field, QLineEdit) or isinstance(entry_field, QTextEdit):
                entry_field.textChanged.connect(self.check_form_data)

        # Add the Refresh button to the layout
        refresh_button = QPushButton("Refresh")
        refresh_button.clicked.connect(self.refresh_form)
        refresh_button.setStyleSheet("background-color: silver")
        vendor_form_layout.addWidget(refresh_button)

        vendor_form_layout.addLayout(form_layout1)
        vendor_form_layout.addWidget(self.submit_button1)
        vendor_form_layout.addWidget(self.clear_button)  # Add the "Clear" button
        vendor_form_layout.addWidget(refresh_button)

        # table_layout.addWidget(QLabel("Vendor Details"))
        self.vendor_table = QTableWidget()
        self.vendor_table.setColumnCount(8)
        self.vendor_table.setHorizontalHeaderLabels(
            ["Vendor Name", "GSTIN", "Phone No", "E-Mail", "State", "Address", "", ""]
        )
        table_layout.addWidget(self.vendor_table)

        # Set the table to resize horizontally based on the available space
        self.vendor_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        table_widget.setWidgetResizable(True)  # Allow the table to be scrollable if it doesn't fit
        table_widget.setWidget(QWidget())
        table_widget.widget().setLayout(table_layout)

        # Add vendor form and table to the layout1
        layout1.addWidget(vendor_form_widget)
        layout1.addWidget(table_widget)

        # Connect the "Edit" and "Delete" buttons to their respective functions
        self.vendor_table.cellClicked.connect(self.cell_clicked)

        # Fetch and display data
        self.fetch_vendor_data()

    def clear_form(self):
        # Clear all input fields in the form
        for entry_field in self.vendor_entry_fields.values():
            if isinstance(entry_field, QLineEdit):
                entry_field.clear()
            elif isinstance(entry_field, QTextEdit):
                entry_field.clear()
            # self.refresh_form()

    def check_form_data(self):
        # Enable/disable the "Clear" button based on whether there is data in the form
        has_data = any(
            entry_field.text() != '' for entry_field in self.vendor_entry_fields.values() if isinstance(entry_field, QLineEdit))
        has_data |= any(
            entry_field.toPlainText() != '' for entry_field in self.vendor_entry_fields.values() if isinstance(
                entry_field, QTextEdit))
        self.clear_button.setEnabled(has_data)

    def cell_clicked(self, row, col):
        if col == self.vendor_table.columnCount() - 2:  # "Edit" button column
            self.edit_row(row)
        elif col == self.vendor_table.columnCount() - 1:  # "Delete" button column
            self.delete_row(row)

    def edit_row(self, row):
        # Get the data from the selected row
        vendor_data = []
        for col in range(self.vendor_table.columnCount() - 2):  # Exclude the "Edit" and "Delete" columns
            item = self.vendor_table.item(row, col)
            if item is not None:
                vendor_data.append(item.text())
            else:
                vendor_data.append("")  # or any default value you prefer

        # Populate the form fields with the data from the selected row
        for label, entry in self.vendor_entry_fields.items():
            if label == "Address:":
                entry.setPlainText(vendor_data.pop(0))
            else:
                entry.setText(vendor_data.pop(0))

        # Set up the form for editing
        self.edit_mode = True
        self.submit_button1.setText("Update")
        self.submit_button1.clicked.disconnect()
        self.submit_button1.clicked.connect(lambda: self.update_data_in_table(row))

    def toggle_button_state(self):
        if self.edit_mode:
            self.submit_button1.setText("Update")
            self.submit_button1.setEnabled(True)
        else:
            self.submit_button1.setText("Save")
            self.submit_button1.setEnabled(True)

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
            self.submit_button1.setEnabled(True)
            self.submit_button1.clicked.disconnect()  # Disconnect all connected slots
            self.submit_button1.clicked.connect(self.add_data_to_table)

    def add_data_to_table(self):
        print("Save button clicked.")
        mandatory_fields = ["Vendor Name:", "GSTIN:", "Phone No:", "E-Mail:", "State:", "Address:"]
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
            # Your insert query for the Vendor table
            add_vendor_query = "INSERT INTO Vendor (VendorName, GSTIN, PhoneNo, Email, State, Address) VALUES (%s, %s, %s, %s, %s, %s)"

            # Insert the data into the table using the class cursor attribute
            self.cursor.execute(add_vendor_query, vendor_data)
            self.db_connection.commit()

        except mysql.connector.Error as error:
            print(f"Failed to insert into MySQL table: {error}")
            self.duplicate_entry()
        finally:
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
            delete_button.clicked.connect(lambda state, row=row_position: self.reset())
            self.vendor_table.setCellWidget(row_position, 7, delete_button)

            self.vendor_table.resizeColumnsToContents()
            self.vendor_table.resizeRowsToContents()

            # Set fixed sizes for columns
            self.vendor_table.setColumnWidth(0, 80)  # Adjust the index and size accordingly
            self.vendor_table.setColumnWidth(1, 100)
            # Add similar lines for other columns as needed

            # Set a fixed size for rows
            self.vendor_table.setRowHeight(0, 30)  # Adjust the index and size accordingly
            # Add similar lines for other rows as needed
            # Toggle the button state after adding data to the table
            self.toggle_button_state()
            self.refresh_form()  # to clear bug

    # pop up warning for duplicate_entry
    def duplicate_entry(self):
        qm = QtWidgets.QMessageBox()
        ret = qm.question(self, '', "Duplicate_entry?", qm.Ok)
        if ret == qm.Ok:
            self.refresh_form()

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

        # Refresh the form after deletion
        self.refresh_form()

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

                    # Add tooltip for the "Address" column
                    if column_name == "Address":
                        item.setToolTip(f"<html><head/><body><p>{data}</p></body></html>")

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

    def filter_vendor_data(self):
        search_text = self.search_bar.text().lower()
        for row in range(self.vendor_table.rowCount()):
            row_visible = any(
                search_text in str(self.vendor_table.item(row, col).text()).lower()
                if self.vendor_table.item(row, col) is not None
                else ""
                for col in range(self.vendor_table.columnCount())
            )
            self.vendor_table.setRowHidden(row, not row_visible)

    # Don't forget to close the database connection
    def closeEvent(self, event):
        self.db_connection.close()
        super().closeEvent(event)

    def displayContent(self, item):
        selected_item_text = item.text()
        if selected_item_text == "Home":
            # Handle the navigation to the Home page here
            # You can implement the logic to switch to the Home page or do any other necessary actions
            print("Navigate to Home page")

# Application execution
if __name__ == '__main__':
    app = QApplication([])
    ex = Vendor_Page()
    ex.show()
    app.exec_()
