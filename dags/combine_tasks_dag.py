import os
from datetime import datetime
import requests
from airflow import DAG
from airflow.decorators import task
from airflow.operators.python_operator import PythonOperator
import logging

with DAG('combine_tasks_demo', description='Combine dag tasks in workflow',
          schedule_interval='@daily',
          start_date=datetime(2024, 2, 27), 
          catchup=False,
          tags=['combine', 'sequence', 'tasks']
          ) as dag:
    @task
    def start():
        pass
    @task
    def do_first_task():
        pass
    @task
    def do_second_task():
        pass
    @task
    def do_third_task_with_second_task():
        pass
    @task
    def do_forth_task():
        pass
    @task
    def goodbye_link_to_all():
        pass
    start() >> do_first_task() >> [do_second_task(), do_third_task_with_second_task()]
    list(dag.tasks) >> goodbye_link_to_all()