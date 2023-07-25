from airflow import DAG
import datetime
import pendulum  
from airflow.operators.python import PythonOperator
from common.common_func import get_sftp # airflow에서는 opt/airflow/plugins까지 path로 잡혀있기 때문에
                                        # common 앞에 plugins.를 붙이면 dag에서 오류가 남
                                        # 하지만 이 상태에서는 실행 시 오류가 나기 때문에 .env에서 경로 추가
                                        # .env 파일은 git에 올릴 필요 없으니 .gitignore 파일에 추가

with DAG(
    dag_id="dags_python_import_func", 
    schedule="30 6 * * *",
    start_date=pendulum.datetime(2023, 7, 1, tz="Asia/Seoul"), 
    catchup=False 
) as dag:
    
    task_get_sftp = PythonOperator(
        task_id='task_get_sftp',
        python_callable=get_sftp
    )