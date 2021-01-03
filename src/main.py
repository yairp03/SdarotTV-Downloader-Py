import os  # for environment variable %HOMEPATH% and mkdir
import tkinter as tk
from tkinter import filedialog
from series import Series
from _utils import get_chrome_version, log, clear
from shutil import copyfile
import easygui
import re


HOME_PATH = os.environ['HOMEPATH'].replace('\\', '/')
DEFAULT_DIR = HOME_PATH + "/Downloads"

EXIT = "exit"

DL_EPISODE = 1
DL_SEASON = 2
DL_SERIES = 3
CHANGE_SERIES = 4

URL_MESSAGE = f"Enter the url of the first episode\n(something like https://sdarot.space/watch/$series$/season/1/episode/1):"
URL_REGEX_PATTERN = r'https?:\/\/.+\/watch\/.*\/season\/[0-9]+\/episode\/[0-9]+'
DRIVER_NAME = 'chromedriver.exe'
MENU = """\
1. Download episode
2. Download season (might take a while)
3. Download whole series (might take a while)\n"""

def main():
    clear()
    while True:
        print("Hi! Welcome to the Sdarot TV Downloader.")
        first_episode_url = ''
        while not re.findall(URL_REGEX_PATTERN, first_episode_url):
            first_episode_url = easygui.enterbox(URL_MESSAGE)
            if first_episode_url == None:
                exit()
        initialize_driver()
        series = Series(first_episode_url)
        choice = take_choice(DL_EPISODE, CHANGE_SERIES, txt=MENU)
        while choice != CHANGE_SERIES:
            if choice == DL_EPISODE:
                download_episode(series)
            elif choice == DL_SEASON:
                download_season(series)
            elif choice == DL_SERIES:
                download_series(series)
            choice = take_choice(DL_EPISODE, CHANGE_SERIES, txt=MENU)
        series.driver.quit()


def take_choice(min_option, max_option, txt=''):
    choice = str(min_option - 1)
    while not (choice.isnumeric() and min_option <= int(choice) <= max_option):
        choice = easygui.enterbox(txt + f"Enter your choice ({min_option}-{max_option}): ")
        if choice == None:
            exit()
    return int(choice)


def download_episode(series, season=0, episode=0, location=None):
    if season == 0:
        season = take_choice(1, series.seasons_amount, txt="Choose season:\n")
        log(f"Season selected: {season}")
    if episode == 0:
        episode = take_choice(1, series.episodes_amount[season], txt="Choose episode:\n")
        log(f"Episode selected: {episode}")
    if not location:
        location = select_folder()
    series.download_episode(season, episode, location + f"/s{season}e{episode}.mp4")


def download_season(series, season=0, location=None):
    if season == 0:
        season = take_choice(1, series.seasons_amount, txt="Choose season:\n")
        log(f"Season chosed: {season}")
    if not location:
        location = select_folder()
    for episode in range(1, series.episodes_amount[season] + 1):
        download_episode(series, season, episode, location)


def download_series(series):
    location = select_folder()
    for season in range(1, series.seasons_amount + 1):
        new_location = location + f"/Season{season}"
        create_dir(new_location)
        download_season(series, season, new_location)


def select_folder():
    root = tk.Tk()
    root.withdraw()
    log("Choosing directory...", end="")
    location = filedialog.askdirectory(
        parent=root, initialdir=HOME_PATH, title="Please select a directory to download to"
    )
    if location != '':
        print(f"Done.\nFolder: {location}")
        return location
    else:
        print(f"Canceled. Choosing default directory: {DEFAULT_DIR}")
        return DEFAULT_DIR


def create_dir(path):
    try:
        os.mkdir(path)
    except OSError:
        log(f"Creation of the directory {path} failed.")
    else:
        log(f"Successfully created the directory {path}.")


def initialize_driver():  
    log('Checking Chrome version...', end='')
    chrome_version = get_chrome_version()
    print(f'Done. Chrome version is: {chrome_version}')
    src_driver = f"chromedrivers/{chrome_version.split('.')[0]}.exe"
    log("Getting the right driver...")
    log(f"Copying from {src_driver} to {DRIVER_NAME}...", end='')
    copyfile(src_driver, DRIVER_NAME)
    print('Done.')


if __name__ == "__main__":
    main()
