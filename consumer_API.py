from kafka import KafkaConsumer
import requests

# Kafka consumer settings
bootstrap_servers = 'your_bootstrap_servers'
topic = 'your_kafka_topic'
group_id = 'your_group_id'

# API endpoint settings
api_endpoint = 'your_api_endpoint'

# Function to make an API call
def make_api_call(data):
    try:
        response = requests.post(api_endpoint, json=data)
        if response.status_code == 200:
            print("API call successful!")
        else:
            print(f"API call failed with status code: {response.status_code}")
    except Exception as e:
        print(f"Error making API call: {str(e)}")

# Create Kafka consumer
consumer = KafkaConsumer(
    topic,
    group_id=group_id,
    bootstrap_servers=bootstrap_servers,
    auto_offset_reset='earliest',  # Start consuming from the beginning of the topic
    enable_auto_commit=False,      # Disable auto-commit to control offset commits manually
)

# Consume messages from Kafka and trigger API call
for message in consumer:
    try:
        # Assuming message value is JSON
        data = json.loads(message.value.decode('utf-8'))
        make_api_call(data)
        
        # Commit offset manually
        consumer.commit()
    except Exception as e:
        print(f"Error processing message: {str(e)}")

