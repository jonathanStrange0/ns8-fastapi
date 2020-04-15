from faker import Faker
import random
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import chromedriver_binary
# import google.cloud.logging
import logging
# logging_client = google.cloud.logging.Client()
# logging_client.setup_logging()

def create_bc_order(url="https://sc-test-store2.mybigcommerce.com", headless=False):

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

    #go to all products:
    product_page = '/html/body/header/div/nav/ul[1]/li[1]/a'
    browser.find_element_by_xpath(product_page).click()

    # Choose Products

    # get list of all products:
    prod = browser.find_elements_by_class_name('product')
    # choose random product:
    num = random.choice(range(len(prod)))

    #choose an individual product:
    p = prod[num]

    #get product url
    prod_url = p.find_element_by_tag_name('a').get_attribute('href')

    # Go to this page:
    browser.get(prod_url)

    #check for colors and sizes:
    try:
        colors = browser.find_element_by_xpath('/html/body/div[2]/div[1]/div/div[1]/section[3]/div[1]/form[1]/div[1]/div[1]/label[1]')
        browser.quit()# just bail if we have to deal with colors or sizes for now - jm
    except:
        pass

    # Adjust number of items to add to cart
    qty = browser.find_element_by_xpath('//*[@id="qty[]"]')
    qty.send_keys(Keys.BACKSPACE)
    qty.send_keys(Keys.DELETE)
    qty.send_keys(str(random.choice(range(1, 11))))

    # Add product to cart
    browser.find_element_by_xpath(
        '//*[@id="form-action-addToCart"]').click()

    # Wait some time...
    time.sleep(2)

    # browser.find_element_by_xpath(
    #     '/html/body/div[7]/a/span').click()

    # Go to the checkout
    # browser.find_element_by_xpath(
    #     '/html/body/div[7]/div[1]/div[2]/div/section[1]/a[1]').click()
    # con_btn = browser.find_element_by_class_name(
    #     'button.button--primary')
    # con_btn = browser.find_element_by_class_name(
    #     'button.button--primary')
    # browser.execute_script("arguments[0].click();", con_btn)
    browser.get(url+'/checkout')
    #wait again:
    time.sleep(8)

    # Fill in the checkout form
    email = browser.find_element_by_xpath('//*[@id="email"]')
    email.send_keys(fake.ascii_free_email())

    # Continue as guest
    browser.find_element_by_xpath('//*[@id="checkout-customer-continue"]').click()

    time.sleep(5)

    first_name = browser.find_element_by_xpath('//*[@id="firstNameInput"]')
    f_name = fake.first_name()
    first_name.send_keys(f_name)

    time.sleep(1)

    last_name = browser.find_element_by_xpath('//*[@id="lastNameInput"]')
    l_name = fake.last_name()
    last_name.send_keys(l_name)

    #Phone Number:
    phone_number = browser.find_element_by_xpath('//*[@id="phoneInput"]')
    phone_number.send_keys(fake.phone_number().split('x')[0])

    time.sleep(1)

    st_ad = browser.find_element_by_xpath('//*[@id="addressLine1Input"]')
    st_ad.send_keys(fake.street_address())

    time.sleep(1)

    city = browser.find_element_by_xpath('//*[@id="cityInput"]')
    city.send_keys(fake.city())

    time.sleep(1)

    state_picker = browser.find_element_by_xpath('//*[@id="provinceCodeInput"]')
    # pull this info out of a library somewhere to make dynamic. Must x-ref with state_abbr
    state = 'Nevada'
    state_picker.send_keys(state)

    time.sleep(1)

    zip = browser.find_element_by_xpath('//*[@id="postCodeInput"]')
    zip.send_keys(fake.postalcode_in_state(state_abbr='NV'))

    # Wait:
    time.sleep(7)

    # Continue to Billing Information:
    # browser.find_element_by_xpath('//*[@id="checkout-shipping-continue"]').click()

    # Wait:
    time.sleep(7)

    element = browser.find_element_by_xpath('//*[@id="checkout-shipping-continue"]')
    browser.execute_script("arguments[0].click();", element)
    # browser.find_element_by_xpath('/html/body/div[1]/div/div/main/div[1]/form/div[2]/button/span').click()

    # Wait:
    time.sleep(10)


    card = browser.find_element_by_xpath('//*[@id="ccNumber"]')
    card.send_keys('4111111111111111')
    time.sleep(2)


    card_name =  browser.find_element_by_xpath('//*[@id="ccName"]')
    card_name.send_keys(f_name + ' ' + l_name)

    expires = browser.find_element_by_xpath('//*[@id="ccExpiry"]')
    expires.send_keys(fake.credit_card_expire(
        start='now', end='+3y', date_format='%m%y'))

    code = browser.find_element_by_xpath('//*[@id="ccCvv"]')
    code.send_keys(fake.credit_card_security_code()[0:3])
    time.sleep(2)

    con_btn = browser.find_element_by_xpath('//*[@id="checkout-payment-continue"]')
    browser.execute_script("arguments[0].click();", con_btn)


    time.sleep(4)
    browser.quit()
