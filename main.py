from fastapi import FastAPI, Depends
from contextlib import asynccontextmanager
from db.session import engine
from db.models import Base, User
from routes.auth import router as auth_router
from auth import jwt
from routes.user import router as user_router
from fastapi_mqtt import FastMQTT, MQTTConfig
from dotenv import load_dotenv
import os

BROKER_HOST = os.getenv("MQTT_BROKER_HOST", default="localhost")
MQTT_USER = os.getenv("MQTT_USER")
MQTT_PASSWORD = os.getenv("MQTT_PASSWORD")

fast_mqtt = FastMQTT(
    config=MQTTConfig(
        host=BROKER_HOST,
        port=8883,
        keepalive=60,
        username=MQTT_USER,
        password=MQTT_PASSWORD,
    )
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    await fast_mqtt.mqtt_startup()
    yield
    await fast_mqtt.mqtt_shutdown()


app = FastAPI(lifespan=lifespan)

app.include_router(auth_router)
app.include_router(user_router)


@app.get("/protected")
def protected(current_user: User = Depends(jwt.get_current_user)):
    # print(current_user.email)
    return "Congrats..."
