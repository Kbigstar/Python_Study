from flask import Flask, request, jsonify, render_template
from openai import OpenAI

app = Flask(__name__)
system_instruction = """
너는 음식점 AI비서야
아래는 음식 종류야. 아래 종류의 메뉴만 있어
- 삼겹살
- 대패 삼겹살
- 물냉
삼겹살을 선택한다면 1인분에 5000원 이라고 말해줘, 대패 삼겹살은 3000원, 물냉을 500원  
위의 메뉴 말고는 없어 
하지만 다른 메뉴를 요청 한다면 다음과 같이 설명해줘 
만드는 방법 
-step1: \\, step2:\\, step3: ..\\ 와 같이 만드는 방법을 설명해줘 

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

@app.route('/ask', methods=['POST'])
def handle_ask():
    user_input = request.json['text']
    response_text = ask(user_input)
    return jsonify({'response': response_text})

if __name__ == '__main__':
    app.run(debug=True)
