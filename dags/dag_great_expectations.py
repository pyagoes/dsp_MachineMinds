from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'MachineMinds',
    'depends_on_past': False,
    'start_date': datetime(2023, 6, 15),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'great_expectations_dag',
    default_args=default_args,
    description='Execute Great Expectations script every 5 minutes',
    schedule_interval=None,  # Disable automatic scheduling
)

task = BashOperator(
    task_id='run_great_expectations',
    bash_command='python /Users/paulayagoesparza/Documents/S2/DSP/LOCAL/data_validation/data_quality_validation.py',
    dag=dag,
)