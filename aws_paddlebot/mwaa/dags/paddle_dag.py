from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
from paddle.paddle import book_paddle_automated
from paddle.data import data

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 9, 20),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
}

dag = DAG(
    'paddle_booking',
    default_args=default_args,
    description='Automate Paddle Court Booking',
    schedule_interval='35 2 * * 6',  # Every Saturday at 2:35 AM UTC (Friday 9:35 PM EST)
)

def run_paddle_script():
    book_paddle_automated(data.COURT1)
    book_paddle_automated(data.COURT2)

run_booking = PythonOperator(
    task_id='run_paddle_booking',
    python_callable=run_paddle_script,
    dag=dag,
)
