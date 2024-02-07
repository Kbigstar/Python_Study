# 시작 경로, 찾을 파일명을 입력받아
# 찾으면 input으로 맞는지 (y/n) 을 입력받아 전체경로를
# 출력하는 함수를 만드시오!.
import os

test = "delay.txt"
if "del" in test:
    print(test, "del 포함 키워드 있음")

def fn_search(dir, file_nm):
    print(dir, file_nm)


    for dirpath, dirname, filename in os.walk(dir):
        for file in filename:
            if file_nm in file:
                print(file, "포함 키워드 있음")
                check = input("이파일이 맞나요? (y/n)")

                if check == 'y':
                    print("파일을 찾았습니다! 종료..")
                    print(dirpath, file)
                    break
                elif check == 'n':
                    continue


# root, nm = input("찾을 시작경로, 파일명을 입력하세요(띄어쓰기로 구분) :").split()
root, nm = "c:/dev" , 'file02'
fn_search(root, nm)