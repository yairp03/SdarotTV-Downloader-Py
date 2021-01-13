import os
from series import Series
from _utils import get_chrome_version, log, clear, create_dir, select_folder, hebrew_string, parse_config_file
from shutil import copyfile
import easygui
import re
from consts.strings import WELCOME_MESSAGE, URL_MESSAGE, MENU, CHOOSE_SEASON, CHOOSE_EPISODE
from consts.consts import DL_EPISODE, DL_SEASON, DL_SERIES, CHANGE_SERIES, DRIVER_NAME, CONFIG_NAME, DEFAULT_CONFIG_VARS
import sys

def main():
    config_vars = parse_config_file(CONFIG_NAME, DEFAULT_CONFIG_VARS)
    initialize_driver()
    series = Series(config_vars['site'], config_vars['headless'])
    while True:
        clear()
        print(WELCOME_MESSAGE)
        series_name = ''
        success = False
        while not success:
            series_name = easygui.enterbox(hebrew_string(URL_MESSAGE))
            if series_name == None:
                sys.exit()
            else:
                series_name = series_name.strip()
            try:
                series.change_series(series_name)
            except Exception as e:
                log("Invalid series name. Try again." + str(e))
            else:
                success = True
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
        choice = easygui.enterbox(hebrew_string(txt) + f"Enter your choice ({min_option}-{max_option}): ")
        if choice == None:
            sys.exit()
        else:
            choice = choice.strip()
    return int(choice)


def download_episode(series, season=0, episode=0, location=None):
    if season == 0:
        season = take_choice(1, series.seasons_amount, txt=CHOOSE_SEASON)
        log(f"Season selected: {season}")
    if episode == 0:
        episode = take_choice(1, series.get_episodes_amount(season), txt=CHOOSE_EPISODE)
        log(f"Episode selected: {episode}")
    if not location:
        location = select_folder()
    series.download_episode(season, episode, location + f"/s{season}e{episode}.mp4")


def download_season(series, season=0, location=None):
    if season == 0:
        season = take_choice(1, series.seasons_amount, txt=CHOOSE_SEASON)
        log(f"Season selected: {season}")
    if not location:
        location = select_folder()
    for episode in range(1, series.get_episodes_amount(season) + 1):
        download_episode(series, season, episode, location)


def download_series(series):
    location = select_folder()
    for season in range(1, series.seasons_amount + 1):
        new_location = location + f"/Season{season}"
        create_dir(new_location)
        download_season(series, season, new_location)


def initialize_driver():  
    log('Checking Chrome version...')
    chrome_version = get_chrome_version()
    log(f'Done. Chrome version is: {chrome_version}')
    src_driver = f"chromedrivers/{chrome_version.split('.')[0]}.exe"
    log("Getting the right driver...")
    log(f"Copying from {src_driver} to {DRIVER_NAME}...")
    copyfile(src_driver, DRIVER_NAME)
    log('Done.')


if __name__ == "__main__":
    main()
