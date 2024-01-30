import time
import psutil

# CPU threshold to trigger an event (in percentage)
cpu_threshold = 80

# Function to monitor CPU usage
def monitor_cpu_usage():
    while True:
        # Get current CPU usage
        cpu_usage = psutil.cpu_percent(interval=1)
        
        # Check if CPU usage exceeds the threshold
        if cpu_usage > cpu_threshold:
            # Trigger an event (e.g., call an API)
            print(f"CPU usage exceeds threshold ({cpu_threshold}%): {cpu_usage}%")
            # Additional actions can be performed here
        
        # Wait for a short interval before checking again
        time.sleep(1)

# Main function
def main():
    monitor_cpu_usage()

if __name__ == '__main__':
    main()

