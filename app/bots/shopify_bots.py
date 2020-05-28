from faker import Faker
import random
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import chromedriver_binary
import google.cloud.logging
import logging
# logging_client = google.cloud.logging.Client()
# logging_client.setup_logging()

def create_shopify_order(url="https://ns8-internal-test-store.myshopify.com/", headless=False):

    # create instance of faker
    fake = Faker()

    # get the store up in selenium

    chrome_options = webdriver.ChromeOptions()
    if headless:
        chrome_options.add_argument('--headless')
    chrome_options.add_argument('user-agent={}'.format(Faker().user_agent()))
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--window-size=1024,768')
    chrome_options.add_argument('--no-sandbox')

    browser = webdriver.Chrome( chrome_options=chrome_options)
    browser.get(url)
    time.sleep(2)

    product_xpath_list = ['/html/body/div[4]/main/div[2]/div/ul/li[1]/div/a',
                            '/html/body/div[4]/main/div[2]/div/ul/li[2]/div/a',
                            '/html/body/div[4]/main/div[2]/div/ul/li[3]/div/a',
                            '/html/body/div[4]/main/div[2]/div/ul/li[4]/div/a']

    # Choose Products
    browser.find_element_by_xpath(random.choice(product_xpath_list)).click()

    # Adjust number of items to add to cart
    # qty = browser.find_elements_by_class_name("input-text.qty.text")[0]
    # qty.send_keys(Keys.BACKSPACE)
    # qty.send_keys(Keys.DELETE)
    # qty.send_keys(str(random.choice(range(1, 11))))

    # Add product to cart
    browser.find_element_by_xpath(
        '/html/body/div[4]/main/div[1]/div/div/div[2]/div[1]/form/div[2]/button/span[1]').click()

    # Wait some time...
    time.sleep(4)

    # Go to the cart
    browser.find_element_by_xpath(
        '/html/body/div[2]/div/a').click()

    # Wait again
    time.sleep(5)

    # Procede to checkout
    browser.find_element_by_xpath(
        '/html/body/div[4]/main/div/div/form/div/div/div/div[3]/input[2]').click()

    #wait again:
    time.sleep(10)

    # Fill in the checkout form
    email = browser.find_element_by_xpath('//*[@id="checkout_email_or_phone"]')
    email.send_keys(fake.ascii_free_email())

    time.sleep(1)

    first_name = browser.find_element_by_xpath('//*[@id="checkout_shipping_address_first_name"]')
    f_name = fake.first_name()
    first_name.send_keys(f_name)

    time.sleep(1)

    last_name = browser.find_element_by_xpath('//*[@id="checkout_shipping_address_last_name"]')
    l_name = fake.last_name()
    last_name.send_keys(l_name)

    time.sleep(1)

    st_ad = browser.find_element_by_xpath('//*[@id="checkout_shipping_address_address1"]')
    st_ad.send_keys(fake.street_address())

    time.sleep(1)

    city = browser.find_element_by_xpath('//*[@id="checkout_shipping_address_city"]')
    city.send_keys(fake.city())

    time.sleep(1)

    state_picker = browser.find_element_by_xpath('//*[@id="checkout_shipping_address_province"]')
    # pull this info out of a library somewhere to make dynamic. Must x-ref with state_abbr
    state = 'New York'
    state_picker.send_keys(state)

    time.sleep(1)

    zip = browser.find_element_by_xpath('//*[@id="checkout_shipping_address_zip"]')
    zip.send_keys(fake.postalcode_in_state(state_abbr='NY'))

    # phone = browser.find_element_by_xpath('//*[@id="billing_phone"]')
    # phone.send_keys(fake.phone_number().split('x')[0])


    # Continue to Billing Information:
    browser.find_element_by_xpath('//*[@id="continue_button"]').click()

    # Wait:
    time.sleep(7)

    element = browser.find_element_by_xpath('//*[@id="continue_button"]')
    browser.execute_script("arguments[0].click();", element)
    # browser.find_element_by_xpath('/html/body/div[1]/div/div/main/div[1]/form/div[2]/button/span').click()

    # Wait:
    time.sleep(10)

    iframes = browser.find_elements_by_tag_name('iframe')
    print('number of iframes: {}'.format(len(iframes)))
    logging.info('number of iframes: {}'.format(len(iframes)))

    for i in range(len(iframes)):
        print('iframe title: {}'.format(iframes[i].get_attribute('name')))
        logging.info('iframe title: {}'.format(iframes[i].get_attribute('name')))

    if len(iframes) > 2:

        browser.switch_to_default_content()
        time.sleep(1)

        iframe = browser.find_elements_by_tag_name('iframe')[1]

        browser.switch_to.frame(iframe)
        # card = browser.find_element_by_name('number')
        card = browser.find_element_by_xpath('//*[@id="number"]')
        card.send_keys('4111111111111111')

        browser.switch_to_default_content()
        time.sleep(1)

        iframe = browser.find_elements_by_tag_name('iframe')[2]
        browser.switch_to.frame(iframe)
        card_name = browser.find_element_by_xpath('//*[@id="name"]')
        card_name.send_keys(f_name +' '+ l_name)

        browser.switch_to_default_content()
        time.sleep(1)

        iframe = browser.find_elements_by_tag_name('iframe')[3]
        browser.switch_to.frame(iframe)
        expires = browser.find_element_by_xpath('//*[@id="expiry"]')
        expires.send_keys(fake.credit_card_expire(
            start='now', end='+3y', date_format='%m%y'))

        browser.switch_to_default_content()
        time.sleep(1)

        iframe = browser.find_elements_by_tag_name('iframe')[4]
        browser.switch_to.frame(iframe)
        code = browser.find_element_by_xpath('//*[@id="verification_value"]')
        code.send_keys(fake.credit_card_security_code()[0:3])


        # print(first_name.get_attribute('value') +
        #       ' ' + last_name.get_attribute('value'))
        # print(st_ad.get_attribute('value'))
        # print(city.get_attribute('value') + ', ' + zip.get_attribute('value'))
        # print(email.get_attribute('value'))
        # print(phone.get_attribute('value'))
        # print(card.get_attribute('value'))
        # print(expires.get_attribute('value'))
        # print(code.get_attribute('value'))

        # Wait a few moments
        time.sleep(10)
        browser.switch_to_default_content()
        # Place the order
        element = browser.find_element_by_xpath('/html/body/div[1]/div/div/main/div[1]/div/form/div[3]/div[1]/button/span')
        browser.execute_script("arguments[0].click();", element)

    else:
        element = browser.find_element_by_xpath('/html/body/div[1]/div/div/main/div[1]/div/form/div[3]/div[1]/button/span')
        browser.execute_script("arguments[0].click();", element)

        card = browser.find_element_by_id('checkout_credit_card_number')
        card.send_keys('4111111111111111')
        time.sleep(2)

        card_name = browser.find_element_by_id('checkout_credit_card_name')
        card_name.send_keys(f_name +' '+ l_name)
        time.sleep(2)

        expires_mo = browser.find_element_by_id('checkout_credit_card_month')
        expires_mo.send_keys('05')
        time.sleep(2)

        expires_yr = browser.find_element_by_id('checkout_credit_card_year')
        expires_yr.send_keys('25')
        time.sleep(2)

        code = browser.find_element_by_id('checkout_credit_card_verification_value')
        code.send_keys(fake.credit_card_security_code()[0:3])
        time.sleep(2)

        con_btn = browser.find_element_by_class_name('step__footer__continue-btn.btn')
        browser.execute_script("arguments[0].click();", con_btn)


    time.sleep(4)
    browser.quit()
