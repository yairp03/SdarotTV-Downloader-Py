import requests
from win32com.client import Dispatch
from datetime import datetime
import os
import tkinter as tk
from tkinter import filedialog
from consts.strings import *
from consts.consts import *


def download_episode(location, url, cookies):
    print("Location to download in: ", location)
    log("Downloading...")
    r = requests.get(url, cookies=cookies)
    f = open(location, "wb")
    for chunk in r.iter_content(chunk_size=255):
        if chunk:  # filter out keep-alive new chunks
            f.write(chunk)
    f.close()
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
