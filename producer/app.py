import random
import time
import json
import os
from datetime import datetime, timezone
from google.cloud import pubsub_v1


# Environment variables
PROJECT_ID = os.getenv("GCP_PROJECT_ID", "local-project")
TOPIC_ID = os.getenv("PUBSUB_TOPIC_RAW", "iot-sensor-data-raw")

# Pub/Sub emulator connection
os.environ["PUBSUB_EMULATOR_HOST"] = "localhost:8085"

publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(PROJECT_ID, TOPIC_ID)


def create_topic_if_not_exists():
    try:
        publisher.create_topic(name=topic_path)
        print("Topic created.")
    except Exception:
        print("Topic already exists.")


def generate_sensor_data(device_id: str) -> dict:
    return {
        "device_id": device_id,
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "temperature_celsius": round(random.uniform(15, 35), 2),
        "humidity_percent": round(random.uniform(30, 80), 2)
    }


def publish_message(data: dict):
    message_json = json.dumps(data)
    message_bytes = message_json.encode("utf-8")

    future = publisher.publish(topic_path, message_bytes)
    print(f"Published message ID: {future.result()}")


def main():
    create_topic_if_not_exists()

    device_id = "sensor_1"

    while True:
        sensor_data = generate_sensor_data(device_id)
        publish_message(sensor_data)
        time.sleep(2)


if __name__ == "__main__":
    main()
