from PyQt5.QtWidgets import *
import sys
from page1 import Page1


class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        # Window setup
        self.setWindowTitle('Inventory')
        self.resize(800, 500)  # Set initial size

        # Create button 1
        self.btn_1 = QPushButton('Vendor Screen', self)
        self.btn_1.clicked.connect(self.button1)

        # Create tab widget (initially empty)
        self.right_widget = QTabWidget()

        # Layout setup
        left_layout = QVBoxLayout()
        left_layout.addWidget(self.btn_1)
        left_layout.addStretch(1)  # Add spacing
        left_widget = QWidget()
        left_widget.setLayout(left_layout)

        # Main layout
        main_layout = QHBoxLayout()
        main_layout.addWidget(left_widget)
        main_layout.addWidget(self.right_widget)
        main_widget = QWidget()
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

        # Initialize Page1 to None
        self.page1 = None

    def button1(self):
        if not self.page1:  # Load Page1 only if not already loaded
            self.page1 = Page1()
            self.right_widget.addTab(self.page1, 'Page 1')
        self.right_widget.setCurrentIndex(self.right_widget.indexOf(self.page1))

# Application execution
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Window()
    ex.show()
    sys.exit(app.exec_())
