from pendulum import datetime
from airflow.datasets import Dataset
from airflow.decorators import dag, task

INSTRUCTIONS = Dataset("file:///opt/airflow/dags/include/cocktail_instructions.txt")
INFO = Dataset("file:///opt/airflow/dags/include/cocktail_info.txt")


@dag(
    "datasets_consumer_dag",
    start_date=datetime(2024, 2, 27),
    schedule=[INSTRUCTIONS, INFO],  # Scheduled on both Datasets
    catchup=False,
    tags=["consumer", "dataset"]
)
def datasets_consumer_dag():
    @task
    def read_about_cocktail():
        cocktail = []
        for filename in ("info", "instructions"):
            with open(f"/opt/airflow/dags/include/cocktail_{filename}.txt", "r") as f:
                contents = f.readlines()
                cocktail.append(contents)

        return [item for sublist in cocktail for item in sublist]

    read_about_cocktail()


datasets_consumer_dag()