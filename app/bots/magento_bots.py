from faker import Faker
import random
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import chromedriver_binary
import time

import google.cloud.logging
import logging
logging_client = google.cloud.logging.Client()
logging_client.setup_logging()

def create_magento_order_wilson(url, headless=False):

    # create instance of faker
    fake = Faker()

    # get the store up in selenium
    # "https://magento-v2-234.ns8demos.com/index.php/"
    # url =  "https://magento-demo.ns8demos.com"
    # opts = Options()
    chrome_options = webdriver.ChromeOptions()
    if headless:
        chrome_options.add_argument('--headless')
    chrome_options.add_argument('user-agent={}'.format(Faker().user_agent()))
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--window-size=1024,768')
    chrome_options.add_argument('--no-sandbox')

    browser = webdriver.Chrome(chrome_options=chrome_options)
    browser.get(url)
    time.sleep(2)

    # Try to close popup:
    try:
        browser.find_element_by_xpath(
            '/html/body/div[4]/div[1]/div/div/div[1]').click()
        time.sleep(4)
    except:
        pass
    # Go to gear site
    browser.find_element_by_xpath(
        '/html/body/div[1]/div/div/div[2]/nav/ul/li[4]/a/span[2]').click()

    # Select Bags
    browser.find_element_by_xpath(
        '/html/body/div[1]/main/div[4]/div[2]/div/div/ul/li[1]/a').click()

    # Choose Products
    browser.find_element_by_xpath(
        '/html/body/div[1]/main/div[3]/div[1]/div[3]/ol/li[1]/div/a/span/span/img').click()

    # Adjust number of items to add to cart
    qty = browser.find_element_by_xpath('//*[@id="qty"]')
    # qty = browser.find_elements_by_class_name("input-text.qty.text")[0]
    qty.send_keys(Keys.BACKSPACE)
    qty.send_keys(Keys.DELETE)

    qty.send_keys(str(random.choice(range(1, 11))))

    # Add product to cart
    time.sleep(5)
    browser.find_element_by_xpath(
        '//*[@id="product-addtocart-button"]').click()

    # Go to the cart
    time.sleep(10)
    browser.get(url + '/index.php/checkout/cart')
    # try:
    #     browser.find_element_by_xpath(
    #         '/html/body/div[1]/main/div[1]/div[2]/div/div/div/a').click()
    #
    #     # Go to checkout
    #     browser.find_element_by_xpath(
    #         '//*[@id="top-cart-btn-checkout"]').click()
    #     # browser.find_element_by_xpath(
    #     #     '/html/body/div[1]/main/div[1]/div[2]/div/div/div/a').click()
    # except:
    #     time.sleep(5)
    #     browser.find_element_by_xpath(
    #         '/html/body/div[1]/main/div[1]/div[2]/div/div/div/a').click()
    #
    #     # Go to checkout
    #     browser.find_element_by_xpath(
    #         '//*[@id="top-cart-btn-checkout"]').click()
    browser.find_element_by_xpath(
        '/html/body/div[1]/main/div[3]/div/div[2]/div[1]/ul/li[1]/button/span').click()

    # Fill in the checkout form
    # Wait for form to load
    time.sleep(15)
    first_name = browser.find_element_by_name('firstname')
    first_name.send_keys(fake.first_name())

    last_name = browser.find_element_by_name('lastname')
    last_name.send_keys(fake.last_name())

    st_ad = browser.find_element_by_name('street[0]')
    st_ad.send_keys(fake.street_address())

    city = browser.find_element_by_name('city')
    city.send_keys(fake.city())

    state_picker = browser.find_element_by_name('region_id')
    # pull this info out of a library somewhere to make dynamic. Must x-ref with state_abbr
    state = 'New York'
    state_picker.send_keys(state)

    zip = browser.find_element_by_name('postcode')
    zip.send_keys(fake.postalcode_in_state(state_abbr='NY'))

    email = browser.find_element_by_xpath('//*[@id="customer-email"]')
    email.send_keys(fake.ascii_free_email())

    phone = browser.find_element_by_name('telephone')
    phone.send_keys(fake.phone_number().split('x')[0])

    # Choose Shipping Method:
    browser.find_element_by_xpath(
        '/html/body/div[1]/main/div[2]/div/div[2]/div[4]/ol/li[2]/div/div[3]/form/div[1]/table/tbody/tr[1]/td[1]/input').click()

    # Print form
    logging.info(first_name.get_attribute('value') +
          ' ' + last_name.get_attribute('value'))
    logging.info(st_ad.get_attribute('value'))
    logging.info(state_picker.get_attribute('value'))
    logging.info(city.get_attribute('value') + ', ' + zip.get_attribute('value'))
    logging.info(email.get_attribute('value'))
    logging.info(phone.get_attribute('value'))

    # Select Next to move to payment:
    browser.find_element_by_xpath(
        '/html/body/div[1]/main/div[2]/div/div[2]/div[4]/ol/li[2]/div/div[3]/form/div[3]/div/button/span').click()

    # Wait a few moments
    time.sleep(7)
    # Locate all the iframes to get through braintree
    iframes = browser.find_elements_by_tag_name('iframe')
    logging.info('number of iframes: {}'.format(len(iframes)))
    # logging.info('number of iframes: {}'.format(len(iframes)))

    for i in range(len(iframes)):
        logging.info('iframe title: {}'.format(iframes[i].get_attribute('name')))
        # logging.info('iframe title: {}'.format(iframes[i].get_attribute('name')))

    # Choose payment method
    # browser.find_element_by_xpath('//*[@id="braintree"]').click()
    browser.switch_to_default_content()
    time.sleep(5)

    # Choose shipping == billing
    browser.find_element_by_xpath('//*[@id="billing-address-same-as-shipping-braintree"]').click()

    # Select ifames
    iframe = browser.find_elements_by_tag_name('iframe')[0]

    browser.switch_to.frame(iframe)
    # card = browser.find_element_by_name('number')
    card = browser.find_element_by_xpath('//*[@id="credit-card-number"]')
    card.send_keys('4111111111111111')

    browser.switch_to_default_content()
    time.sleep(1)

    # Create expiration mo/year
    exp_date = fake.credit_card_expire(start='now', end='+3y', date_format='%m%y')
    exp_mo = exp_date[0:2]
    exp_yr = exp_date[-2:]

    #enter expires month
    iframe = browser.find_elements_by_tag_name('iframe')[1]
    browser.switch_to.frame(iframe)
    expires_mo = browser.find_element_by_xpath('//*[@id="expiration-month"]')
    expires_mo.send_keys(exp_mo)

    browser.switch_to_default_content()
    time.sleep(1)

    #enter expires year
    iframe = browser.find_elements_by_tag_name('iframe')[2]
    browser.switch_to.frame(iframe)
    expires_yr = browser.find_element_by_xpath('//*[@id="expiration-year"]')
    expires_yr.send_keys(exp_yr)
    # expires.send_keys(fake.credit_card_expire(
    #     start='now', end='+3y', date_format='%m%y'))

    browser.switch_to_default_content()
    time.sleep(1)

    iframe = browser.find_elements_by_tag_name('iframe')[3]
    browser.switch_to.frame(iframe)
    code = browser.find_element_by_xpath('//*[@id="cvv"]')
    code.send_keys(fake.credit_card_security_code()[0:3])



    # try:
    #     # Assume the billing and shipping address are the same and checked
    #     time.sleep(7)
    #     # Place the order
    #     browser.find_element_by_xpath(
    #         '/html/body/div[2]/main/div[2]/div/div[2]/div[4]/ol/li[3]/div/form/fieldset/div[1]/div/div/div[2]/div[2]/div[4]/div/button/span').click()
    # except:
    #     browser.find_element_by_xpath(
    #         '//*[@id="billing-address-same-as-shipping-checkmo"]').click()
    #     time.sleep(7)
    #     browser.find_element_by_xpath(
    #         '/html/body/div[2]/main/div[2]/div/div[2]/div[4]/ol/li[3]/div/form/fieldset/div[1]/div/div/div[2]/div[2]/div[4]/div/button/span').click()

    browser.switch_to_default_content()
    time.sleep(10)

    # browser.find_element_by_xpath(
    #         '/html/body/div[1]/main/div[2]/div/div[2]/div[4]/ol/li[3]/div/form/fieldset/div[1]/div/div/div[2]/div[2]/div[4]/div/button/span').click()
    browser.find_element_by_class_name('action.primary.checkout').click()
    time.sleep(4)
    browser.quit()
