import sqlite3
conn = sqlite3.connect('mydb.db')
cur = conn.cursor()
cur.execute("SELECT * FROM stock WHERE market = 'KOSPI'")

#  커서는 휘발성이라 저장하여 사용해야 한다. [1회성]
# for row in cur:
#     print(row)

rows = cur.fetchall() # 전체
# 한개 fetchone(), 일부 fetchmany(3) (보통 all을 쓰고 쿼리문으로 조작)
conn.close()
for row in rows:
    print(row)

