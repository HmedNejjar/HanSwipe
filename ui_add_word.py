import sys
from base_ui import GradientLabel, GradientButton, BaseWindow
from data_manager import DataManager
from PyQt5.QtGui import QFont, QPainter, QLinearGradient, QColor
from PyQt5.QtWidgets import QVBoxLayout, QWidget, QMessageBox, QApplication
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QLineEdit
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

class GradientInputField(QWidget):
    def __init__(self, placeholder, parent=None):
        super().__init__(parent)
        self.setFixedSize(300, 50)
        
        # Create QLineEdit inside the widget
        self.input = QLineEdit(self)
        self.input.setPlaceholderText(placeholder)
        self.input.setFont(QFont("Arial", 12))
        self.input.setStyleSheet("""
            QLineEdit {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(138, 43, 226, 200), 
                    stop:1 rgba(0, 102, 255, 200));
                border: none;
                border-radius: 15px;
                color: white;
                padding-left: 15px;
            }
            QLineEdit::placeholder {
                color: rgba(255,255,255,150);
            }
        """)
        self.input.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.input.setFixedSize(self.size())

    def resizeEvent(self, event):
        self.input.setFixedSize(self.size())
        super().resizeEvent(event)


class AddWordWindow(BaseWindow):
    def __init__(self):
        super().__init__("HanSwipe | Mastering Chinese", 360, 640)
        self.data_manager = DataManager()
    # Remove default title
        self.title_label.deleteLater()
        
        # Create custom title
        self.create_title()
        
        # Create input fields
        self.create_inputs()
        
        # Create Done button
        self.create_done_button()
        
        # Style credits
        self.style_credits()

    def create_title(self):
        self.title_label = GradientLabel("Add Word", self)
        self.title_label.move(30, 30)
        self.title_label.setFont(QFont("Arial", 30, QFont.Bold))
        self.apply_shadow(self.title_label)

    def create_inputs(self):
        # Create container widget
        self.input_container = QWidget(self)
        self.input_container.setGeometry(30, 120, 300, 300)
        self.input_container.setStyleSheet("background: transparent")
        
        # Create layout
        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Create input fields
        self.input_chinese = GradientInputField("Chinese (汉字)", self.input_container)
        self.apply_shadow(self.input_chinese)
        self.input_pinyin = GradientInputField("Pinyin", self.input_container)
        self.apply_shadow(self.input_pinyin)
        self.input_english = GradientInputField("English Meaning", self.input_container)
        self.apply_shadow(self.input_english)
        
        # Add to layout
        layout.addWidget(self.input_chinese)
        layout.addWidget(self.input_pinyin)
        layout.addWidget(self.input_english)
        
        self.input_container.setLayout(layout)

    def create_done_button(self):
        self.done_button = GradientButton("Done", self)
        self.done_button.setGeometry(30, 520, 300, 60)
        self.done_button.setFont(QFont("Arial", 20, QFont.Bold))
        self.apply_shadow(self.done_button)
        
        self.done_button.clicked.connect(self.save_word_data, )

    def save_word_data(self):
        """Collect input data and save to dictionary"""
        chinese = self.input_chinese.input.text().strip()
        pinyin = self.input_pinyin.input.text().strip()
        english = self.input_english.input.text().strip()

        if not chinese or not pinyin or not english:
            QMessageBox.warning(self, "Missing Information", 
                               "Please fill in all fields before saving.")
            return

        try:
            # Save the word using data manager
            word_id = self.data_manager.add_word(chinese, pinyin, english)
            
            # Show success message
            QMessageBox.information(self, "Success", 
                                  f"Word '{chinese}' saved successfully!")
            
            # Clear the input fields
            self.input_chinese.input.clear()
            self.input_pinyin.input.clear()
            self.input_english.input.clear()
            self.close()
            
            # Focus back to Chinese input
            self.input_chinese.input.setFocus()
            
        except Exception as e:
            QMessageBox.critical(self, "Error", 
                               f"An error occurred while saving:\n{str(e)}")
    def style_credits(self):
        self.credits.setStyleSheet("color: white; background: transparent;")
        self.credits.move((self.width() - self.credits.width()) // 2, self.height() - 40)

    def paintEvent(self, event):
        painter = QPainter(self)
        gradient = QLinearGradient(0, 0, self.width(), self.height())
        gradient.setColorAt(0, QColor(0, 102, 255))   # Blue
        gradient.setColorAt(1, QColor(138, 43, 226))  # Violet
        painter.fillRect(self.rect(), gradient)
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AddWordWindow()
    window.show()
    sys.exit(app.exec_())