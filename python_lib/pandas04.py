import pandas as pd
from DBManager import DBManager
import FinanceDataReader as fdr

db = DBManager()
conn = db.get_connection()
sql = """
        SELECT *
        FROM stock
        WHERE use_yn = 'Y'
"""
insert_sql = """
    INSERT INTO stock_price (code, seq, price, create_dt)
    VALUES (:1, stock_seq.NEXTVAL, :2, :3)
"""

df = pd.read_sql(con = conn, sql = sql)
# print(df.head())
for idx, row in df.iterrows():
    code = row['CODE']
    name = row['NAME']
    print(code, name)
    stock_data = fdr.DataReader(code)

    #  날짜 index를 -> 컬럼으로 -> 타입을 문자열 년월일로
    stock_df = stock_data.reset_index()
    date = stock_df['Date'].dt.strftime('%Y-%m-%d')
    stock_df['Close'].astype(str) # 문자열로
    stock_df['Date'] = date
    print(stock_data.head())

    for i, v in stock_df.iterrows():
        try:
            db.insert(insert_sql, [code, v['Close'], v['Date']])
        except Exception as e:
            print(str(e))

