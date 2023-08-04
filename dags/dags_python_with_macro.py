from airflow import DAG
import pendulum
from airflow.decorators import task

with DAG(
    dag_id="dags_python_with_macro",
    schedule="10 0 * * *",
    start_date=pendulum.datetime(2023, 8, 1, tz="Asia/Seoul"),
    catchup=False
) as dag:
    
    @task(task_id='task_using_macros',
      templates_dict={'start_date':'{{ (data_interval_end.in_timezone("Asia/Seoul") + macros.dateutil.relativedelta.relativedelta(months=-1, day=1)) | ds }}',
                      'end_date': '{{ (data_interval_end.in_timezone("Asia/Seoul").replace(day=1) + macros.dateutil.relativedelta.relativedelta(days=-1)) | ds }}'
     }
    )
    def get_datetime_macro(**kwargs): # 'templates_dict'(str 그대로) 가 key 값이 되고 뒤에 선언된 함수 전체가 value 값이 됨
        
        templates_dict = kwargs.get('templates_dict') or {} # 위 딕셔너리 전체가 할당된 상태
        if templates_dict:
            start_date = templates_dict.get('start_date') or 'start_date 없음'
            end_date = templates_dict.get('end_date') or 'end_date 없음'
            print(start_date)
            print(end_date)


    @task(task_id='task_direct_calc')
    def get_datetime_calc(**kwargs):
        from dateutil.relativedelta import relativedelta # 라이브러리를 task decorator 안에 따로 선언한 이유? : 스케줄러 부하 경감
                                                         # 파일 맨 상단, with DAG 시작 전, operator 시작 전 부분에서의 선언 내용이 많을수록 스케줄러가 많은 부하를 받음
                                                         # 대규모 환경에서는 이 문제로 골치를 많이 썩음 -> DAG 설계시 잘 고려해야
        data_interval_end = kwargs['data_interval_end']
        prev_month_day_first = data_interval_end.in_timezone('Asia/Seoul') + relativedelta(months=-1, day=1)
        prev_month_day_last = data_interval_end.in_timezone('Asia/Seoul').replace(day=1) +  relativedelta(days=-1)
        print(prev_month_day_first.strftime('%Y-%m-%d'))
        print(prev_month_day_last.strftime('%Y-%m-%d'))

    get_datetime_macro() >> get_datetime_calc()