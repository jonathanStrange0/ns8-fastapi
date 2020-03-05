from fastapi import FastAPI, BackgroundTasks
import os
from app.schemas.traffic_schema import TrafficAddress
from app.schemas.client_schema import Client
from app.schemas.order_address_schema import OrderAddress
from app.bots.browse_page import browse_page

import firebase_admin
from firebase_admin import credentials
from google.cloud import firestore
from google.cloud.firestore_v1.field_path import FieldPath
from apscheduler.schedulers.background import BackgroundScheduler


cred = credentials.Certificate(os.getenv('GOOGLE_APPLICATION_CREDENTIALS'))
firebase_admin.initialize_app(cred)
app = FastAPI()
db = firestore.Client()
scheduler = BackgroundScheduler()


###############################################################################
##### GENERATING CLIENT INFO HERE #############################################
###############################################################################


@app.post("/clients/")
def create_client(client: Client):
    """
        docstring for post() new client
    """

    # db = firestore.Client()
    doc_ref = db.collection(u'clients').document(client.client_name)
    doc_ref.set({
        u'client_id': None,
        u'client_name': client.client_name
    })

    return doc_ref.get().to_dict()


@app.get("/clients/{client_id}")
def get_client(client_id: int):
    """
        docstring for get(client_id)
    """
    # TODO: retreive a client from database and return as json object

    return {"hello": "World"}


@app.put("/clients/{client_id}")
def update_client(client_id: int, client: Client):
    """
        docstring for put(client_id)
    """
    # TODO: retreive a client from database and update it

    return {"Update Status": "Complete"}


@app.delete("/clients/{client_id}")
def delete_client(client_id: int, client: Client):
    """
        docstring for delete(client_id)
    """
    # TODO: retreive a client from database and delete it
    return {"Delete Status": "Success"}

###############################################################################
##### GENERATING TRAFFIC ADDRESSES HERE #######################################
###############################################################################


@app.post("/traffic/")
def create_traffic_address(traffic_address: TrafficAddress):
    """
        docstring for post() new traffic address
    """
    print(traffic_address.address)

    _, doc_ref = db.collection(u'traffic').add({
        u'client_id': None,
        u'address': traffic_address.address
    })
    #
    return doc_ref.get().to_dict()


@app.get("/traffic/{traffic_id}")
def get_traffic_address(traffic_id: str, traffic_address: TrafficAddress):
    obj = {'client_id': address.client_id, "client": address.client,
           "store_address": address.address}
    print("This object will be created: ", obj)
    print("now making request to the associated address")
    # # TODO: fire background process to generate traffic and return success
    return obj


@app.put("/traffic/{traffic_id}")
def update_traffic_address(traffic_id: str, traffic_address: TrafficAddress):
    """
        docstring for put(client_id)
    """
    # TODO: retreive a client from database and update it

    return {"Update Status": "Complete"}


@app.delete("/clients/{traffic_id}")
def delete_traffic_address(traffic_id: str):
    """
        docstring for delete(client_id)
    """
    # TODO: retreive a client from database and delete it
    return {"Delete Status": "Success"}

###############################################################################
##### GENERATING ORDER ADDRESSES HERE #########################################
###############################################################################


###############################################################################
##### Website Calls being made here   #########################################
###############################################################################


@app.get("/traffic/ping/{traffic_id}")
def ping_site_with_chrome(traffic_id: str, background_tasks: BackgroundTasks):
    doc_ref = db.collection(u'traffic').document(traffic_id)
    address = doc_ref.get().to_dict()['address']
    print("now making request to the associated address: ", address)

    # add the job to the scheduler and start the scheduler if it hasn't been yet
    scheduler.add_job(browse_page,  'interval', args=[
                      address], seconds=15, id=traffic_id, name='browse_page')
    if not scheduler.running:
        scheduler.start()

    # fastapi also offers a background task functionality, maybe later.
    # background_tasks.add_task(browse_page, address)
    # browse_page(address)

    return {"Browsed Page": address}


@app.get("/shutdown")
def shutdown_background_tasks():
    """
        Kill the running APScheduler and restart it
    """
    try:
        # scheduler = BackgroundScheduler()
        scheduler.shutdown()
        scheduler.start()
    except:
        pass
