from airflow import DAG
import datetime
import pendulum  # datetime 타입을 더 쉽게 쓸 수 있도록 하는 라이브러리
from airflow.operators.bash import BashOperator

with DAG(
    dag_id="dags_bash_operator", # 이 값이 Airflow 화면의 DAG 이름과 동일. 파이썬 파일명과는 무관함 주의
                                    # 강사님의 경험상 DAG 파일명과 DAG ID는 일치시키는 게 좋음
                                    # 나중에 DAG을 무수히 생성했을 때 파일 찾기가 용이하기 때문
    schedule="0 0 * * *", # 분/시/일/월/요일 순
    start_date=pendulum.datetime(2021, 1, 1, tz="Asia/Seoul"), # UTC는 한국 시간 - 9
    catchup=False, #start date부터 현재 일자 간의 누락된 구간까지 소급해서 돌릴지 여부 결정.
                    #True로 설정해서 돌릴 경우 처음부터 차례로 돌지 않고 한꺼번에 돌기 때문에 웬만하면 False임
    # tags=["example", "example2"], #DAG명 아래 파란 박스
) as dag:
    bash_t1 = BashOperator(
        task_id="bash_t1", # 파이썬 파일명-DAG id의 관계와는 달리 상관 없지만 역시 편의상 객체명과 동일하게 설정
        bash_command="echo whoami", # echo = print라 생각
    )
    bash_t2 = BashOperator(
        task_id="bash_t2", 
        bash_command="echo $HOSTNAME", # HOSTNAME이라는 환경변수 값을 출력
    )
    
    bash_t1 >> bash_t2