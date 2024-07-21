# src/main_window.py

from PyQt6.QtWidgets import QMainWindow
from src.text_editor import TextEditor
from src.menu_bar import MenuBar
from src.theme_manager import ThemeManager

class WompPad(QMainWindow):
    def __init__(self):
        super().__init__()
        self.text_editor = None
        self.menu_bar = None
        self.theme_manager = None
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('WompPad')
        self.setGeometry(100, 100, 800, 600)
        
        self.text_editor = TextEditor(self)
        self.setCentralWidget(self.text_editor)
        
        # Add some initial text
        self.text_editor.setText("Welcome to WompPad!\nThis is some initial text to search.")
        
        self.theme_manager = ThemeManager(self)
        
        self.menu_bar = MenuBar(self)
        self.setMenuBar(self.menu_bar)
        
        self.theme_manager.set_theme('dark')  # Set default theme