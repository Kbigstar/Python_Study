import random
# 사용자가 로또 번호에 포함시키고 싶은 번호가 있다면
# 1 ~ 5 개 까지만 입력을 받아서 사용자 번호가
# 포함된 로또번호를 생성 해주세요
nums = input("희망하는 숫자가 있다면 띄어쓰기로 입력해주세요").split()
print(nums)
set_nums = set(nums)
print(set_nums)

while True:
    if len(set_nums) == 6:
        print(set_nums)
        break
    set_nums.add(random.randint(1, 45))
