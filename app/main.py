from fastapi import FastAPI, BackgroundTasks, Depends, Header, HTTPException

from app.routers import users_routes, traffic_address_routes, order_address_routes

from app.schemas.client_schema import Client
from app.schemas.order_address_schema import OrderAddress
from app.firebase.fb_client import fb_client

db = fb_client()

# define the app
app = FastAPI(
    title='NS8 Traffic API',
    description='This is the api that will allow us to programatically drive traffic to our demo sites'
)

# Include routers
# app.include_router(users_routes.router)

app.include_router(traffic_address_routes.router, tags=['traffic'])
app.include_router(order_address_routes.router, tags=['orders'])
