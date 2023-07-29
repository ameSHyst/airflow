from airflow import DAG
import pendulum
import datetime
from airflow.operators.bash import BashOperator

with DAG(
    dag_id="dags_bash_with_template",
    schedule="10 0 * * *",
    start_date=pendulum.datetime(2023, 7, 1, tz="Asia/Seoul"),
    catchup=False
) as dag:
    
    bash_t1= BashOperator(
        task_id='bash_t1',
        bash_command='echo "data_interval_end: {{ data_interval_end }} "'
    )
    
    bash_t2= BashOperator(
        task_id='bash_t2',
        env={
            'START_DATE': '{{data_interval_start | ds}}', # | ds 붙이면 yyyy-mm-dd 형태로 출력
            'END_DATE': '{{data_interval_end | ds}}'
        },
        bash_command='echo $START_DATE && echo $END_DATE'
    )
    
    bash_t1 >> bash_t2