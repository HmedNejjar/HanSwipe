import sys
from base_ui import BaseWindow, GradientLabel, GradientButton
from PyQt5.QtGui import QFont, QIcon, QPainter
from PyQt5.QtWidgets import QApplication, QVBoxLayout, QWidget, QLabel, QHBoxLayout
from PyQt5.QtCore import Qt
from data_manager import DataManager

class TestWindow(BaseWindow):
    def __init__(self):
        super().__init__("HanSwipe | Mastering Chinese", 360, 640)
        self.data_manager = DataManager()
        self.current_word_index = 0
        self.word_ids = list(self.data_manager.words.keys())
        self.showing_answer = False
        
        self.setup_ui()
        self.load_current_word()
    
    def setup_ui(self):
        # Remove default title
        self.title_label.deleteLater()
        
        # Create custom title
        self.title_background = GradientLabel("Test Yourself", self)
        self.title_background.move(30, 30)
        self.title_background.setFont(QFont("Arial", 30, QFont.Bold))
        self.apply_shadow(self.title_background)
        
        # Create main content area
        self.content_widget = QWidget(self)
        self.content_widget.setGeometry(30, 120, 300, 300)
        self.content_widget.setStyleSheet("background: transparent")
        
        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Word display button
        self.word_button = GradientButton("", self.content_widget)
        self.word_button.setFixedSize(300, 200)
        self.word_button.setFont(QFont("Arial", 24, QFont.Bold))
        self.word_button.clicked.connect(self.toggle_answer)
        self.apply_shadow(self.word_button)
        
        # Info label
        self.info_label = QLabel("Click to reveal answer", self.content_widget)
        self.info_label.setAlignment(Qt.AlignCenter)
        self.info_label.setStyleSheet("color: white; font: 14px;")
        self.info_label.setFixedHeight(30)
        
        layout.addWidget(self.word_button)
        layout.addWidget(self.info_label)
        self.content_widget.setLayout(layout)
        
        # Navigation arrows
        self.nav_widget = QWidget(self)
        self.nav_widget.setGeometry(30, 450, 300, 60)
        self.nav_widget.setStyleSheet("background: transparent")
        
        nav_layout = QHBoxLayout()
        nav_layout.setContentsMargins(0, 0, 0, 0)
        nav_layout.setSpacing(20)
        
        # Left arrow button
        self.left_btn = GradientButton("❌", self.nav_widget)
        self.left_btn.setFixedSize(60, 60)
        self.left_btn.setFont(QFont("Arial", 20, QFont.Bold))
        self.left_btn.clicked.connect(self.previous_word)
        self.apply_shadow(self.left_btn)
        
        # Right arrow button
        self.right_btn = GradientButton("✅", self.nav_widget)
        self.right_btn.setFixedSize(60, 60)
        self.right_btn.setFont(QFont("Arial", 20, QFont.Bold))
        self.right_btn.clicked.connect(self.next_word)
        self.apply_shadow(self.right_btn)
        
        nav_layout.addWidget(self.left_btn)
        nav_layout.addStretch()
        nav_layout.addWidget(self.right_btn)
        self.nav_widget.setLayout(nav_layout)
    
    def load_current_word(self):
        """Load the current word based on index"""
        if not self.word_ids:
            self.word_button.setText("No words available")
            self.word_button.setEnabled(False)
            self.info_label.setText("Add words first in the main menu")
            self.left_btn.setEnabled(False)
            self.right_btn.setEnabled(False)
            return
        
        self.showing_answer = False
        word_id = self.word_ids[self.current_word_index]
        word_data = self.data_manager.words[word_id]
        
        self.word_button.setText(word_data['chinese'])
        self.info_label.setText("Click to reveal answer")
    
    def next_word(self):
        """Move to the next word"""
        if not self.word_ids:
            return
            
        self.current_word_index = (self.current_word_index + 1) % len(self.word_ids)
        self.load_current_word()
    
    def previous_word(self):
        """Move to the previous word"""
        if not self.word_ids:
            return
            
        self.current_word_index = (self.current_word_index - 1) % len(self.word_ids)
        self.load_current_word()
    
    def toggle_answer(self):
        """Toggle between showing question and answer"""
        if not self.word_ids:
            return
            
        word_id = self.word_ids[self.current_word_index]
        word_data = self.data_manager.words[word_id]
        
        if self.showing_answer:
            self.word_button.setText(word_data['chinese'])
            self.info_label.setText("Click to reveal answer")
        else:
            answer_text = f"{word_data['pinyin']}\n\n{word_data['english']}"
            self.word_button.setText(answer_text)
            self.info_label.setText("Click to hide answer")
        
        self.showing_answer = not self.showing_answer

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TestWindow()
    window.show()
    sys.exit(app.exec_())