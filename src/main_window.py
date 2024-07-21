# src/main_window.py

from PyQt6.QtWidgets import QMainWindow
from .text_editor import TextEditor
from .menu_bar import MenuBar
from .theme_manager import ThemeManager

class WompPad(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('WompPad')
        self.setGeometry(100, 100, 800, 600)

        self.text_editor = TextEditor(self)
        self.setCentralWidget(self.text_editor)

        self.menu_bar = MenuBar(self)
        self.setMenuBar(self.menu_bar)

        self.theme_manager = ThemeManager(self)
        self.theme_manager.set_theme('dark')  # Set default theme