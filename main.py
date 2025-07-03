from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from db.session import engine
from db.models import Base, Admin
from routes.auth import router as auth_router
from routes.parking import router as parking_router
from routes.register import router as register_router
from routes.request import router as request_router
from routes.plates import router as plate_router
from auth import jwt
from routes.admin import router as user_router
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
    Base.metadata.create_all(bind=engine)
    yield
    stop_mqtt()


app = FastAPI(lifespan=lifespan)

origins =[
    "http://localhost:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins, 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(auth_router)
app.include_router(user_router)
app.include_router(parking_router)
app.include_router(register_router)
app.include_router(request_router)
app.include_router(plate_router)


@app.get("/protected")
def protected(current_user: Admin = Depends(jwt.get_current_user)):
    # print(current_user.email)
    return "Congrats..."
