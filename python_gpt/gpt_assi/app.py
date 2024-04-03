from flask import Flask, request, jsonify, render_template
from openai import OpenAI

app = Flask(__name__)
system_instruction = """
너는 일정추천 AI비서야
오늘은 2024년 04월 02일이야.
아래는 일정 추천 종류야. 아래 종류의 추천만 있어
- 여행
- 운동
- 맛집
- 도서
여행을 선택한다면 국내, 해외인지 확인받고 그에 따른 여행지를 추천해줘
운동을 선택한다면 혼자, 그룹인지 확인받고 그에따른 운동을 3가지 정도 추천 해줘
맛집을 선택한다면 한식,일식,양식,중식 중에 확인받고 그에 따른 대한민국 맛집을 추천해줘
도서를 선택한다면 4가지의 장르를 예로들어 하나씩 추천해줘
마지막으로 사용자가 좋은것 같다고하면 어느 일정에 추가하시겠습니까? 라는 질문을 하고
사용자가 동의하고 예를들어 20240101 이라고 하면 20240101 일정을 추가합니다! 라고 답변해주고
0101 라고 일정을 입력해도 20240101 일정을 추가합니다! 라고 답변해줘

마지막으로 일정이 아닌 다른질문에도 간단한 답변을 해줘
"""
messages = [{"role": "system", "content": system_instruction}]
client = OpenAI(api_key="")

def ask(text):
    # Simulate adding user input and generating a bot response
    user_input = {"role": "user", "content": text}
    messages.append(user_input)

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages)

    bot_text = response.choices[0].message.content
    bot_resp = {"role": "assistant", "content": bot_text}
    messages.append(bot_resp)
    return bot_text

@app.route('/')
def index():
    return render_template('chat.html')

@app.route('/ask1', methods=['POST'])
def handle_ask():
    user_input = request.json['text']
    response_text = ask(user_input)
    return jsonify({'response': response_text})

if __name__ == '__main__':
    app.run(debug=True)
