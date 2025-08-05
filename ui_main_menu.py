import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QDesktopWidget, QLabel, QPushButton, QGraphicsDropShadowEffect
from PyQt5.QtGui import QIcon, QFont, QPainter, QLinearGradient, QColor, QPixmap, QBrush
from PyQt5.QtCore import Qt, QPropertyAnimation, QEasingCurve, QTimer, QRect

class GradientLabel(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(300, 70)
        self.setStyleSheet("border-radius: 15px; background: transparent;")

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Gradient for title box
        gradient = QLinearGradient(0, 0, self.width(), self.height())
        gradient.setColorAt(0, QColor(138, 43, 226))   # Violet
        gradient.setColorAt(1, QColor(0, 102, 255))   # Blue

        brush = QBrush(gradient)
        painter.setBrush(brush)
        painter.setPen(Qt.NoPen)

        rect = QRect(0, 0, self.width(), self.height())
        painter.drawRoundedRect(rect, 15, 15)

class GradientButton(QPushButton):
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
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Gradient for button box
        gradient = QLinearGradient(0, 0, self.width(), self.height())
        gradient.setColorAt(0, QColor(138, 43, 226))   # Violet
        gradient.setColorAt(1, QColor(0, 102, 255))   # Blue

        brush = QBrush(gradient)
        painter.setBrush(brush)
        painter.setPen(Qt.NoPen)

        rect = QRect(0, 0, self.width(), self.height())
        painter.drawRoundedRect(rect, 15, 15)
        
        super().paintEvent(event)
    
    def mousePressEvent(self, event):
        self.animateBounce()
        super().mousePressEvent(event)

    def animateBounce(self):
        '''Animates the button with a bounce effect when pressed'''
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

        # Animate grow
        self._grow_anim = QPropertyAnimation(self, b"geometry")
        self._grow_anim.setDuration(100)
        self._grow_anim.setStartValue(original_geometry)
        self._grow_anim.setEndValue(bigger_geometry)
        self._grow_anim.setEasingCurve(QEasingCurve.OutQuad)
        self._grow_anim.start()

        # Animate shrink after a short delay
        def shrink_back():
            self._shrink_anim = QPropertyAnimation(self, b"geometry")
            self._shrink_anim.setDuration(100)
            self._shrink_anim.setStartValue(self.geometry())
            self._shrink_anim.setEndValue(original_geometry)
            self._shrink_anim.setEasingCurve(QEasingCurve.InQuad)
            self._shrink_anim.start()

        QTimer.singleShot(100, shrink_back)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("HanSwipe | Mastering Chinese")
        self.setWindowIcon(QIcon("app_logo.png"))
        self.setFixedSize(360, 640)
        self.center_window()

        # Gradient blue box with rounded corners
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
        
        #"Add Word" Button
        self.addWordButton = GradientButton("Add Word", self)
        self.ButtonDesign(self.addWordButton, 30, 450)
        
        #"Test Yourself" Button
        self.TestYourselfButton = GradientButton("Test Yourself", self)
        self.ButtonDesign(self.TestYourselfButton, 30, 350)
        
        self.credits = QLabel("Made by Bakr Marhfoul", self)
        self.credits.setFont(QFont("Arial", 12))
        self.credits.setStyleSheet("color: white; background: transparent;")
        
        # Get width and height of label text
        self.credits.adjustSize()
        label_width = self.credits.width()
        label_height = self.credits.height()
        
        # Calculate x to center, y to stick to bottom (with padding)
        window_width = self.width()
        window_height = self.height()
        x = (window_width - label_width) // 2
        y = window_height - label_height - 10  # 10px padding from bottom
        
        self.credits.move(x, y)

    def center_window(self):
        '''Centers the main window on the screen'''
        frame_geometry = self.frameGeometry()
        screen_center = QDesktopWidget().availableGeometry().center()
        frame_geometry.moveCenter(screen_center)
        self.move(frame_geometry.topLeft())

    def paintEvent(self, event):
        '''Paints the main window background with a diagonal blue-violet gradient.'''
        painter = QPainter(self)
        gradient = QLinearGradient(0, 0, self.width(), self.height())
        gradient.setColorAt(0, QColor(0, 102, 255))   # Blue
        gradient.setColorAt(1, QColor(138, 43, 226))  # Violet
        painter.fillRect(self.rect(), gradient)
        
    def ButtonDesign(self, button, pos_x, pos_y):
        '''Applies geometry, font, style, and shadow to a button.'''
        button.setGeometry(pos_x, pos_y, 300, 70)
        button.setFont(QFont("Arial", 20, QFont.Bold))
        button.setStyleSheet("color: white; background-color: transparent;")
        
        button_shadow = QGraphicsDropShadowEffect(self)
        button_shadow.setBlurRadius(20)
        button_shadow.setOffset(0, 6)
        button_shadow.setColor(QColor(0, 0, 0, 150))
        button.setGraphicsEffect(button_shadow)
        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())