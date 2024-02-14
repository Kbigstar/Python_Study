# python Data Types
# list(배열), dict(key:value), tuple(수정X), set(중복x)
# 동적배열 타입이 자유로움.
arr = [1, 2, "nick", [3, 4]]
print(arr[1])  # index로 접근
arr.append(5)  # 추가
arr[1] = 20    # 수정
print(arr * 10) # 배열 곱하기
# 딕셔너리 dict key:value
my_dict = {} # 비어있는 딕셔너리
print(type(my_dict))
my_dict2 = {"nick": 10, "judy": 20,
            "alice": [1, 2]}
print(my_dict2["nick"])
my_dict2["jack"] = 20
print(my_dict2)
# Tuple 순서가 있지만 변경이 불가능
my_tuple = (1, 2, 3)
print(my_tuple[1])
# my_tuple[1] = 10 #오류남
# set 순서가 없고 중복을 허용하지 않음.
#다른 자료의 비어있는 선언과 다르게 set 키워드필요
my_set = set()
my_set2 = {1, 1, 1, 2, 3}
print(my_set2)
my_set2.add(2)  # 요소 추가
print(my_set2)

# 타입 변환
a = "10"
print(type(a))
a = int(a)
print(type(a))
msg = int(input("숫자를 입력하세요:"))
if msg > 5:
    print("입력은 5보다 큼")
elif msg == 5:
    print("입력은 5입니다.")
elif msg == 6:
    pass # 아무 처리 없을때
else:
    print("입력은 5보다 작아요.")

# 반복문 for
# 기본 for 문1 (배열의 요소 값만 필요할때)
for v in arr:
    print(v)
# for 문2 (인덱스와 요소 값이 필요할때)
for i, v in enumerate(arr):
    print(i, v)
# for 문3 (단순 반복)
for i in range(3): # 0, 1, 2
    print(i)


