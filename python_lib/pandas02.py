import FinanceDataReader as fdr
import pandas as pd

# pip install xlsxwriter
# pip install openpyxl
# 한국 거래소 상장종목
df_krx = fdr.StockListing("KRX")
# print(df_krx.head())

# DataFrame 반복문
# DataFrame에서 열은 Series 객체
for value in df_krx['Name']:
    print(value)

# iterrows()
for idx, row in df_krx.iterrows():
    print(idx, row['Name'], row['Code'])

hanhwa = fdr.DataReader("000880") # 종목 코드만 입력 (전체)
# hanhwa = fdr.DataReader("000880", "2023") # 특정 년도
# hanhwa = fdr.DataReader("000880", "2024-01-01, "2024-02-20") # 특정 기간

with pd.ExcelWriter("hanhwa.xlsx", engine='openpyxl') as writer:
    hanhwa.to_excel(writer, sheet_name='sheet1')

