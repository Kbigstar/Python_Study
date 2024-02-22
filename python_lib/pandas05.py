import pandas as pd
from DBManager import DBManager
import requests
import json

db = DBManager()
conn = db.get_connection()
sql = """
        SELECT *
        FROM stock
        WHERE use_yn = 'Y'
"""

merge_sql = '''
MERGE
    INTO stock_bbs a
    USING dual 
        ON (a.code = :1
            and a.discussion_id = :2)
WHEN MATCHED THEN
    UPDATE 
        SET read_count = :3
            , good_count = :4
            , bad_count = :5
            , comment_count = :6
WHEN NOT MATCHED THEN
    INSERT (a.code, a.discussion_id, a.read_count, a.good_count, a.bad_count
        , a.comment_count, a.title, a.contents, a.create_dt)
    VALUES (:7, :8, :9, :10, :11, :12, :13, :14, to_date(:15, 'YYYY-MM-DD HH24:MI:SS'))
'''

df = pd.read_sql(con = conn, sql = sql)
# print(df.head())
for idx, row in df.iterrows():
    code = row['CODE']
    name = row['NAME']
    print(code, name)
    url = "https://m.stock.naver.com/api/discuss/localStock/{0}?rsno=0&size=100".format(code)
    res = requests.get(url)
    json_data = json.loads(res.text)
    for v in json_data:
        print(v)

        discussionId = v['discussionId']
        title = v['title']
        contents = v['contents']
        readCount = v['readCount']
        goodCount = v['goodCount']
        badCount = v['badCount']
        commentCount = v['commentCount']
        date = v['date'][:19]

        try:
            db.insert(merge_sql, [code, discussionId
                , readCount, goodCount, badCount, commentCount,
                                  code, discussionId, readCount, goodCount, badCount, commentCount, title, contents, date])
        except Exception as e:
            print(str(e))