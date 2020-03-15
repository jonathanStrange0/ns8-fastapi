from fastapi import FastAPI, BackgroundTasks, Depends, Header, HTTPException

from app.routers import users_routes, traffic_address_routes

from app.schemas.client_schema import Client
from app.schemas.order_address_schema import OrderAddress
from app.firebase.fb_client import fb_client
# import firebase_admin
# from firebase_admin import credentials
# from google.cloud import firestore
# from google.cloud.firestore_v1.field_path import FieldPath

#
# cred = credentials.Certificate(os.getenv('GOOGLE_APPLICATION_CREDENTIALS'))
# firebase_admin.initialize_app(cred)

# call the firebase client so it initiates the db connection
db = fb_client()

# define the app
app = FastAPI()

# Include routers
# app.include_router(users_routes.router)

app.include_router(traffic_address_routes.router, tags=['traffic'])
