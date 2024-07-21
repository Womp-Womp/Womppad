# src/theme_manager.py
from PyQt6.QtWidgets import QFileDialog, QMessageBox
from PyQt6.QtCore import QFile, QTextStream

class ThemeManager:
    def __init__(self, parent):
        self.parent = parent

    def set_theme(self, theme):
        if theme == 'light':
            self.parent.setStyleSheet("""
                QMainWindow { background-color: #FFFFFF; }
                QMenuBar { background-color: #F0F0F0; }
                QMenuBar::item:selected { background-color: #D0D0D0; }
            """)
        elif theme == 'dark':
            self.parent.setStyleSheet("""
                QMainWindow { background-color: #2B2B2B; }
                QMenuBar { background-color: #3C3F41; color: #FFFFFF; }
                QMenuBar::item:selected { background-color: #4B6EAF; }
            """)
        
        self.parent.text_editor.set_theme(theme)

    def load_custom_css(self):
        filename, _ = QFileDialog.getOpenFileName(self.parent, "Open CSS File", "", "CSS Files (*.css);;All Files (*)")
        if filename:
            file = QFile(filename)
            if file.open(QFile.ReadOnly | QFile.Text):
                stream = QTextStream(file)
                self.parent.setStyleSheet(stream.readAll())
                file.close()
            else:
                QMessageBox.warning(self.parent, "Error", "Unable to open the CSS file.")