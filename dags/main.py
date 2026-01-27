from airflow import DAG
import pendulum
from datetime import datetime, timedelta
from airflow.operators.trigger_dagrun import TriggerDagRunOperator

from api.video_stats import (
    get_play_list_id,
    get_videos_id,
    extracted_data,
    save_to_json,
)

# Define the local timezone
local_tz = pendulum.timezone("Asia/Kolkata")

# Default Args
default_args = {
    "owner": "dataengineers",
    "depends_on_past": False,
    "email_on_failure": False,
    "email_on_retry": False,
    "email": "data@engineers.com",
    # 'retries': 1,
    # 'retry_delay': timedelta(minutes=5),
    "max_active_runs": 1,
    "dagrun_timeout": timedelta(hours=1),
    "start_date": datetime(2025, 1, 1, tzinfo=local_tz),
    # 'end_date': datetime(2030, 12, 31, tzinfo=local_tz),
}


# DAG 1: produce_json
with DAG(
    dag_id="produce_json",
    default_args=default_args,
    description="DAG to produce JSON file with raw data",
    schedule="0 14 * * *",
    catchup=False,
) as dag:

    # Define tasks
    playlist_id = get_play_list_id()
    video_ids = get_videos_id(playlist_id)
    extract_data = extracted_data(video_ids)
    save_to_json_task = save_to_json(extract_data)

    # Define dependencies
    playlist_id >> video_ids >> extract_data >> save_to_json_task