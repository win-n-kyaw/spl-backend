from fastapi import FastAPI, Depends
from contextlib import asynccontextmanager
from db.session import engine
from db.models import Base, User
from routes.auth import router as auth_router
from routes.parking import router as parking_router
from auth import jwt
from routes.user import router as user_router
from dotenv import load_dotenv
from mqtt.client import start_mqtt, stop_mqtt
import os

# import logging

# logging.basicConfig(level=logging.DEBUG)

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

app.include_router(auth_router)
app.include_router(user_router)
app.include_router(parking_router)


@app.get("/protected")
def protected(current_user: User = Depends(jwt.get_current_user)):
    # print(current_user.email)
    return "Congrats..."
