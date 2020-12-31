import requests
from printer import log


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
