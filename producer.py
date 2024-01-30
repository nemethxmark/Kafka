import time
import json
import requests
from confluent_kafka import Producer

# Kafka broker settings
bootstrap_servers = 'localhost:9092'
topic = 'walkme_data'

# WalkMe API endpoint
walkme_api_url = 'YOUR_WALKME_API_ENDPOINT'
api_key = 'YOUR_API_KEY'

def fetch_walkme_data():
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }
    response = requests.get(walkme_api_url, headers=headers)
    return response.json()

def delivery_callback(err, msg):
    if err:
        print(f'Message delivery failed: {err}')
    else:
        print(f'Message delivered to {msg.topic()} [{msg.partition()}]')

def produce_to_kafka(producer, data):
    producer.produce(topic, json.dumps(data), callback=delivery_callback)
    producer.poll(0)
    producer.flush()

if __name__ == '__main__':
    # Kafka producer configuration
    conf = {
        'bootstrap.servers': bootstrap_servers
    }
    producer = Producer(conf)

    try:
        while True:
            # Fetch data from WalkMe API
            walkme_data = fetch_walkme_data()

            # Produce data to Kafka
            produce_to_kafka(producer, walkme_data)

            # Wait for 60 seconds
            time.sleep(60)
    except KeyboardInterrupt:
        pass
    finally:
        # Close the Kafka producer
        producer.flush()
        producer.close()

