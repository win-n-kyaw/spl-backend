import os
from dotenv import load_dotenv
import paho.mqtt.client as mqtt
from paho.mqtt.enums import CallbackAPIVersion
from . import handler

load_dotenv()

MQTT_USER = os.getenv("MQTT_USER")
MQTT_PASSWORD = os.getenv("MQTT_PASSWORD")
MQTT_HOST = os.getenv("MQTT_BROKER_HOST", "localhost")
MQTT_TOPIC = os.getenv("MQTT_TOPIC")
client_id = "spl-backend"

mqtt_client = mqtt.Client(
    callback_api_version=CallbackAPIVersion.VERSION2,
    client_id=client_id,
    userdata={"topic": MQTT_TOPIC},
)
mqtt_client.username_pw_set(MQTT_USER, MQTT_PASSWORD)
mqtt_client.tls_set()
mqtt_client.on_connect = handler.on_connect
mqtt_client.on_message = handler.on_message


def start_mqtt():
    try:
        print("Starting mqtt...")
        mqtt_client.connect(
            host=MQTT_HOST,
            port=8883,
        )
        mqtt_client.loop_start()
    except Exception as e:
        print(f"Unexpected Error occured: {e}")


def stop_mqtt():
    print("Stopping mqtt")
    mqtt_client.loop_stop()
    mqtt_client.disconnect()
