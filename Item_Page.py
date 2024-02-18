from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5 import QtWidgets
from PyQt5.QtGui import *
from PyQt5.QtCore import *

import mysql.connector

class Item_Page(QWidget):
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
        self.Item_Details(main_layout)

        self.edit_button = QPushButton("Edit")
        self.edit_button.setEnabled(False)  # Initially disable the "Edit" button

        # Install event filter on the application instance
        QApplication.instance().installEventFilter(self)

    def eventFilter(self, obj, event):
        if event.type() == QEvent.KeyPress:
            if isinstance(obj, Item_Page):  # Check if the active widget is an instance of Item_Page
        #if obj == self and event.type() == QEvent.KeyPress:
            #if isinstance(Item_Page):

                # Check if Ctrl+S is pressed
                if event.modifiers() == Qt.ControlModifier and event.key() == Qt.Key_S:
                    self.add_data_to_item_table()
                elif event.modifiers() == Qt.ControlModifier and event.key() == Qt.Key_C:
                    self.clear_item_form()
                elif event.modifiers() == Qt.ControlModifier and event.key() == Qt.Key_R:
                    self.refresh_item_form()
                elif event.modifiers() == Qt.ControlModifier and event.key() == Qt.Key_E:
                    self.edit_item_row()
                elif event.modifiers() == Qt.ControlModifier and event.key() == Qt.Key_D:
                    self.delete_selected_rows()
                elif event.modifiers() == Qt.ControlModifier and event.key() == Qt.Key_U:
                    self.update_data_in_item_table()
                
                    return True
        # Continue processing other events
        return super().eventFilter(obj, event)

        # # Create a shortcut for Ctrl+S
        # shortcut = QShortcut(QKeySequence(Qt.ControlModifier + Qt.Key_S), self)
        # shortcut.activated.connect(self.add_data_to_item_table)


    def Item_Details(self, layout1):
        item_form_widget = QWidget()
        table_widget = QWidget()
        table_widget = QScrollArea()

        item_form_layout = QVBoxLayout(item_form_widget)
        item_form_layout.setAlignment(Qt.AlignTop)

        # Add search bar
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Search Item...")
        self.search_bar.textChanged.connect(self.filter_item_data)

        # Add the search bar to the main layout
        item_form_layout.addWidget(self.search_bar)
        # To add space between search bar and Vendor Details
        item_form_layout.addWidget(QLabel(""))
        item_form_layout.addWidget(QLabel(""))
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
                entry_field.clear()

        # Add the Refresh button to the layout
        refresh_button = QPushButton("Refresh")
        refresh_button.clicked.connect(self.refresh_item_form)
        refresh_button.setStyleSheet("background-color: silver")

        # Add the buttons for edit and delete
        edit_delete_layout = QHBoxLayout()
        edit_button = QPushButton("Edit")
        edit_delete_layout.addWidget(edit_button)
        edit_button.clicked.connect(lambda: self.edit_item_row())

        delete_button = QPushButton("Delete")
        delete_button.clicked.connect(lambda: self.delete_selected_rows())
        edit_delete_layout.addWidget(delete_button)

        item_form_layout.addLayout(form_layout1)
        item_form_layout.addWidget(self.submit_button1)
        item_form_layout.addWidget(self.clear_button)  # Add the "Clear" button
        item_form_layout.addWidget(refresh_button)
        item_form_layout.addLayout(edit_delete_layout)  # Add edit and delete buttons

        # table_layout.addWidget(QLabel("Item Details"))
        self.item_table = QTableWidget()
        self.item_table.setColumnCount(3)  # Adjust the number of columns as needed
        self.item_table.setHorizontalHeaderLabels(["", "ID", "Item Name"])

        # Clear the table
        self.item_table.clearContents()
        self.item_table.setRowCount(0)
        
        # Fetch and display data before adding the table to the layout
        self.fetch_item_data()

        # Set the table to resize horizontally based on the available space
        for i in range(1, self.item_table.columnCount()):
            self.item_table.horizontalHeader().setSectionResizeMode(i, QHeaderView.Stretch)

        table_widget.setWidget(self.item_table)
        table_widget.setWidgetResizable(True)  # Allow the table to be scrollable if it doesn't fit

        layout1.addWidget(item_form_widget)
        self.connect_form_fields()
        layout1.addWidget(table_widget)  # Add the table to the layout

        for row in range(self.item_table.rowCount()):
            checkbox = self.item_table.cellWidget(row, 0)
            checkbox.stateChanged.connect(self.update_edit_button_state)
            
    # To set clear button state based on data presence
    def connect_form_fields(self):
        for entry_field in self.item_entry_fields.values():
            if isinstance(entry_field, QLineEdit):
                entry_field.textChanged.connect(self.check_item_form_data)

    def update_edit_button_state(self):
        # Get the count of selected rows based on the checkboxes
        selected_rows = sum(1 for row in range(self.item_table.rowCount()) if self.item_table.cellWidget(row, 0).isChecked())
        # Enable the "Edit" button only when exactly one checkbox is selected
        self.edit_button.setEnabled(selected_rows == 1)

    def clear_item_form(self):
        # Clear all input fields in the form
        for entry_field in self.item_entry_fields.values():
            if isinstance(entry_field, QLineEdit):
                entry_field.clear()

    def check_item_form_data(self):
        # Enable/disable the "Clear" button based on whether there is data in the form
        has_data = any(entry_field.text() != '' for entry_field in self.item_entry_fields.values() if isinstance(entry_field, QLineEdit))
        self.clear_button.setEnabled(has_data)

    def edit_item_row(self):
        # Get the selected row indices based on the checkboxes
        selected_rows = []
        for row in range(self.item_table.rowCount()):
            checkbox = self.item_table.cellWidget(row, 0)
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
            item_id = self.item_table.item(selected_row, 1).text()  # Assuming Item ID is in the second column

            # Populate the form fields with the data from the selected row
            for label, entry in self.item_entry_fields.items():
                if label == "Item Name:":
                    entry.setText(self.item_table.item(selected_row, 2).text())  # Set Item Name instead of ID

            # Set up the form for editing
            self.edit_mode = True
            self.submit_button1.setText("Update")
            self.submit_button1.clicked.disconnect()
            self.submit_button1.clicked.connect(lambda: self.update_data_in_item_table(selected_row, item_id))

            # Enable the edit button only when one checkbox is selected
            self.edit_button.setEnabled(True)

    def update_data_in_item_table(self, row, item_id):
        mandatory_fields = ["Item Name:"]
        for field in mandatory_fields:
            if not self.item_entry_fields[field].text():
                QtWidgets.QMessageBox.warning(self, "Error", f"{field} is mandatory.")
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
        self.toggle_item_button_state()
        # Disable the "Update" button when there is no data in the table
        #if self.item_table.rowCount() == 0:
        self.edit_mode = False
        self.submit_button1.setText("Save")
        self.submit_button1.setEnabled(True)
        self.submit_button1.clicked.disconnect()  # Disconnect all connected slots
        self.submit_button1.clicked.connect(self.add_data_to_item_table)

    @pyqtSlot()
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

            # Add checkbox to each row
            check_box = QCheckBox()
            check_box.setStyleSheet("QCheckBox { padding-left: 15px; }")
            self.item_table.setCellWidget(row_position, 0, check_box)

            # Add the item data to the table
            item = QTableWidgetItem(str(item_id))  # Auto-generated ID
            item.setFlags(item.flags() & ~Qt.ItemIsEditable)  # Make the item non-editable
            self.item_table.setItem(row_position, 1, item)  # Assuming ID is in the first column

            item = QTableWidgetItem(item_name)
            item.setFlags(item.flags() & ~Qt.ItemIsEditable)  # Make the item non-editable
            self.item_table.setItem(row_position, 2, item)  # Assuming Item Name is in the second column
            self.item_table.horizontalHeader().setDefaultSectionSize(30)  # Adjust the width as needed
            self.item_table.setColumnWidth(1, 100)

            self.clear_item_form()

            # Toggle the button state after adding data to the table
            self.toggle_item_button_state()

    # pop up warning for duplicate_entry
    def duplicate_entry(self):
        qm = QtWidgets.QMessageBox()
        ret = qm.question(self, '', "Duplicate_entry?", qm.Ok)
        if ret == qm.Ok:
            self.refresh_form()

    def delete_item_row(self, row):
        item_id = self.item_table.item(row, 1).text()  # Assuming ItemID is in the second column
        reply = QMessageBox.question(self, 'Delete Confirmation', f'Do you want to delete Item with ID {item_id}?',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            # Iterate over the rows in reverse order to avoid index issues when deleting
            for row in range(self.item_table.rowCount() - 1, -1, -1):
                # Check if the checkbox in the first column is checked
                check_box = self.item_table.cellWidget(row, 0)
                if isinstance(check_box, QCheckBox) and check_box.isChecked():
                    # Get the item ID from the selected row
                    item_id = self.item_table.item(row, 1).text()  # Assuming ItemID is in the second column

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
            self.item_table.setHorizontalHeaderLabels(["","Item ID", "Item Name", "", ""])

            # Iterate over the records and populate the QTableWidget
            for row, record in enumerate(records):
                self.item_table.insertRow(row)

                # Add checkbox to each row
                check_box = QCheckBox()
                check_box.setStyleSheet("QCheckBox { padding-left: 15px; }")
                self.item_table.setCellWidget(row, 0, check_box)

                self.item_table.horizontalHeader().setDefaultSectionSize(30)  # Adjust the width as needed
                self.item_table.setColumnWidth(1, 100)

                for col, data in enumerate(record):
                    item = QTableWidgetItem(str(data))
                    item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                    self.item_table.setItem(row, col + 1, item)


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

    def delete_selected_rows(self):
        # List to store the row indices of selected rows
        rows_to_delete = []

        # Iterate over the rows in reverse order to avoid index issues when deleting
        for row in range(self.item_table.rowCount()):
            # Check if the checkbox in the first column is checked
            check_box = self.item_table.cellWidget(row, 0)
            if isinstance(check_box, QCheckBox) and check_box.isChecked():
                # Append the row index to the list of rows to delete
                rows_to_delete.append(row)

        if len(rows_to_delete) > 1:
            # Confirmation dialog
            confirmation = QMessageBox.question(self, 'Confirmation', 'Are you sure you want to delete the selected rows?',
                                            QMessageBox.Yes | QMessageBox.No)
        else:
            confirmation = QMessageBox.question(self, 'Confirmation', 'Are you sure you want to delete the selected row?',
                                            QMessageBox.Yes | QMessageBox.No)
        
        if confirmation == QMessageBox.Yes:
            # Iterate over the list of rows to delete in reverse order to avoid index issues
            for row in reversed(rows_to_delete):
                # Get the item ID from the selected row
                item_id = self.item_table.item(row, 1).text()  # Assuming ItemID is in the second column
    
                try:
                    # Your delete query for the Item table
                    delete_item_query = "DELETE FROM Item WHERE ItemID = %s"
    
                    # Delete the data from the table using the class cursor attribute
                    self.cursor.execute(delete_item_query, (item_id,))
                    self.db_connection.commit()
    
                except mysql.connector.Error as error:
                    print(f"Failed to delete from MySQL table: {error}")
                finally:
                    # Remove the row from the table widget
                    self.item_table.removeRow(row)
        self.refresh_item_form()

    
# Application execution
if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    ex = Item_Page()
    ex.show()
    app.exec_()
