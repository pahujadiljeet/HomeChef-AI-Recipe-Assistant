# chatbot_panel.py
from PyQt5.QtWidgets import QWidget, QSizePolicy, QVBoxLayout, QHBoxLayout, QTextEdit, QLineEdit, QPushButton, QLabel, QScrollArea
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from backend.gpt_api import ask_ai

class ChatbotPanel(QWidget):
    def __init__(self, parent=None, go_home_callback=None):
        super().__init__(parent)
        self.go_home_callback = go_home_callback
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setStyleSheet("background:#fdfdfd; border-radius:12px;")

        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(10)
        main_layout.setContentsMargins(15, 15, 15, 15)

        # Title
        self.title = QLabel("🤖 AI Chatbot - Ask me anything about cooking!")
        self.title.setFont(QFont("Arial", 18, QFont.Bold))
        main_layout.addWidget(self.title, alignment=Qt.AlignCenter)

        # Scrollable chat area
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setStyleSheet("background:#f5f5f5; border:none;")
        main_layout.addWidget(self.scroll_area, 1)

        # Container for chat messages
        self.chat_container = QWidget()
        self.chat_layout = QVBoxLayout(self.chat_container)
        self.chat_layout.setAlignment(Qt.AlignTop)
        self.chat_layout.setSpacing(10)
        self.scroll_area.setWidget(self.chat_container)

        # Input row
        input_layout = QHBoxLayout()
        self.input_box = QLineEdit()
        self.input_box.setPlaceholderText("Type your message here...")
        self.input_box.setFont(QFont("Arial", 16))
        input_layout.addWidget(self.input_box)

        self.send_btn = QPushButton("Send")
        self.send_btn.setFont(QFont("Arial", 16))
        self.send_btn.setStyleSheet("background:#4CAF50; color:white; border-radius:8px; padding:8px;")
        self.send_btn.clicked.connect(self.send_message)
        input_layout.addWidget(self.send_btn)
        main_layout.addLayout(input_layout)

        # Back/Home button
        self.back_btn = QPushButton("⬅ Back to Home")
        self.back_btn.setFont(QFont("Arial", 14, QFont.Bold))
        self.back_btn.setStyleSheet("""
            background:#FF5722;
            color:white;
            border-radius:10px;
            padding:10px;
        """)
        self.back_btn.clicked.connect(self.go_back)
        main_layout.addWidget(self.back_btn, alignment=Qt.AlignCenter)

    def go_back(self):
        if self.go_home_callback:
            self.go_home_callback()

    def add_message(self, text, sender='user'):
        bubble = QLabel(text)
        bubble.setWordWrap(True)
        bubble.setFont(QFont("Arial", 14))
        bubble.setTextInteractionFlags(Qt.TextSelectableByMouse)

        if sender == 'user':
            bubble.setStyleSheet("""
                background-color: #DCF8C6;
                padding:10px;
                border-radius:12px;
                max-width: 400px;
            """)
            alignment = Qt.AlignRight
        else:
            bubble.setStyleSheet("""
                background-color: #FFFFFF;
                padding:10px;
                border-radius:12px;
                max-width: 400px;
            """)
            alignment = Qt.AlignLeft

        wrapper = QHBoxLayout()
        wrapper.setAlignment(alignment)
        wrapper.addWidget(bubble)
        self.chat_layout.addLayout(wrapper)
        self.scroll_area.verticalScrollBar().setValue(self.scroll_area.verticalScrollBar().maximum())

    def send_message(self):
        user_text = self.input_box.text().strip()
        if not user_text:
            return
        self.add_message(user_text, sender='user')
        self.input_box.clear()
        try:
            ai_reply = ask_ai(user_text)
            self.add_message(ai_reply, sender='ai')
        except Exception as e:
            self.add_message(f"⚠️ Error: {e}", sender='ai')
