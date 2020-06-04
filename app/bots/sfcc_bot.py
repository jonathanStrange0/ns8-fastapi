from faker import Faker
import random
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import chromedriver_binary
import google.cloud.logging
import logging
logging_client = google.cloud.logging.Client()
logging_client.setup_logging()


def create_salesforce_order(url="https://ns801-tech-prtnr-na04-dw.demandware.net/on/demandware.store/Sites-RefArch-Site", headless=False):

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

    browser = webdriver.Chrome(options=chrome_options)
    browser.get(url)
    time.sleep(2)

    consent = browser.find_element_by_xpath(
        '/html/body/div[5]/div/div/div[3]/div/button[1]')
    if consent:
        consent.click()

    # go to all categories:
    browser.get('https://ns801-tech-prtnr-na04-dw.demandware.net/s/RefArch/electronics?lang=en_US')



    # Choose category:
    categories=browser.find_elements_by_class_name('category-item')
    print(categories)
    category=categories[random.choice(range(len(categories)))]
    cat_url=category.find_elements_by_tag_name("a")[0].get_attribute('href')
    print(cat_url)
    # Got to page:
    browser.get(cat_url)

    # Choose Products

    # get list of all products:
    prod=browser.find_elements_by_class_name('product')

    # choose random product:
    num=random.choice(range(len(prod)))

    # choose an individual product:
    p=prod[num]

    # get product url
    prod_url=p.find_element_by_tag_name('a').get_attribute('href')

    # Go to this page:
    browser.get(prod_url)

    # Adjust number of items to add to cart
    qty=browser.find_element_by_xpath('//*[@id="quantity-1"]')
    qty.send_keys(Keys.BACKSPACE)
    qty.send_keys(Keys.DELETE)
    qty.send_keys(str(random.choice(range(1, 11))))

    try:
        # Add product to cart
        browser.find_element_by_xpath(
            '/html/body/div[1]/div/div/div[2]/div[2]/div[4]/div[6]/div[2]/div/button').click()
    except:
        # If there's some kind of issue, just move on and we'll try with a different product.
        pass
    # Wait some time...
    time.sleep(2)

    # Go to cart
    browser.find_element_by_xpath(
        '/html/body/div[1]/div/div/div[2]/div[2]/div[4]/div[6]/div[2]/div/button').click()

    # Go to checkout
    browser.get('https://ns801-tech-prtnr-na04-dw.demandware.net/s/RefArch/cart?lang=en_US')

    # Go to the checkout
    browser.find_element_by_xpath(
        '/html/body/div[1]/div/div[3]/div[1]/div[2]/div[10]/div/div[2]/a').click()
    time.sleep(5)

    # Checkout as guest:
    browser.find_element_by_xpath('/html/body/div[1]/div/div/div[2]/div/div[1]/div[2]/a').click()

    # wait again:
    time.sleep(8)

    # Fill in the checkout form

    first_name = browser.find_element_by_xpath('//*[@id="shippingFirstNamedefault"]')
    f_name = fake.first_name()
    first_name.send_keys(f_name)

    time.sleep(1)

    last_name = browser.find_element_by_xpath('//*[@id="shippingLastNamedefault"]')
    l_name = fake.last_name()
    last_name.send_keys(l_name)

    phone_number = browser.find_element_by_xpath('//*[@id="shippingPhoneNumberdefault"]')
    phone_number.send_keys(fake.phone_number().split('x')[0])

    st_ad = browser.find_element_by_xpath('//*[@id="shippingAddressOnedefault"]')
    st_ad.send_keys(fake.street_address())

    time.sleep(1)

    city = browser.find_element_by_xpath('//*[@id="shippingAddressCitydefault"]')
    city.send_keys(fake.city())

    time.sleep(1)

    state_picker = browser.find_element_by_xpath('//*[@id="shippingStatedefault"]')
    # pull this info out of a library somewhere to make dynamic. Must x-ref with state_abbr
    state = 'Nevada'
    state_picker.send_keys(state)

    country_picker = browser.find_element_by_xpath('//*[@id="shippingCountrydefault"]')
    # pull this info out of a library somewhere to make dynamic. Must x-ref with state_abbr
    country = 'United States'
    country_picker.send_keys(country)

    time.sleep(2)

    zip = browser.find_element_by_xpath('//*[@id="shippingZipCodedefault"]')
    zip_text = fake.postalcode_in_state(state_abbr='NV')
    zip.send_keys(zip_text[0:5])

    time.sleep(10)

    # Continue
    browser.find_element_by_xpath('/html/body/div[1]/div/div[1]/div[3]/div[1]/div[7]/div/div/button[1]').click()

    # Wait:
    time.sleep(7)

    # Continue to Billing Information:
    # browser.find_element_by_xpath('//*[@id="checkout-shipping-continue"]').click()

    # # Wait:
    # time.sleep(7)
    email = browser.find_element_by_xpath('//*[@id="email"]')
    email.send_keys(fake.ascii_free_email())

    card = browser.find_element_by_xpath('//*[@id="cardNumber"]')
    card.send_keys('4111111111111111')
    time.sleep(2)


    # card_name =  browser.find_element_by_xpath('//*[@id="ccName"]')
    # card_name.send_keys(f_name + ' ' + l_name)

    expires_mo = browser.find_element_by_xpath('//*[@id="expirationMonth"]')
    expires_mo.send_keys('05')

    time.sleep(2)

    expires_yr = browser.find_element_by_xpath('//*[@id="expirationYear"]')
    expires_yr.send_keys('2')
    expires_yr.send_keys('2')

    time.sleep(2)

    code = browser.find_element_by_xpath('//*[@id="securityCode"]')
    code.send_keys(fake.credit_card_security_code()[0:3])
    time.sleep(2)

    con_btn = browser.find_element_by_xpath('/html/body/div[1]/div/div[1]/div[3]/div[1]/div[7]/div/div/button[2]')
    browser.execute_script("arguments[0].click();", con_btn)


    time.sleep(4)
    browser.quit()
