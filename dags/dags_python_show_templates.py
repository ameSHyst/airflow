from airflow import DAG
import pendulum
import datetime
from airflow.decorators import task

with DAG(
    dag_id="dags_python_show_template",
    schedule="30 9 * * *",
    start_date=pendulum.datetime(2023, 7, 10, tz="Asia/Seoul"),
    catchup=True # 7/10 ~ 7/29 사이 구간 모두 수행
) as dag:
    
    @task(task_id='python_task')
    def show_templates(**kwargs):
        from pprint import pprint # 줄넘김 등을 좀 더 예쁘게 print해줌
        pprint(kwargs)
        
    show_templates()