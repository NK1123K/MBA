from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QTableWidget, QComboBox, QLineEdit, QPushButton, QTableWidgetItem
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

class PurchaseEntryPage(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        self.setLayout(layout)

        label = QLabel("Purchase Entry Page")
        layout.addWidget(label)

        # Table Widget
        self.table_widget = QTableWidget()
        self.table_widget.setColumnCount(7)  # Added two extra columns for buttons
        self.table_widget.setHorizontalHeaderLabels(["Vendor Name", "Price", "Discount Price", "GST %", "Total Amount", "Clear", "Delete"])
        layout.addWidget(self.table_widget)

        # Add first row with default input fields
        self.add_new_row()

        # Add Row Button
        add_row_button = QPushButton("Add Row")
        add_row_button.clicked.connect(self.add_new_row)
        layout.addWidget(add_row_button)

    def add_new_row(self):
        row_position = self.table_widget.rowCount()
        self.table_widget.insertRow(row_position)
        self.populate_cells(row_position)

    def populate_cells(self, row):
        # Vendor Name (Searchable Dropdown)
        vendor_dropdown = QComboBox()
        # Populate the vendor dropdown with vendors from the database or any other source
        vendor_dropdown.addItem("Vendor 1")
        vendor_dropdown.addItem("Vendor 2")
        self.table_widget.setCellWidget(row, 0, vendor_dropdown)

        # Price
        price_input = QLineEdit()
        self.table_widget.setCellWidget(row, 1, price_input)

        # Discount Price
        discount_input = QLineEdit()
        self.table_widget.setCellWidget(row, 2, discount_input)

        # GST %
        gst_dropdown = QComboBox()
        gst_dropdown.addItems(["1%", "2%", "3%", "5%", "18%", "25%"])
        self.table_widget.setCellWidget(row, 3, gst_dropdown)

        # Total Amount (Non-editable)
        total_amount_input = QLineEdit()
        total_amount_input.setReadOnly(True)
        self.table_widget.setCellWidget(row, 4, total_amount_input)

        # Clear Button
        clear_button = QPushButton("Clear")
        clear_button.setFont(QFont("Arial", 8))  # Increase font size
        clear_button.clicked.connect(lambda: self.clear_row(row))
        self.table_widget.setCellWidget(row, 5, clear_button)

        # Delete Button
        delete_button = QPushButton("Delete")
        delete_button.setFont(QFont("Arial", 8))  # Increase font size
        delete_button.clicked.connect(lambda: self.delete_row(row))
        self.table_widget.setCellWidget(row, 6, delete_button)

    def clear_row(self, row):
        # Clear all input fields in the row
        for col in range(self.table_widget.columnCount() - 3):  # Exclude the last three columns for buttons
            cell_widget = self.table_widget.cellWidget(row, col)
            if isinstance(cell_widget, QComboBox):
                cell_widget.setCurrentIndex(0)
            elif isinstance(cell_widget, QLineEdit):
                cell_widget.clear()

    def delete_row(self, row):
        # Remove the row from the table
        self.table_widget.removeRow(row)

