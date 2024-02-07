# try ...exception
def calc(values):
    sum = 0
    try:
        sum = values[0] + values[1] + values[2]
    except IndexError as e:
        print("index error")    # index 오류만

    except Exception as e:
        print(str(e))   # 모든 에러 상황
    else:
        print("에러 없음")  # 에러가 없을때 만 실행
    finally:
        print(sum)  # 에러가 있던 없던 실행함.

# calc([1, 2])  # index error
calc([True, True, True])

try:
    print("^^" % 4)
except Exception as e:
    print(str(e))

