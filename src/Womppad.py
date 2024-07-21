#Womppad.py
#v0.01
#MVS
import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QTextEdit, QMenuBar, QMenu, QFileDialog, QMessageBox
from PyQt6.QtGui import QAction
from PyQt6.QtCore import QFile, QTextStream

class WompPad(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('WompPad')
        self.setGeometry(100, 100, 800, 600)

        # Create text edit widget
        self.text_edit = QTextEdit(self)
        self.setCentralWidget(self.text_edit)

        # Create menu bar
        self.create_menu_bar()

    def create_menu_bar(self):
        menubar = self.menuBar()

        # File menu
        file_menu = menubar.addMenu('File')

        # New file action
        new_file_action = QAction('New', self)
        new_file_action.setShortcut('Ctrl+N')
        new_file_action.triggered.connect(self.new_file)
        file_menu.addAction(new_file_action)

        # Open file action
        open_file_action = QAction('Open', self)
        open_file_action.setShortcut('Ctrl+O')
        open_file_action.triggered.connect(self.open_file)
        file_menu.addAction(open_file_action)

        # Save file action
        save_file_action = QAction('Save', self)
        save_file_action.setShortcut('Ctrl+S')
        save_file_action.triggered.connect(self.save_file)
        file_menu.addAction(save_file_action)

        # Exit action
        exit_action = QAction('Exit', self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # Themes menu
        themes_menu = menubar.addMenu('Themes')

        # Light theme action
        light_theme_action = QAction('Light Theme', self)
        light_theme_action.triggered.connect(lambda: self.set_theme('light'))
        themes_menu.addAction(light_theme_action)

        # Dark theme action
        dark_theme_action = QAction('Dark Theme', self)
        dark_theme_action.triggered.connect(lambda: self.set_theme('dark'))
        themes_menu.addAction(dark_theme_action)

        # Custom CSS action
        custom_css_action = QAction('Load Custom CSS', self)
        custom_css_action.triggered.connect(self.load_custom_css)
        themes_menu.addAction(custom_css_action)

    def set_theme(self, theme):
        if theme == 'light':
            self.setStyleSheet("""
                QMainWindow { background-color: #FFFFFF; }
                QTextEdit { background-color: #FFFFFF; color: #000000; }
                QMenuBar { background-color: #F0F0F0; }
                QMenuBar::item:selected { background-color: #D0D0D0; }
            """)
        elif theme == 'dark':
            self.setStyleSheet("""
                QMainWindow { background-color: #2B2B2B; }
                QTextEdit { background-color: #2B2B2B; color: #FFFFFF; }
                QMenuBar { background-color: #3C3F41; color: #FFFFFF; }
                QMenuBar::item:selected { background-color: #4B6EAF; }
            """)

    def load_custom_css(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Open CSS File", "", "CSS Files (*.css);;All Files (*)")
        if filename:
            file = QFile(filename)
            if file.open(QFile.ReadOnly | QFile.Text):
                stream = QTextStream(file)
                self.setStyleSheet(stream.readAll())
                file.close()
            else:
                QMessageBox.warning(self, "Error", "Unable to open the CSS file.")

    def new_file(self):
        self.text_edit.clear()

    def open_file(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Open File", "", "Text Files (*.txt);;All Files (*)")
        if filename:
            with open(filename, 'r') as file:
                self.text_edit.setText(file.read())

    def save_file(self):
        filename, _ = QFileDialog.getSaveFileName(self, "Save File", "", "Text Files (*.txt);;All Files (*)")
        if filename:
            with open(filename, 'w') as file:
                file.write(self.text_edit.toPlainText())
                
if __name__ == '__main__':
    app = QApplication(sys.argv)
    womppad = WompPad()
    womppad.show()
    sys.exit(app.exec())