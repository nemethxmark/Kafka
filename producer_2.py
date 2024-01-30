import time
import json
import requests
from confluent_kafka import Producer

# Kafka broker settings
bootstrap_servers = 'localhost:9092'
topic = 'walkme_data'

# WalkMe API endpoint and authentication details
walkme_api_url = 'YOUR_WALKME_API_ENDPOINT'
client_id = 'YOUR_CLIENT_ID'
client_secret = 'YOUR_CLIENT_SECRET'

def get_access_token():
    auth_url = 'https://oauth.walkme.com/oauth/token'
    data = {
        'grant_type': 'client_credentials',
        'client_id': client_id,
        'client_secret': client_secret
    }
    response = requests.post(auth_url, data=data)
    return response.json()['access_token']

def fetch_walkme_data(access_token):
    headers = {
        'Authorization': f'Bearer {access_token}',
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
    # Get access token
    access_token = get_access_token()

    # Kafka producer configuration
    conf = {
        'bootstrap.servers': bootstrap_servers
    }
    producer = Producer(conf)

    try:
        while True:
            # Fetch data from WalkMe API using the access token
            walkme_data = fetch_walkme_data(access_token)

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

