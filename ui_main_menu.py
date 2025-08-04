import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QDesktopWidget, QLabel, QWidget, QGraphicsDropShadowEffect
from PyQt5.QtGui import QIcon, QFont, QPainter, QLinearGradient, QColor, QPixmap, QBrush
from PyQt5.QtCore import Qt, QRect

class GradientLabel(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(300, 70)
        self.setStyleSheet("border-radius: 15px; background: transparent;")

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Gradient for red box
        gradient = QLinearGradient(0, 0, self.width(), self.height())
        gradient.setColorAt(0, QColor(138, 43, 226))   # Violet
        gradient.setColorAt(1, QColor(0, 102, 255))   # Blue

        brush = QBrush(gradient)
        painter.setBrush(brush)
        painter.setPen(Qt.NoPen)

        rect = QRect(0, 0, self.width(), self.height())
        painter.drawRoundedRect(rect, 15, 15)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("HanSwipe | Mastering Chinese")
        self.setWindowIcon(QIcon("app_logo.png"))
        self.setFixedSize(360, 640)
        self.center_window()

        # Gradient red box with rounded corners
        self.title_background = GradientLabel(self)
        self.title_background.move(30, 30)

        # Drop shadow effect
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(20)
        shadow.setOffset(0, 6)
        shadow.setColor(QColor(0, 0, 0, 150))
        self.title_background.setGraphicsEffect(shadow)

        # Title text
        self.MenuTitle = QLabel("HanSwipe", self.title_background)
        self.MenuTitle.setFont(QFont("Arial", 30, QFont.Bold))
        self.MenuTitle.setStyleSheet("color: white; background-color: transparent;")
        self.MenuTitle.setAlignment(Qt.AlignCenter)
        self.MenuTitle.setGeometry(0, 0, 300, 70)

    def center_window(self):
        frame_geometry = self.frameGeometry()
        screen_center = QDesktopWidget().availableGeometry().center()
        frame_geometry.moveCenter(screen_center)
        self.move(frame_geometry.topLeft())

    def paintEvent(self, event):
        painter = QPainter(self)
        gradient = QLinearGradient(0, 0, self.width(), self.height())
        gradient.setColorAt(0, QColor(0, 102, 255))   # Blue
        gradient.setColorAt(1, QColor(138, 43, 226))  # Violet
        painter.fillRect(self.rect(), gradient)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())