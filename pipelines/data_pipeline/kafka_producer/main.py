import requests
import time
import json
import random
from kafka import KafkaProducer

# ----------------------------------------------------

TOPIC = "anomaly_detection_topic"

# API Configuration
API_URL = "http://localhost:8000/generate"  # Use "/generate/normal" or "/generate/anomalous" for specific data

# ----------------------------------------------------

# Kafka Configuration
producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)


def fetch_data_from_api():
    try:
        response = requests.get(API_URL)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"API Error: {response.status_code}")
            return None
    except Exception as e:
        print(f"Failed to fetch data: {e}")
        return None

def send_to_kafka(data):
    if data:
        producer.send(TOPIC, value=data)
        producer.flush()
        print(f"Sent to Kafka: {data}")

if __name__ == "__main__":
    while True:
        data = fetch_data_from_api()
        if data:
            send_to_kafka(data)
        time.sleep(random.uniform(0.1, 1.0))  # Simulate real-time intervals