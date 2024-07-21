#Womppad.py
#v0.01
#MVS
import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QTextEdit, QMenuBar, QMenu, QFileDialog
from PyQt6.QtGui import QAction

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