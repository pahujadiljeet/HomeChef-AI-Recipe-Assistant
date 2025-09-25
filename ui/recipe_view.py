# ui/recipe_view.py
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QSplitter,
    QListWidget, QListWidgetItem, QLabel, QPushButton, QTextEdit,
    QLineEdit, QScrollArea, QSizePolicy, QMessageBox
)
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt, QSize
from backend import recipe_manager
import os

class RecipeView(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("🍽️ Recipes - HomeChef")
        self.showMaximized()

        central = QWidget()
        self.setCentralWidget(central)
        layout = QHBoxLayout(central)

        splitter = QSplitter(Qt.Horizontal)
        layout.addWidget(splitter)

        # ---------------- LEFT PANEL ----------------
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)
        left_layout.setContentsMargins(15, 15, 15, 15)
        left_layout.setSpacing(12)

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("🔍 Search recipes by title or ingredient...")
        self.search_input.returnPressed.connect(self.on_search)
        self.search_input.setFont(QFont("Arial", 14))
        self.search_input.setStyleSheet("""
            QLineEdit {
                padding: 10px; border-radius: 12px; border: 2px solid #ccc;
            }
            QLineEdit:focus {
                border: 2px solid #4CAF50;
            }
        """)
        left_layout.addWidget(self.search_input)

        self.list_widget = QListWidget()
        self.list_widget.setIconSize(QSize(64, 64))
        self.list_widget.itemClicked.connect(self.on_item_click)
        self.list_widget.setStyleSheet("""
            QListWidget::item {
                padding: 8px; border-radius: 10px;
            }
            QListWidget::item:selected {
                background-color: #4CAF50; color: white;
            }
        """)
        left_layout.addWidget(self.list_widget, 1)

        refresh_btn = QPushButton("🔄 Refresh Recipes")
        refresh_btn.clicked.connect(self.load_recipes)
        refresh_btn.setStyleSheet(self.modern_button_style("#4CAF50"))
        left_layout.addWidget(refresh_btn)

        splitter.addWidget(left_widget)
        splitter.setStretchFactor(0, 30)

        # ---------------- RIGHT PANEL ----------------
        right_scroll = QScrollArea()
        right_scroll.setWidgetResizable(True)
        right_content = QWidget()
        right_layout = QVBoxLayout(right_content)
        right_layout.setContentsMargins(20, 20, 20, 20)
        right_layout.setSpacing(15)

        # Back button
        back_btn = QPushButton("⬅ Back to Home")
        back_btn.setStyleSheet(self.modern_button_style("#555"))
        back_btn.clicked.connect(self.go_home)
        right_layout.addWidget(back_btn, alignment=Qt.AlignLeft)

        # Image
        self.image_label = QLabel()
        self.image_label.setFixedHeight(260)
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setStyleSheet("border: 2px dashed #ccc; border-radius:12px;")
        right_layout.addWidget(self.image_label)

        # Title
        self.title_label = QLabel("<h2>Title</h2>")
        self.title_label.setFont(QFont("Arial", 20, QFont.Bold))
        right_layout.addWidget(self.title_label)

        # Meta
        self.meta_label = QLabel("")
        self.meta_label.setStyleSheet("color: #666; font-size: 14px;")
        right_layout.addWidget(self.meta_label)

        # Ingredients
        ing_title = QLabel("📝 Ingredients")
        ing_title.setFont(QFont("Arial", 16, QFont.Bold))
        right_layout.addWidget(ing_title)

        self.ingredients_text = QTextEdit()
        self.ingredients_text.setReadOnly(True)
        self.ingredients_text.setStyleSheet("background:#f1f1f1; border-radius:10px; padding:10px;")
        right_layout.addWidget(self.ingredients_text)

        # Instructions
        inst_title = QLabel("👨‍🍳 Instructions")
        inst_title.setFont(QFont("Arial", 16, QFont.Bold))
        right_layout.addWidget(inst_title)

        self.instructions_text = QTextEdit()
        self.instructions_text.setReadOnly(True)
        self.instructions_text.setStyleSheet("background:#f1f1f1; border-radius:10px; padding:10px;")
        right_layout.addWidget(self.instructions_text, 1)

        # Buttons row
        btn_layout = QHBoxLayout()
        self.fav_btn = QPushButton("❤ Add to Favorites")
        self.fav_btn.setStyleSheet(self.modern_button_style("#ff4081"))
        self.fav_btn.clicked.connect(self.add_to_favorites)
        btn_layout.addWidget(self.fav_btn)

        self.start_btn = QPushButton("▶ Start Cooking")
        self.start_btn.setStyleSheet(self.modern_button_style("#2196F3"))
        self.start_btn.clicked.connect(self.start_cooking)
        btn_layout.addWidget(self.start_btn)
        right_layout.addLayout(btn_layout)

        right_scroll.setWidget(right_content)
        splitter.addWidget(right_scroll)
        splitter.setStretchFactor(1, 70)

        self.recipes = []
        self.current_recipe = None
        self.load_recipes()

    # ---------------- HELPER ----------------
    def modern_button_style(self, color):
        return f"""
            QPushButton {{
                background-color: {color};
                color: white;
                border-radius: 12px;
                padding: 10px;
                font-size: 14px;
            }}
            QPushButton:hover {{
                background-color: #555;
            }}
        """

    # ---------------- METHODS ----------------
    def go_home(self):
        self.close()
        if self.parent():
            self.parent().showMaximized()

    def get_asset_path(self, image_filename):
        base = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        if not image_filename:
            return None
        candidate = os.path.join(base, 'assets', os.path.basename(image_filename))
        if os.path.exists(candidate):
            return candidate
        candidate2 = os.path.join(base, image_filename)
        if os.path.exists(candidate2):
            return candidate2
        return None

    def load_recipes(self):
        self.recipes = recipe_manager.get_all_recipes_dict()
        self.list_widget.clear()
        for r in self.recipes:
            item = QListWidgetItem(r['title'])
            item.setData(Qt.UserRole, r['id'])
            self.list_widget.addItem(item)

    def on_item_click(self, item):
        recipe_id = item.data(Qt.UserRole)
        recipe = recipe_manager.get_recipe_by_id(recipe_id)
        if recipe:
            self.display_recipe(recipe)

    def display_recipe(self, recipe):
        self.current_recipe = recipe
        self.title_label.setText(f"<h2>{recipe['title']}</h2>")
        time_str = recipe.get('time', '-') or '-'
        diff_str = recipe.get('difficulty', '-') or '-'
        self.meta_label.setText(f"⏱ {time_str}   |   ⚡ Difficulty: {diff_str}")
        self.ingredients_text.setPlainText("\n".join(f"- {i.strip()}" for i in recipe['ingredients']))
        self.instructions_text.setPlainText(recipe.get('instructions', ''))

        img_path = self.get_asset_path(recipe.get('image', ''))
        if img_path:
            pix = QPixmap(img_path).scaled(
                self.image_label.width(),
                self.image_label.height(),
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )
            self.image_label.setPixmap(pix)
        else:
            self.image_label.setText("No image available")

    def add_to_favorites(self):
        if not self.current_recipe:
            QMessageBox.information(self, "No selection", "Please select a recipe first.")
            return
        recipe_manager.add_favorite(self.current_recipe['id'])
        QMessageBox.information(self, "Saved", f"'{self.current_recipe['title']}' added to favorites.")

    def start_cooking(self):
        if not self.current_recipe:
            QMessageBox.information(self, "No selection", "Please select a recipe first.")
            return
        QMessageBox.information(
            self, "Start Cooking",
            f"Starting cooking: {self.current_recipe['title']} (feature to be expanded)"
        )

    def on_search(self):
        q = self.search_input.text().strip().lower()
        if not q:
            self.load_recipes()
            return
        self.list_widget.clear()
        for r in self.recipes:
            if q in r['title'].lower() or any(q in ing.lower() for ing in r['ingredients']):
                item = QListWidgetItem(r['title'])
                item.setData(Qt.UserRole, r['id'])
                self.list_widget.addItem(item)
