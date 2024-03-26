import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

arr = [
     [0, 0, 0, 0, 1] # 사용자 1 선택결과
    ,[0, 0, 0, 1, 1] # 0 왼쪽 / 0.5 중간 / 1 오른쪽
    ,[0.5, 1, 0, 1, 1]
    ,[1, 1, 0, 1, 1]
    ,[1, 1, 1, 1, 1]
]

res = np.array(arr)
# 코사인 유사도
sim_matrix = cosine_similarity(res)
# 사용자 1과 가까운 유저 찾기
user_1_matrix = sim_matrix[0]
user_1_sim_id = [(i + 1, round(sim, 4)) for i, sim in enumerate(user_1_matrix)]
# 유사도 높은 순 으로 정렬
sort_sim = sorted(user_1_sim_id[1:], key=lambda x : x[1], reverse=True)
print(sort_sim)