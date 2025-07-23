from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from routes.login_controller import login_router
from routes.parking_controller import router as parking_router
from routes.register_controller import register_router
from routes.request_controller import request_router
from routes.plate_controller import router as plate_router
from routes.admin_controller import router as user_router
from dotenv import load_dotenv
from mqtt.client import start_mqtt, stop_mqtt
import os

load_dotenv()

BROKER_HOST = os.getenv("MQTT_BROKER_HOST", default="localhost")
MQTT_USER = os.getenv("MQTT_USER")
MQTT_PASSWORD = os.getenv("MQTT_PASSWORD")


@asynccontextmanager
async def lifespan(app: FastAPI):
    start_mqtt()
    # Base.metadata.create_all(bind=engine)
    yield
    stop_mqtt()


app = FastAPI(lifespan=lifespan)

origins =[
    "http://localhost:7979",
    "http://localhost:5173"
    # "http://192.168.0.101:5173" 
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins, 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(login_router)
app.include_router(user_router)
app.include_router(parking_router)
app.include_router(register_router)
app.include_router(request_router)
app.include_router(plate_router)
