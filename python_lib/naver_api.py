import  requests

q = "둔산동맛집"
s = 1
url = "https://openapi.naver.com/v1/search/blog?query={0}&start={1}&display=100".format(q, s)
CLIENT_ID = "" # Naver Developers Client ID
SECRET = "" # Naver Developers Client Secret

header = {"X-Naver-Client-Id" : CLIENT_ID
          ,"X-Naver-Client-Secret" : SECRET}
res = requests.get(url, headers=header)
# print(res)
json_data = res.json()
# print(json_data)

items = json_data['items']

for i, v in enumerate(items):
    print(v)