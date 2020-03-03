from fastapi import FastAPI
from pydantic import BaseModel
# import requests

app = FastAPI()


class Address(BaseModel):
    """
        Desccribes an address to drive robotic traffic to \n
        client_id is an integer \n
        client: string \n
        store_address: string
    """
    client_id: int
    client: str
    store_address: str


@app.get("/addresses/{client_id}")
def update_item(client_id: int):
    """
        this is a cool docstring
    """
    obj = {'client_id': address.client_id, "client": address.client,
           "store_address": address.store_address}
    print("This object will be created: ", obj)
    print("now making request to the associated address")
    print(requests.get(obj["store_address"]).status_code)
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--window-size=1024,768')
    chrome_options.add_argument('--no-sandbox')

    browser = webdriver.Chrome(chrome_options=chrome_options)
    browser.get(obj['store_address'])
    browser.quit()

    return {"hello": "World"}


@app.put("/addresses/{client_id}")
def update_item(client_id: int, address: Address):
    obj = {'client_id': address.client_id, "client": address.client,
           "store_address": address.store_address}
    print("This object will be created: ", obj)
    print("now making request to the associated address")

    return obj
