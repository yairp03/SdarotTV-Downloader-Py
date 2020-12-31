from time import sleep

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait

from _utils import download_episode, log

class Series:
    def __init__(self, first_episode_url):
        log("Creating Driver...", end="")
        options = webdriver.ChromeOptions()
        options.add_argument("headless")
        self.driver = webdriver.Chrome(options=options)
        print("Done.")
        log("Extracting series url from given url...", end="")
        self.series_url = self.extract_series_url(first_episode_url)
        print("Done.\nSeries url is:", self.series_url)

        log("Extracting site url from given url...", end="")
        self.site_url = self.extract_site_url()
        print("Done.\nSite url is:", self.site_url)

        log("Calculating amount of seasons...", end="")
        self.seasons_amount = self.calculate_seasons_amount()
        print(f"Done.\nThere are {self.seasons_amount} seasons.")

        self.episodes_amount = {}
        log("Calculating amount of episodes for each season:\n", end="")
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

    def navigate(self, url, delay=0):
        self.driver.get(url)
        sleep(delay)

    def download_episode(self, season, episode, location):
        log("Waiting for episode to load...", end="")
        self.navigate(self.wrap_episode(season, episode))
        print("Done.")

        log("Finding and clicking the proceed button (might take about 30 seconds)...")
        tries_left = 5
        while True:
            try:
                tries_left -= 1
                WebDriverWait(self.driver, 40).until(ec.element_to_be_clickable((By.ID, "proceed")))
            except TimeoutException:
                if tries_left == 0:
                    log("Time out. Skipping this episode.")
                    return
                log(f"Error. Trying again {tries_left} more times. Refreshing...")
                self.driver.execute_script("location.reload(true);")
            else:
                break
        proceed_btn = self.driver.find_element_by_id("proceed")
        proceed_btn.click()
        log("Done.")

        log("Finding Video...", end="")
        video = self.driver.find_element_by_id("videojs_html5_api")
        url = video.get_attribute("src")
        print(f"Done.\nUrl is: {url}")

        log("Getting cookies...", end="")
        cookies_dict = {}
        for cookie in self.driver.get_cookies():
            cookies_dict[cookie["name"]] = cookie["value"]
        print("Done.\nResults:", cookies_dict)

        download_episode(location, url, cookies_dict)
