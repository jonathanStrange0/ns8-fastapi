from fastapi import APIRouter
from app.schemas.order_address_schema import OrderAddress
from app.firebase.fb_client import fb_client
router = APIRouter()
db = fb_client()


###############################################################################
##### GENERATING ORDER ADDRESSES HERE #########################################
###############################################################################
