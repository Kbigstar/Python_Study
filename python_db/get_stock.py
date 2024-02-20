sql = { 'select_data': '''
                        SELECT *
                        FROM stock
                        WHERE USE_YN ='Y'
                        '''
       , 'insert_data': '''
                  INSERT INTO stock_price (code, seq, price)
                  VALUES (:1, stock_seq.NEXTVAL, :2)
                  '''
       }
# 정해진 시간 마다
# 조회 종목의 현재가를 수집하여 stock_price 테이블에 저장 함.

import cx_Oracle
import naver_price
from apscheduler.schedulers.blocking import BlockingScheduler
import pytz
import datetime
import mylogger as logger
log = logger.make_logger("stock.log", "get_stock.py")
seoul = pytz.timezone("Asia/Seoul")

def fn_current_price():
       # print("수집 시작!")
       # print(datetime.datetime.now())
       log.info("fn_current_price start!!")
       # conn = cx_Oracle.connect("study", ?, "127.0.0.1:1521/xe")
       # 실행시 ? <-- 비밀번호로 바꾸기
       cur = conn.cursor()
       cur.execute(sql['select_data'])
       rows = cur.fetchall()

       try:
              for row in rows:
                     code = row[0]
                     nm = row[1]
                     price = naver_price.get_price(code)
                     print(code, nm, price)
                     cur.execute(sql['insert_data'], [code, price])
       except Exception as e: # 오류 발생시
              log.exception(str(e))
              conn.rollback()
       else: # 오류 없이 정상 처리시
              conn.commit()
       finally: # 오류, 정상 모두 마지막에 수행
              conn.close()
# fn_current_price()

if __name__ == '__main__':
       log.info("start stock scheduler")
       sched = BlockingScheduler()
       sched.add_job(fn_current_price, 'interval',minutes = 2, timezone = seoul)
       print("스케줄러 작동!!")
       sched.start()
