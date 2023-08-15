from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.providers.http.operators.http import SimpleHttpOperator
from airflow.decorators import task
import pendulum

with DAG(
    dag_id='dags_simple_http_operator',
    start_date=pendulum.datetime(2023, 8, 1, tz='Asia/Seoul'),
    catchup=False,
    schedule=None
) as dag:

    '''서울시립미술관 전시 현황'''
    tb_exhibition_info = SimpleHttpOperator(
        task_id='tb_exhibition_info',
        http_conn_id='openapi.seoul.go.kr',
        endpoint='{{var.value.apikey_openapi_seoul_go_kr}}/xml/ListExhibitionOfSeoulMOAInfo/1/10/', # 동일한 API 키로 여러 DAG이 개발된 상태에서 키 변경시 대응하거나, 
                                                                                                   # API 키를 코드에 노출시키지 않기 위해 전역변수 사용
        method='GET',
        headers={'Content-Type': 'application/xml',
                        'charset': 'utf-8',
                        'Accept': '*/*'
                        }
    )

    @task(task_id='python_2')
    def python_2(**kwargs):
        ti = kwargs['ti']
        rslt = ti.xcom_pull(task_ids='tb_exhibition_info')
        import json
        from pprint import pprint

        pprint(json.loads(rslt))
        
    tb_exhibition_info >> python_2()