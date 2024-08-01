from selenium.webdriver import Firefox, FirefoxOptions
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from time import sleep
from dotenv import load_dotenv
from os import getenv

class YTChannelChecker:
    VIDEO_TITLE_LINK_ID = "video-title-link"
    VIDEO_TITLE_ID = "video-title"
    OPTIONS = FirefoxOptions()
    OPTIONS.set_preference("network.cookie.cookieBehavior", 2)

    def __init__(self):
        self.driver = Firefox(YTChannelChecker.OPTIONS)
        self.closed = False

    def __del__(self):
        if not self.closed:
            self.close()

    def close(self):
        self.closed = True
        self.driver.close()

    def check_channel(self, url : str, minimal_times : dict[str, int], sleep_duration = 3) -> dict[str, str]:
        res = dict()
        self.driver.get(url)
        sleep(sleep_duration)
        
        details = self.driver.find_elements(By.ID, 'details')
        
        for div in details:
            link = div.find_element(By.ID, YTChannelChecker.VIDEO_TITLE_LINK_ID)
            spans = [span for span in div.find_elements(By.TAG_NAME, 'span') if 'ago' in span.text]
        
            time = spans[0].text.split() if spans else None
            valid = time and any((unit in time[1] and int(time[0]) <= max_unit) for unit, max_unit in minimal_times.items())
            if not valid:
                break
        
            title = link.get_attribute('title') 
            link = link.get_attribute('href')
            res[title] = link
        return res

def _main(urls):
    ytch = YTChannelChecker()
    times = { 'day' : 14}
    accum = dict()
    for url in urls:
        accum.update(ytch.check_channel(url, times))

    if not accum:
        print('No new videos from given channels')
    else:
        for title, link in accum.items():
            print(title, link, sep='\n', end='\n\n')

def _get_urls(filename : str, type : str = 'channel_names'):
    load_dotenv()
    wrap = lambda x: x

    match type:
        case 'channel_names':
            wrap = lambda x: f'https://www.youtube.com/{x}/videos'
    channel_names = getenv('CHANNEL_NAMES') or ""
    return map(wrap, channel_names.split('\n'))

if __name__ == '__main__':
    _main(_get_urls('channel_names.txt'))
