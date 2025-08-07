import sys
from PyQt5.QtWidgets import QApplication
from ui_main_menu import MainWindow
from ui_add_word import AddWordWindow
from ui_test_screen import FlashcardWindow

class AppControl:
    """Controls the application flow and window switching."""
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.main_window = MainWindow()
        self.add_word = AddWordWindow()
        self.test_yourself = FlashcardWindow()
        
        # Connect button signals to window switching methods
        self.main_window.addWordButton.clicked.connect(self.show_add_word)
        self.add_word.done_button.clicked.connect(self.goto_menu)
        self.main_window.testYourselfButton.clicked.connect(self.test_yourself_window)
        
    def show_add_word(self):
        self.add_word.show()
        self.main_window.hide()
    
    def goto_menu(self):
        self.main_window.show()
        self.add_word.close()
    
    def test_yourself_window(self):
        self.test_yourself.show()
        self.main_window.close()
    
    def run(self):
        self.main_window.show()
        sys.exit(self.app.exec_())
        
if __name__ == "__main__":
    Controller = AppControl()
    Controller.run()