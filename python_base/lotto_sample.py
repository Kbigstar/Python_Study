import random
# 사용자가 로또 번호에 포함시키고 싶은 번호가 있다면
# 1 ~ 5 개 까지만 입력을 받아서 사용자 번호가
# 포함된 로또번호를 생성해 주세요
nums = input("희망하는 숫자가 있다면 띄어쓰기로 입력해주세요").split()
set_nums = set(nums)
if len(set_nums) > 5:
    print("희망 숫자는 5개 이하로 가능합니다.")
else:
    while True:
        if len(set_nums) == 6:
            break
        set_nums.add(random.randint(1, 45))
    print(set_nums)