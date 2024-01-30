import time
import psycopg2
from psycopg2 import OperationalError

# Database connection settings
db_host = 'your_db_host'
db_port = 'your_db_port'
db_name = 'your_db_name'
db_user = 'your_db_user'
db_password = 'your_db_password'

# Table to monitor
table_name = 'your_table_name'

# Function to monitor database table for new records
def monitor_database_changes():
    conn = None
    last_max_id = 0
    
    try:
        # Connect to the database
        conn = psycopg2.connect(
            dbname=db_name,
            user=db_user,
            password=db_password,
            host=db_host,
            port=db_port
        )
        
        while True:
            # Query the database for new records
            cursor = conn.cursor()
            cursor.execute(f"SELECT * FROM {table_name} WHERE id > %s", (last_max_id,))
            records = cursor.fetchall()
            
            # Process new records
            for record in records:
                # Trigger an event (e.g., call an API)
                print("New record inserted:", record)
                # Additional actions can be performed here
                
                # Update last_max_id
                last_max_id = max(record[0], last_max_id)
                
            # Close cursor
            cursor.close()
            
            # Wait for a short interval before checking again
            time.sleep(1)
    
    except OperationalError as e:
        print(f"Error connecting to the database: {e}")
    
    finally:
        # Close database connection
        if conn is not None:
            conn.close()

# Main function
def main():
    monitor_database_changes()

if __name__ == '__main__':
    main()

