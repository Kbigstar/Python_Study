# import 라이브러리 불러오는 방법
import random
test = random.randint(1, 45) #랜덤 정수 1 ~ 45
# print(test)
# 사용자에게 로또 생성 수량을 입력받아 입력받은 수량만큼
# 출력하시오
# arr = [1, 2]
# print(len(arr)) #배열의 사이즈
# idx = 0
# while True:
#     if idx == 5:
#         break
#     print("반복")
#     idx += 1

# 1.사용자가 원하는 수량입력 (받기 입력 타입은 str)
# 2.수량만큼 for문
cnt = int(input("로또 생성기 입니다 ^^ 몇개를 원하세요?"))
for i in range(cnt):
    lotto = set()
    while True:
        lotto.add(random.randint(1, 45))
        if 6 == len(lotto):
            print(lotto)
            break

# 3.해당 반복 마다 6개의 1~45사이의 로또값 생성 (while)
    # tip. 로또번호는 무조건 6개
    #      set() 자료형은 중복을 허용하지 않음.
# 4.로또 번호 출력




import random
user_num = int(input("로또 생성기 입니다 ^^ 몇개를 원하세요?"))
for i in range(user_num):
    lotto = set()
    while True:
        lotto.add(random.randint(1, 45)) # 랜덤 정수 1 ~ 45
        if len(lotto) == 6:
            break
    print(lotto)
print("good luck")