import pandas as pd
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from DBManager import DBManager
from sklearn.metrics.pairwise import cosine_similarity


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

sql_user = """ 
    SELECT a.email
          ,a.nick_name
          ,b.q_id
          ,b.select_option
    FROM tb_user a
        ,tb_response b
    WHERE a.email = b.email
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

def fn_get_data(target):
    df = pd.read_sql(con=db.conn, sql=sql_user)
    option_mapping = {'A': 0, 'B': 1, 'N': 0.5}
    df['SELECT_VALUE'] = df['SELECT_OPTION'].map(option_mapping)
    print(df.head())

    matrix = df.pivot_table(index='EMAIL', columns='Q_ID', values='SELECT_VALUE')
    sim_matrix = cosine_similarity(matrix)
    print(sim_matrix)

    sim_df = pd.DataFrame(sim_matrix, index=matrix.index, columns=matrix.index)
    print(sim_df.head())

    target_user = '127897@naver.com'
    # 해당 사용자의 유사도
    target_user_sim = sim_df[target_user]
    # 자신 제외하고 유사도 높은 순으로 정렬
    sorted_sim = target_user_sim.drop(target_user).sort_values(ascending=False)

    # 결과 출력
    print(target_user + ' 사용자와 유사한 사용자 순서')
    return sorted_sim.reset_index().values.tolist()


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
    sim_list = fn_get_data(email)

    return jsonify({"message":"결과가 성공적으로 저장됨."
                    ,"result":sim_list}), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
