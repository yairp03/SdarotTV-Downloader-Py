import requests
from win32com.client import Dispatch
from datetime import datetime
import os
import tkinter as tk
from tkinter import filedialog
from consts.strings import *
from consts.consts import *
import sys


def download_episode(location, url, cookies):
    log("Location to download in: " + location)
    file_size = int(requests.head(url, cookies=cookies).headers['Content-Length'])
    log("File size: " + str(int(file_size / MB)) + "MB")
    downloaded = 0
    ProgressBar.startProgress("Downloading")
    try:
        with requests.get(url, cookies=cookies, stream=True) as r:
            r.raise_for_status()
            with open(location, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192): 
                    downloaded += f.write(chunk)
                    ProgressBar.progress(downloaded / file_size * 100)
    except:
        log("Download failed. Try again.")
    else:
        ProgressBar.endProgress()
        log('Done.')


def get_version_via_com(filename):
    parser = Dispatch("Scripting.FileSystemObject")
    try:
        version = parser.GetFileVersion(filename)
    except Exception:
        return None
    return version

def get_chrome_version():
    paths = [r"C:\Program Files\Google\Chrome\Application\chrome.exe",
             r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"]
    return list(filter(None, [get_version_via_com(p) for p in paths]))[0]


def log(s, end='\n'):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {s}", flush=True, end=end)


def clear():
    os.system("cls")


def create_dir(path):
    try:
        os.mkdir(path)
    except OSError:
        log(f"Creation of the directory {path} failed.")
    else:
        log(f"Successfully created the directory {path}.")


def select_folder():
    root = tk.Tk()
    root.withdraw()
    log("Choosing directory...")
    location = filedialog.askdirectory(
        parent=root, initialdir=HOME_PATH, title=CHOOSE_DIR
    )
    if location != '':
        log(f"Done. Folder: {location}")
        return location
    else:
        log(f"Canceled. Choosing default directory: {DEFAULT_DIR}")
        return DEFAULT_DIR


def hebrew_string(s):
    return '\n'.join([' '.join(i.split(' ')[::-1]) for i in s.split('\n')])


class ProgressBar:
    progress_x = 0
    
    @classmethod
    def startProgress(cls, title):
        sys.stdout.write(title + ": [" + "-"*40 + "]" + chr(8)*41)
        sys.stdout.flush()
        cls.progress_x = 0

    @classmethod
    def progress(cls, x):
        x = int(x * 40 // 100)
        sys.stdout.write("#" * (x - cls.progress_x))
        sys.stdout.flush()
        cls.progress_x = x
    
    @classmethod
    def endProgress(cls):
        sys.stdout.write("#" * (40 - cls.progress_x) + "]\n")
        sys.stdout.flush()
