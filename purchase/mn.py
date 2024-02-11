import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QHBoxLayout, QListWidget, QStackedWidget, QLabel
from vpp import Vendor_Page as VP
from ip import Item_Page as IP
from PurchaseEntryPage import PurchaseEntryPage  # Import the PurchaseEntryPage class

class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        central_layout = QHBoxLayout(central_widget)

        menu_widget = QListWidget()
        menu_widget.setMaximumWidth(150)
        menu_widget.addItem("Home")
        menu_widget.addItem("Vendor Details")
        menu_widget.addItem("Item Details")
        menu_widget.addItem("Purchase Entry")  # Add Purchase Entry menu item
        menu_widget.setStyleSheet("background-color: grey")
        menu_widget.itemClicked.connect(self.displayContent)
        central_layout.addWidget(menu_widget)

        # Create a QStackedWidget
        self.stacked_widget = QStackedWidget()
        central_layout.addWidget(self.stacked_widget)

        # Create widgets for different pages
        home_widget = QWidget()
        home_layout = QHBoxLayout(home_widget)
        home_layout.addWidget(QLabel("Home Page"))
        self.stacked_widget.addWidget(home_widget)

        # Add your Vendor Details page widget here
        vendor_details_widget = QWidget()
        vendor_details_layout = QHBoxLayout(vendor_details_widget)
        vendor_page_instance = VP()
        vendor_page_instance.Vendor_Details(vendor_details_layout)
        self.stacked_widget.addWidget(vendor_details_widget)

        item_details_widget = QWidget()
        item_details_layout = QHBoxLayout(item_details_widget)
        item_page_instance = IP()
        item_page_instance.Item_Details(item_details_layout)
        self.stacked_widget.addWidget(item_details_widget)

        # Add Purchase Entry page widget here
        purchase_entry_widget = PurchaseEntryPage()
        self.stacked_widget.addWidget(purchase_entry_widget)

    def displayContent(self, item):
        selected_item_text = item.text()
        if selected_item_text == "Home":
            self.stacked_widget.setCurrentIndex(0)
        elif selected_item_text == "Vendor Details":
            self.stacked_widget.setCurrentIndex(1)
        elif selected_item_text == "Item Details":
            self.stacked_widget.setCurrentIndex(2)
        elif selected_item_text == "Purchase Entry":  # Handle Purchase Entry menu item
            self.stacked_widget.setCurrentIndex(3)


# Application execution
if __name__ == '__main__':
    try:
        app = QApplication(sys.argv)
        ex = Window()
        ex.show()
        sys.exit(app.exec_())
    except Exception as e:
        print(f"An error occurred: {e}")

#    def delete_row(self, row):
#         # Remove the row from the table
#         self.table_widget.removeRow(row)