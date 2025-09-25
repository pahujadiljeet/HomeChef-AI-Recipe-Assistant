# main_window.py
from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QPushButton, QLabel, QSizePolicy, QStackedLayout
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

from ui.recipe_view import RecipeView
from ui.recipe_suggestions import RecipeSuggestionsWindow
from ui.favorites_view import FavoritesWindow
from ui.chatbot_panel import ChatbotPanel
from ui.grocery_list import GroceryListWindow

class HomeChefApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🍳 HomeChef - AI Recipe Assistant")
        self.showMaximized()

        # ----------------------
        # Central stacked layout
        # ----------------------
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.stack = QStackedLayout(self.central_widget)

        # ----------------------
        # Home container
        # ----------------------
        self.home_container = QWidget()
        self.home_layout = QVBoxLayout(self.home_container)
        self.home_layout.setAlignment(Qt.AlignCenter)
        self.home_layout.setSpacing(25)

        self.label = QLabel("🍳 Welcome to HomeChef!")
        self.label.setFont(QFont("Segoe UI", 32, QFont.Bold))
        self.label.setStyleSheet("color: #222;")
        self.home_layout.addWidget(self.label, alignment=Qt.AlignCenter)

        self.recipe_button = self.create_modern_button("📖 Recipes", "#4CAF50", self.open_recipes)
        self.chatbot_button = self.create_modern_button("🤖 AI Chatbot", "#FF9800", self.open_chatbot)
        self.grocery_button = self.create_modern_button("🛒 Grocery List", "#2196F3", self.open_grocery_list)
        self.suggest_button = self.create_modern_button("✨ Smart Suggestions", "#9C27B0", self.open_suggestions)
        self.fav_button = self.create_modern_button("⭐ Favorites", "#E91E63", self.open_favorites)

        self.home_layout.addWidget(self.recipe_button)
        self.home_layout.addWidget(self.chatbot_button)
        self.home_layout.addWidget(self.grocery_button)
        self.home_layout.addWidget(self.suggest_button)
        self.home_layout.addWidget(self.fav_button)

        # Add home to stack
        self.stack.addWidget(self.home_container)

        # ----------------------
        # Window references
        # ----------------------
        self.recipe_window = None
        self.suggestions_window = None
        self.favorites_window = None
        self.grocery_window = None
        self.chatbot_panel = None

        # Modern gradient background
        self.setStyleSheet("""
            QMainWindow {
                background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                                  stop:0 #fdfbfb, stop:1 #ebedee);
            }
        """)

    # Modern button helper
    def create_modern_button(self, text, color, callback):
        btn = QPushButton(text)
        btn.setFixedSize(380, 70)
        btn.setFont(QFont("Segoe UI", 16, QFont.Bold))
        btn.clicked.connect(callback)
        btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {color};
                color: white;
                border-radius: 15px;
                padding: 12px;
            }}
            QPushButton:hover {{
                background-color: {color};
                opacity: 0.85;
            }}
        """)
        return btn

    # Open windows
    def open_recipes(self):
        if not self.recipe_window:
            self.recipe_window = RecipeView(self)
        self.recipe_window.showMaximized()

    def open_suggestions(self):
        if not self.suggestions_window:
            self.suggestions_window = RecipeSuggestionsWindow(self)
        self.suggestions_window.showMaximized()

    def open_favorites(self):
        if not self.favorites_window:
            self.favorites_window = FavoritesWindow(self)
        self.favorites_window.showMaximized()

    def open_grocery_list(self):
        if not self.grocery_window:
            self.grocery_window = GroceryListWindow(self)
        self.grocery_window.showMaximized()
        self.grocery_window.raise_()
        self.grocery_window.activateWindow()

    # =========================
    # Back to home
    # =========================
    def show_home(self):
        self.stack.setCurrentWidget(self.home_container)

    # =========================
    # Open Chatbot
    # =========================
    def open_chatbot(self):
        if not self.chatbot_panel:
            self.chatbot_panel = ChatbotPanel(parent=self, go_home_callback=self.show_home)
            self.stack.addWidget(self.chatbot_panel)
        self.stack.setCurrentWidget(self.chatbot_panel)
