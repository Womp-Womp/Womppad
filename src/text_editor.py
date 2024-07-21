# src/text_editor.py
# src/text_editor.py

import re
from PyQt6.QtWidgets import QTextEdit, QMessageBox, QPushButton
from PyQt6.QtGui import QTextCursor
from PyQt6.QtGui import QTextDocument
from src.search_replace_dialog import SearchReplaceDialog

class TextEditor(QTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
        self.search_dialog = None
        self.last_search_position = 0
        self.current_match = None
        self.file_path = None  # Add this line

    def init_ui(self):
        self.setFontFamily("Courier")
        self.setFontPointSize(12)

    def log(self, message):
        print(f"DEBUG: {message}")

    def log_current_text(self):
        text = self.toPlainText()
        self.log(f"Current text (first 100 chars): {text[:100]}")

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

    def open_file(self):
        filename, _ = QFileDialog.getOpenFileName(self.parent, "Open File", "", "Text Files (*.txt);;All Files (*)")
        if filename:
            with open(filename, 'r') as file:
                # Assuming self.parent.text_editor has a method to get the current tab's text editor widget
                current_text_editor = self.parent.text_editor.get_current_tab_text_editor()
                current_text_editor.setText(file.read())

    def save_file(self):
        filename, _ = QFileDialog.getSaveFileName(self.parent, "Save File", "", "Text Files (*.txt);;All Files (*)")
        if filename:
            with open(filename, 'w') as file:
                # Assuming self.parent.text_editor has a method to get the current tab's text editor widget
                current_text_editor = self.parent.text_editor.get_current_tab_text_editor()
                file.write(current_text_editor.toPlainText())

    def show_search_replace_dialog(self):
        self.log("show_search_replace_dialog called")
        self.log_current_text()
        if not self.search_dialog:
            self.search_dialog = SearchReplaceDialog(self)
            self.log("SearchReplaceDialog created")
        
        # Disconnect any existing connections to avoid duplicates
        try:
            self.search_dialog.search_button.clicked.disconnect()
            self.search_dialog.replace_button.clicked.disconnect()
            self.search_dialog.replace_all_button.clicked.disconnect()
            self.search_dialog.find_next_button.clicked.disconnect()
        except (TypeError, AttributeError):
            pass  # No connections to disconnect or button doesn't exist

        self.search_dialog.search_button.clicked.connect(self.search_text)
        self.search_dialog.replace_button.clicked.connect(self.replace_text)
        self.search_dialog.replace_all_button.clicked.connect(self.replace_all_text)
        
        # Add Find Next button if it doesn't exist
        if not hasattr(self.search_dialog, 'find_next_button'):
            self.search_dialog.find_next_button = QPushButton("Find Next")
            self.search_dialog.layout().addWidget(self.search_dialog.find_next_button)
        self.search_dialog.find_next_button.clicked.connect(self.find_next)
        
        self.log("Button connections established")
        
        self.search_dialog.show()
        self.log("SearchReplaceDialog shown")

    def search_text(self):
        self.log("search_text called")
        self.log_current_text()
        search_string = self.search_dialog.search_input.text()
        self.log(f"Searching for: {search_string}")
        case_sensitive = self.search_dialog.case_sensitive.isChecked()
        whole_word = self.search_dialog.whole_word.isChecked()
        self.log(f"Case sensitive: {case_sensitive}, Whole word: {whole_word}")

        text = self.toPlainText()
        flags = re.IGNORECASE if not case_sensitive else 0
        pattern = r'\b' + re.escape(search_string) + r'\b' if whole_word else re.escape(search_string)

        # First, search from the last position to the end
        match = re.search(pattern, text[self.last_search_position:], flags)
        
        # If not found, wrap around to the beginning
        if not match and self.last_search_position > 0:
            self.log("Wrapping search to beginning of file")
            match = re.search(pattern, text[:self.last_search_position], flags)
            if match:
                start, end = match.span()
            else:
                start = end = 0  # Reset if still not found
        elif match:
            start = self.last_search_position + match.start()
            end = self.last_search_position + match.end()
        else:
            start = end = 0  # Reset if not found at all

        if start != end:
            self.last_search_position = end
            self.current_match = (start, end)
            self.log(f"Text found at position: {start}")
            cursor = self.textCursor()
            cursor.setPosition(start)
            cursor.setPosition(end, QTextCursor.MoveMode.KeepAnchor)
            self.setTextCursor(cursor)
            self.ensureCursorVisible()
        else:
            self.last_search_position = 0  # Reset for next search
            self.current_match = None
            self.log("Text not found")
            QMessageBox.information(self, "Search Result", "Text not found.")
        
        # Store the last search parameters
        self.last_search = (search_string, case_sensitive, whole_word)
    def find_next(self):
        if not hasattr(self, 'last_search'):
            self.search_text()
            return

        self.search_text()  # This will automatically continue from last_search_position

    def replace_text(self):
        self.log("replace_text called")
        if self.current_match:
            self.log("Text found, replacing")
            replace_string = self.search_dialog.replace_input.text()
            cursor = self.textCursor()
            cursor.setPosition(self.current_match[0])
            cursor.setPosition(self.current_match[1], QTextCursor.MoveMode.KeepAnchor)
            cursor.insertText(replace_string)
            self.last_search_position = cursor.position()
            self.current_match = None
            self.log("Text replaced")
            self.find_next()  # Automatically find the next match
        else:
            self.log("No text found to replace")
            QMessageBox.information(self, "Replace", "No text found to replace. Try searching first.")

    def replace_all_text(self):
        self.log("replace_all_text called")
        search_string = self.search_dialog.search_input.text()
        replace_string = self.search_dialog.replace_input.text()
        self.log(f"Replacing all '{search_string}' with '{replace_string}'")
        case_sensitive = self.search_dialog.case_sensitive.isChecked()
        whole_word = self.search_dialog.whole_word.isChecked()

        text = self.toPlainText()
        flags = re.IGNORECASE if not case_sensitive else 0
        pattern = r'\b' + re.escape(search_string) + r'\b' if whole_word else re.escape(search_string)

        new_text, count = re.subn(pattern, replace_string, text, flags=flags)
        
        if count > 0:
            self.setText(new_text)
            self.last_search_position = 0  # Reset search position after replace all
            self.current_match = None
            self.log(f"Replaced {count} occurrences")
            QMessageBox.information(self, "Replace All", f"Replaced {count} occurrences.")
        else:
            self.log("No occurrences found")
            QMessageBox.information(self, "Replace All", "No occurrences found.")