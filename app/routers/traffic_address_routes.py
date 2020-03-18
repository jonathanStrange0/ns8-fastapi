from app.page_browse_scheduler import PeriodicBrowser
import threading
from fastapi import APIRouter, BackgroundTasks
from app.schemas.traffic_schema import TrafficAddress
from app.firebase.fb_client import fb_client
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.executors.pool import ProcessPoolExecutor
from apscheduler.jobstores.base import BaseJobStore
from app.bots.browse_page import browse_page, recurring_browser
from datetime import datetime
from pathlib import Path
import schedule
import time
import sched
import google.cloud.logging
import logging

# executors = {
#    'default': ProcessPoolExecutor(20)
# }
# job_defaults = {
#     'coalesce': False,
#     'max_instances': 5
# }
scheduler = BackgroundScheduler()
# scheduler.configure(executors=executors)  # , job_defaults=job_defaults)
router = APIRouter()
db = fb_client()
s = sched.scheduler(time.time, time.sleep)
schedule_event_listing = {}
logging_client = google.cloud.logging.Client()

logging_client.setup_logging()


###############################################################################
##### GENERATING TRAFFIC ADDRESSES HERE #######################################
###############################################################################


@router.post("/traffic/")
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


@router.get("/traffic/{traffic_id}")
def get_traffic_address(traffic_id: str, traffic_address: TrafficAddress):
    obj = {'client_id': address.client_id, "client": address.client,
           "store_address": address.address}
    print("This object will be created: ", obj)
    print("now making request to the associated address")
    # # TODO: fire background process to generate traffic and return success
    return obj


@router.put("/traffic/{traffic_id}")
def update_traffic_address(traffic_id: str, traffic_address: TrafficAddress):
    """
        docstring for put(client_id)
    """
    # TODO: retreive a client from database and update it

    return {"Update Status": "Complete"}


@router.delete("/clients/{traffic_id}")
def delete_traffic_address(traffic_id: str):
    """
        docstring for delete(client_id)
    """
    # TODO: retreive a client from database and delete it
    return {"Delete Status": "Success"}

###############################################################################
##### Website Calls being made here   #########################################
###############################################################################


@router.get("/traffic/ping/{traffic_id}")
def ping_site_with_chrome(traffic_id: str, interval: int, background_tasks: BackgroundTasks):
    # def ping_site_with_chrome(traffic_id: str, interval: int):
    doc_ref = db.collection(u'traffic').document(traffic_id)
    address = doc_ref.get().to_dict()['address']
    if traffic_id not in schedule_event_listing.keys():
        pb = PeriodicBrowser(interval, address)
        schedule_event_listing[traffic_id] = pb
        background_tasks.add_task(pb.start, browse_page)
        logging.info('set address to be browsed: {} with interavl: {}, scheduler listing object {}'.format(
            address, interval, schedule_event_listing[traffic_id]))
        return {'Address ID': traffic_id,
                'Address Scheduled for Browsing': address,
                'Browsing Interval (Seconds)': interval}
    else:
        return {'Address ID': traffic_id,
                'Already Running': True}


@router.get("/shutdown/{traffic_id}")
def shutdown_background_tasks(traffic_id: str):
    """
        Kill the running APScheduler and restart it
    """
    try:
        browser_to_stop = schedule_event_listing[traffic_id]
        browser_to_stop.stop()
        del schedule_event_listing[traffic_id]
        return {'Stopped Address ID': traffic_id}
    except Exception as e:
        return {'Error': e}
