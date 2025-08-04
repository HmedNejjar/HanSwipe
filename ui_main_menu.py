import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QDesktopWidget
from PyQt5.QtGui import QIcon

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("HanSwipe | Mastering Chinese")
        self.setWindowIcon(QIcon("app_logo.png"))
        self.setFixedSize(360, 640)
        self.center_window()

    def center_window(self):
        frame_geometry = self.frameGeometry()  # Get the geometry of the main window
        screen_center = QDesktopWidget().availableGeometry().center()  # Find the center point of the available screen
        frame_geometry.moveCenter(screen_center)   # Move the window's geometry to the center
        self.move(frame_geometry.topLeft())   # Move the top-left of the window to the computed top-left position
