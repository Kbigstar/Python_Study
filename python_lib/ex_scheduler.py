# 주기적으로 실행할 수 있게 해주는 라이브러리
# pip install apscheduler
import datetime

from apscheduler.schedulers.blocking import BlockingScheduler
import pytz
seoul = pytz.timezone('Asia/Seoul')


# interval : 주기적으로 실행
# cron : 원하는 시간, 다양한 시간에 실행
def test_interval():
    print("interval")
    print(datetime.datetime.now())

def test_cron():
    print("cron")
    print(datetime.datetime.now())
sched = BlockingScheduler()
#  job 등록 10초 마다 함수 호출
sched.add_job(test_interval, 'interval', seconds = 1, timezone = seoul)
#  cron 원하는 주기, 시간설정 ㅡmo
sched.add_job(test_cron, 'cron', day_of_week='mon-fri', hour = '15', minute = '38', timezone = seoul)
sched.start()