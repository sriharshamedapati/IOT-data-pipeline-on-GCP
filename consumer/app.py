import os
import json
import time
import mysql.connector
from datetime import datetime, timezone
from google.cloud import pubsub_v1
from mysql.connector import Error

print("RUNNING UPDATED CONSUMER FILE")

# ===============================
# Environment variables
# ===============================

PROJECT_ID = os.getenv("GCP_PROJECT_ID", "local-project")
TOPIC_ID = os.getenv("PUBSUB_TOPIC_RAW", "iot-sensor-data-raw")
SUBSCRIPTION_ID = "iot-sensor-sub"

# DO NOT override PUBSUB_EMULATOR_HOST here
# Docker compose already provides it

MYSQL_HOST = os.getenv("MYSQL_HOST", "mysql-db")
MYSQL_USER = os.getenv("MYSQL_USER", "root")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "password123")
MYSQL_DATABASE = os.getenv("MYSQL_DATABASE", "iot_data")

# ===============================
# Create Pub/Sub clients
# ===============================

subscriber = pubsub_v1.SubscriberClient()
publisher = pubsub_v1.PublisherClient()

topic_path = publisher.topic_path(PROJECT_ID, TOPIC_ID)
subscription_path = subscriber.subscription_path(PROJECT_ID, SUBSCRIPTION_ID)

# ===============================
# MySQL Connection with Retry
# ===============================

def create_db_connection():
    retries = 20

    while retries > 0:
        try:
            print("Trying to connect to MySQL...")

            connection = mysql.connector.connect(
                host=MYSQL_HOST,
                user=MYSQL_USER,
                password=MYSQL_PASSWORD,
                database=MYSQL_DATABASE,
                port=3306
            )

            if connection.is_connected():
                print("MySQL connected successfully ✅")
                return connection

        except Error as e:
            print("MySQL not ready yet. Retrying in 5 seconds...")
            print("Error:", e)
            retries -= 1
            time.sleep(5)

    raise Exception("Could not connect to MySQL after retries.")

print("Creating global DB connection...")

db_conn = create_db_connection()
db_cursor = db_conn.cursor()

print("Global DB connection ready.")

# ===============================
# Topic setup
# ===============================

def create_topic_if_not_exists():
    try:
        publisher.create_topic(request={"name": topic_path})
        print("Topic created.")
    except Exception:
        print("Topic already exists.")

# ===============================
# Subscription setup
# ===============================

def create_subscription_if_not_exists():
    try:
        subscriber.create_subscription(
            name=subscription_path,
            topic=topic_path,
        )
        print("Subscription created.")
    except Exception:
        print("Subscription already exists.")

# ===============================
# Validation logic
# ===============================

def validate_message(data: dict):

    required_fields = [
        "device_id",
        "timestamp_utc",
        "temperature_celsius",
        "humidity_percent",
    ]

    for field in required_fields:
        if field not in data:
            raise ValueError(f"Missing field: {field}")

    temperature = float(data["temperature_celsius"])
    humidity = float(data["humidity_percent"])

    if not (-50 <= temperature <= 100):
        raise ValueError("Temperature out of range")

    if not (0 <= humidity <= 100):
        raise ValueError("Humidity out of range")

    datetime.fromisoformat(data["timestamp_utc"])

# ===============================
# Message callback
# ===============================

def callback(message):

    print("CALLBACK TRIGGERED")

    try:
        raw = message.data.decode("utf-8")
        print(f"Received raw: {raw}")

        data = json.loads(raw)
        print("JSON parsed")

        validate_message(data)
        print("Validation passed")

        insert_query = """
        INSERT INTO sensor_readings
        (device_id, timestamp_utc, temperature_celsius, humidity_percent, processing_timestamp_utc)
        VALUES (%s, %s, %s, %s, %s)
        """

        values = (
            data["device_id"],
            datetime.fromisoformat(data["timestamp_utc"]),
            float(data["temperature_celsius"]),
            float(data["humidity_percent"]),
            datetime.now(timezone.utc)
        )

        db_cursor.execute(insert_query, values)
        db_conn.commit()

        print("Inserted into MySQL ✅")

        message.ack()

    except Exception as e:
        print("ERROR OCCURRED:")
        print(e)
        message.ack()

# ===============================
# Main listener
# ===============================

def main():
    create_topic_if_not_exists()
    create_subscription_if_not_exists()

    streaming_pull_future = subscriber.subscribe(
        subscription_path,
        callback=callback
    )

    print("Listening for messages...")

    try:
        streaming_pull_future.result()
    except KeyboardInterrupt:
        streaming_pull_future.cancel()

if __name__ == "__main__":
    main()
