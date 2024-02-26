import requests

CLIENT_ID = "" # Naver Developers Client ID
SECRET = "" # Naver Developers Client Secret
def get_naver(query):
    s = 1
    url = "https://openapi.naver.com/v1/search/blog?query={0}&start={1}&display=100".format(query, s)
    header = {"X-Naver-Client-Id": CLIENT_ID
        , "X-Naver-Client-Secret": SECRET}
    res = requests.get(url, headers=header)
    json_data = res.json()

    items = json_data['items']

    for i, v in enumerate(items):
        print(v)

    return json_data