import os

HOME_PATH = os.environ['HOMEPATH'].replace('\\', '/')
DEFAULT_DIR = HOME_PATH + '/Downloads'

DL_EPISODE = 1
DL_SEASON = 2
DL_SERIES = 3
CHANGE_SERIES = 4

URL_REGEX_PATTERN = r'https?:\/\/.+\/watch\/.*\/season\/[0-9]+\/episode\/[0-9]+'
DRIVER_NAME = 'chromedriver.exe'

VIDEO_HTML_ID = 'videojs_html5_api'
SEARCH_BAR_ID = 'liveSearch'
SERIES_NAME_XPATH = '//*[@id="watchEpisode"]/div[1]/div/h1/strong/span'

MB = 1_000_000

WAIT_FPS = 5
LOADING_TIME = 32
PROGRESS_BAR_CHAR = '█'

SITE_URL = 'https://sdarot.space/'
WATCH_URL = SITE_URL + 'watch'
SEARCH_URL = SITE_URL + 'search'