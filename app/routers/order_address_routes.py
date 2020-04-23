from fastapi import APIRouter, BackgroundTasks
from app.schemas.order_address_schema import OrderAddress
from app.bots.order_bot import create_woo_order, create_magento_order, create_magento_order_mediotype
from app.bots.shopify_bots import create_shopify_order
from app.bots.big_com_bots import create_bc_order
from app.periodic import PeriodicFunction
import google.cloud.logging
import logging
import requests
logging_client = google.cloud.logging.Client()
logging_client.setup_logging()

# from app.firebase.fb_client import fb_client
router = APIRouter()
# db = fb_client()
schedule_event_listing = {}


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


@router.get('/orders/magento_ns8')
def place_magento_order(background_tasks: BackgroundTasks):
    try:
        # background_tasks.add_task(create_magento_order, True)
        create_magento_order(url='https://magento-demo-1.ns8demos.com/', headless=True)
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


@router.get('/orders/big_commerce')
def place_bigcommerce_order():
    try:
        create_bc_order(headless=True)
        return {'Status' : 'Success'}
    except Exception as e:
        return {'Status': 'Failed',
                'error' : e}



@router.get('/orders/ping/repeatorders/')
def ping_a_bunch(address:str, interval:int, background_tasks: BackgroundTasks):

    # browsing_address = 'http://127.0.0.1:8000/traffic/ping/pingonetime/{}'.format(traffic_id)
    # browsing_address = '{}/{}'.format(address,traffic_id)
    if address not in schedule_event_listing.keys():
        pf = PeriodicFunction(interval, address)
        logging.info('set pf')
        schedule_event_listing[hash(address)] = pf
        logging.info('about to schedule background repetitive browsing task')
        background_tasks.add_task(pf.start, requests.get)
        # threading.Thread(target=pb.start).start()
        logging.info('set background task')
        logging.info('set address to be browsed: {} with interval: {}, scheduler listing object {}'.format(
            address, interval, schedule_event_listing[hash(address)]))
        return {'Address ID': hash(address),
                'Address Scheduled for Browsing': address,
                'Browsing Interval (Seconds)': interval}
    else:
        return {'Address ID': hash(address),
                'Already Running': True}



@router.get("/orders/shutdown/")
def shutdown_background_tasks(address: str):
    """
        Kill the running process of your choosing
    """
    try:
        browser_to_stop = schedule_event_listing[hash(address)]
        browser_to_stop.stop()
        del schedule_event_listing[hash(address)]
        logging.info('remaining scheduled events {}'.format(
            schedule_event_listing.keys()))
        return {'Stopped Address ID': address}
    except Exception as e:
        return {'Error': e}
