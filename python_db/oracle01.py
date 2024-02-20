# pip install cx_Oracle
import cx_Oracle
import csv
conn = cx_Oracle.connect("study", "study", "127.0.0.1:1521/xe")
# 파일경로
csv_path = 'kospi_list.csv'
dict_list = []
with open(csv_path, mode='r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    # 각 행을 추가
    for row in reader:
        dict_list.append(row)
cursor = conn.cursor()
insert_sql = """
    INSERT INTO stock (code, name, market, marcap, stocks)
    VALUES (:1, :2, :3, :4, :5)
"""
for item in dict_list:
    cursor.execute(insert_sql
                   ,[ item['Code'], item['Name'], item['Market']
                    ,item['Marcap'], item['Stocks'] ])
conn.commit()
conn.close()
