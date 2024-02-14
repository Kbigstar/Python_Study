# 안녕
# 주석 ctrl + /
print("hi")
# 문자열 '' <-- or "" or """""" or ''''''
a = "hi"
b = """
    hi hello
    오호 !
"""
# python 식별자 :변수, 함수, 클래스,모듈..의 이름
# 규칙
# 1.알파벳, 숫자, 언더스코어(_)로 구성
# 2.숫자로 시작할 수 없음.
# 3.대소문자를 구별함.
# 4.예약어를 사용할 수 없음(ex. for, while, if..)
# 보통 변수는 스네이크 표기법사용
my_var = 10 # 자료형에 타입이 붙지 않음 자동 인식
print(type(my_var))
print(my_var)
print(type(a))
# 문자열 곱하기(*) 가능
print("=" * 100)
print(a * 100)
# 기본 문자열 함수
print(a.upper())
print("HELLO".lower())
c = "Life is to Short".replace("Short","Long")
print(c)
d = c.split() #문자열 나누기 default 공백
print(d)
# 문자열 입력받기
msg = input("문자를 입력하세요:")
print(msg)


