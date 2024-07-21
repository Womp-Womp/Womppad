# src/main_window.py

from PyQt6.QtWidgets import QMainWindow, QTabWidget, QFileDialog, QMessageBox, QTabBar, QStylePainter, QStyleOptionTab, QStyle
from PyQt6.QtGui import QCloseEvent, QMouseEvent, QPainter
from PyQt6.QtCore import Qt, QRect, QPoint
from src.text_editor import TextEditor
from src.menu_bar import MenuBar
from src.theme_manager import ThemeManager
import os

class InlineEditTabBar(QTabBar):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.setElideMode(Qt.TextElideMode.ElideRight)
        self.setExpanding(False)
        self.setMovable(True)
        self.setTabsClosable(True)
        self.editing_index = -1
        self.editing_text = ""

    def mouseDoubleClickEvent(self, event: QMouseEvent):
        index = self.tabAt(event.pos())
        if index != -1:
            self.editing_index = index
            self.editing_text = self.tabText(index)
            self.update()

    def mousePressEvent(self, event: QMouseEvent):
        if self.editing_index != -1:
            self.editing_index = -1
            self.update()
        super().mousePressEvent(event)

    def keyPressEvent(self, event):
        if self.editing_index != -1:
            if event.key() == Qt.Key.Key_Escape:
                self.editing_index = -1
            elif event.key() == Qt.Key.Key_Return or event.key() == Qt.Key.Key_Enter:
                self.setTabText(self.editing_index, self.editing_text)
                self.parentWidget().parentWidget().update_editor_file_path(self.editing_index)
                self.editing_index = -1
            elif event.key() == Qt.Key.Key_Backspace:
                self.editing_text = self.editing_text[:-1]
            else:
                self.editing_text += event.text()
            self.update()
        else:
            super().keyPressEvent(event)

    def paintEvent(self, event):
        painter = QStylePainter(self)
        option = QStyleOptionTab()

        for i in range(self.count()):
            self.initStyleOption(option, i)
            if i == self.editing_index:
                # Draw the tab without text
                option.text = ""
                painter.drawControl(QStyle.ControlElement.CE_TabBarTab, option)
                
                # Draw the editing text
                painter.setPen(option.palette.text().color())
                rect = self.tabRect(i)
                painter.drawText(rect, Qt.AlignmentFlag.AlignCenter, self.editing_text)
            else:
                # For non-editing tabs, draw normally
                painter.drawControl(QStyle.ControlElement.CE_TabBarTab, option)

class TabWidget(QTabWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setTabBar(InlineEditTabBar(self))

class WompPad(QMainWindow):
    def __init__(self):
        super().__init__()
        self.tab_widget = None
        self.theme_manager = None
        self.menu_bar = None
        self.current_theme = 'dark'  # Default theme
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('WompPad')
        self.setGeometry(100, 100, 800, 600)
        
        self.tab_widget = TabWidget(self)
        self.tab_widget.tabCloseRequested.connect(self.close_tab)
        self.setCentralWidget(self.tab_widget)
        
        self.theme_manager = ThemeManager(self)
        
        self.menu_bar = MenuBar(self)
        self.setMenuBar(self.menu_bar)
        
        self.new_file()  # Open a new file by default

    def new_file(self):
        new_editor = TextEditor(self)
        self.theme_manager.set_theme(self.current_theme, new_editor)
        index = self.tab_widget.addTab(new_editor, "Untitled")
        self.tab_widget.setCurrentIndex(index)

    def open_file(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Open File", "", "Text Files (*.txt);;All Files (*)")
        if filename:
            for i in range(self.tab_widget.count()):
                if self.tab_widget.tabText(i) == os.path.basename(filename):
                    self.tab_widget.setCurrentIndex(i)
                    return
            
            new_editor = TextEditor(self)
            self.theme_manager.set_theme(self.current_theme, new_editor)
            with open(filename, 'r') as file:
                new_editor.setText(file.read())
            new_editor.file_path = filename
            index = self.tab_widget.addTab(new_editor, os.path.basename(filename))
            self.tab_widget.setCurrentIndex(index)

    def save_file(self):
        current_editor = self.tab_widget.currentWidget()
        if current_editor:
            if hasattr(current_editor, 'file_path') and current_editor.file_path:
                with open(current_editor.file_path, 'w') as file:
                    file.write(current_editor.toPlainText())
            else:
                self.save_file_as()

    def save_file_as(self):
        current_editor = self.tab_widget.currentWidget()
        if current_editor:
            filename, _ = QFileDialog.getSaveFileName(self, "Save File", "", "Text Files (*.txt);;All Files (*)")
            if filename:
                with open(filename, 'w') as file:
                    file.write(current_editor.toPlainText())
                current_editor.file_path = filename
                self.tab_widget.setTabText(self.tab_widget.currentIndex(), os.path.basename(filename))

    def close_tab(self, index):
        if self.tab_widget.count() > 1:
            self.tab_widget.removeTab(index)
        else:
            self.close()

    def set_theme(self, theme):
        self.current_theme = theme
        for i in range(self.tab_widget.count()):
            editor = self.tab_widget.widget(i)
            self.theme_manager.set_theme(theme, editor)

    def update_editor_file_path(self, index):
        editor = self.tab_widget.widget(index)
        if editor is not None:
            new_name = self.tab_widget.tabText(index)
            if hasattr(editor, 'file_path') and editor.file_path:
                editor.file_path = os.path.join(os.path.dirname(editor.file_path), new_name)
            else:
                editor.file_path = None


    def closeEvent(self, event: QCloseEvent):
        for i in range(self.tab_widget.count()):
            editor = self.tab_widget.widget(i)
            if editor.document().isModified():
                reply = QMessageBox.question(self, "Save Changes",
                                             f"Do you want to save changes to {self.tab_widget.tabText(i)}?",
                                             QMessageBox.StandardButton.Save |
                                             QMessageBox.StandardButton.Discard |
                                             QMessageBox.StandardButton.Cancel)
                if reply == QMessageBox.StandardButton.Save:
                    self.tab_widget.setCurrentIndex(i)
                    self.save_file()
                elif reply == QMessageBox.StandardButton.Cancel:
                    event.ignore()
                    return
        event.accept()