from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import chromedriver_binary
from faker import Faker


class BrowserBot():

    def __init__(self, url=None, headless=False):
        self.url = url
        self.headless = headless
        self.opts = webdriver.ChromeOptions()
        if headless:
            self.opts.add_argument('--headless')
        # self.opts.add_argument('user-agent={}'.format(Faker().user_agent()))
        self.opts.add_argument('--disable-gpu')
        self.opts.add_argument('--disable-dev-shm-usage')
        self.opts.add_argument('--window-size=1024,768')
        self.opts.add_argument('--no-sandbox')

        self.browser = webdriver.Chrome( chrome_options=self.opts)
