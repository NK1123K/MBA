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

        self.edit_button = QPushButton("Edit")
        self.edit_button.setEnabled(False)  # Initially disable the "Edit" button

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
        self.submit_button1.clicked.connect(self.add_data_to_vendor_table)
        self.submit_button1.setStyleSheet("background-color: Cyan")

        self.clear_button = QPushButton("Clear")
        self.clear_button.clicked.connect(self.clear_vendor_form)
        self.clear_button.setStyleSheet("background-color: LightGray")

        # Connect the button state to a method to enable/disable it based on form data
        self.clear_button.setEnabled(False)
        self.check_vendor_form_data()
        for entry_field in self.vendor_entry_fields.values():
            if isinstance(entry_field, QLineEdit) or isinstance(entry_field, QTextEdit):
                entry_field.textChanged.connect(self.check_vendor_form_data)

        # Add the Refresh button to the layout
        refresh_button = QPushButton("Refresh")
        refresh_button.clicked.connect(self.refresh_form)
        refresh_button.setStyleSheet("background-color: silver")
        vendor_form_layout.addWidget(refresh_button)

        # Add the buttons for edit and delete
        edit_delete_layout = QHBoxLayout()
        edit_button = QPushButton("Edit")
        edit_button.clicked.connect(lambda: self.edit_vendor_row())
        edit_delete_layout.addWidget(edit_button)

        delete_button = QPushButton("Delete")
        delete_button.clicked.connect(lambda: self.delete_selected_rows())
        edit_delete_layout.addWidget(delete_button)

        vendor_form_layout.addLayout(form_layout1)
        vendor_form_layout.addWidget(self.submit_button1)
        vendor_form_layout.addWidget(self.clear_button)  # Add the "Clear" button
        vendor_form_layout.addWidget(refresh_button)
        vendor_form_layout.addLayout(edit_delete_layout)  # Add edit and delete buttons

        # table_layout.addWidget(QLabel("Vendor Details"))
        self.vendor_table = QTableWidget()
        self.vendor_table.setColumnCount(7)
        self.vendor_table.setHorizontalHeaderLabels(
            ["","Vendor Name", "GSTIN", "Phone No", "E-Mail", "State", "Address"]
        )
        # Set the width of the first column (checkbox column)
        self.vendor_table.setColumnWidth(0, 20)  # Adjust the width as needed
        table_layout.addWidget(self.vendor_table)

        for i in range(1, self.vendor_table.columnCount()):
            self.vendor_table.horizontalHeader().setSectionResizeMode(i, QHeaderView.Stretch)

        table_widget.setWidgetResizable(True)  # Allow the table to be scrollable if it doesn't fit
        table_widget.setWidget(QWidget())
        table_widget.widget().setLayout(table_layout)

        # Add vendor form and table to the layout1
        layout1.addWidget(vendor_form_widget)
        layout1.addWidget(table_widget)

        # Fetch and display data
        self.fetch_vendor_data()

        for row in range(self.vendor_table.rowCount()):
            checkbox = self.vendor_table.cellWidget(row, 0)
            checkbox.stateChanged.connect(self.update_edit_button_state)

    def update_edit_button_state(self):
        # Get the count of selected rows based on the checkboxes
        selected_rows = sum(1 for row in range(self.vendor_table.rowCount()) if self.vendor_table.cellWidget(row, 0).isChecked())
        # Enable the "Edit" button only when exactly one checkbox is selected
        self.edit_button.setEnabled(selected_rows == 1)

    def clear_vendor_form(self):
        # Clear all input fields in the form
        for entry_field in self.vendor_entry_fields.values():
            if isinstance(entry_field, QLineEdit):
                entry_field.clear()
            elif isinstance(entry_field, QTextEdit):
                entry_field.clear()

    def check_vendor_form_data(self):
        # Enable/disable the "Clear" button based on whether there is data in the form
        has_data = any(
            entry_field.text() != '' for entry_field in self.vendor_entry_fields.values() if isinstance(entry_field, QLineEdit))
        has_data |= any(
            entry_field.toPlainText() != '' for entry_field in self.vendor_entry_fields.values() if isinstance(
                entry_field, QTextEdit))
        self.clear_button.setEnabled(has_data)

    def edit_vendor_row(self):
        # Get the selected row indices based on the checkboxes
        selected_rows = []
        for row in range(self.vendor_table.rowCount()):
            checkbox = self.vendor_table.cellWidget(row, 0)
            if checkbox.isChecked():
                selected_rows.append(row)

        if len(selected_rows) > 1:
            self.edit_button.setEnabled(False)
            QtWidgets.QMessageBox.warning(self, "Error", "Please select exactly one row to edit.")
        elif len(selected_rows) < 1:
            QtWidgets.QMessageBox.warning(self, "Error", "Please select a row to edit.")
            return
        else:
            # For simplicity, let's assume editing only the first selected row
            selected_row = selected_rows[0]

            # Get the item ID from the selected row
            vendor_id = self.vendor_table.item(selected_row, 1).text()

            # Populate the form fields with the data from the selected row
            for label, entry in self.vendor_entry_fields.items():
                if label == "Address:":
                    entry.setText(self.vendor_table.item(selected_row, 6).text())  # Set Item Name instead of ID
                else:
                    # Find the column index based on the label
                    col_index = list(self.vendor_entry_fields.keys()).index(label)
                    entry.setText(self.vendor_table.item(selected_row, col_index + 1).text())

                # Enable the edit button only when one checkbox is selected
                self.edit_button.setEnabled(True)

                # Set up the form for editing
                self.edit_mode = True
                self.submit_button1.setText("Update")
                self.submit_button1.clicked.disconnect()
                self.submit_button1.clicked.connect(lambda: self.update_data_in_table(selected_row, vendor_id))

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
            self.submit_button1.clicked.connect(self.add_data_to_vendor_table)

    def update_data_in_table(self, row, vendor_id):
        mandatory_fields = ["Vendor Name:", "GSTIN:", "Phone No:", "E-Mail:", "State:"]
        for field in mandatory_fields:
            if not self.vendor_entry_fields[field].text():
                QtWidgets.QMessageBox.warning(self, "Error", f"{field} is mandatory.")
                return

        vendor_data = []
        for label, entry in self.vendor_entry_fields.items():
            if label == "Address:":
                vendor_data.append(entry.toPlainText())
            else:
                vendor_data.append(entry.text())

        try:
            # Your update query for the Vendor table
            update_vendor_query = "UPDATE Vendor SET VendorName = %s, GSTIN = %s, PhoneNo = %s, Email = %s, State = %s, Address = %s WHERE VendorName = %s"

            # Append the VendorName to the vendor_data for the WHERE clause
            vendor_data.append(vendor_id)

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

            # Add the vendor data to the table, excluding the last element (VendorName for WHERE clause)
            for col, data in enumerate(vendor_data[:-1]):
                vendor = QTableWidgetItem(str(data))
                vendor.setFlags(vendor.flags() & ~Qt.ItemIsEditable)  # Make the vendor non-editable
                self.vendor_table.setItem(row, col + 1, vendor)

        # Call toggle_button_state after the update is completed
        self.toggle_button_state()

    def populate_table_with_vendor_data(self):
        # Fetch and display fresh data
        self.fetch_vendor_data()

        # Disable the "Update" button when there is no data in the table
        if self.vendor_table.rowCount() == 0:
            self.edit_mode = False
            self.submit_button1.setText("Save")
            self.submit_button1.setEnabled(True)
            self.submit_button1.clicked.disconnect()  # Disconnect all connected slots
            self.submit_button1.clicked.connect(self.add_data_to_vendor_table)

            # Connect the stateChanged signal of each checkbox to update_edit_button_state
            for row in range(self.vendor_table.rowCount()):
                checkbox = self.vendor_table.cellWidget(row, 0)
                checkbox.stateChanged.connect(self.update_edit_button_state)

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
        #if self.vendor_table.rowCount() == 0:
        self.edit_mode = False
        self.submit_button1.setText("Save")
        self.submit_button1.setEnabled(True)
        self.submit_button1.clicked.disconnect()  # Disconnect all connected slots
        self.submit_button1.clicked.connect(self.add_data_to_vendor_table)

    def add_data_to_vendor_table(self):
        mandatory_fields = ["Vendor Name:", "GSTIN:", "Phone No:", "E-Mail:", "State:", "Address:"]
        for field in mandatory_fields:
            entry = self.vendor_entry_fields[field]
            if isinstance(entry, QTextEdit) and not entry.toPlainText():
                QtWidgets.QMessageBox.warning(self, "Error", f"{field} is mandatory.")
                return
            elif isinstance(entry, QLineEdit) and not entry.text():
                QtWidgets.QMessageBox.warning(self, "Error", f"{field} is mandatory.")
                return
                
        vendor_data = []
        for label, entry in self.vendor_entry_fields.items():
            data = entry.toPlainText() if isinstance(entry, QTextEdit) else entry.text()
            vendor_data.append(data)

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

            # Add checkbox to each row
            check_box = QCheckBox()
            check_box.setStyleSheet(" QCheckBox { padding-left: 15px; }")
            self.vendor_table.setCellWidget(row_position, 0, check_box)

            # Connect checkbox stateChanged signal to a lambda function to capture the row index
            check_box.stateChanged.connect(lambda state, row=row_position: self.update_edit_button_state(row))

            # Clear the input fields after adding data to the table
            for entry in self.vendor_entry_fields.values():
                if isinstance(entry, QLineEdit):
                    entry.clear()  # Clear QLineEdit widgets
                # Do not clear QTextEdit widgets
                elif isinstance(entry, QTextEdit):
                    entry.setPlainText("")  # Clear QTextEdit widgets

            # Add the vendor data to the table, excluding the last element (ID)
            for col, data in enumerate(vendor_data): 
                vendor = QTableWidgetItem(str(data))
                vendor.setFlags(vendor.flags() & ~Qt.ItemIsEditable)  # Make the vendor non-editable
                self.vendor_table.setItem(row_position, col+1, vendor)

            self.vendor_table.resizeColumnsToContents()
            self.vendor_table.resizeRowsToContents()
            self.vendor_table.horizontalHeader().setDefaultSectionSize(50)  # Adjust the width as needed
            self.vendor_table.setColumnWidth(1, 100)

            # Set a fixed size for rows
            self.vendor_table.setRowHeight(0, 30)  # Adjust the index and size accordingly

            # Toggle the button state after adding data to the table
            self.toggle_button_state()
            self.refresh_form()  # to clear bug 

    # pop up warning for duplicate_entry
    def duplicate_entry(self):
        qm = QtWidgets.QMessageBox()
        ret = qm.question(self, '', "Duplicate_entry?", qm.Ok)
        if ret == qm.Ok:
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
                    vendor = QTableWidgetItem(str(data))
                    vendor.setFlags(vendor.flags() & ~Qt.ItemIsEditable)
                    self.vendor_table.setItem(row, col+1, vendor)

                    # Add tooltip for the "Address" column
                    if column_name == "Address":
                        vendor.setToolTip(f"<html><head/><body><p>{data}</p></body></html>")

                # Add checkbox to each row
                check_box = QCheckBox()
                check_box.setStyleSheet("QCheckBox { padding-left: 15px; }")
                self.vendor_table.setCellWidget(row, 0, check_box)

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

    def displayContent(self, vendor):
        selected_vendor_text = vendor.text()
        if selected_vendor_text == "Home":
            # Handle the navigation to the Home page here
            # You can implement the logic to switch to the Home page or do any other necessary actions
            print("Navigate to Home page")

    def delete_selected_rows(self):
        # List to store the row indices of selected rows
        rows_to_delete = []

        # Iterate over the rows in reverse order to avoid index issues when deleting
        for row in range(self.vendor_table.rowCount()):
            # Check if the checkbox in the first column is checked
            check_box = self.vendor_table.cellWidget(row, 0)
            if isinstance(check_box, QCheckBox) and check_box.isChecked():
                # Append the row index to the list of rows to delete
                rows_to_delete.append(row)

        if len(rows_to_delete) > 1:
            # Confirmation dialog
            confirmation = QMessageBox.question(self, 'Confirmation', 'Are you sure you want to delete the selected rows?',
                                            QMessageBox.Yes | QMessageBox.No)
        elif len(rows_to_delete) == 1:
            confirmation = QMessageBox.question(self, 'Confirmation', 'Are you sure you want to delete the selected row?',
                                            QMessageBox.Yes | QMessageBox.No)
        else:
            confirmation = QtWidgets.QMessageBox.warning(self, "Error", "Please select a row to delete.")
        
        if confirmation == QMessageBox.Yes:
            # Iterate over the list of rows to delete in reverse order to avoid index issues
            for row in reversed(rows_to_delete):
                # Get the vendor name from the selected row
                vendor_name = self.vendor_table.item(row, 1).text()  # Assuming VendorName is in the second column

                try:
                    # Your delete query for the Vendor table
                    delete_vendor_query = "DELETE FROM Vendor WHERE VendorName = %s"

                    # Delete the data from the table using the class cursor attribute
                    self.cursor.execute(delete_vendor_query, (vendor_name,))
                    self.db_connection.commit()

                except mysql.connector.Error as error:
                    print(f"Failed to delete from MySQL table: {error}")

                finally:
                    # Remove the row from the table widget
                    self.vendor_table.removeRow(row)
        self.refresh_form()

# Application execution
if __name__ == '__main__':
    app = QApplication([])
    ex = Vendor_Page()
    ex.show()
    app.exec_()
