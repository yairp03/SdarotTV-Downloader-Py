import os  # for environment variable %HOMEPATH% and mkdir
import tkinter as tk
from tkinter import filedialog
from series import Series
from printer import log

EXIT = "exit"

DL_EPISODE = 1
DL_SEASON = 2
DL_SERIES = 3
CHANGE_SERIES = 4


def main():
    print("Hi! Welcome to the Sdarot TV Downloader.")
    while (
            first_episode_url := input(
                f"Enter the url of the first episode (something like https://sdarot.space/watch/$series$/season/1/episode/1):\n(Enter '{EXIT}' to exit)\n"
            )
    ) != EXIT:
        series = Series(first_episode_url)
        print_menu()
        while (choice := take_choice(DL_EPISODE, CHANGE_SERIES)) != CHANGE_SERIES:
            if choice == DL_EPISODE:
                download_episode(series)
            elif choice == DL_SEASON:
                download_season(series)
            elif choice == DL_SERIES:
                download_series(series)
            print_menu()
        series.driver.quit()


def print_menu():
    print(
        """\
1. Download episode
2. Download season (might take a while)
3. Download whole series (might take a while)
4. Change series"""
    )


def take_choice(min_option, max_option):
    choice = min_option - 1
    while choice < min_option or choice > max_option:
        try:
            choice = int(input(f"Enter your choice ({min_option}-{max_option}): "))
        except ValueError:
            print("Not a valid Number")
    return choice


def download_episode(series, season=0, episode=0, location=None):
    if season == 0:
        print("Choose season:")
        season = take_choice(1, series.seasons_amount)
    if episode == 0:
        print("Choose episode:")
        episode = take_choice(1, series.episodes_amount[season])
    if not location:
        location = select_folder()
    series.download_episode(season, episode, location + f"/s{season}e{episode}.mp4")


def download_season(series, season=0, location=None):
    if season == 0:
        print("Choose season:")
        season = take_choice(1, series.seasons_amount)
    if not location:
        location = select_folder()
    for episode in range(1, series.episodes_amount[season] + 1):
        download_episode(series, season, episode, location)


def download_series(series):
    location = select_folder()
    for season in range(1, series.seasons_amount + 1):
        new_location = location + f'/Season{season}'
        create_dir(new_location)
        download_season(series, season, new_location)


def select_folder():
    root = tk.Tk()
    root.withdraw()
    log("Choosing directory...", end="")
    location = filedialog.askdirectory(
        parent=root, initialdir="/", title="Please select a directory to download to"
    )
    print(f"Done.\nFolder: {location}")
    return location


def create_dir(path):
    try:
        os.mkdir(path)
    except OSError:
        log(f"Creation of the directory {path} failed.")
    else:
        log(f"Successfully created the directory {path}.")


if __name__ == "__main__":
    main()
