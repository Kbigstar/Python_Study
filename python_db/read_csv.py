import csv
# 파일경로
# csv_path = 'kospi_list.csv'
csv_path = 'kosdaq_list.csv'
dict_list = []
with open(csv_path, mode='r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    # 각 행을 추가
    for row in reader:
        dict_list.append(row)

import  sqlite3
conn = sqlite3.connect('mydb.db')
cursor = conn.cursor()
insert_sql = """
    INSERT INTO stock VALUES (?, ?, ?, ?, ?)
"""
for item in dict_list:
    cursor.execute(insert_sql
                   ,[ item['Code'], item['Name'], item['Market']
                    ,item['Marcap'], item['Stocks'] ])
conn.commit()
conn.close()