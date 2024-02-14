# 시작 경로, 찾을 파일명을 입력받아
# 찾으면 input 으로 맞는지 (y/n) 을 입력받아 전체경로를
# 출력하는 함수를 만드시오!.
import os
def fn_search(dir, file_nm):
    # 현재 디렉토리부터 시작하여 모든 하위 디렉토리 탐색
    for root, dirs, files in os.walk(dir):
        print(root)
        for file in files:
            if file_nm in file:
                full_path = os.path.join(root, file_nm)
                print("=" * 100)
                print(file)
                # 사용자에게 삭제 여부를 묻기
                user_input = input("이 파일이 맞나요? (y/n): ").lower()
                if user_input == 'y':
                    # 파일 삭제
                    print("파일을 찾았습니다.")
                    print(os.path.join(root, file))
                    print("=" * 100)
                    return
    print("파일을 찾을 수 없습니다.")
    print("=" * 100)

if __name__ == '__main__':
    while True:
        msg = input("찾을 시작경로, 파일명을 입력하세요 (종료q):").split()
        if msg[0] == 'q':
            print("종료 합니다.")
            break
        fn_search(msg[0], msg[1])



