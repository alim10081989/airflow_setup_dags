from datetime import datetime

from airflow import DAG
from airflow.exceptions import AirflowSkipException
from airflow.operators.python import PythonOperator
from airflow.utils.trigger_rule import TriggerRule


def my_func(**context):
    # If the DagRun start date is not a Monday, then skip this task
    dag_run_start_date = context['dag_run'].start_date
    if dag_run_start_date.weekday() != 0:
        raise AirflowSkipException

    # Anything beyond this line will be executed only if the
    # task is not skipped, based on the condition specified above
    print('Hi from task_b')


with DAG(
    'skip_dag_check',
    start_date=datetime(2024, 2, 27),
    catchup=False,
    tags=['skip', 'tasks', 'example'],
    schedule_interval="@daily"
) as dag:
    first_task = PythonOperator(task_id='task_a', python_callable=lambda: print('Hi from task_a'))
    second_task = PythonOperator(task_id='task_b', python_callable=my_func)
    third_task = PythonOperator(
        task_id='task_c',
        python_callable=lambda: print('Hi form task_c'),
        trigger_rule=TriggerRule.NONE_FAILED
    )

    first_task >> second_task >> third_task