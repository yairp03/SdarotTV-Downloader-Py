import requests
from win32com.client import Dispatch
from datetime import datetime
import os


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
