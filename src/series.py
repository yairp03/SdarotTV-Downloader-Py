from time import sleep

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys

from _utils import download_episode, log, ProgressBar

from consts.consts import VIDEO_HTML_ID, SEARCH_BAR_ID, SERIES_NAME_XPATH, WAIT_FPS, SITE_URL, WATCH_URL, SEARCH_URL, LOADING_TIME

class Series:
    def __init__(self):
        log("Creating Driver...")
        options = webdriver.ChromeOptions()
        options.add_argument("headless")
        self.driver = webdriver.Chrome(options=options)
        log("Done.")
        
        self.site_url = SITE_URL
        log("Site url is: " + self.site_url)
        
        self.series_url = ''
        self.series_name = ''
        self.seasons_amount = ''
        self._episodes_amount = {}
        # log("Calculating amount of episodes for each season:")
        # self.calculate_episodes_amount()
        # log(f"Done.")

    def find_series_url(self, series_name):
        self.navigate(self.site_url)
        self.driver.find_element_by_id(SEARCH_BAR_ID).send_keys(series_name + Keys.ENTER)
        if self.driver.current_url.startswith(SEARCH_URL):
            log("Not supporting search yet.")
            raise NotImplementedError()
        return self.driver.current_url
    
    def find_series_name(self):
        self.navigate(self.series_url)
        series_name = self.driver.find_element_by_xpath(SERIES_NAME_XPATH).text
        return series_name

    def calculate_seasons_amount(self):
        self.navigate(self.wrap_episode(1, 1))
        return int(
            self.driver.find_element_by_id("season").text.split("\n")[-1]
        )

    # def calculate_episodes_amount(self):
    #     for season in range(1, self.seasons_amount + 1):
    #         self._episodes_amount[season] = self.calculate_season_episodes_amount(season)

    def calculate_season_episodes_amount(self, season):
        self.navigate(self.wrap_episode(season, 1))
        episode_amount = int(self.driver.find_element_by_id("episode").text.split("\n")[-1])
        log(f"Season {season}: {episode_amount} episodes.")
        return episode_amount

    def wrap_episode(self, season, episode):
        return f"{self.series_url}/season/{season}/episode/{episode}"
    
    def get_episodes_amount(self, season):
        if season not in self._episodes_amount:
            self._episodes_amount[season] = self.calculate_season_episodes_amount(season)
        return self._episodes_amount[season]

    def navigate(self, url):
        self.driver.get(url)
    
    def change_series(self, series_name):
        log("Finding series url...")
        self.series_url = self.find_series_url(series_name)
        log("Done. Series url is: " + self.series_url)
        
        log("Finding series name...")
        self.series_name = self.find_series_name()
        log("Done. Series name is: " + self.series_name)
        
        log("Calculating amount of seasons...")
        self.seasons_amount = self.calculate_seasons_amount()
        log(f"Done. There are {self.seasons_amount} seasons.")
        
        self._episodes_amount = {}

    def download_episode(self, season, episode, location):
        log(f"Starting process for season {season} episode {episode}...")
        self.navigate(self.wrap_episode(season, episode))
        tries_left = 5
        while True:
            try:
                tries_left -= 1
                pb = ProgressBar('Loading episode')
                for i in range(WAIT_FPS * LOADING_TIME):
                    sleep(1 / WAIT_FPS)
                    pb.progress((i + 1) / (WAIT_FPS * LOADING_TIME) * 100)
                pb.endProgress()
                WebDriverWait(self.driver, 10).until(ec.element_to_be_clickable((By.ID, "proceed")))
            except TimeoutException:
                if tries_left == 0:
                    log("Time out. Skipping this episode.")
                    return
                log(f"Error. Trying again {tries_left} more times. Refreshing...")
                # Hard refresh (Ctrl + F5)
                self.driver.execute_script("location.reload(true);")
            else:
                break
            # Click proceed Button
        self.driver.find_element_by_id("proceed").click()
        log("Done.")

        log("Finding Video...")
        url = self.driver.find_element_by_id(VIDEO_HTML_ID).get_attribute("src")
        log(f"Done. Video url is: {url}")

        log("Getting cookies...")
        cookies_dict = {}
        for cookie in self.driver.get_cookies():
            cookies_dict[cookie["name"]] = cookie["value"]
        log("Done. Results: " + str(cookies_dict))

        download_episode(location, url, cookies_dict)
