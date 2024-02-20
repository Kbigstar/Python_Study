import datetime

# 현재 날짜와 시간
now = datetime.datetime.now()
print(now)

# 특정 날짜와 시간
dt = datetime.datetime(2024, 2, 19, 12, 30)
print(dt)

#오늘 날짜만
today = datetime.date.today()
print(today)

# 날짜와 시간을 문자열로 반환(포멧)
formatted = now.strftime("%Y-%m-%d %H:%M:%S") # 년도 YYYY로 반환
# formatted = now.strftime("%y-%m-%d %H:%M:%S") # 년도 YY로 반환
print(formatted)

# 문자를 날짜로
str_to_dt = datetime.datetime.strptime("2024-02-18", "%Y-%m-%d")
print(str_to_dt)

st_date = datetime.date(2024, 1, 1)
end_date = datetime.date(2024, 2, 20)
delta = end_date - st_date # 날짜연산
print(delta)

weekday = end_date.weekday() # 월 : 0, 화 : 1, 수 : 2 ...
print("요일 : ", weekday)

import calendar
year = 2024
month = 2
first_weekday, num_days = calendar.monthrange(year, month)
# 2024년 2월 첫번쨰 요일 목요일 : 3 / 끝나는일 29일 반환
print(f"{year}년 {month}월")
print("월 화 수 목 금 토 일")
# 첫째날 시작 요일까지 공백으로 출력
print("   "* first_weekday, end="")
# 1일 부터 마지막날 까지 출력
for day in range(1, num_days + 1):
    print(f"{day:2}", end=" ") # {day:2} <-- 2자리 차지하도록
    first_weekday += 1
    if first_weekday == 7: # 요일의 마지막 새로운 줄로
        print()
        first_weekday = 0


