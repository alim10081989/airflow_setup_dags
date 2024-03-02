from airflow import DAG
from airflow.decorators import task
from airflow.operators.bash import BashOperator
from airflow.operators.trigger_dagrun import TriggerDagRunOperator
from datetime import datetime

# upstream DAG
with DAG(
  dag_id="upstream_trigger_dag",
  start_date=datetime(2024, 2, 28),
  schedule_interval="@daily",
  tags=["downstreamB", "parent", "trigger"]
) as dag:
  start_task = BashOperator(
    task_id="start_task",
    bash_command="echo 'Start task'",
  )
  trigger_A = TriggerDagRunOperator(
    task_id="trigger_A",
    trigger_dag_id="downstream_dag_A",
    conf={"message":"Message to pass to downstream DAG A."},
  )
  trigger_B = TriggerDagRunOperator(
    task_id="trigger_B",
    trigger_dag_id="downstream_dag_B",
    conf={"message":"Message to pass to downstream DAG B."},
  )
  start_task >> trigger_A >> trigger_B

# downstream DAG A
with DAG(
  dag_id="downstream_dag_A",
  start_date=datetime(2024, 2, 28),
  schedule_interval="@daily",
  tags=["downstreamA", "child", "trigger"]
) as dag:
  downstream_task = BashOperator(
    task_id="downstream_task_A",
    bash_command='echo "Upstream message: $message"',
    env={"message": '{{ dag_run.conf.get("message") }}'},
)

# downstream DAG B
with DAG(
  dag_id="downstream_dag_B",
  start_date=datetime(2024, 2, 28),
  schedule_interval="@daily",
  tags=["downstreamB", "child", "trigger"]
) as dag:
  downstream_task = BashOperator(
    task_id="downstream_task_B",
    bash_command='echo "Upstream message: $message"',
    env={"message": '{{ dag_run.conf.get("message") }}'},
)