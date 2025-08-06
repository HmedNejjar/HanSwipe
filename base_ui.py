import sys
from PyQt5.QtWidgets import QMainWindow, QLabel, QGraphicsDropShadowEffect, QPushButton
from PyQt5.QtGui import QIcon, QFont, QPainter, QLinearGradient, QColor, QBrush
from PyQt5.QtCore import Qt, QRect, QPropertyAnimation, QEasingCurve, QTimer


class GradientLabel(QLabel):
    """A QLabel with a diagonal violet-to-blue gradient background and rounded corners."""
    def __init__(self, text="", parent=None):
        super().__init__(text, parent)
        self.setFixedSize(300, 70)
        self.setFont(QFont("Arial", 24, QFont.Bold))
        self.setAlignment(Qt.AlignCenter)
        self.setStyleSheet("color: white; background: transparent; border-radius: 15px;")

    def paintEvent(self, event):
        """Custom paint event to draw the gradient background."""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        gradient = QLinearGradient(0, 0, self.width(), self.height())
        gradient.setColorAt(0, QColor(138, 43, 226))  # Violet
        gradient.setColorAt(1, QColor(0, 102, 255))   # Blue

        painter.setBrush(QBrush(gradient))
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(QRect(0, 0, self.width(), self.height()), 15, 15)

        super().paintEvent(event)


class BaseWindow(QMainWindow):
    """Base window with gradient title, credits label, and dark background."""
    def __init__(self, title, width=1000, height=700):
        super().__init__()
        self.setWindowIcon(QIcon("app_logo.ico"))
        self.setWindowTitle(title)
        self.setFixedSize(360, 640)
        self.setGeometry(100, 100, width, height)

        self.setStyleSheet("background-color: #121212;")  # Dark mode

        # Center window
        self.center()

        # Add gradient title label
        self.title_label = GradientLabel("汉/A", self)
        self.title_label.move(50, 30)
        self.apply_shadow(self.title_label)

        # Add credits label at bottom center
        self.credits = QLabel("Made by Bakr Marhfoul", self)
        self.credits.setFont(QFont("Arial", 12))
        self.credits.setStyleSheet("color: white;")
        self.credits.adjustSize()
        self.credits.move((self.width() - self.credits.width()) // 2, self.height() - 40)
        self.credits.setFixedHeight(30)
        self.credits.raise_()

    def resizeEvent(self, event):
        """Keep credits label at bottom center on resize."""
        self.credits.move((self.width() - self.credits.width()) // 2, self.height() - 40)
        super().resizeEvent(event)

    def center(self):
        """Center the window on the screen."""
        screen_geometry = self.screen().availableGeometry()
        x = (screen_geometry.width() - self.width()) // 2
        y = (screen_geometry.height() - self.height()) // 2
        self.move(x, y)

    def apply_shadow(self, widget):
        """Apply a drop shadow effect to the given widget."""
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(25)
        shadow.setXOffset(0)
        shadow.setYOffset(4)
        shadow.setColor(QColor(0, 0, 0, 180))
        widget.setGraphicsEffect(shadow)
        
class GradientButton(QPushButton):
    """A QPushButton with a diagonal violet-to-blue gradient background and bounce animation."""
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setFixedSize(300, 60)
        self.setStyleSheet("""
            QPushButton {
                color: white;
                border-radius: 15px;
                background: transparent;
                padding: 10px;
                font: bold 16px;
            }
        """)

    def paintEvent(self, event):
        """Custom paint event to draw the gradient background."""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        gradient = QLinearGradient(0, 0, self.width(), self.height())
        gradient.setColorAt(0, QColor(138, 43, 226))  #Violet
        gradient.setColorAt(1, QColor(0, 102, 255))   #Blue

        painter.setBrush(QBrush(gradient))
        painter.setPen(Qt.NoPen)

        rect = QRect(0, 0, self.width(), self.height())
        painter.drawRoundedRect(rect, 15, 15)

        super().paintEvent(event)

    def mousePressEvent(self, event):
        """Trigger bounce animation on mouse press."""
        self.animateBounce()
        super().mousePressEvent(event)

    def animateBounce(self):
        """Animate the button with a bounce effect when pressed."""
        original_geometry = self.geometry()

        scale_factor = 1.05
        width_increase = int(self.width() * (scale_factor - 1))
        height_increase = int(self.height() * (scale_factor - 1))
        bigger_geometry = QRect(
            original_geometry.x() - width_increase // 2,
            original_geometry.y() - height_increase // 2,
            original_geometry.width() + width_increase,
            original_geometry.height() + height_increase
        )

        self._grow_anim = QPropertyAnimation(self, b"geometry")
        self._grow_anim.setDuration(100)
        self._grow_anim.setStartValue(original_geometry)
        self._grow_anim.setEndValue(bigger_geometry)
        self._grow_anim.setEasingCurve(QEasingCurve.OutQuad)
        self._grow_anim.start()

        def shrink_back():
            self._shrink_anim = QPropertyAnimation(self, b"geometry")
            self._shrink_anim.setDuration(100)
            self._shrink_anim.setStartValue(self.geometry())
            self._shrink_anim.setEndValue(original_geometry)
            self._shrink_anim.setEasingCurve(QEasingCurve.InQuad)
            self._shrink_anim.start()

        QTimer.singleShot(100, shrink_back)