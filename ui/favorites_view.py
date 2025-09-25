# ui/favorites_view.py
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QListWidget, QListWidgetItem,
    QMessageBox, QPushButton, QLabel, QHBoxLayout
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from backend import recipe_manager

class FavoritesWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("⭐ Favorites - HomeChef")
        self.showMaximized()  # Full screen

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
        self.title = QLabel("⭐ Your Favorite Recipes")
        self.title.setFont(QFont("Segoe UI", 28, QFont.Bold))
        self.title.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.title)

        # Favorites list
        self.fav_list = QListWidget()
        self.fav_list.setFont(QFont("Segoe UI", 16))
        self.fav_list.setStyleSheet("""
            QListWidget {
                background: #fff;
                border: 2px solid #ccc;
                border-radius: 12px;
                padding: 10px;
            }
        """)
        layout.addWidget(self.fav_list)

        # Buttons layout
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(20)

        self.btn_remove = QPushButton("🗑 Remove Selected")
        self.btn_remove.setFont(QFont("Segoe UI", 16, QFont.Bold))
        self.btn_remove.setStyleSheet("""
            QPushButton {
                background-color: #F44336;
                color: white;
                border-radius: 12px;
                padding: 12px;
            }
            QPushButton:hover {
                background-color: #e53935;
            }
        """)
        self.btn_remove.clicked.connect(self.remove_selected)
        btn_layout.addWidget(self.btn_remove)

        self.btn_refresh = QPushButton("🔄 Refresh")
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
        self.btn_refresh.clicked.connect(self.load_favorites)
        btn_layout.addWidget(self.btn_refresh)

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

        layout.addLayout(btn_layout)

        self.load_favorites()
        self.show()

    def load_favorites(self):
        """Load favorites (expects recipe_manager.get_favorites() to return list of dicts)."""
        self.fav_list.clear()
        try:
            favorites = recipe_manager.get_favorites()
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Could not load favorites: {e}")
            return

        if not favorites:
            # Optional: placeholder when empty
            # self.fav_list.addItem("(No favorites yet)")
            return

        for r in favorites:
            title = r.get('title') or r.get('name') or "Untitled"
            item = QListWidgetItem(title)
            item.setData(Qt.UserRole, r.get('id'))
            self.fav_list.addItem(item)

    def remove_selected(self):
        item = self.fav_list.currentItem()
        if not item:
            QMessageBox.information(self, "No selection", "Please select a favorite to remove.")
            return
        recipe_id = item.data(Qt.UserRole)
        recipe_manager.remove_favorite(recipe_id)
        QMessageBox.information(self, "Removed", f"Removed '{item.text()}' from favorites.")
        self.load_favorites()
