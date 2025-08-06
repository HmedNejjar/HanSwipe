import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QFont, QLinearGradient, QColor, QPainter
from base_ui import BaseWindow, GradientLabel, GradientButton

class MainWindow(BaseWindow):
    def __init__(self):
        # Initialize with custom title and mobile-friendly size
        super().__init__("HanSwipe | Mastering Chinese", 360, 640)
        
        # Customize the UI
        self.setup_ui()

    def setup_ui(self):
        """Setup all UI components"""
        # Remove default title and create custom one
        self.title_label.deleteLater()
        self.create_custom_title()
        
        # Create buttons
        self.create_buttons()
        
        # Adjust credits styling to match design
        self.style_credits()

    def create_custom_title(self):
        """Create the HanSwipe title with gradient background"""
        self.title_background = GradientLabel("HanSwipe", self)
        self.title_background.move(30, 30)
        self.title_background.setFont(QFont("Arial", 30, QFont.Bold))
        self.apply_shadow(self.title_background)

    def create_buttons(self):
        """Create and position all buttons"""
        # "Add Word" button
        self.addWordButton = GradientButton("Add Word", self)
        self.style_button(self.addWordButton, 30, 450)
        
        # "Test Yourself" button
        self.testYourselfButton = GradientButton("Test Yourself", self)
        self.style_button(self.testYourselfButton, 30, 350)

    def style_button(self, button, x, y):
        """Apply consistent styling to buttons"""
        button.setGeometry(x, y, 300, 60)
        button.setFont(QFont("Arial", 30, QFont.Bold))
        self.apply_shadow(button)

    def style_credits(self):
        """Adjust credits label styling"""
        self.credits.setStyleSheet("color: white; background: transparent;")
        self.credits.move((self.width() - self.credits.width()) // 2, self.height() - 40)

    def paintEvent(self, event):
        """Override to maintain the gradient background"""
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