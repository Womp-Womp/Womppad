# src/search_replace_dialog.py

from PyQt6.QtWidgets import (QDialog, QLabel, QLineEdit, QCheckBox, 
                             QPushButton, QVBoxLayout, QHBoxLayout)

class SearchReplaceDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Search and Replace")
        self.setGeometry(300, 300, 350, 200)

        layout = QVBoxLayout()

        # Search
        search_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_button = QPushButton("Search")
        search_layout.addWidget(QLabel("Search for:"))
        search_layout.addWidget(self.search_input)
        search_layout.addWidget(self.search_button)
        layout.addLayout(search_layout)

        # Find Next button
        self.find_next_button = QPushButton("Find Next")
        layout.addWidget(self.find_next_button)

        # Replace
        replace_layout = QHBoxLayout()
        self.replace_input = QLineEdit()
        self.replace_button = QPushButton("Replace")
        replace_layout.addWidget(QLabel("Replace with:"))
        replace_layout.addWidget(self.replace_input)
        replace_layout.addWidget(self.replace_button)
        layout.addLayout(replace_layout)

        # Replace All button
        self.replace_all_button = QPushButton("Replace All")
        layout.addWidget(self.replace_all_button)

        # Options
        options_layout = QHBoxLayout()
        self.case_sensitive = QCheckBox("Case sensitive")
        self.whole_word = QCheckBox("Whole word")
        options_layout.addWidget(self.case_sensitive)
        options_layout.addWidget(self.whole_word)
        layout.addLayout(options_layout)

        self.setLayout(layout)