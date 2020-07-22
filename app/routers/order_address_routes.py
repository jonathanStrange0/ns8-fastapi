from fastapi import APIRouter, BackgroundTasks
from app.schemas.order_address_schema import OrderAddress
from app.bots.order_bot import create_woo_order, create_magento_order, create_magento_order_mediotype
from app.bots.shopify_bots import create_shopify_order, create_shopify_order_kacoko
from app.bots.big_com_bots import create_bc_order
from app.bots.presta_bot import create_presta_order, create_presta_testing_order
from app.bots.magento_bots import create_magento_order_wilson
from app.bots.sap_bot import create_sap_order
from app.periodic import PeriodicFunction
from app.firebase.fb_client import fb_client
import google.cloud.logging
import logging
import requests
import uuid
logging_client = google.cloud.logging.Client()
logging_client.setup_logging()

# from app.firebase.fb_client import fb_client
router = APIRouter()
# db = fb_client()
schedule_event_listing = {}
db = fb_client()

###############################################################################
##### GENERATING ORDER ADDRESSES HERE #########################################
###############################################################################

@router.get('/orders/woo')
def place_woo_order(background_tasks: BackgroundTasks):
    try:
        # background_tasks.add_task(create_woo_order, True)
        create_woo_order(headless=True)
        return {'Status' : 'Success'}
    except Exception as e:
        return {'Status': 'Failuer',
                'error' : e}


@router.get('/orders/magento_ns8/{traffic_id}')
def place_magento_order(traffic_id: str, background_tasks: BackgroundTasks):
    doc_ref = db.collection(u'traffic').document(traffic_id)
    address = doc_ref.get().to_dict()['address']
    try:
        # background_tasks.add_task(create_magento_order, True)
        create_magento_order_wilson(url=address, headless=True)
        return {'Status' : 'Success'}
    except Exception as e:
        return {'Status': 'Failed',
                'error' : e}


@router.get('/orders/mediotype')
def place_mediotype_order(background_tasks: BackgroundTasks):
    try:
        # background_tasks.add_task(create_magento_order_mediotype, True)
        create_magento_order_mediotype(headless=True)
        return {'Status' : 'Success'}
    except Exception as e:
        return {'Status': 'Failed',
                'error' : e}

@router.get('/orders/shopify')
def place_shopify_order(background_tasks: BackgroundTasks):
    address = None
    if address:
        try:
            create_shopify_order(url=address, headless=True)
            return {'Status' : 'Success'}
        except Exception as e:
            return {'Status': 'Failed',
                    'error' : e}
    else:
        try:
            create_shopify_order(headless=True)
            return {'Status' : 'Success'}
        except Exception as e:
            return {'Status': 'Failed',
                    'error' : e}

@router.get('/orders/shopify_kacoko')
def place_shopify_order(background_tasks: BackgroundTasks):
    address = None
    if address:
        try:
            create_shopify_order_kacoko(url=address, headless=True)
            return {'Status' : 'Success'}
        except Exception as e:
            return {'Status': 'Failed',
                    'error' : e}
    else:
        try:
            create_shopify_order_kacoko(headless=True)
            return {'Status' : 'Success'}
        except Exception as e:
            return {'Status': 'Failed',
                    'error' : e}


@router.get('/orders/big_commerce')
def place_bigcommerce_order():
    try:
        create_bc_order(headless=True)
        return {'Status' : 'Success'}
    except Exception as e:
        return {'Status': 'Failed',
                'error' : e}

@router.get('/orders/presta_testing')
def place_presta_testing_order():
    """
        route specifically for driving orders to the prestashop/NS8 V2 test store.
    """
    try:
        create_presta_testing_order(headless=True)
        return {'Status' : 'Success'}
    except Exception as e:
        return {'Status': 'Failed',
                'error' : e}


@router.get('/orders/sap_order')
def place_sap_order():
    """
        order from the NS8 electronics SAP Store
    """
    try:
        create_sap_order    (headless=True)
        return {'Status' : 'Success'}
    except Exception as e:
        return {'Status': 'Failed',
                'error' : e}



# @router.get('/test_route')
# def test_route(address:str):
#     event = db.collection(u'scheduled_events').document(u'{}'.format(str(uuid.uuid4()))
#
#     if event.get().exists:
#         print("there's a doc here")
#     else:
#         print('no doc returned, adding')
#         event.set({
#             u'address':address
#         })


@router.get('/orders/ping/repeatorders/')
def ping_a_bunch(address:str, interval:int, background_tasks: BackgroundTasks):

    # scheduled_events = db.collection(u'scheduled_events').document(u'{}'.format(hash(address)))
    # doc_ref = db.collection(u'traffic').document(traffic_id)
    evt_id = str(uuid.uuid4())
    evt_data = {
        u'address' : address,
        u'browsing_interval': interval
    }


    if evt_id not in schedule_event_listing.keys():
        event = db.collection(u'scheduled_events').document(u'{}'.format(evt_id)).set(evt_data)
        pf = PeriodicFunction(interval, address)
        logging.info('set pf')
        schedule_event_listing[evt_id] = pf
        logging.info('about to schedule background repetitive browsing task')
        background_tasks.add_task(pf.start, requests.get)
        # threading.Thread(target=pb.start).start()
        logging.info('set background task')
        logging.info('set address to be browsed: {} with interval: {}, scheduler listing object {}'.format(
            address, interval, schedule_event_listing[evt_id]))
        return {'Address ID':evt_id,
                'Address Scheduled for Browsing': address,
                'Browsing Interval (Seconds)': interval}
    else:
        # Should really be updating here
        ## TODO: apply an update.
        return {'Address ID': evt_id,
                'Already Running': True}



@router.get("/orders/shutdown/")
def shutdown_background_tasks(address: str):
    """
        Kill the running process(es) of your choosing
        with the address specified:
            eg address='www.apple.com' will kill all order events related to www.apple.com
    """
    try:
        events = db.collection(u'scheduled_events').where(u'address', u'==', address).stream()
        # print(events)
        stopped_addresses = []
        for event in events:

            # evt_id = event.to_dict()['evt_id']
            # print(event)
            # print(u'{} => {}'.format(event.id, event.to_dict()))
            event.reference.delete()
            browser_to_stop = schedule_event_listing[event.id]
            browser_to_stop.stop()
            del schedule_event_listing[event.id]
            logging.info('remaining scheduled events {}'.format(
                schedule_event_listing.keys()))
            stopped_addresses.append(event.to_dict()['address'])
        return {'Stopped Address ID': stopped_addresses}
    except Exception as e:
        return {'Error': e}
