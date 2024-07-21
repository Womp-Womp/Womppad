# src/menu_bar.py

from PyQt6.QtWidgets import QMenuBar, QMenu, QFileDialog
from PyQt6.QtGui import QAction

class MenuBar(QMenuBar):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.init_ui()

    def init_ui(self):
        self.create_file_menu()
        self.create_edit_menu()
        self.create_themes_menu()

    def create_file_menu(self):
        file_menu = QMenu("File", self)
        self.addMenu(file_menu)

        new_file_action = QAction('New', self)
        new_file_action.setShortcut('Ctrl+N')
        new_file_action.triggered.connect(self.parent.text_editor.clear)
        file_menu.addAction(new_file_action)

        open_file_action = QAction('Open', self)
        open_file_action.setShortcut('Ctrl+O')
        open_file_action.triggered.connect(self.open_file)
        file_menu.addAction(open_file_action)

        save_file_action = QAction('Save', self)
        save_file_action.setShortcut('Ctrl+S')
        save_file_action.triggered.connect(self.save_file)
        file_menu.addAction(save_file_action)

        exit_action = QAction('Exit', self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.triggered.connect(self.parent.close)
        file_menu.addAction(exit_action)

    def create_edit_menu(self):
        edit_menu = QMenu("Edit", self)
        self.addMenu(edit_menu)

        search_replace_action = QAction('Search and Replace', self)
        search_replace_action.setShortcut('Ctrl+F')
        search_replace_action.triggered.connect(self.show_search_replace_dialog)
        edit_menu.addAction(search_replace_action)

    def create_themes_menu(self):
        themes_menu = QMenu("Themes", self)
        self.addMenu(themes_menu)

        light_theme_action = QAction('Light Theme', self)
        light_theme_action.triggered.connect(lambda: self.parent.theme_manager.set_theme('light'))
        themes_menu.addAction(light_theme_action)

        dark_theme_action = QAction('Dark Theme', self)
        dark_theme_action.triggered.connect(lambda: self.parent.theme_manager.set_theme('dark'))
        themes_menu.addAction(dark_theme_action)

        custom_css_action = QAction('Load Custom CSS', self)
        custom_css_action.triggered.connect(self.parent.theme_manager.load_custom_css)
        themes_menu.addAction(custom_css_action)

    def open_file(self):
        filename, _ = QFileDialog.getOpenFileName(self.parent, "Open File", "", "Text Files (*.txt);;All Files (*)")
        if filename:
            with open(filename, 'r') as file:
                self.parent.text_editor.setText(file.read())

    def save_file(self):
        filename, _ = QFileDialog.getSaveFileName(self.parent, "Save File", "", "Text Files (*.txt);;All Files (*)")
        if filename:
            with open(filename, 'w') as file:
                file.write(self.parent.text_editor.toPlainText())

    def show_search_replace_dialog(self):
        if hasattr(self.parent, 'text_editor'):
            self.parent.text_editor.show_search_replace_dialog()