# import 라이브러리 불러오는 방법
import random

test = random.randint(1, 45)    # 랜덤 정수 1 ~ 45

# 사용자에게 로또 생성 수량을 입력 받아
# 입력받은 수량만큼 출력하시오
arr = [1, 2]
print(len(arr))     # 배열의 사이즈

idx = 0
while True:
    if idx == 5:
        break

    print("반복")
    idx += 1    # python 에선 idx++ 불가

# 1. 사용자가 원하는 수량 입력받기 받기 입력타입은 str
# 2. 수량만큼 for문
# 3. 해당 반복 마다 6개의 1 ~ 45 사이의 로또값 생성 (while)
# 4. 로또 번호 출력



my_lotto = set()

# my_lotto.add(1)
# my_lotto.add(3)
# my_lotto.add(5)
# print(my_lotto)
# print(len(my_lotto))
# if my_lotto.union({1}):
#     print("hi")
# my_lotto.add(2)
#
# my_lotto.clear()
# print(my_lotto)

msg = input("몇개의 로또를 뽑으시나요?")
for i in range(int(msg)):
    print(i)


for i in range(int(msg)):
    my_lotto = set() # 입력 만큼 선언
    while True:
        my_lotto.add(random.randint(1, 45))
        if len(my_lotto) == 6:
            print(my_lotto)
            break



