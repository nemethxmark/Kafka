from airflow import DAG
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults
from airflow.sensors.base_sensor_operator import BaseSensorOperator
from kafka import KafkaConsumer
from datetime import datetime, timedelta

class KafkaMessageSensor(BaseSensorOperator):
    """
    Custom sensor to listen for messages on a Kafka topic.
    """
    @apply_defaults
    def __init__(self, kafka_topic, bootstrap_servers, group_id, *args, **kwargs):
        super(KafkaMessageSensor, self).__init__(*args, **kwargs)
        self.kafka_topic = kafka_topic
        self.bootstrap_servers = bootstrap_servers
        self.group_id = group_id

    def poke(self, context):
        try:
            consumer = KafkaConsumer(
                self.kafka_topic,
                group_id=self.group_id,
                bootstrap_servers=self.bootstrap_servers,
                auto_offset_reset='earliest',  # Adjust as needed
                enable_auto_commit=False,  # Disable auto-commit to control offset commits manually
            )

            for message in consumer:
                # If a message is received, trigger the DAG
                return True
        except Exception as e:
            self.log.error("Error while consuming Kafka message: %s", str(e))
            return False

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 1, 1),
    'retries': 1,
}

with DAG('kafka_trigger_dag', default_args=default_args, schedule_interval=None) as dag:

    wait_for_kafka_message = KafkaMessageSensor(
        task_id='wait_for_kafka_message',
        kafka_topic='your_kafka_topic',
        bootstrap_servers='your_bootstrap_servers',
        group_id='airflow',
        poke_interval=10,  # Adjust as needed
    )

    # Define other tasks here

    wait_for_kafka_message >> other_tasks

