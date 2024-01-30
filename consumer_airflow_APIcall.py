from airflow import DAG
from airflow.operators.http_operator import SimpleHttpOperator
from airflow.operators.dummy_operator import DummyOperator
from airflow.utils.dates import days_ago
from datetime import datetime, timedelta
from airflow.sensors.base_sensor_operator import BaseSensorOperator
from kafka import KafkaConsumer

# Define the DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': days_ago(1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'kafka_to_api_dag',
    default_args=default_args,
    description='A DAG triggered by a Kafka message, which then makes an API call',
    schedule_interval=None,
)

# Define the sensor to listen for Kafka messages
class KafkaMessageSensor(BaseSensorOperator):
    def __init__(self, topic, bootstrap_servers, group_id, **kwargs):
        super().__init__(**kwargs)
        self.topic = topic
        self.bootstrap_servers = bootstrap_servers
        self.group_id = group_id

    def poke(self, context):
        try:
            consumer = KafkaConsumer(
                self.topic,
                group_id=self.group_id,
                bootstrap_servers=self.bootstrap_servers,
                auto_offset_reset='earliest',
                enable_auto_commit=False,
            )
            for message in consumer:
                return True
        except Exception as e:
            self.log.error("Error while consuming Kafka message: %s", str(e))
            return False

# Define the Kafka sensor task
kafka_sensor_task = KafkaMessageSensor(
    task_id='kafka_sensor_task',
    topic='your_kafka_topic',
    bootstrap_servers='your_bootstrap_servers',
    group_id='airflow',
    dag=dag,
)

# Define the API call task
api_call_task = SimpleHttpOperator(
    task_id='api_call_task',
    method='POST',
    http_conn_id='your_http_conn_id',  # The connection ID configured in Airflow for your HTTP endpoint
    endpoint='your_api_endpoint',      # The endpoint of your API
    data='{"key": "value"}',           # The data to send with the request (if needed)
    headers={"Content-Type": "application/json"},  # Headers for the request
    dag=dag,
)

# Define the final task (dummy task)
final_task = DummyOperator(task_id='final_task', dag=dag)

# Define the execution sequence
kafka_sensor_task >> api_call_task >> final_task

