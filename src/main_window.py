# src/main_window.py

from PyQt6.QtWidgets import QMainWindow
from src.text_editor import TextEditor
from src.menu_bar import MenuBar
from src.theme_manager import ThemeManager
from PyQt6.QtWidgets import QMainWindow, QTabWidget
from src.text_editor import TextEditor
from src.menu_bar import MenuBar
from src.theme_manager import ThemeManager

class WompPad(QMainWindow):
    def __init__(self):
        super().__init__()
        self.text_editor = None
        self.menu_bar = None
        self.theme_manager = None
        self.tab_widget = None
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('WompPad')
        self.setGeometry(100, 100, 800, 600)
        
        self.tab_widget = QTabWidget(self)
        self.setCentralWidget(self.tab_widget)
        
        self.text_editor = TextEditor(self)
        self.tab_widget.addTab(self.text_editor, "Untitled")
        
        self.theme_manager = ThemeManager(self)
        
        self.menu_bar = MenuBar(self)
        self.setMenuBar(self.menu_bar)
        
        self.theme_manager.set_theme('dark')  # Set default theme
    
    def new_file(self):
        new_editor = TextEditor()
        self.tab_widget.addTab(new_editor, "Untitled")
        self.tab_widget.setCurrentWidget(new_editor)

    def open_file(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Open File", "", "Text Files (*.txt);;All Files (*)")
        if filename:
            new_editor = TextEditor()
            with open(filename, 'r') as file:
                new_editor.setText(file.read())
            self.tab_widget.addTab(new_editor, filename)
            self.tab_widget.setCurrentWidget(new_editor)
