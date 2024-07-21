import sys
from PyQt6.QtWidgets import QApplication
from main_window import WompPad

def main():
    app = QApplication(sys.argv)
    womppad = WompPad()
    womppad.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()