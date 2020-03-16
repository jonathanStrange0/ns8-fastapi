from fastapi import APIRouter, BackgroundTasks
from app.schemas.traffic_schema import TrafficAddress
from app.firebase.fb_client import fb_client
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.executors.pool import ProcessPoolExecutor
from apscheduler.jobstores.base import BaseJobStore
from app.bots.browse_page import browse_page

executors = {
    'default': ProcessPoolExecutor(20)
}
# job_defaults = {
#     'coalesce': False,
#     'max_instances': 5
# }
scheduler = BackgroundScheduler()
scheduler.configure(executors=executors)  # , job_defaults=job_defaults)
router = APIRouter()
db = fb_client()


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
    doc_ref = db.collection(u'traffic').document(traffic_id)
    address = doc_ref.get().to_dict()['address']
    print("now making request to the associated address: ", address)

    if not scheduler.running:
        scheduler.start()
    if traffic_id not in list(map(lambda x: x.id, scheduler.get_jobs())):
        # add the job to the scheduler and start the scheduler if it hasn't been yet
        scheduler.add_job(browse_page,  'interval', args=[
                          address], seconds=interval, id=traffic_id, name='browse_page')
    else:
        return {"This address is scheudled for traffic already": address}
    # fastapi also offers a background task functionality, maybe later.
    # background_tasks.add_task(browse_page, address)
    # browse_page(address)

    return {"Browsed Page": address}


@router.get("/shutdown")
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
