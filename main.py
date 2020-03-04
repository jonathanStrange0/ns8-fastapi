from fastapi import FastAPI
from pydantic import BaseModel
import firebase_admin
from firebase_admin import credentials
from google.cloud import firestore
from google.cloud.firestore_v1.field_path import FieldPath
cred = credentials.Certificate(
    "./firebase-admin.json")
firebase_admin.initialize_app(cred)
app = FastAPI()


class TrafficAddress(BaseModel):
    """
        Desccribes an address to drive robotic traffic to \n
        client_id is an integer \n
        client: string \n
        store_address: string
    """
    client_id: int
    client: str
    address: str


class OrderAddress(BaseModel):
    """
        Desccribes an address to drive robotic traffic to \n
        client_id is an integer \n
        client: string \n
        store_address: string
    """
    client_id: int
    client: str
    address: str


class Client(BaseModel):
    """
        the client object used in database
    """
    client_name: str


@app.get("/clients/{client_id}")
def update_item(client_id: int):
    """
        docstring for get(client_id)
    """
    # TODO: retreive a client from database and return as json object

    return {"hello": "World"}


@app.post("/clients/")
def update_item(client: Client):
    """
        docstring for post() new client
    """
    # TODO: create a client and add to database, return as sucess json object
    # add a new user document????
    db = firestore.Client()
    doc_ref = db.collection(u'clients').document(client.client_name)
    doc_ref.set({
        u'client_name': client.client_name
    })
    # print(db.collection(u'clients').document(
    #     client.client_name).get('client_name'))
    fp = FieldPath()
    print(client.client_name)
    # path = fp.from_string(
    #     'clients.' + str(client.client_name) + '.client_name')
    # print(path)
    # return {"Client": db.collection(u'clients').document(client.client_name).get()}
    # return {"Something": "MIght have HAapenED"}


@app.put("/clients/{client_id}")
def update_item(client_id: int, client: Client):
    """
        docstring for put(client_id)
    """
    # TODO: retreive a client from database and update it

    return {"Update Status": "Complete"}


@app.delete("/clients/{client_id}")
def update_item(client_id: int, client: Client):
    """
        docstring for delete(client_id)
    """
    # TODO: retreive a client from database and delete it
    return {"Delete Status": "Success"}


@app.get("/traffic/{client_id}")
def update_item(client_id: int, address: TrafficAddress):
    obj = {'client_id': address.client_id, "client": address.client,
           "store_address": address.address}
    print("This object will be created: ", obj)
    print("now making request to the associated address")

    return obj
