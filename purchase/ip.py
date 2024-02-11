from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5 import QtWidgets
from PyQt5.QtGui import QIntValidator

import mysql.connector

class Item_Page(QWidget):
    def __init__(self):
        super().__init__()
        self.edit_mode = False 
        self.db_connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='root',
            database='test'
        )
        self.cursor = self.db_connection.cursor()

        # Add search bar
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Search Item...")
        self.search_bar.textChanged.connect(self.filter_item_data)

    def Item_Details(self, layout1):
        item_form_widget = QWidget()
        table_widget = QWidget()
        table_widget = QScrollArea()

        item_form_layout = QVBoxLayout(item_form_widget)
        table_layout = QVBoxLayout(table_widget)

        item_form_layout.setAlignment(Qt.AlignTop)

        item_form_layout.addWidget(QLabel("Item Details"))

        item_form_widget.setMinimumSize(300, 0)
        item_form_widget.setMaximumSize(300, 800)
        table_widget.setMinimumSize(300, 0)

        form_layout1 = QFormLayout()

        labels1 = [
            "Item Name:"
        ]

        self.item_entry_fields = {}

        for label_text in labels1:
            label1 = QLabel(label_text)

            # Integer validator for ID
            if label_text == "ID:":
                entry1 = QLineEdit()
                entry1.setReadOnly(True)  # ID should be auto-filled and read-only
            else:
                entry1 = QLineEdit()

            # Set placeholders for specific fields
            if label_text == "Item Name:":
                entry1.setPlaceholderText("Enter Item Name")

            form_layout1.addRow(label1, entry1)
            self.item_entry_fields[label_text] = entry1


        self.submit_button1 = QPushButton("Save")
        self.submit_button1.clicked.connect(self.add_data_to_item_table)
        self.submit_button1.setStyleSheet("background-color: Cyan")

        self.clear_button = QPushButton("Clear")
        self.clear_button.clicked.connect(self.clear_item_form)
        self.clear_button.setStyleSheet("background-color: LightGray")

        # Connect the button state to a method to enable/disable it based on form data
        self.clear_button.setEnabled(False)
        self.check_item_form_data()
        for entry_field in self.item_entry_fields.values():
            if isinstance(entry_field, QLineEdit):
                entry_field.textChanged.connect(self.check_item_form_data)

        # Add the Refresh button to the layout
        refresh_button = QPushButton("Refresh")
        refresh_button.clicked.connect(self.refresh_item_form)
        refresh_button.setStyleSheet("background-color: silver")
        item_form_layout.addWidget(refresh_button)

        item_form_layout.addLayout(form_layout1)
        item_form_layout.addWidget(self.submit_button1)
        item_form_layout.addWidget(self.clear_button)  # Add the "Clear" button
        item_form_layout.addWidget(refresh_button)

        # table_layout.addWidget(QLabel("Item Details"))
        self.item_table = QTableWidget()
        self.item_table.setColumnCount(4)  # Adjust the number of columns as needed
        self.item_table.setHorizontalHeaderLabels(["ID", "Item Name", "", ""])
        
        # Fetch and display data before adding the table to the layout
        self.fetch_item_data()

        # Set the table to resize horizontally based on the available space
        self.item_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        table_widget.setWidget(self.item_table)
        table_widget.setWidgetResizable(True)  # Allow the table to be scrollable if it doesn't fit

        layout1.addWidget(item_form_widget)
        layout1.addWidget(table_widget)  # Add the table to the layout

        # Add the search bar to the layout
        item_form_layout.addWidget(self.search_bar)

        # Connect the "Edit" and "Delete" buttons to their respective functions
        self.item_table.cellClicked.connect(self.cell_clicked_item)

    def clear_item_form(self):
        # Clear all input fields in the form
        for entry_field in self.item_entry_fields.values():
            if isinstance(entry_field, QLineEdit):
                entry_field.clear()

    def check_item_form_data(self):
        # Enable/disable the "Clear" button based on whether there is data in the form
        has_data = any(entry_field.text() != '' for entry_field in self.item_entry_fields.values() if isinstance(entry_field, QLineEdit))
        self.clear_button.setEnabled(has_data)

    def cell_clicked_item(self, row, col):
        if col == self.item_table.columnCount() - 2:  # "Edit" button column
            self.edit_row_item(row)
        elif col == self.item_table.columnCount() - 1:  # "Delete" button column
            self.delete_row_item(row)

    def edit_row_item(self, row):
        # Get the data from the selected row
        item_data = []
        for col in range(self.item_table.columnCount() - 1):  # Exclude the "Edit" column
            item = self.item_table.item(row, col)
            if item is not None:
                item_data.append(item.text())
            else:
                item_data.append("")  # or any default value you prefer

        # Populate the form fields with the data from the selected row
        for label, entry in self.item_entry_fields.items():
            if label == "Item Name:":
                entry.setText(item_data[1])  # Set Item Name instead of ID
            else:
                entry.setText(item_data.pop(0))

        # Set up the form for editing
        self.edit_mode = True
        self.submit_button1.setText("Update")
        self.submit_button1.clicked.disconnect()
        self.submit_button1.clicked.connect(lambda: self.update_data_in_item_table(row))


    def update_data_in_item_table(self, row):
        mandatory_fields = ["Item Name:"]
        for field in mandatory_fields:
            if not self.item_entry_fields[field].text():
                QtWidgets.QMessageBox.warning(self, "Error", f"{field} is mandatory.")
                return

        # Get the item ID from the selected row
        item_id_item = self.item_table.item(row, 0)
        if item_id_item is not None:
            item_id = item_id_item.text()
        else:
            QtWidgets.QMessageBox.warning(self, "Error", "Selected row does not have a valid Item ID.")
            return

        item_name = str(self.item_entry_fields["Item Name:"].text())

        try:
            # Your update query for the Item table
            update_item_query = "UPDATE Item SET ItemName = %s WHERE ItemID = %s"

            # Update the data in the table using the class cursor attribute
            self.cursor.execute(update_item_query, (item_name, int(item_id)))
            self.db_connection.commit()

        except mysql.connector.Error as error:
            print(f"Failed to update MySQL table: {error}")
        finally:
            # Refresh the entire form immediately after updating the data
            self.refresh_item_form()

            # Set the form back to "Add" mode
            self.edit_mode = False

            # Clear the input fields after updating data in the table
            for entry in self.item_entry_fields.values():
                if isinstance(entry, QLineEdit):
                    entry.clear()  # Clear QLineEdit widgets

            # Add the item data to the table
            self.populate_table_with_item_data()

        # Call toggle_button_state after the update is completed
        self.toggle_item_button_state()

    def populate_table_with_item_data(self):
        # Fetch and display fresh data
        self.fetch_item_data()

        # Disable the "Update" button when there is no data in the table
        if self.item_table.rowCount() == 0:
            self.edit_mode = False
            self.submit_button1.setText("Save")
            self.submit_button1.setEnabled(True)
            self.submit_button1.clicked.disconnect()  # Disconnect all connected slots
            self.submit_button1.clicked.connect(self.add_data_to_item_table)


    def refresh_item_form(self):
        # Clear the input fields
        for entry in self.item_entry_fields.values():
            if isinstance(entry, QLineEdit):
                entry.clear()

        # Clear the table
        self.item_table.clearContents()
        self.item_table.setRowCount(0)

        # Fetch and display fresh data
        self.fetch_item_data()
        # Disable the "Update" button when there is no data in the table
        if self.item_table.rowCount() == 0:
            self.edit_mode = False
            self.submit_button1.setText("Save")
            self.submit_button1.setEnabled(True)
            self.submit_button1.clicked.disconnect()  # Disconnect all connected slots
            self.submit_button1.clicked.connect(self.add_data_to_item_table)

    def add_data_to_item_table(self):
        mandatory_fields = ["Item Name:"]
        for field in mandatory_fields:
            entry = self.item_entry_fields[field]
            if not entry.text():
                QtWidgets.QMessageBox.warning(self, "Error", f"{field} is mandatory.")
                return

        item_name = str(self.item_entry_fields["Item Name:"].text())

        try:
            # Your insert query for the Item table
            add_item_query = "INSERT INTO Item (ItemName) VALUES (%s)"

            # Insert the data into the table using the class cursor attribute
            self.cursor.execute(add_item_query, (item_name,))
            self.db_connection.commit()

            # Fetch the auto-generated ID for the inserted row
            self.cursor.execute("SELECT LAST_INSERT_ID()")
            item_id = self.cursor.fetchone()[0]

        except mysql.connector.Error as error:
            print(f"Failed to insert into MySQL table: {error}")
        finally:
            row_position = self.item_table.rowCount()
            self.item_table.insertRow(row_position)

            # Add the item data to the table
            item = QTableWidgetItem(str(item_id))  # Auto-generated ID
            item.setFlags(item.flags() & ~Qt.ItemIsEditable)  # Make the item non-editable
            self.item_table.setItem(row_position, 0, item)  # Assuming ID is in the first column

            item = QTableWidgetItem(item_name)
            item.setFlags(item.flags() & ~Qt.ItemIsEditable)  # Make the item non-editable
            self.item_table.setItem(row_position, 1, item)  # Assuming Item Name is in the second column

            # Add the "Edit" button to the new row
            edit_button = QPushButton("Edit")
            edit_button.clicked.connect(lambda state, row=row_position: self.edit_row_item(row))
            self.item_table.setCellWidget(row_position, 2, edit_button)

            # Add the "Delete" button to each row
            delete_button = QPushButton("Delete")
            delete_button.clicked.connect(lambda state, row=row_position: self.delete_row_item(row))
            self.item_table.setCellWidget(row_position, 3, delete_button)

            # Set a fixed size for the "Delete" button column
            #self.item_table.setColumnWidth(3, 80)  
            # Assuming the "Delete" button is in the third column, adjust the size accordingly

            # Set fixed size for all columns
            for col in range(self.item_table.columnCount()):
                self.item_table.horizontalHeader().setSectionResizeMode(col, QHeaderView.Fixed)

            self.clear_item_form()

            # Toggle the button state after adding data to the table
            self.toggle_item_button_state()

    def delete_row_item(self, row):
        item_id = self.item_table.item(row, 0).text()  # Assuming ItemID is in the second column
        reply = QMessageBox.question(self, 'Delete Confirmation', f'Do you want to delete Item with ID {item_id}?',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            try:
                # Your delete query for the Item table
                delete_item_query = "DELETE FROM Item WHERE ItemID = %s"

                # Delete the data from the table using the class cursor attribute
                self.cursor.execute(delete_item_query, (item_id,))
                self.db_connection.commit()

            except mysql.connector.Error as error:
                print(f"Failed to delete from MySQL table: {error}")
            finally:
                # Refresh the entire form immediately after deleting the data
                self.refresh_item_form()

    def toggle_item_button_state(self):
        if self.edit_mode:
            self.submit_button1.setText("Update")
            self.submit_button1.setEnabled(True)
        else:
            self.submit_button1.setText("Save")
            self.submit_button1.setEnabled(True)

        # Connect the appropriate function based on the edit mode
        if self.edit_mode:
            self.submit_button1.clicked.disconnect()
            self.submit_button1.clicked.connect(lambda: self.update_data_in_item_table(self.current_edit_row))
        else:
            self.submit_button1.clicked.disconnect()
            self.submit_button1.clicked.connect(self.add_data_to_item_table)

    # Modify the fetch_item_data function to properly populate the Item Name
    def fetch_item_data(self):
        try:
            # Your select query to fetch data from the Item table
            select_query = "SELECT ItemID, ItemName FROM Item"

            self.cursor.execute(select_query)

            # Fetch all the results from the cursor
            records = self.cursor.fetchall()

            # Clear the existing table before populating it with new data
            self.item_table.setRowCount(0)

            # Set the horizontal header labels for clarity
            self.item_table.setHorizontalHeaderLabels(["Item ID", "Item Name", "", ""])

            # Iterate over the records and populate the QTableWidget
            for row, record in enumerate(records):
                self.item_table.insertRow(row)

                for col, data in enumerate(record):
                    item = QTableWidgetItem(str(data))
                    item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                    self.item_table.setItem(row, col, item)

                # Add the "Edit" button to each row
                edit_button = QPushButton("Edit")
                edit_button.clicked.connect(lambda state, row=row: self.edit_row_item(row))
                self.item_table.setCellWidget(row, 2, edit_button)

                # Add the "Delete" button to each row
                delete_button = QPushButton("Delete")
                delete_button.clicked.connect(lambda state, row=row: self.delete_row_item(row))
                self.item_table.setCellWidget(row, 3, delete_button)

                # Set a fixed size for the "Delete" button column
                #self.item_table.setColumnWidth(3, 80)  
                # Assuming the "Delete" button is in the third column, adjust the index and size accordingly

        except mysql.connector.Error as error:
            print(f"Failed to fetch data from MySQL table: {error}")


    def filter_item_data(self):
        search_text = self.search_bar.text().lower()
        for row in range(self.item_table.rowCount()):
            row_visible = any(
                search_text in str(self.item_table.item(row, col).text()).lower()
                if self.item_table.item(row, col) is not None
                else ""
                for col in range(self.item_table.columnCount())
            )
            self.item_table.setRowHidden(row, not row_visible)

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
    ex = Item_Page()
    ex.show()
    app.exec_()
