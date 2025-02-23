from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
from kafka import KafkaConsumer
import pandas as pd
import json
import boto3
import pyarrow.parquet as pq
from io import BytesIO

# Kafka Configuration
KAFKA_BROKER = "localhost:9092"
KAFKA_TOPIC = "real_time_data"
BATCH_SIZE = 100  # Number of messages per batch

# S3 Configuration
S3_BUCKET = "your-s3-bucket-name"
S3_FOLDER = "kafka_data/"
AWS_ACCESS_KEY = "your-access-key"
AWS_SECRET_KEY = "your-secret-key"

def fetch_and_store_kafka_messages():
    """Fetches messages from Kafka in batches and stores them as Parquet files in S3."""
    
    consumer = KafkaConsumer(
        KAFKA_TOPIC,
        bootstrap_servers=KAFKA_BROKER,
        value_deserializer=lambda x: json.loads(x.decode('utf-8')),
        auto_offset_reset='earliest',
        enable_auto_commit=True
    )

    messages = []
    for _ in range(BATCH_SIZE):
        msg = next(consumer, None)
        if msg:
            messages.append(msg.value)

    if not messages:
        print("No new messages found.")
        return

    # Convert to DataFrame
    df = pd.DataFrame(messages)

    # Convert DataFrame to Parquet format
    parquet_buffer = BytesIO()
    df.to_parquet(parquet_buffer, engine='pyarrow')

    # Upload to S3
    s3_client = boto3.client(
        's3',
        aws_access_key_id=AWS_ACCESS_KEY,
        aws_secret_access_key=AWS_SECRET_KEY
    )
    
    file_name = f"{S3_FOLDER}kafka_batch_{datetime.utcnow().strftime('%Y%m%d%H%M%S')}.parquet"
    s3_client.put_object(Bucket=S3_BUCKET, Key=file_name, Body=parquet_buffer.getvalue())

    print(f"Uploaded {len(messages)} records to S3: {file_name}")

# Airflow DAG Configuration
default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": datetime(2025, 1, 1),
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    "kafka_to_s3_dag",
    default_args=default_args,
    schedule_interval="*/5 * * * *",  # Runs every 5 minutes
    catchup=False
) as dag:

    task_fetch_and_store = PythonOperator(
        task_id="fetch_and_store_kafka_messages",
        python_callable=fetch_and_store_kafka_messages
    )

    task_fetch_and_store
