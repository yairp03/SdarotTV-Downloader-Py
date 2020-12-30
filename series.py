from selenium import webdriver
from time import sleep
from downloader import download_episode

COOL_DELAY = 1.5

class Series:
    
    def __init__(self, first_episode_url):
        print('Creating Driver...', end='')
        self.driver = webdriver.Chrome()
        print('Done.')
        print('Extracting series url from given url...', end='')
        self.series_url = self.extract_series_url(first_episode_url)
        print('Done.\nSeries url is:', self.series_url)
        
        print('Extracting site url from given url...', end='')
        self.extract_site_url()
        print('Done.\nSite url is:', self.site_url)
        
        print('Calculating amount of seasons:')
        self.calculate_seasons_amount()
        print(f'Done. There are {self.seasons_amount} seasons.')
        
        print('Calculating amount of episodes for each season:')
        self.calculate_episodes_amount()
        print(f'Done.')

    def print_data(self):
        print('driver: ', self.driver)
        print('site_url: ', self.site_url)
        print('series_url: ', self.series_url)
        print('seasons_amount: ', self.seasons_amount)
        print('episodes_amount: ', self.episodes_amount)
    
    @staticmethod
    def extract_series_url(first_episode_url):
        return '/'.join(first_episode_url.split('/')[:-4])

    def extract_site_url(self):
        self.site_url = '/'.join(self.series_url.split('/')[:-2]) + '/'
    
    def calculate_seasons_amount(self):
        self.navigate(self.wrap_episode(1, 1), 0)
        self.seasons_amount = int(self.driver.find_element_by_id('season').text.split('\n')[-1])
    
    def calculate_episodes_amount(self):
        self.episodes_amount = {}
        for season in range(1, self.seasons_amount + 1):
            self.episodes_amount[season] = self.calculate_season_episodes_amount(season)
            print(f'Season {season}: {self.episodes_amount[season]} episodes.')
    
    def calculate_season_episodes_amount(self, season):
        self.navigate(self.wrap_episode(season, 1))
        return int(self.driver.find_element_by_id('episode').text.split('\n')[-1])
        
    
    def wrap_episode(self, season, episode):
        return f'{self.series_url}/season/{season}/episode/{episode}'
    
    def navigate(self, url, delay=0):
        self.driver.get(url)
        sleep(delay)
        