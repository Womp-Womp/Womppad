# src/menu_bar.py

from PyQt6.QtWidgets import QMenuBar, QMenu
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
        new_file_action.triggered.connect(self.parent.new_file)
        file_menu.addAction(new_file_action)

        new_tab_action = QAction('New Tab', self)
        new_tab_action.setShortcut('Ctrl+T')
        new_tab_action.triggered.connect(self.parent.new_file)
        file_menu.addAction(new_tab_action)

        open_file_action = QAction('Open', self)
        open_file_action.setShortcut('Ctrl+O')
        open_file_action.triggered.connect(self.parent.open_file)
        file_menu.addAction(open_file_action)

        save_file_action = QAction('Save', self)
        save_file_action.setShortcut('Ctrl+S')
        save_file_action.triggered.connect(self.parent.save_file)
        file_menu.addAction(save_file_action)

        save_as_action = QAction('Save As...', self)
        save_as_action.setShortcut('Ctrl+Shift+S')
        save_as_action.triggered.connect(self.parent.save_file_as)
        file_menu.addAction(save_as_action)

        #rename_tab_action = QAction('Rename Tab', self)
        #rename_tab_action.triggered.connect(self.parent.rename_tab)
        #file_menu.addAction(rename_tab_action)

        close_tab_action = QAction('Close Tab', self)
        close_tab_action.setShortcut('Ctrl+W')
        close_tab_action.triggered.connect(lambda: self.parent.close_tab(self.parent.tab_widget.currentIndex()))
        file_menu.addAction(close_tab_action)

        exit_action = QAction('Exit', self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.triggered.connect(self.parent.close)
        file_menu.addAction(exit_action)

    def create_edit_menu(self):
        edit_menu = QMenu("Edit", self)
        self.addMenu(edit_menu)

        undo_action = QAction('Undo', self)
        undo_action.setShortcut('Ctrl+Z')
        undo_action.triggered.connect(lambda: self.parent.tab_widget.currentWidget().undo())
        edit_menu.addAction(undo_action)

        redo_action = QAction('Redo', self)
        redo_action.setShortcut('Ctrl+Y')
        redo_action.triggered.connect(lambda: self.parent.tab_widget.currentWidget().redo())
        edit_menu.addAction(redo_action)

        cut_action = QAction('Cut', self)
        cut_action.setShortcut('Ctrl+X')
        cut_action.triggered.connect(lambda: self.parent.tab_widget.currentWidget().cut())
        edit_menu.addAction(cut_action)

        copy_action = QAction('Copy', self)
        copy_action.setShortcut('Ctrl+C')
        copy_action.triggered.connect(lambda: self.parent.tab_widget.currentWidget().copy())
        edit_menu.addAction(copy_action)

        paste_action = QAction('Paste', self)
        paste_action.setShortcut('Ctrl+V')
        paste_action.triggered.connect(lambda: self.parent.tab_widget.currentWidget().paste())
        edit_menu.addAction(paste_action)

        select_all_action = QAction('Select All', self)
        select_all_action.setShortcut('Ctrl+A')
        select_all_action.triggered.connect(lambda: self.parent.tab_widget.currentWidget().selectAll())
        edit_menu.addAction(select_all_action)

        search_replace_action = QAction('Search and Replace', self)
        search_replace_action.setShortcut('Ctrl+F')
        search_replace_action.triggered.connect(lambda: self.parent.tab_widget.currentWidget().show_search_replace_dialog())
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
    
    def update_editor_file_path(self, index):
        editor = self.tab_widget.widget(index)
        new_name = self.tab_widget.tabText(index)
        if hasattr(editor, 'file_path') and editor.file_path:
            editor.file_path = os.path.join(os.path.dirname(editor.file_path), new_name)
        else:
            editor.file_path = None