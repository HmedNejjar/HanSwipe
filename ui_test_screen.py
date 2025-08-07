"""
Flashcard testing window with flip animation and progress tracking.
"""
import random
from PyQt5.QtWidgets import QLabel, QHBoxLayout, QVBoxLayout, QWidget
from PyQt5.QtGui import QFont, QPainter, QLinearGradient, QColor, QTransform
from PyQt5.QtCore import Qt, QPropertyAnimation, pyqtProperty, QRect
from base_ui import BaseWindow, GradientButton, GradientLabel
from data_manager import DataManager

class FlipCard(GradientButton):
    """Custom button with flip animation showing Chinese/Pinyin/English."""
    
    def __init__(self, text, parent=None):
        """
        Initialize the flip card with front text.
        
        Args:
            text (str): Initial text to display
            parent (QWidget): Parent widget
        """
        super().__init__(text, parent)
        self._rotation = 0
        self._current_text = text
        self._back_text = ""
        self.flipped = False
        self.setFont(QFont("Arial", 24, QFont.Bold))
        self.setStyleSheet("background: transparent; color: white")

    def setBackText(self, text):
        """
        Set the text to show when flipped.
        
        Args:
            text (str): Back side text
        """
        self._back_text = text

    def flip(self):
        """Animate the flip between front and back."""
        self.animation = QPropertyAnimation(self, b"rotation")
        self.animation.setDuration(400)
        self.animation.setStartValue(0)
        self.animation.setEndValue(180)
        self.animation.valueChanged.connect(self.update)
        self.animation.finished.connect(self.swapText)
        self.animation.start()

    def swapText(self):
        """Swap between front and back text after flip animation completes."""
        self.flipped = not self.flipped
        self._rotation = 0
        self.setText(self._back_text if self.flipped else self._current_text)
        self.update()

    def setText(self, text):
        """Set text while maintaining current flip state."""
        if not self.flipped:
            self._current_text = text
        else:
            self._back_text = text
        super().setText(text)

    def getRotation(self):
        """Get current rotation angle."""
        return self._rotation

    def setRotation(self, angle):
        """Set rotation angle for animation."""
        self._rotation = angle
        self.update()

    rotation = pyqtProperty(int, fget=getRotation, fset=setRotation)

    def paintEvent(self, event):
        """Custom painting with rotation transformation."""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        transform = QTransform()

        transform.translate(self.width() / 2, self.height() / 2)
        angle = self._rotation % 360
        if 90 < angle <= 270:
            transform.scale(-1, 1)
        transform.rotate(angle, Qt.YAxis)
        transform.translate(-self.width() / 2, -self.height() / 2)
        painter.setTransform(transform)

        gradient = QLinearGradient(0, 0, self.width(), self.height())
        gradient.setColorAt(0, QColor(138, 43, 226))
        gradient.setColorAt(1, QColor(0, 102, 255))
        painter.setBrush(gradient)
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(QRect(0, 0, self.width(), self.height()), 15, 15)

        painter.resetTransform()
        super().paintEvent(event)


class FlashcardWindow(BaseWindow):
    """Window for testing vocabulary knowledge with flashcards."""
    
    def __init__(self, data_manager):
        """
        Initialize the flashcard window.
        
        Args:
            data_manager (DataManager): Shared data manager instance
        """
        super().__init__("HanSwipe | Flashcards", 360, 640)
        self.data_manager = data_manager
        self.word_ids = []
        self.current_index = 0
        self.know_count = 0
        self.dont_know_count = 0

        self.setup_ui()
        self.refresh_words()

    def setup_ui(self):
        """Setup all UI components including flashcard and buttons."""
        self.title_label.deleteLater()

        # Title
        self.custom_title = GradientLabel("Test Yourself", self)
        self.custom_title.setFont(QFont("Arial", 30, QFont.Bold))
        self.custom_title.move(30, 30)
        self.apply_shadow(self.custom_title)

        # Main widget to contain layout
        central = QWidget(self)
        central.setGeometry(30, 100, 300, 460)
        central.setStyleSheet("background: transparent;")

        # Main vertical layout
        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addStretch()

        # Flip card
        self.flashcard = FlipCard("", self)
        self.flashcard.setFixedSize(300, 240)
        self.flashcard.clicked.connect(self.flip_card)
        self.apply_shadow(self.flashcard)
        layout.addWidget(self.flashcard, alignment=Qt.AlignCenter)

        # Counter
        self.counter_label = QLabel("", self)
        self.counter_label.setFont(QFont("Arial", 12))
        self.counter_label.setStyleSheet("color: white; background: transparent;")
        self.counter_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.counter_label)

        # Buttons
        btn_row = QHBoxLayout()
        btn_row.setSpacing(20)

        self.know_btn = GradientButton("✅", self)
        self.know_btn.setFixedSize(60, 60)
        self.know_btn.setFont(QFont("Arial", 18, QFont.Bold))
        self.know_btn.clicked.connect(self.mark_known)
        self.apply_shadow(self.know_btn)
        self.know_btn.setStyleSheet("""
            QPushButton {
                background: transparent;
                border: none;
                color: white;
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(138, 43, 226, 150), 
                    stop:1 rgba(0, 102, 255, 150));
            }
        """)

        self.dont_know_btn = GradientButton("❌", self)
        self.dont_know_btn.setFixedSize(60, 60)
        self.dont_know_btn.setFont(QFont("Arial", 18, QFont.Bold))
        self.dont_know_btn.clicked.connect(self.mark_unknown)
        self.apply_shadow(self.dont_know_btn)
        self.dont_know_btn.setStyleSheet(self.know_btn.styleSheet())

        btn_row.addStretch()
        btn_row.addWidget(self.know_btn)
        btn_row.addWidget(self.dont_know_btn)
        btn_row.addStretch()

        layout.addLayout(btn_row)
        layout.addStretch()

        central.setLayout(layout)
        self.style_credits()

    def style_credits(self):
        """Style the credits label at the bottom."""
        self.credits.setStyleSheet("color: white; background: transparent;")
        self.credits.move((self.width() - self.credits.width()) // 2, self.height() - 40)

    def refresh_words(self):
        """Refresh the word list from data manager and reset counters."""
        self.word_ids = list(self.data_manager.words.keys())
        random.shuffle(self.word_ids)
        self.current_index = 0
        self.know_count = 0
        self.dont_know_count = 0
        self.load_word()

    def load_word(self):
        """Load current word or show completion message if done."""
        if not self.word_ids:
            self.flashcard.setText("No words available")
            self.flashcard.setBackText("")
            self.know_btn.setEnabled(False)
            self.dont_know_btn.setEnabled(False)
            self.counter_label.setText("Add words from the main menu")
            return

        if self.current_index >= len(self.word_ids):
            self.flashcard.setText("🎉 Done!")
            self.flashcard.setBackText("")
            self.know_btn.setEnabled(False)
            self.dont_know_btn.setEnabled(False)
            self.counter_label.setText(f"Known: {self.know_count} / {self.know_count + self.dont_know_count}")
            return

        word_id = self.word_ids[self.current_index]
        word = self.data_manager.words[word_id]
        self.flashcard.setText(word["chinese"])
        self.flashcard.setBackText(f"{word['pinyin']}\n\n{word['english']}")
        self.flashcard.flipped = False
        self.counter_label.setText(f"Known: {self.know_count}   |   Don't know: {self.dont_know_count}")

    def flip_card(self):
        """Flip the current flashcard."""
        self.flashcard.flip()

    def mark_known(self):
        """Mark current word as known and advance to next word."""
        self.know_count += 1
        self.next_word()

    def mark_unknown(self):
        """Mark current word as unknown and advance to next word."""
        self.dont_know_count += 1
        self.next_word()

    def next_word(self):
        """Advance to the next word in the list."""
        self.current_index += 1
        self.load_word()

    def paintEvent(self, event):
        """Paint the gradient background."""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        gradient = QLinearGradient(0, 0, self.width(), self.height())
        gradient.setColorAt(0, QColor(0, 102, 255))
        gradient.setColorAt(1, QColor(138, 43, 226))
        painter.fillRect(self.rect(), gradient)
        painter.end()