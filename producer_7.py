import time
import os

# Directory to monitor
directory_path = 'your_directory_to_monitor'

# Function to monitor directory for new files
def monitor_directory_changes(directory_path):
    # Get the initial list of files in the directory
    initial_files = set(os.listdir(directory_path))
    
    while True:
        # Get the current list of files in the directory
        current_files = set(os.listdir(directory_path))
        
        # Find new files (files in current_files but not in initial_files)
        new_files = current_files - initial_files
        
        # Process new files
        for file in new_files:
            # Trigger an event (e.g., call an API)
            print("New file created:", os.path.join(directory_path, file))
            # Additional actions can be performed here
            
        # Update initial_files for the next iteration
        initial_files = current_files
        
        # Wait for a short interval before checking again
        time.sleep(1)

# Main function
def main():
    monitor_directory_changes(directory_path)

if __name__ == '__main__':
    main()

