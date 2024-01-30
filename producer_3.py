import time
import json
import requests
from kafka import KafkaProducer

# Kafka producer settings
bootstrap_servers = 'your_bootstrap_servers'
topic = 'your_kafka_topic'

# API endpoint settings
api_endpoint = 'your_api_endpoint'

# Function to monitor something and trigger API call
def monitor_and_call_api():
    # Example: Monitor a file for changes
    # Replace this with your own monitoring logic
    while True:
        # Check for changes in the file
        # If an event occurs, read the data and call the API
        try:
            with open('your_file_to_monitor.txt', 'r') as file:
                data = file.read()
                if data:
                    # Call the API endpoint
                    response = requests.post(api_endpoint, json={'data': data})
                    if response.status_code == 200:
                        print("API call successful!")
                        return data  # Return the data to be sent to Kafka
                    else:
                        print(f"API call failed with status code: {response.status_code}")
        except Exception as e:
            print(f"Error monitoring and calling API: {str(e)}")
        time.sleep(1)  # Adjust sleep time as needed

# Function to produce data to Kafka
def produce_to_kafka(data):
    producer = KafkaProducer(bootstrap_servers=bootstrap_servers)
    producer.send(topic, json.dumps(data).encode('utf-8'))
    producer.flush()
    producer.close()

# Main function
def main():
    while True:
        # Monitor something and call API
        data = monitor_and_call_api()
        
        # If data is returned from the API call, produce it to Kafka
        if data:
            produce_to_kafka(data)

if __name__ == '__main__':
    main()

