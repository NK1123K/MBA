import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QFormLayout, QTableWidget, QTableWidgetItem, QDateEdit, QListWidget, QStackedWidget, QListWidgetItem
from PyQt5.QtCore import QDate

class SideNavigationMenu(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Side Navigation Menu")
        self.setGeometry(100, 100, 800, 500)
        self.initUI()

    def initUI(self):
        # Create a central widget to hold the main content
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        central_layout = QHBoxLayout(central_widget)

        # Create a QListWidget for the navigation menu
        menu_widget = QListWidget()
        menu_widget.setMaximumWidth(150)  # Reduce the width to move it further to the left
        menu_widget.addItem("Home")
        menu_widget.addItem("Product List")
        menu_widget.setStyleSheet("background-color: grey")    #color
        menu_widget.itemClicked.connect(self.displayContent)
        central_layout.addWidget(menu_widget)

        # Create a stacked widget for the content
        self.stacked_widget = QStackedWidget()
        central_layout.addWidget(self.stacked_widget)

        # Create the content area for Home
        home_widget = QWidget()
        home_layout = QVBoxLayout(home_widget)
        home_label = QLabel("Welcome to the Home Page")
        home_layout.addWidget(home_label)
        self.stacked_widget.addWidget(home_widget)

        # Create the content area for Product List
        product_list_widget = QWidget()
        product_list_layout = QHBoxLayout(product_list_widget)
        self.stacked_widget.addWidget(product_list_widget)
        self.Product_List(product_list_layout)

    def displayContent(self, item):
        selected_item_text = item.text()
        if selected_item_text == "Home":
            self.stacked_widget.setCurrentIndex(0)
        elif selected_item_text == "Product List":
            self.stacked_widget.setCurrentIndex(1)

    def Product_List(self, layout):
        product_form_widget = QWidget()
        table_widget = QWidget()

        product_form_layout = QVBoxLayout(product_form_widget)
        table_layout = QVBoxLayout(table_widget)

        product_form_layout.setAlignment(Qt.AlignTop)

        product_form_layout.addWidget(QLabel("Product Details"))

        product_form_widget.setMinimumSize(300, 0)  # Set the minimum width to 300 pixels
        product_form_widget.setMaximumSize(300, 800)  # Set the maximum width and height
        table_widget.setMinimumSize(300, 0)  # Set the minimum width to 300 pixels

        form_layout = QFormLayout()

        labels = [
            "Product Name:",
            "Quantity:",
            "Vendor Name:",
            "Product Buy Price:",
            "Selling Price:",
            "Free:",
            "Purchase Date:",
            "Invoice Number:",
            "Expiry Date:"
        ]

        self.entry_fields = {}

        for label_text in labels:
            label = QLabel(label_text)
            entry = QLineEdit() if "Date" not in label_text else QDateEdit()
            if "Date" in label_text:
                entry.setCalendarPopup(True)
                entry.setDate(QDate.currentDate())
            form_layout.addRow(label, entry)
            self.entry_fields[label_text] = entry

        self.submit_button = QPushButton("Add Product")
        self.submit_button.clicked.connect(self.add_product_to_table)
        self.submit_button.setStyleSheet("background-color : cyan")    #color

        back_button = QPushButton("Back")
        back_button.clicked.connect(lambda: self.displayContent(QListWidgetItem("Home")))  # Navigate back to Home
        back_button.setStyleSheet("background-color : silver")  #color
        product_form_layout.addLayout(form_layout)
        product_form_layout.addWidget(self.submit_button)
        product_form_layout.addWidget(back_button)

        table_layout.addWidget(QLabel("Product List"))
        self.product_table = QTableWidget()
        self.product_table.setColumnCount(9)
        self.product_table.setHorizontalHeaderLabels(["Product Name", "Quantity", "Vendor Name", "Buy Price", "Sell Price", "Free", "Purchase Date", "Invoice Number", "Expiry Date"])
        table_layout.addWidget(self.product_table)

        layout.addWidget(product_form_widget)
        layout.addWidget(table_widget)

    def add_product_to_table(self):
        product_data = [self.entry_fields[label].text() if "Date" not in label else self.entry_fields[label].date().toString("dd-MM-yyyy") for label in self.entry_fields]
        row_position = self.product_table.rowCount()
        self.product_table.insertRow(row_position)
        for col, data in enumerate(product_data):
            item = QTableWidgetItem(data)
            self.product_table.setItem(row_position, col, item)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SideNavigationMenu()
    window.show()
    sys.exit(app.exec_())
