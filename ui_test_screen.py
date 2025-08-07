import sys
import random
from PyQt5.QtWidgets import QApplication, QLabel, QHBoxLayout, QWidget
from PyQt5.QtGui import QFont, QPainter, QLinearGradient, QColor, QTransform
from PyQt5.QtCore import Qt, QPropertyAnimation, pyqtProperty, QRect
from base_ui import BaseWindow, GradientButton, GradientLabel
from data_manager import DataManager


class FlipCard(GradientButton):
    """A GradientButton subclass that can animate flip effect."""
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self._rotation = 0
        self._current_text = text
        self._back_text = ""
        self.flipped = False
        self.setFont(QFont("Arial", 24, QFont.Bold))

    def setBackText(self, text):
        self._back_text = text

    def flip(self):
        self.animation = QPropertyAnimation(self, b"rotation")
        self.animation.setDuration(400)
        self.animation.setStartValue(0)
        self.animation.setEndValue(180)
        self.animation.valueChanged.connect(self.update)
        self.animation.finished.connect(self.swapText)
        self.animation.start()

    def swapText(self):
        self.flipped = not self.flipped
        self._rotation = 0
        self.setText(self._back_text if self.flipped else self._current_text)
        self.update()

    def setText(self, text):
        if not self.flipped:
            self._current_text = text
        else:
            self._back_text = text
        super().setText(text)

    def getRotation(self):
        return self._rotation

    def setRotation(self, angle):
        self._rotation = angle
        self.update()

    rotation = pyqtProperty(int, fget=getRotation, fset=setRotation)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        transform = QTransform()

        # Rotate around the vertical center
        transform.translate(self.width() / 2, self.height() / 2)
        angle = self._rotation % 360
        if 90 < angle <= 270:
            transform.scale(-1, 1)
        transform.rotate(angle, Qt.YAxis)
        transform.translate(-self.width() / 2, -self.height() / 2)
        painter.setTransform(transform)

        # Paint background gradient
        gradient = QLinearGradient(0, 0, self.width(), self.height())
        gradient.setColorAt(0, QColor(138, 43, 226))
        gradient.setColorAt(1, QColor(0, 102, 255))
        painter.setBrush(gradient)
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(QRect(0, 0, self.width(), self.height()), 15, 15)

        # Paint text
        painter.resetTransform()
        super().paintEvent(event)


class FlashcardWindow(BaseWindow):
    def __init__(self):
        super().__init__("HanSwipe | Flashcards", 360, 640)
        self.data_manager = DataManager()
        self.word_ids = list(self.data_manager.words.keys())
        random.shuffle(self.word_ids)

        self.current_index = 0
        self.know_count = 0
        self.dont_know_count = 0

        self.setup_ui()
        self.load_word()

    def setup_ui(self):
        self.title_label.deleteLater()

        # Title
        self.custom_title = GradientLabel("Test Yourself", self)
        self.custom_title.move(30, 30)
        self.custom_title.setFont(QFont("Arial", 30, QFont.Bold))
        self.apply_shadow(self.custom_title)

        # Flashcard with flip effect
        self.flashcard = FlipCard("", self)
        self.flashcard.setGeometry(30, 120, 300, 220)
        self.flashcard.clicked.connect(self.flip_card)
        self.apply_shadow(self.flashcard)

        # Counter
        self.counter_label = QLabel("", self)
        self.counter_label.setFont(QFont("Arial", 12))
        self.counter_label.setStyleSheet("color: white; background: transparent;")
        self.counter_label.setGeometry(30, 360, 300, 30)
        self.counter_label.setAlignment(Qt.AlignCenter)

        # Buttons
        self.know_btn = GradientButton("✅ I know it", self)
        self.know_btn.setGeometry(30, 450, 140, 60)
        self.know_btn.setFont(QFont("Arial", 14, QFont.Bold))
        self.know_btn.clicked.connect(self.mark_known)
        self.apply_shadow(self.know_btn)

        self.dont_know_btn = GradientButton("❌ Don't know", self)
        self.dont_know_btn.setGeometry(190, 450, 140, 60)
        self.dont_know_btn.setFont(QFont("Arial", 14, QFont.Bold))
        self.dont_know_btn.clicked.connect(self.mark_unknown)
        self.apply_shadow(self.dont_know_btn)

        self.style_credits()

    def style_credits(self):
        self.credits.setStyleSheet("color: white; background: transparent;")
        self.credits.move((self.width() - self.credits.width()) // 2, self.height() - 40)

    def load_word(self):
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
        self.flashcard.flip()

    def mark_known(self):
        self.know_count += 1
        self.next_word()

    def mark_unknown(self):
        self.dont_know_count += 1
        self.next_word()

    def next_word(self):
        self.current_index += 1
        self.load_word()

    def paintEvent(self, event):
        """Background gradient like the main menu"""
        painter = QPainter(self)
        gradient = QLinearGradient(0, 0, self.width(), self.height())
        gradient.setColorAt(0, QColor(0, 102, 255))
        gradient.setColorAt(1, QColor(138, 43, 226))
        painter.fillRect(self.rect(), gradient)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FlashcardWindow()
    window.show()
    sys.exit(app.exec_())
