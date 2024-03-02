from datetime import datetime

from airflow import DAG
from airflow.decorators import task

with DAG('called_dag', description='Target DAG called',
          schedule_interval='0 */2 * * *',
          start_date=datetime(2022, 8, 18), catchup=False,
          tags=["child", "remote", "trigger"]
          ) as dag:
    @task(task_id='start', retries=2)
    def start():
        context = {}
        my_file_name = 'fintechexplained{date}'.format(date=datetime.now())
        context['my_file_name'] = my_file_name
        return context
    @task
    def main(context):
        my_file_name = context['my_file_name']
        print(f'main-->{my_file_name}')
        return context
    @task
    def end(context):
        my_file_name = context['my_file_name']
        print(f'end-->{my_file_name}')

    data = start()
    result = main(data)
    end(result)