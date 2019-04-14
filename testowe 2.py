import os
from shutil import move
from time import strftime

"""To skip files or folders put them in exceptions."""
EXCEPTIONS = ["desktop.ini", "exception_1.txt", "exception_2.avi", "Projekty"]
"""Desktop folder path: 'path' + 'desktop_folder'"""
DESKTOP_PATH = os.path.join("C:\\", "Users", "Jake", "Desktop")
"""Backup folder path: 'path' + 'backup_folder' + 'current_date'"""
BACKUP_PATH = os.path.join("D:\\", "Desktop_backups", f"{strftime('%m.%d.%Y')}", "")

os.makedirs(BACKUP_PATH, exist_ok=True)
os.chdir(DESKTOP_PATH)
desktop_files = os.listdir(os.getcwd())

for file in desktop_files:
    if file not in EXCEPTIONS:
        move(file, BACKUP_PATH)
