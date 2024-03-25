# pip install openai
from openai import OpenAI
import os
# 환경변수로 설정하여 사용할수있음
# 임시로 일단 코드에 적어서 사용
api_key = "" # api key
client = OpenAI(api_key=api_key)
system = """
너는 음식점 AI 비서야
아래는 음식종류. 아래 종류의 메뉴 말고 다른메뉴는 없어
- 삼겹살
- 대패 삼겹살
- 물냉
삼겹살은 1인분에 5000원.
"""

message = [{"role" : "system"
            ,"content" : "system"}]

def ask(text):
    user_input = {"role" : "user", "context" : text}
    message.append(user_input)

     # 기본적인 사용법
    resp = client.chat.completions.create(
        model="gpt-3.5-turbo"
        ,messages= message
    )

    bot_text = resp.choices[0].message.content
    bot_resp = {"role":"assistant", "content":bot_text}
    message.append(bot_resp)
    return bot_text

while True:
    user_input = input("주문 하세요 :")
    bot_resp = ask(user_input)
    print(f"bot:{bot_resp}")