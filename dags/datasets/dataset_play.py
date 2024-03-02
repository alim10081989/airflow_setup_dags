from airflow import DAG, Dataset
# from airflow.datasets import Dataset
from airflow.operators.bash import BashOperator

import pendulum

account_dimension = Dataset("file:///opt/airflow/dags/reporting/dim_accounts")
sku_dimension = Dataset("file:///opt/airflow/dags/reporting/dim_sku")
fact_table1 = Dataset("file:///opt/airflow/dags/reporting/fact_table1")
fact_table2 = Dataset("file:///opt/airflow/dags/reporting/fact_table2")

with DAG(
    "load_reporting_dim_accounts",
    catchup=False,
    start_date=pendulum.datetime(2024, 2, 27, tz="UTC"),
    schedule_interval="@daily",
    tags=["producer_accounts", "dataset"],
) as dag1:
    BashOperator(outlets=[account_dimension], task_id="producing_task_1", 
                 bash_command="sleep 5")

with DAG(
    "load_reporting_dim_sku",
    catchup=False,
    start_date=pendulum.datetime(2024, 2, 27, tz="UTC"),
    schedule_interval="@daily",
    tags=["producer_sku", "dataset"],
) as dag1:
    BashOperator(outlets=[sku_dimension], task_id="producing_task_1", 
                 bash_command="sleep 5")


with DAG(
    "load_reporting_fact_table1",
    catchup=False,
    start_date=pendulum.datetime(2024, 2, 27, tz="UTC"),
    schedule=[account_dimension,sku_dimension],
    tags=["consumes_account", "consumes_sku", "dataset"],
) as dag3:
    # [END dag_dep]
    BashOperator(
        outlets=[fact_table1],
        task_id="consuming_1",
        bash_command="sleep 5",
    )

with DAG(
    "load_reporting_fact_table2",
    catchup=False,
    start_date=pendulum.datetime(2024, 2, 27, tz="UTC"),
    schedule=[fact_table1,sku_dimension],
    tags=["consumes_fact_tables1", "consumes_sku", "dataset"],
) as dag4:
    # [END dag_dep]
    BashOperator(
        task_id="consuming_1",
        bash_command="sleep 5",
    )