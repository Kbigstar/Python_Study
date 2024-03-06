import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

df = pd.read_csv('./Mall_Customers.csv')
print(df.info())
print(df.describe())
# 좋은 군집 찾기 (kmeans는 군집수를 몇개로 할지가 중요함)
# 군집내 거리가 가깝고 군집간에는 거리가 먼 군집이 좋은 군집이다.
# 그룹에 포함된 데이터들의 퍼짐정도를 inertia 라고함
df['Gender'] = df['Gender'].map({"Female":1, "Male":0})
# customerId 빼고
data = df[['Gender', 'Age', 'Annual Income', 'Spending Score']]
cnt = list(range(1, 11))
inertia = []
for i in cnt:
    model = KMeans(n_clusters=i, algorithm="lloyd")
    model.fit(data)
    inertia.append(model.inertia_)

plt.plot(cnt, inertia, '-0')
plt.xlabel('Cluster(K)')
plt .ylabel('inertia')
plt.show()