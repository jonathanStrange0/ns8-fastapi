from selenium import webdriver
import chromedriver_binary
from faker import Faker
import time
import os
import google.cloud.logging
import logging

logging_client = google.cloud.logging.Client()
logging_client.setup_logging()


def browse_page(page):
    """
    Browse a webpage

    Use Selenium and chrome to headlessly move to page and then quit.

    Args:
        page (string): webpage address

    Returns:
        None

    """
    try:
        # if 'https://' not in page[0:8]:
        #     page = 'https://' + page
        print("WE ARE BROWSING TO THIS PAGE: {}".format(page))
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument(
            'user-agent={}'.format(Faker().user_agent()))
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--window-size=1024,768')
        chrome_options.add_argument('--no-sandbox')

        browser = webdriver.Chrome(chrome_options=chrome_options)

        # browser = webdriver.Chrome(
        #     chromedriver_binary, chrome_options=chrome_options)
        browser.get(page)
        time.sleep(3)
        browser.quit()

        return True
    except:
        return 'Exception'


def recurring_browser(scheduler, interval, action, action_args=(), action_kwargs={}):
    event = scheduler.enter(interval, 1, recurring_browser,
                            (scheduler, interval, action, action_args, action_kwargs))
    action(*action_args, **action_kwargs)
    scheduler.run()
    # return event
