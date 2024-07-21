# src/main.py
import os
os.environ['QT_QPA_PLATFORM'] = 'xcb'

import sys
from PyQt6.QtWidgets import QApplication
from src.main_window import WompPad

def main():
    app = QApplication(sys.argv)
    womppad = WompPad()
    womppad.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()