import pandas as pd
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from DBManager import DBManager

app = Flask(__name__)
CORS(app)

db = DBManager()
sel = """ SELECT * FROM tb_questions """
merge_1 = """
    MERGE INTO tb_user a
    USING DUAL
    ON (email = :1)
    WHEN MATCHED THEN
        UPDATE SET nick_name = :2
    WHEN NOT MATCHED THEN
        INSERT (email, nick_name)
        VALUES(:3, :4)
"""
merge_2 = """
    MERGE INTO tb_response a
    USING DUAL
    ON (a.email = :1
       AND a.q_id = :2)
    WHEN MATCHED THEN
        UPDATE SET a.select_option = :3
    WHEN NOT MATCHED THEN
        INSERT (a.email, a.q_id, a.select_option) VALUES(:4, :5, :6)
"""

q = pd.read_sql(con=db.conn, sql=sel)
print(q.head())

# DB에서 조회
questions = []
for i, v in q.iterrows():
    questions.append({'q_id' : v['Q_ID']
                      ,'contents' : v['Q_CONTENTS']
                      ,'option_a' : v['OPTION_A']
                      ,'option_b' : v['OPTION_B']})

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/start")
def start():
    return jsonify(questions)
@app.route("/save", methods=['POST'])
def save_result():
    data = request.json
    print(data)

    email = data.get("email")
    nick = data.get("nickNm")
    answers = data.get("answers")

    try:
        # tb_user MERGE
        db.insert(merge_1, [email, nick, email, nick])

        # tb_responce MERGE
        for answer in answers:
            p_id = answer[0]
            result = answer[1]
            db.insert(merge_2, [email, p_id, result, email, p_id, result])
    except Exception as e:
        print(str(e))

    return jsonify({"message":"결과가 성공적으로 저장됨."}), 200

if __name__ == '__main__':
    app.run(debug=True)
