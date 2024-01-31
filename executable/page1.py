from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt

class Page1(QWidget):
    def __init__(self):
        super().__init__()

        # Input form
        form_layout = QFormLayout()
        self.vendor_name_edit = QLineEdit()
        self.gstin_edit = QLineEdit()
        self.phone_no_edit = QLineEdit()
        self.email_edit = QLineEdit()
        self.state_edit = QLineEdit()
        self.address_edit = QLineEdit()
        form_layout.addRow('Vendor Name:', self.vendor_name_edit)
        form_layout.addRow('GSTIN:', self.gstin_edit)
        form_layout.addRow('Phone No:', self.phone_no_edit)
        form_layout.addRow('Email:', self.email_edit)
        form_layout.addRow('State:', self.state_edit)
        form_layout.addRow('Address:', self.address_edit)

        # Set maximum width for each input field
        for field in (form_layout.itemAt(i).widget() for i in range(form_layout.rowCount())):
            field.setMaximumWidth(200)  # Adjust if needed

        # Create a widget for the form and buttons
        form_and_buttons_widget = QWidget()
        form_and_buttons_layout = QVBoxLayout(form_and_buttons_widget)
        form_and_buttons_layout.addLayout(form_layout)

        # Buttons
        delete_button = QPushButton('Delete')  # Changed from 'View' to 'Delete'
        save_button = QPushButton('Save')
        form_and_buttons_layout.addWidget(delete_button)
        form_and_buttons_layout.addWidget(save_button)

        # Table
        self.table = QTableWidget(0, 6)
        self.table.setHorizontalHeaderLabels(['Vendor Name', 'GSTIN', 'Phone No', 'Email', 'State', 'Address'])

        # Add a line below the table heading
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        form_and_buttons_layout.addWidget(line)

        # Main layout
        main_layout = QHBoxLayout(self)
        main_layout.addWidget(form_and_buttons_widget)
        main_layout.addWidget(self.table)

        # Connect signals and slots
        delete_button.clicked.connect(self.delete_data)
        save_button.clicked.connect(self.save_data)
        self.table.itemClicked.connect(self.table_item_clicked)  # Connect itemClicked signal

    def save_data(self):
        if self.all_fields_filled():
            reply = QMessageBox.question(self, 'Save Data', 'Are you sure you want to save?',
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes:
                row = self.table.rowCount()
                self.table.insertRow(row)
                self.table.setItem(row, 0, QTableWidgetItem(self.vendor_name_edit.text()))
                self.table.setItem(row, 1, QTableWidgetItem(self.gstin_edit.text()))
                self.table.setItem(row, 2, QTableWidgetItem(self.phone_no_edit.text()))
                self.table.setItem(row, 3, QTableWidgetItem(self.email_edit.text()))
                self.table.setItem(row, 4, QTableWidgetItem(self.state_edit.text()))
                self.table.setItem(row, 5, QTableWidgetItem(self.address_edit.text()))
                self.clear_fields()  # Clear input fields after saving

    def delete_data(self):
        selected_row = self.table.currentRow()
        if selected_row >= 0:
            vendor_name = self.table.item(selected_row, 0).text()
            gstin = self.table.item(selected_row, 1).text()

            confirmation_message = f"Are you sure you want to delete the following data?\n\n"\
                                   f"Vendor Name: {vendor_name}\n"\
                                   f"GSTIN: {gstin}"

            reply = QMessageBox.question(self, 'Delete Data', confirmation_message,
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes:
                self.table.removeRow(selected_row)

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
