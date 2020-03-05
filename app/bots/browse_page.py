from selenium import webdriver
import chromedriver_binary


def browse_page(page):
    if page[0:7] != 'https://':
        page = 'https://' + page
    print("WE ARE BROWSING TO THIS PAGE: {}".format(page))
    chrome_options = webdriver.ChromeOptions()
    # chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--window-size=1024,768')
    chrome_options.add_argument('--no-sandbox')

    browser = webdriver.Chrome(chrome_options=chrome_options)
    browser.get(page)
    browser.quit()
