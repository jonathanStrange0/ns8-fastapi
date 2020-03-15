from fastapi import APIRouter
from app.schemas.utm_parameters import Utm_Parameters
from app.firebase.fb_client import fb_client
router = APIRouter()
db = fb_client()
