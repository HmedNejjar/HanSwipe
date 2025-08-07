"""
Main menu window with options to add words or test yourself.
"""
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QFont, QLinearGradient, QColor, QPainter
from base_ui import BaseWindow, GradientLabel, GradientButton

class MainWindow(BaseWindow):
    """Main menu window with navigation buttons."""
    
    def __init__(self, data_manager):
        """
        Initialize the main window with custom title and buttons.
        
        Args:
            data_manager (DataManager): Shared data manager instance
        """
        super().__init__("HanSwipe | Mastering Chinese", 360, 640)
        self.data_manager = data_manager
        self.setup_ui()

    def setup_ui(self):
        """Setup all UI components including title and buttons."""
        self.title_label.deleteLater()
        self.create_custom_title()
        self.create_buttons()
        self.style_credits()

    def create_custom_title(self):
        """Create the HanSwipe title with gradient background."""
        self.title_background = GradientLabel("HanSwipe", self)
        self.title_background.move(30, 30)
        self.title_background.setFont(QFont("Arial", 30, QFont.Bold))
        self.apply_shadow(self.title_background)

    def create_buttons(self):
        """Create and position all navigation buttons."""
        # "Add Word" button
        self.addWordButton = GradientButton("Add Word", self)
        self.style_button(self.addWordButton, 30, 450)
        
        # "Test Yourself" button
        self.testYourselfButton = GradientButton("Test Yourself", self)
        self.style_button(self.testYourselfButton, 30, 350)

    def style_button(self, button, x, y):
        """
        Apply consistent styling to buttons.
        
        Args:
            button (QPushButton): Button to style
            x (int): X position
            y (int): Y position
        """
        button.setGeometry(x, y, 300, 60)
        button.setFont(QFont("Arial", 30, QFont.Bold))
        self.apply_shadow(button)

    def style_credits(self):
        """Adjust credits label styling and position."""
        self.credits.setStyleSheet("color: white; background: transparent;")
        self.credits.move((self.width() - self.credits.width()) // 2, self.height() - 40)

    def paintEvent(self, event):
        """
        Paint the gradient background.
        
        Args:
            event (QPaintEvent): Paint event
        """
        painter = QPainter(self)
        gradient = QLinearGradient(0, 0, self.width(), self.height())
        gradient.setColorAt(0, QColor(0, 102, 255))   # Blue
        gradient.setColorAt(1, QColor(138, 43, 226))  # Violet
        painter.fillRect(self.rect(), gradient)