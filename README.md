# Airflow Setup

- Create folders ```dags,plugins,logs``` under ```airflow``` directory at any chosen path within system

```
mkdir -p airflow/{dags,plugins,logs}
```

- Place ```docker-compose.yml``` file under ```airflow``` directory.
- Run below command

```
docker-compose up airflow-init
docker-compose up
```

- Access airflow at url ```http://localhost:8080```.
- Place dag files available under [dags](../dags/) under folder ```{directory}/dags``` and it should be displayed on the airflow ```DAGS``` section.