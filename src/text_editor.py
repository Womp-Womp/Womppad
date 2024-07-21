# src/text_editor.py

from PyQt6.QtWidgets import QTextEdit

class TextEditor(QTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        # Set default font
        self.setFontFamily("Courier")
        self.setFontPointSize(12)

    def set_theme(self, theme):
        if theme == 'light':
            self.setStyleSheet("""
                QTextEdit {
                    background-color: #FFFFFF;
                    color: #000000;
                }
            """)
        elif theme == 'dark':
            self.setStyleSheet("""
                QTextEdit {
                    background-color: #2B2B2B;
                    color: #FFFFFF;
                }
            """)