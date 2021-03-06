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

def create_sap_order(url="https://electronics.cled7lxnr3-ns8azuree1-d1-public.model-t.cc.commerce.ondemand.com/yacceleratorstorefront/electronics/en/", headless=False):

    # create instance of faker
    # Faker.seed(42)
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



    #go to all products:
    product_page = 'https://electronics.cled7lxnr3-ns8azuree1-d1-public.model-t.cc.commerce.ondemand.com/yacceleratorstorefront/electronics/en/Open-Catalogue/c/1'
    browser.get(product_page)

    # Choose Products

    # get list of all products:
    prod = browser.find_elements_by_class_name('product__list--item')

    # choose random product:
    num = random.choice(range(len(prod)))

    #choose an individual product:
    p = prod[num]

    #get product url
    prod_url = p.find_element_by_tag_name('a').get_attribute('href')

    # Go to this page:
    browser.get(prod_url)

    # Adjust number of items to add to cart
    qty = browser.find_element_by_xpath('//*[@id="pdpAddtoCartInput"]')
    qty.send_keys(Keys.BACKSPACE)
    qty.send_keys(Keys.DELETE)
    qty.send_keys(str(random.choice(range(1, 6))))

    try:
        # Add product to cart
        browser.find_element_by_xpath(
            '//*[@id="addToCartButton"]').click()
    except:
        # If there's some kind of issue, just move on and we'll try with a different product.
        return None
    # Wait some time...
    time.sleep(2)

    # Go to cart
    browser.find_element_by_xpath(
        '/html/body/div[4]/div[1]/div[2]/div[2]/div[1]/div/a[1]').click()

    # Go to checkout
    browser.find_element_by_xpath(
        '/html/body/main/div[3]/div[3]/div[5]/div[2]/div/div[1]/button').click()

    time.sleep(8)

    # Fill in the checkout form
    guest_email = fake.ascii_safe_email()
    email = browser.find_element_by_xpath('//*[@id="guest.email"]')
    email.send_keys(guest_email)
    confirm_email = browser.find_element_by_xpath('//*[@id="guest.confirm.email"]')
    confirm_email.send_keys(guest_email)

    time.sleep(5)

    #checkout as guest
    browser.find_element_by_xpath('/html/body/main/div[3]/div/div[1]/div[2]/div/div/form/div[3]/button').click()

    # select country:
    country = browser.find_element_by_xpath('//*[@id="address.country"]')
    country.send_keys('united states')

    time.sleep(4)

    first_name = browser.find_element_by_xpath('//*[@id="address.firstName"]')
    f_name = fake.first_name()
    first_name.send_keys(f_name)

    time.sleep(1)

    last_name = browser.find_element_by_xpath('//*[@id="address.surname"]')
    l_name = fake.last_name()
    last_name.send_keys(l_name)

    st_ad = browser.find_element_by_xpath('//*[@id="address.line1"]')
    st_ad.send_keys(fake.street_address())

    time.sleep(1)

    city = browser.find_element_by_xpath('//*[@id="address.townCity"]')
    city.send_keys(fake.city())

    time.sleep(1)

    state_picker = browser.find_element_by_xpath('//*[@id="address.region"]')
    # pull this info out of a library somewhere to make dynamic. Must x-ref with state_abbr
    state = 'Nevada'
    state_picker.send_keys(state)

    time.sleep(2)

    zip = browser.find_element_by_xpath('//*[@id="address.postcode"]')
    zip_text = fake.postalcode_in_state(state_abbr='NV')
    zip.send_keys(zip_text)

    phone = browser.find_element_by_xpath('//*[@id="address.phone"]')
    phone.send_keys(fake.phone_number().split('x')[0])

    # Continue
    browser.find_element_by_xpath('//*[@id="addressSubmit"]').click()

    # Wait:
    time.sleep(7)

    # Select shipping:
    element = browser.find_element_by_xpath('//*[@id="deliveryMethodSubmit"]')
    browser.execute_script("arguments[0].click();", element)

    # Pay by CC:

    time.sleep(5)

    card_type = browser.find_element_by_xpath('//*[@id="card_cardType"]')
    card_type.send_keys('visa')

    time.sleep(1)

    card_name = browser.find_element_by_xpath('//*[@id="card_nameOnCard"]')
    card_name.send_keys(f_name + ' ' + l_name)

    time.sleep(1)

    card = browser.find_element_by_xpath('//*[@id="card_accountNumber"]')
    card.send_keys('4111111111111111')

    time.sleep(1)

    # Create expiration mo/year
    exp_date = fake.credit_card_expire(start='now', end='+3y', date_format='%m%Y')
    exp_mo = exp_date[0:2]
    exp_yr = exp_date[-4:]

    #enter expires month
    # iframe = browser.find_elements_by_tag_name('iframe')[1]
    # browser.switch_to.frame(iframe)
    expires_mo = browser.find_element_by_xpath('//*[@id="ExpiryMonth"]')
    expires_mo.send_keys(exp_mo)
    expires_yr = browser.find_element_by_xpath('//*[@id="ExpiryYear"]')
    expires_yr.send_keys(exp_yr)

    # browser.switch_to_default_content()
    time.sleep(1)

    # iframe = browser.find_elements_by_tag_name('iframe')[2]
    # browser.switch_to.frame(iframe)
    code = browser.find_element_by_xpath('//*[@id="card_cvNumber"]')
    code.send_keys(fake.credit_card_security_code()[0:3])

    con_btn = browser.find_element_by_xpath('/html/body/main/div[3]/div/div[1]/div[2]/div/button')
    browser.execute_script("arguments[0].click();", con_btn)

    time.sleep(2)

     # Accept TOS:
    browser.find_element_by_xpath('//*[@id="Terms1"]').click()

    time.sleep(2)

    con_btn = browser.find_element_by_xpath('//*[@id="placeOrder"]')
    browser.execute_script("arguments[0].click();", con_btn)

    time.sleep(4)
    browser.quit()
#
# def create_presta_testing_order(url="http://prestashop-02.testing.ns8demos.com/index.php", headless=False):
#
#     # create instance of faker
#     fake = Faker()
#     # get the store up in selenium
#
#     chrome_options = webdriver.ChromeOptions()
#     if headless:
#         chrome_options.add_argument('--headless')
#     chrome_options.add_argument('user-agent={}'.format(Faker().user_agent()))
#     chrome_options.add_argument('--disable-gpu')
#     chrome_options.add_argument('--disable-dev-shm-usage')
#     chrome_options.add_argument('--window-size=1024,768')
#     chrome_options.add_argument('--no-sandbox')
#
#     browser = webdriver.Chrome(options=chrome_options)
#     browser.get(url)
#     time.sleep(2)
#
#
#
#     #go to all products:
#     product_page = url + '?id_category=6&controller=category'
#     browser.get(product_page)
#
#     # Choose Products
#
#     # get list of all products:
#     prod = browser.find_elements_by_class_name('product-miniature.js-product-miniature')
#
#     # choose random product:
#     num = random.choice(range(len(prod)))
#
#     #choose an individual product:
#     p = prod[num]
#
#     #get product url
#     prod_url = p.find_element_by_tag_name('a').get_attribute('href')
#
#     # Go to this page:
#     browser.get(prod_url)
#
#     # Adjust number of items to add to cart
#     qty = browser.find_element_by_xpath('//*[@id="quantity_wanted"]')
#     qty.send_keys(Keys.BACKSPACE)
#     qty.send_keys(Keys.DELETE)
#     qty.send_keys(str(random.choice(range(1, 11))))
#
#     try:
#         # Add product to cart
#         browser.find_element_by_xpath(
#             '/html/body/main/section/div/div/section/div[1]/div[2]/div[2]/div[2]/form/div[2]/div/div[2]/button').click()
#     except:
#         # If there's some kind of issue, just move on and we'll try with a different product.
#         pass
#     # Wait some time...
#     time.sleep(3)
#
#     # Go to cart
#     browser.find_element_by_xpath(
#         '/html/body/div[1]/div/div/div[2]/div/div[2]/div/div/a').click()
#     time.sleep(3)
#     # Go to checkout
#     browser.find_element_by_xpath(
#         '/html/body/main/section/div/div/section/div/div[2]/div[1]/div[2]/div/a').click()
#
#     time.sleep(8)
#
#     # Fill in the checkout form
#     email = browser.find_element_by_xpath('/html/body/section/div/section/div/div[1]/section[1]/div/div/div[1]/form/section/div[4]/div[1]/input')
#     email.send_keys(fake.ascii_free_email())
#
#
#
#     time.sleep(5)
#
#     first_name = browser.find_element_by_xpath('/html/body/section/div/section/div/div[1]/section[1]/div/div/div[1]/form/section/div[2]/div[1]/input')
#     f_name = fake.first_name()
#     first_name.send_keys(f_name)
#
#     time.sleep(1)
#
#     last_name = browser.find_element_by_xpath('/html/body/section/div/section/div/div[1]/section[1]/div/div/div[1]/form/section/div[3]/div[1]/input')
#     l_name = fake.last_name()
#     last_name.send_keys(l_name)
#
#     #Agree to T's and C's
#     try:
#         element = browser.find_element_by_xpath('/html/body/section/div/section/div/div[1]/section[1]/div/div/div[1]/form/section/div[9]/div[1]/span/label/input')
#         browser.execute_script("arguments[0].click();", element)
#     except:
#         pass
#
#     # Continue as guest
#     browser.find_element_by_xpath('/html/body/section/div/section/div/div[1]/section[1]/div/div/div[1]/form/footer/button').click()
#
#     time.sleep(4)
#
#     st_ad = browser.find_element_by_xpath('/html/body/section/div/section/div/div[1]/section[2]/div/div/form/div/div/section/div[4]/div[1]/input')
#     st_ad.send_keys(fake.street_address())
#
#     time.sleep(1)
#
#     city = browser.find_element_by_xpath('/html/body/section/div/section/div/div[1]/section[2]/div/div/form/div/div/section/div[6]/div[1]/input')
#     city.send_keys(fake.city())
#
#     time.sleep(1)
#
#     state_picker = browser.find_element_by_xpath('/html/body/section/div/section/div/div[1]/section[2]/div/div/form/div/div/section/div[7]/div[1]/select')
#     # pull this info out of a library somewhere to make dynamic. Must x-ref with state_abbr
#     state = 'Nevada'
#     state_picker.send_keys(state)
#
#     time.sleep(2)
#
#     zip = browser.find_element_by_xpath('html/body/section/div/section/div/div[1]/section[2]/div/div/form/div/div/section/div[8]/div[1]/input')
#     zip_text = fake.postalcode_in_state(state_abbr='NV')
#     zip.send_keys(zip_text)
#
#     # Continue
#     browser.find_element_by_xpath('/html/body/section/div/section/div/div[1]/section[2]/div/div/form/div/div/footer/button').click()
#
#     # Wait:
#     time.sleep(7)
#
#     # Continue to Billing Information / Select Shipping:
#
#     element = browser.find_element_by_xpath('/html/body/section/div/section/div/div[1]/section[3]/div/div[2]/form/button')
#     browser.execute_script("arguments[0].click();", element)
#     # browser.find_element_by_xpath('/html/body/div[1]/div/div/main/div[1]/form/div[2]/button/span').click()
#
#     # Wait:
#     time.sleep(10)
#
#     # Pay by CC:
#     # browser.find_element_by_xpath('//*[@id="payment-option-1”]').click()
#     element = browser.find_element_by_xpath('/html/body/section/div/section/div/div[1]/section[4]/div/div[2]/div[1]/div/label/span')
#     browser.execute_script("arguments[0].click();", element)
#
#     time.sleep(5)
#     iframe = browser.find_elements_by_tag_name('iframe')[0]
#
#     browser.switch_to.frame(iframe)
#     card = browser.find_element_by_name('cardnumber')
#     # card = browser.find_element_by_xpath('//*[@id="stripe-card-number"]')
#     card.send_keys('4111111111111111')
#
#     browser.switch_to_default_content()
#     time.sleep(3)
#
#     # Create expiration mo/year
#     exp_date = fake.credit_card_expire(start='now', end='+3y', date_format='%m%y')
#     exp_mo = exp_date[0:2]
#     exp_yr = exp_date[-2:]
#
#     #enter expires month
#     iframe = browser.find_elements_by_tag_name('iframe')[1]
#     browser.switch_to.frame(iframe)
#     expires_mo = browser.find_element_by_name('exp-date')
#     expires_mo.send_keys(exp_mo + exp_yr)
#
#     browser.switch_to_default_content()
#     time.sleep(1)
#
#     iframe = browser.find_elements_by_tag_name('iframe')[2]
#     browser.switch_to.frame(iframe)
#     code = browser.find_element_by_name('cvc')
#     code.send_keys(fake.credit_card_security_code()[0:3])
#
#     browser.switch_to_default_content()
#     time.sleep(5)
#
#
#     # Accept TOS:
#     browser.find_element_by_xpath('//*[@id="conditions_to_approve[terms-and-conditions]"]').click()
#     # element = browser.find_element_by_xpath('//*[@id="conditions_to_approve[terms-and-conditions]"]')
#     # browser.execute_script("arguments[0].click();", element)
#
#     con_btn = browser.find_element_by_xpath('/html/body/section/div/section/div/div[1]/section[4]/div/div[3]/div[1]/button')
#     browser.execute_script("arguments[0].click();", con_btn)
#
#
#     time.sleep(5)
#     browser.quit()
