import json
from schemas.parking import ParkingPayload
from db.models import ParkingSnapshot
from db.session import get_db


def on_connect(client, userdata, flags, rc, properties):
    print(f"on_connect: client_id={client._client_id.decode()}, rc={rc}")
    if rc == 0:
        print("MQTT connected successfully.")
        topic = userdata.get("topic")
        if topic:
            client.subscribe(topic, qos=1)
            print(f"Subscribed to topic: {topic}")
    else:
        print(f"MQTT connection failed with code {rc}")


def on_message(client, userdata, msg):
    try:
        topic = msg.topic
        payload = msg.payload.decode()
        print(f"Message received: topic={topic}, payload={payload}")

        data = json.loads(payload)
        validated = ParkingPayload(**data)

        db_gen = get_db()
        db = next(db_gen)

        snapshot = ParkingSnapshot(
            lot_id=validated.lot_id,
            timestamp=validated.timestamp,
            available_spaces=validated.available_spaces,
            total_spaces=validated.total_spaces,
            occupied_spaces=validated.occupied_spaces,
            occupacy_rate=validated.occupancy_rate,
            confidence=validated.confidence,
            processing_time_seconds=validated.processing_time_seconds
        )
        db.add(snapshot)
        db.commit()

        print("Saved to DB")

    except Exception as err:
        print(f"Error processing message: {err}")
    finally:
        try:
            db_gen.close()  # type: ignore
        except:
            pass


# Sample Payload
# {
#   "lot_id": "CAMT_01",
#   "available_spots": 5
# }
# Full Payload
# {
#   "lot_id": "CAMT_01",
#   "available_spots": 12,
#   "total_spots": 30,
#   "timestamp": "2025-06-27T14:30:00Z"
# }
