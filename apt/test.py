import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize

# 데이터 생성
data = np.array([[30, 20, 15], [1, 19, 15]])

# 데이터의 크기에 따라 사각형의 크기를 정규화
norm = Normalize(vmin=data.min(), vmax=data.max())
sizes = norm(data)

# 시각화
plt.figure(figsize=(8, 6))  # 그래프의 크기 설정
for i in range(data.shape[0]):
    for j in range(data.shape[1]):
        rect = plt.Rectangle((data.shape[1] - j - 0.5, i - 0.5), 1, 1, color=plt.cm.hot(sizes[i, j]))
        plt.gca().add_patch(rect)

plt.xticks(np.arange(data.shape[1]), ['C', 'B', 'A'])  # 역순으로 레이블 설정
plt.yticks(np.arange(data.shape[0]), ['1', '2'])
plt.grid(True)
plt.show()
