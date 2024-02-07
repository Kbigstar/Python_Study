# 기본 형태
def fn_name(param):
    print("함수 실행")
    return param * 2

print(fn_name('팽수'))

# 가변길이 파라미터 0 ~ n개 파라미터를 받을 수 있음
def fn_total(*numbers):
    tot = 0
    for n in numbers:
        tot += n
    return tot

print(fn_total())
print(fn_total(1,10,10))

def fn_sum_mul(choice, *args):
    if choice == '+':
        result = 0
        for n in args:
            result +=2
    elif choice == '*':
        result = 1
        for n in args:
            result *= n
    return result

print(fn_sum_mul('+', 1,2,3,4))
print(fn_sum_mul('*', 1,2,3,4))
# return이 0 ~ n개 가능
def fn_name(param):
    nms = param.split()
    return nms[0], nms[1]
last, first = fn_name("홍 길 동")
print(last, first)
nm = fn_name("김 길동")    # 튜플형태
print(nm)

# named 파라미터
def report(name, age, score=0):  # default 값 설정 가능
    print(name, age, score)
report(age=10, name="jack", score=100)
report(age=10, name="judy")

# lambda 함수 (익명함수)
func = (lambda x: x + 1)
print(func)
# 변수에 담아 사용
func2 = lambda x, y: x * y + 1
print(func2(2,4))
# map 활용
arr = [1, 2, 3, 4, 5]
result = list(map(lambda x: x**2, arr))
print('result', result)

