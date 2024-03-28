import sqlite3
import pandas as pd
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)
CORS(app)

sel = """ SELECT * FROM tb_questions """
merge_1 = """
    INSERT INTO tb_user (email, nick_name)
    VALUES (?, ?)
    ON CONFLICT(email) DO UPDATE SET
    nick_name=excluded.nick_name
"""
merge_2 = """
    INSERT INTO tb_response(email, q_id, select_option)
    VALUES(?, ?, ?) 
    ON CONFLICT(email, q_id) DO UPDATE SET
    select_option = excluded.select_option
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

conn = sqlite3.connect("letter.db", check_same_thread=False)
q = pd.read_sql(con=conn, sql=sel)
print(q.head())

# DB에서 조회
questions = []
for i, v in q.iterrows():
    questions.append({'q_id' : v['q_id']
                      ,'contents' : v['q_content']
                      ,'option_a' : v['option_a']
                      ,'option_b' : v['option_b']})

def fn_get_data(target):
    df = pd.read_sql(con=conn, sql=sql_user)
    option_mapping = {'A': 0, 'B': 1, 'N': 0.5}
    df['select_value'] = df['select_option'].map(option_mapping)
    print(df.head())

    matrix = df.pivot_table(index='email', columns='q_id', values='select_value')
    # matrix.dropna(inplace=True) # NaN 값을 포함하는 행 제거
    matrix.fillna(0, inplace=True)
    sim_matrix = cosine_similarity(matrix)
    print(sim_matrix)

    sim_df = pd.DataFrame(sim_matrix, index=matrix.index, columns=matrix.index)
    print(sim_df.head())

    target_user = target
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
        cursor = conn.cursor()
        cursor.execute(merge_1, (email, nick))

        # tb_responce MERGE
        for answer in answers:
            q_id = answer[0]
            result = answer[1]
            cursor.execute(merge_2, (email, q_id, result))
        cursor.close()
        conn.commit()
    except Exception as e:
        print(str(e))
    sim_list = fn_get_data(email)

    return jsonify({"message":"결과가 성공적으로 저장됨."
                    ,"result":sim_list}), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
