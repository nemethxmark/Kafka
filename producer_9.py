import time
import random

# Function to simulate sensor data
def generate_sensor_data():
    # Simulate sensor readings
    temperature = random.uniform(20, 30)  # Temperature in Celsius
    humidity = random.uniform(40, 60)     # Humidity in percentage
    
    return temperature, humidity

# Function to monitor sensor data
def monitor_sensor_data():
    while True:
        # Generate sensor data
        temperature, humidity = generate_sensor_data()
        
        # Check if sensor readings exceed thresholds
        if temperature > 25:
            # Trigger an event (e.g., call an API)
            print(f"Temperature exceeds threshold: {temperature}°C")
            # Additional actions can be performed here
        
        if humidity > 50:
            # Trigger an event (e.g., call an API)
            print(f"Humidity exceeds threshold: {humidity}%")
            # Additional actions can be performed here
        
        # Wait for a short interval before generating new data
        time.sleep(1)

# Main function
def main():
    monitor_sensor_data()

if __name__ == '__main__':
    main()

