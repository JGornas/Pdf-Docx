import os
from shutil import move
from time import strftime

"""To skip files or folders put them in exceptions."""
EXCEPTIONS = ["desktop.ini", "exception_1.txt", "exception_2.avi", "Projekty"]
"""Desktop folder path: 'path' + 'desktop_folder'"""
DESKTOP_PATH = os.path.join("C:\\", "Users", "Jake", "Desktop", "1")
"""Backup folder path: 'path' + 'backup_folder' + 'current_date'"""
BACKUP_PATH = os.path.join("D:\\", "Desktop_backups", f"{strftime('%m.%d.%Y')}", "2", "")

os.makedirs(BACKUP_PATH, exist_ok=True)
os.chdir(DESKTOP_PATH)
desktop_files = os.listdir(os.getcwd())

#for file in desktop_files:
#    if file not in EXCEPTIONS:
#        move(file, BACKUP_PATH)

#[move(file, BACKUP_PATH) for file in desktop_files if file not in EXCEPTIONS]


#[move(file, os.path.join("D:\\", "Desktop_backups", f"{strftime('%m.%d.%Y')}", "2", "")) for file in os.listdir(os.chdir(os.path.join("C:\\", "Users", "Jake", "Desktop", "1"))) if file not in ["desktop.ini", "exception_1.txt", "exception_2.avi", "Projekty"]]
