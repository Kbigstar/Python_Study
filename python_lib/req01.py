import requests
# requests 는 python에서 http요청을 쉽게 할 수 있는 라이브러리
url = "https://api.upbit.com/v1/market/all"
res = requests.get(url)
if res.status_code == 200:
    print("정상응답")
    obj = res.json()
    for v in obj:
        print(v['market'])
else:
    print("오류")
# post
data = {"key": "test"}
# https://httpbin.org/post 테스트 url (요청 값 그대로 리턴함)
post_res = requests.post("https://httpbin.org/post", data=data)
print(post_res.text)