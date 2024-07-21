# src/utils/file_operations.py

import os
import sys

def get_documents_dir():
    if sys.platform == 'win32':
        import winreg
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders")
        return winreg.QueryValueEx(key, "Personal")[0]
    elif sys.platform == 'darwin':
        return os.path.expanduser('~/Documents')
    else:  # linux and other unix systems
        return os.path.expanduser('~/Documents')

def safe_open_file(filename, mode='r'):
    try:
        return open(filename, mode)
    except IOError as e:
        print(f"Error opening file {filename}: {e}")
        return None

def safe_save_file(filename, content):
    try:
        with open(filename, 'w') as file:
            file.write(content)
        return True
    except IOError as e:
        print(f"Error saving file {filename}: {e}")
        return False