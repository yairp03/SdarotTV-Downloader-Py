from time import sleep

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait

from _utils import download_episode, log, ProgressBar

from consts.consts import VIDEO_HTML_ID, WAIT_FPS

class Series:
    def __init__(self, first_episode_url):
        log("Creating Driver...")
        options = webdriver.ChromeOptions()
        options.add_argument("headless")
        self.driver = webdriver.Chrome(options=options)
        log("Done.")
        log("Extracting series url from given url...")
        self.series_url = self.extract_series_url(first_episode_url)
        log("Done. Series url is: " + self.series_url)

        log("Extracting site url from given url...")
        self.site_url = self.extract_site_url()
        log("Done. Site url is: " + self.site_url)

        log("Calculating amount of seasons...")
        self.seasons_amount = self.calculate_seasons_amount()
        log(f"Done. There are {self.seasons_amount} seasons.")

        self.episodes_amount = {}
        log("Calculating amount of episodes for each season:")
        self.calculate_episodes_amount()
        log(f"Done.")

    def print_data(self):
        log("driver: ", self.driver)
        log("site_url: ", self.site_url)
        log("series_url: ", self.series_url)
        log("seasons_amount: ", self.seasons_amount)
        log("episodes_amount: ", self.episodes_amount)

    @staticmethod
    def extract_series_url(first_episode_url):
        return "/".join(first_episode_url.split("/")[:-4])

    def extract_site_url(self):
        return "/".join(self.series_url.split("/")[:-2]) + "/"

    def calculate_seasons_amount(self):
        self.navigate(self.wrap_episode(1, 1), 0)
        return int(
            self.driver.find_element_by_id("season").text.split("\n")[-1]
        )

    def calculate_episodes_amount(self):
        for season in range(1, self.seasons_amount + 1):
            self.episodes_amount[season] = self.calculate_season_episodes_amount(season)
            log(f"Season {season}: {self.episodes_amount[season]} episodes.")

    def calculate_season_episodes_amount(self, season):
        self.navigate(self.wrap_episode(season, 1))
        return int(self.driver.find_element_by_id("episode").text.split("\n")[-1])

    def wrap_episode(self, season, episode):
        return f"{self.series_url}/season/{season}/episode/{episode}"

    def navigate(self, url):
        self.driver.get(url)

    def download_episode(self, season, episode, location):
        log("Waiting for episode to load...")
        self.navigate(self.wrap_episode(season, episode))
        log("Done.")
        tries_left = 5
        while True:
            try:
                tries_left -= 1
                ProgressBar.startProgress('Loading episode')
                for i in range(WAIT_FPS * 30):
                    sleep(1 / WAIT_FPS)
                    ProgressBar.progress((i + 11) / (WAIT_FPS * 30) * 100)
                ProgressBar.endProgress()
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
        proceed_btn = self.driver.find_element_by_id("proceed")
        proceed_btn.click()
        log("Done.")

        log("Finding Video...")
        video = self.driver.find_element_by_id(VIDEO_HTML_ID)
        url = video.get_attribute("src")
        log(f"Done. Url is: {url}")

        log("Getting cookies...")
        cookies_dict = {}
        for cookie in self.driver.get_cookies():
            cookies_dict[cookie["name"]] = cookie["value"]
        log("Done. Results: " + str(cookies_dict))

        download_episode(location, url, cookies_dict)
