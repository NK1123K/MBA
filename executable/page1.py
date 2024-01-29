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

        form_widget = QWidget()
        form_widget.setLayout(form_layout)

        # Set size policy for the form widget
        form_widget.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        # Set width to 20% of the overall screen size
        form_widget.setMaximumWidth(int(QApplication.desktop().screenGeometry().width() * 0.2))

        # View button
        view_button = QPushButton('View')
        view_button.clicked.connect(self.view_data)

        # Save button
        save_button = QPushButton('Save')
        save_button.clicked.connect(self.save_data)

        # Create a widget for button layout
        button_widget = QWidget()
        button_layout = QHBoxLayout(button_widget)
        button_layout.addWidget(view_button)
        button_layout.addWidget(save_button)

        # Create a splitter to divide the form and table
        splitter = QSplitter(Qt.Horizontal)

        # Table
        self.table = QTableWidget(5, 6)
        self.table.setHorizontalHeaderLabels(['Vendor Name', 'GSTIN', 'Phone No', 'Email', 'State', 'Address'])

        # Add widgets to splitter
        splitter.addWidget(form_widget)
        splitter.addWidget(button_widget)
        splitter.addWidget(self.table)

        # Set the size of the splitter handle (the bar between form and table)
        splitter.setHandleWidth(1)

        # Set the main layout of the window
        main_layout = QHBoxLayout(self)
        main_layout.addWidget(splitter)

        self.setLayout(main_layout)

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

    def view_data(self):
        # Implement the action when the "View" button is clicked
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
