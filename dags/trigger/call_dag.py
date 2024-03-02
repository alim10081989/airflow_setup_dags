from datetime import datetime

from airflow import DAG
from airflow.decorators import task
from airflow.operators.trigger_dagrun import TriggerDagRunOperator

with DAG('calling_dag', description='Call dag using trigger run operator',
          schedule_interval='@daily',
          start_date=datetime(2024, 2, 27), catchup=False,
          tags=["parent", "remote", "trigger"]
          ) as dag:
    @task
    def start():
        print('start')


    trigger_pass_data = TriggerDagRunOperator(
        task_id="trigger_run",
        trigger_dag_id="called_dag",
        dag=dag,
    )

    start() >> trigger_pass_data