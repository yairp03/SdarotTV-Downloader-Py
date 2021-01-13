import requests
from win32com.client import Dispatch
from datetime import datetime
import os
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog
from consts.strings import CHOOSE_DIR
from consts.consts import MB, DEFAULT_DIR, HOME_PATH, PROGRESS_BAR_CHAR, PROGRESS_BAR_LEN, TK_PAD
import sys


def download_episode(location, url, cookies):
    log("Location to download in: " + location)
    file_size = int(requests.head(url, cookies=cookies).headers['Content-Length'])
    log("File size: " + str(int(file_size / MB)) + "MB")
    downloaded = 0
    pb = ProgressBar("Downloading")
    try:
        with requests.get(url, cookies=cookies, stream=True) as r:
            r.raise_for_status()
            with open(location, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192): 
                    downloaded += f.write(chunk)
                    pb.progress(downloaded / file_size * 100)
    except:
        log("Download failed. Try again.")
    else:
        pb.endProgress()
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
    root.destroy()
    if location != '':
        log(f"Done. Folder: {location}")
        return location
    else:
        log(f"Canceled. Choosing default directory: {DEFAULT_DIR}")
        return DEFAULT_DIR


def hebrew_string(s):
    return '\n'.join([' '.join(i.split(' ')[::-1]) for i in s.split('\n')])


class ProgressBar:
    
    def __init__(self, title):
        self.root = tk.Tk()
        self.root.title(title)
        self.root.geometry(str(PROGRESS_BAR_LEN + TK_PAD) + "x45")
        self.progress_bar = ttk.Progressbar(self.root, orient=tk.HORIZONTAL, length=PROGRESS_BAR_LEN, mode='determinate')
        self.progress_bar.pack(pady=10)
        self.root.update()
        self.progress_x = 0
    
    def progress(self, x):
        self.progress_bar['value'] = x
        self.root.update()
        self.progress_x = x
    
    def endProgress(self):
        self.root.destroy()
        self.root = None
        del self.progress_bar
        self.progress_bar = None
