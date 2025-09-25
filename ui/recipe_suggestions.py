# ui/recipe_suggestions.py
import difflib
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QListWidget, QListWidgetItem,
    QPushButton, QLabel, QMessageBox, QHBoxLayout
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from backend import recipe_manager

class RecipeSuggestionsWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("💡 Smart Recipe Suggestions")
        self.showMaximized()  # Open full screen

        # Gradient background
        self.setStyleSheet("""
            QMainWindow {
                background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                                  stop:0 #fdfbfb, stop:1 #ebedee);
            }
        """)

        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(50, 30, 50, 30)
        layout.setSpacing(20)

        # Title
        self.title = QLabel("💡 Smart Recipe Suggestions")
        self.title.setFont(QFont("Segoe UI", 28, QFont.Bold))
        self.title.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.title)

        # Info label
        self.info_label = QLabel("Recipes suggested based on your grocery list:")
        self.info_label.setFont(QFont("Segoe UI", 18))
        layout.addWidget(self.info_label)

        # Suggestions list
        self.suggestions_list = QListWidget()
        self.suggestions_list.setFont(QFont("Segoe UI", 16))
        self.suggestions_list.setStyleSheet("""
            QListWidget {
                background: #fff;
                border: 2px solid #ccc;
                border-radius: 12px;
                padding: 10px;
            }
        """)
        layout.addWidget(self.suggestions_list)

        # Buttons layout
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(20)

        self.btn_refresh = QPushButton("🔄 Refresh Suggestions")
        self.btn_refresh.setFont(QFont("Segoe UI", 16, QFont.Bold))
        self.btn_refresh.setStyleSheet("""
            QPushButton {
                background-color: #FF9800;
                color: white;
                border-radius: 12px;
                padding: 12px;
            }
            QPushButton:hover {
                background-color: #fb8c00;
            }
        """)
        self.btn_refresh.clicked.connect(self.load_suggestions)
        btn_layout.addWidget(self.btn_refresh)

        self.btn_close = QPushButton("Close")
        self.btn_close.setFont(QFont("Segoe UI", 16, QFont.Bold))
        self.btn_close.setStyleSheet("""
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
        self.btn_close.clicked.connect(self.close)
        btn_layout.addWidget(self.btn_close)

        layout.addLayout(btn_layout)

        self.load_suggestions()
        self.show()  # Important to display properly

    def load_suggestions(self):
        self.suggestions_list.clear()
        grocery_items = recipe_manager.get_grocery_items()

        if not grocery_items:
            QMessageBox.information(self, "No Grocery Items", "Your grocery list is empty!")
            return

        grocery_items_lower = [item.strip().lower() for item in grocery_items]
        all_recipes = recipe_manager.get_all_recipes_dict()

        recipe_scores = []

        for recipe in all_recipes:
            ingredients_lower = [ing.strip().lower() for ing in recipe['ingredients']]
            match_count = 0

            for g_item in grocery_items_lower:
                # Direct match
                if any(g_item in ing for ing in ingredients_lower):
                    match_count += 1
                    continue

                # Fuzzy match
                for ing in ingredients_lower:
                    if difflib.SequenceMatcher(None, g_item, ing).ratio() > 0.75:
                        match_count += 1
                        break

            if match_count > 0:
                recipe_scores.append((match_count, recipe))

        if not recipe_scores:
            QMessageBox.information(self, "No Suggestions", "No recipes match your grocery list!")
            return

        # Sort by best matches first
        recipe_scores.sort(key=lambda x: x[0], reverse=True)

        for score, recipe in recipe_scores:
            item = QListWidgetItem(f"{recipe['title']}  (matches: {score})")
            self.suggestions_list.addItem(item)
