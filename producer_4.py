import time
import os

# Path to the file to monitor
file_path = 'your_file_to_monitor.txt'

# Function to monitor file modifications
def monitor_file_modifications(file_path):
    # Get the initial modification time of the file
    last_modified_time = os.path.getmtime(file_path)
    
    while True:
        # Check if the file has been modified
        current_modified_time = os.path.getmtime(file_path)
        if current_modified_time != last_modified_time:
            # File has been modified, trigger an event
            print("File has been modified!")
            # Additional actions can be performed here, such as calling an API
            # For simplicity, we'll just print the file content
            with open(file_path, 'r') as file:
                print("File content:")
                print(file.read())
            # Update last modified time
            last_modified_time = current_modified_time
        
        # Wait for a short interval before checking again
        time.sleep(1)

# Main function
def main():
    monitor_file_modifications(file_path)

if __name__ == '__main__':
    main()

