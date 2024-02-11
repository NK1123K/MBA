from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from VendorDBOperations import VendorDBOperations

class AddressEditDialog(QDialog):
    def __init__(self, vendor_data):
        super().__init__()
        self.vendor_data = vendor_data
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Edit Vendor Details")
        layout = QFormLayout()
        self.vendor_name_edit = QLineEdit()
        self.gstin_edit = QLineEdit()
        self.phone_no_edit = QLineEdit()
        self.email_edit = QLineEdit()
        self.state_edit = QLineEdit()
        self.address_edit = QTextEdit()
        
        layout.addRow('Vendor Name:', self.vendor_name_edit)
        layout.addRow('GSTIN:', self.gstin_edit)
        layout.addRow('Phone No:', self.phone_no_edit)
        layout.addRow('Email:', self.email_edit)
        layout.addRow('State:', self.state_edit)
        layout.addRow('Address:', self.address_edit)

        # Set initial values for the fields
        self.vendor_name_edit.setText(self.vendor_data[0])
        self.gstin_edit.setText(self.vendor_data[1])
        self.phone_no_edit.setText(self.vendor_data[2])
        self.email_edit.setText(self.vendor_data[3])
        self.state_edit.setText(self.vendor_data[4])
        self.address_edit.setPlainText(self.vendor_data[5])

        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)
        self.setLayout(layout)

class Page1(QWidget):
    def __init__(self):
        super().__init__()
        self.db_operations = VendorDBOperations()
        self.init_ui()

    def init_ui(self):
        # Input form
        form_layout = QFormLayout()
        self.vendor_name_edit = QLineEdit()
        self.gstin_edit = QLineEdit()
        self.phone_no_edit = QLineEdit()
        self.email_edit = QLineEdit()
        self.state_edit = QLineEdit()
        self.address_edit = QTextEdit()  # Use QTextEdit for multi-line text input

        form_layout.addRow('Vendor Name:', self.vendor_name_edit)
        form_layout.addRow('GSTIN:', self.gstin_edit)
        form_layout.addRow('Phone No:', self.phone_no_edit)
        form_layout.addRow('Email:', self.email_edit)
        form_layout.addRow('State:', self.state_edit)
        form_layout.addRow('Address:', self.address_edit)
        

        # Set maximum width for each input field
        for field in (self.vendor_name_edit, self.gstin_edit, self.phone_no_edit,
                      self.email_edit, self.state_edit):
            field.setMaximumWidth(200)  # Adjust if needed

        # Create a widget for the form and buttons
        form_and_buttons_widget = QWidget()
        form_and_buttons_layout = QVBoxLayout(form_and_buttons_widget)
        form_and_buttons_layout.addLayout(form_layout)

        # Buttons
        buttons_layout = QHBoxLayout()
        delete_button = QPushButton('Delete')  # Changed from 'View' to 'Delete'
        save_button = QPushButton('Save')
        buttons_layout.addWidget(delete_button)
        buttons_layout.addWidget(save_button)
        form_and_buttons_layout.addLayout(buttons_layout)

        # Add search input field and search button
        search_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        search_button = QPushButton('Search')
        search_layout.addWidget(self.search_input)
        search_layout.addWidget(search_button)
        form_and_buttons_layout.addLayout(search_layout)

        # Add refresh table button
        refresh_button = QPushButton('Refresh Table')
        form_and_buttons_layout.addWidget(refresh_button)

        # Table
        self.table = QTableWidget(0, 8)  # Adjusted column count, added one for the checkbox and one for the edit button
        self.table.setHorizontalHeaderLabels(['', 'Vendor Name', 'GSTIN', 'Phone No', 'Email', 'State', 'Address', 'Edit'])
        self.table.horizontalHeader().setSectionResizeMode(6, QHeaderView.Stretch)  # Set stretch factor for Address column
        self.table.horizontalHeader().setSectionResizeMode(7, QHeaderView.Fixed)  # Set fixed width for Edit column
        self.table.horizontalHeader().resizeSection(7, 60)  # Set width for Edit column
        self.table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)  # Set size policy
        self.populate_table()  # Populate table initially

        # Add a line below the table heading
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        form_and_buttons_layout.addWidget(line)

        # Main layout
        main_layout = QHBoxLayout(self)
        main_layout.addWidget(form_and_buttons_widget)

        # Add table to a container widget with a layout for adjusting its width
        table_container = QWidget()
        table_layout = QVBoxLayout(table_container)
        table_layout.addWidget(self.table)
        main_layout.addWidget(table_container, 75)  # Set table width to 75% of the window width

        # Connect signals and slots
        delete_button.clicked.connect(self.delete_data)
        save_button.clicked.connect(self.save_data)
        search_button.clicked.connect(self.search_data)
        refresh_button.clicked.connect(self.refresh_table)  # Connect refresh button to refresh_table method
        self.table.itemClicked.connect(self.table_item_clicked)  # Connect itemClicked signal

    def save_data(self):
        if self.all_fields_filled():
            reply = QMessageBox.question(self, 'Save Data', 'Are you sure you want to save?',
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes:
                vendor_data = (
                    self.vendor_name_edit.text(),
                    self.gstin_edit.text(),
                    self.phone_no_edit.text(),
                    self.email_edit.text(),
                    self.state_edit.text(),
                    self.address_edit.toPlainText()  # Use toPlainText() to get the text from QTextEdit
                )
                self.db_operations.insert_vendor(vendor_data)
                self.populate_table()  # Repopulate table after saving
                self.clear_fields()  # Clear input fields after saving

    def delete_data(self):
        selected_row = self.table.currentRow()
        if selected_row >= 0:
            vendor_id = self.table.item(selected_row, 1).text()  # Assuming vendor_id is in the second column
            confirmation_message = "Are you sure you want to delete the selected vendor?"
            reply = QMessageBox.question(self, 'Delete Data', confirmation_message,
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes:
                self.db_operations.delete_vendor(vendor_id)
                self.populate_table()  # Repopulate table after deleting

    def search_data(self):
        search_text = self.search_input.text().strip()
        if search_text:
            self.populate_table(search_text)

    def refresh_table(self):
        self.populate_table()  # Call populate_table without any search text to refresh the table

    def populate_table(self, search_text=None):
        self.table.setRowCount(0)  # Clear existing data
        vendors = self.db_operations.get_all_vendors(search_text)  # Retrieve all vendors from the database with optional search_text
        for vendor in vendors:
            row_position = self.table.rowCount()
            self.table.insertRow(row_position)
            checkbox_item = QTableWidgetItem()
            checkbox_item.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
            checkbox_item.setCheckState(Qt.Unchecked)
            self.table.setItem(row_position, 0, checkbox_item)
            for column, data in enumerate(vendor[1:]):  # Skip the vendor ID column
                self.table.setItem(row_position, column + 1, QTableWidgetItem(str(data)))

            # Add Edit button
            edit_button = QPushButton('Edit')
            edit_button.clicked.connect(lambda _, row=row_position: self.edit_address(row))
            self.table.setCellWidget(row_position, 7, edit_button)

    def edit_address(self, row):
        address = self.table.item(row, 6).text()  # Get the address text from the table
        dialog = AddressEditDialog(address)
        if dialog.exec_():
            new_address = dialog.address_edit.toPlainText()
            # Update the address in the database or perform any other necessary action

    def table_item_clicked(self, item):
        # Implement the action when an item from the table is clicked
        pass

    def all_fields_filled(self):
        return all(field.text() for field in (self.vendor_name_edit, self.gstin_edit, self.phone_no_edit,
                                               self.email_edit, self.state_edit, self.address_edit))

    def clear_fields(self):
        for field in (self.vendor_name_edit, self.gstin_edit, self.phone_no_edit,
                      self.email_edit, self.state_edit, self.address_edit):
            field.clear()

if __name__ == "__main__":
    app = QApplication([])
    window = Page1()
    window.show()
    app.exec_()
