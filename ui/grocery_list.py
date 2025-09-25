# ui/grocery_list.py
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QListWidget, QListWidgetItem,
    QLineEdit, QPushButton, QLabel, QMessageBox
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from backend import recipe_manager

class GroceryListWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("🛒 Grocery List")
        self.showMaximized()  # Open full screen
        self.setStyleSheet("background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #fdfbfb, stop:1 #ebedee);")

        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(50, 30, 50, 30)
        main_layout.setSpacing(20)

        # Title
        title = QLabel("🛒 My Grocery List")
        title.setFont(QFont("Segoe UI", 28, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title)

        # Input + Add button
        input_layout = QHBoxLayout()
        self.input_item = QLineEdit()
        self.input_item.setPlaceholderText("Enter grocery item")
        self.input_item.setFont(QFont("Segoe UI", 16))
        self.input_item.setStyleSheet("""
            QLineEdit {
                padding: 12px;
                border: 2px solid #ccc;
                border-radius: 10px;
            }
            QLineEdit:focus {
                border: 2px solid #4CAF50;
            }
        """)
        input_layout.addWidget(self.input_item)

        self.btn_add = QPushButton("Add")
        self.btn_add.setFont(QFont("Segoe UI", 16, QFont.Bold))
        self.btn_add.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border-radius: 12px;
                padding: 12px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        self.btn_add.clicked.connect(self.add_item)
        input_layout.addWidget(self.btn_add)

        main_layout.addLayout(input_layout)

        # Grocery list
        self.list_widget = QListWidget()
        self.list_widget.setFont(QFont("Segoe UI", 16))
        self.list_widget.setStyleSheet("""
            QListWidget {
                background: #fff;
                border: 2px solid #ccc;
                border-radius: 12px;
                padding: 10px;
            }
        """)
        main_layout.addWidget(self.list_widget)

        # Buttons layout
        btn_layout = QHBoxLayout()
        self.btn_remove = QPushButton("Remove Selected")
        self.btn_remove.setFont(QFont("Segoe UI", 16, QFont.Bold))
        self.btn_remove.setStyleSheet("""
            QPushButton {
                background-color: #E91E63;
                color: white;
                border-radius: 12px;
                padding: 12px;
            }
            QPushButton:hover {
                background-color: #d81b60;
            }
        """)
        self.btn_remove.clicked.connect(self.remove_selected)
        btn_layout.addWidget(self.btn_remove)

        self.btn_close = QPushButton("Close")
        self.btn_close.setFont(QFont("Segoe UI", 16, QFont.Bold))
        self.btn_close.setStyleSheet("""
            QPushButton {
                background-color: #9C27B0;
                color: white;
                border-radius: 12px;
                padding: 12px;
            }
            QPushButton:hover {
                background-color: #8e24aa;
            }
        """)
        self.btn_close.clicked.connect(self.close)
        btn_layout.addWidget(self.btn_close)

        main_layout.addLayout(btn_layout)

        self.load_items()
        self.show()  # Important to display the window properly

    def load_items(self):
        self.list_widget.clear()
        items = recipe_manager.get_grocery_items()
        for item in items:
            list_item = QListWidgetItem(item)
            self.list_widget.addItem(list_item)

    def add_item(self):
        item_name = self.input_item.text().strip()
        if not item_name:
            QMessageBox.warning(self, "Empty Input", "Please enter an item name.")
            return
        recipe_manager.add_grocery_item(item_name)
        self.input_item.clear()
        self.load_items()

    def remove_selected(self):
        selected_item = self.list_widget.currentItem()
        if not selected_item:
            QMessageBox.warning(self, "No Selection", "Please select an item to remove.")
            return
        item_name = selected_item.text()
        recipe_manager.remove_grocery_item(item_name)
        self.load_items()
