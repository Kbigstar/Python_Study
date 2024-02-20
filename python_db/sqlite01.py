import sqlite3
# sqlite3 경량 db
# 파일이 db임, 경량db이기 때문에 (여러 유저 사용은 X)
conn = sqlite3.connect("mydb.db")
# 일회성 사용은 :memory:
sql = """
     CREATE TABLE stock (
            code VARCHAR2(10) PRIMARY KEY
           ,name VARCHAR2(100)
           ,market VARCHAR2(10)
           ,marcap NUMBER
           ,stocks NUMBER
     )
"""
cur = conn.cursor()
cur.execute(sql)
conn.close()


