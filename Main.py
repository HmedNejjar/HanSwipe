"""
Main application controller that manages window switching and data sharing.
Creates a single DataManager instance shared across all windows.
"""

import sys
from PyQt5.QtWidgets import QApplication
from ui_main_menu import MainWindow
from ui_add_word import AddWordWindow
from ui_test_screen import FlashcardWindow
from data_manager import DataManager

class AppControl:
    """Main application controller that manages window switching and data sharing."""
    
    def __init__(self):
        """
        Initialize the application controller.
        Creates QApplication, DataManager, and all windows.
        Connects button signals to window switching methods.
        """
        self.app = QApplication(sys.argv)
        self.data_manager = DataManager()  # Single DataManager instance for all windows
        
        # Initialize all windows with the shared DataManager
        self.main_window = MainWindow(self.data_manager)
        self.add_word = AddWordWindow(self.data_manager)
        self.test_yourself = FlashcardWindow(self.data_manager)
        
        # Connect button signals to window switching methods
        self.main_window.addWordButton.clicked.connect(self.show_add_word)
        self.add_word.done_button.clicked.connect(self.goto_menu)
        self.main_window.testYourselfButton.clicked.connect(self.test_yourself_window)
        
    def show_add_word(self):
        """Show the Add Word window and hide the main menu."""
        self.add_word.show()
        self.main_window.hide()
    
    def goto_menu(self):
        """Return to main menu from Add Word window."""
        self.main_window.show()
        self.add_word.close()
    
    def test_yourself_window(self):
        """Show the Test Yourself window with refreshed word list."""
        self.test_yourself.refresh_words()  # Refresh words before showing
        self.test_yourself.show()
        self.main_window.close()
    
    def run(self):
        """Start the application and enter the main event loop."""
        self.main_window.show()
        sys.exit(self.app.exec_())
        
if __name__ == "__main__":
    controller = AppControl()
    controller.run()