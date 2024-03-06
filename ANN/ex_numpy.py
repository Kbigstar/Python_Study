# 넘파이 numpy 별칭으로 보통 np로 사용
# 다차원 연산을 지원함.
# 많은 머신러닝(딥러닝) 관련 라이브러리에서 기본 데이터 형태로 사용
import numpy as np
python_arr = [1, 2, 3]
arr1 = np.array(python_arr)
print('일반 array:', python_arr)
print('ndarry:', arr1)
arr2 = np.array([[1, 2, 3]
                ,[2, 3, 4]])
arr3 = np.array([[[1, 2, 3], [4, 5, 6]], [[7, 8, 9 ], [10, 11, 12]]])
print('arr1(type):',type(arr1), arr1.shape, arr1.ndim)
print('arr2(type):',type(arr2), arr2.shape, arr2.ndim)
print('arr2(type):',type(arr3), arr3.shape, arr3.ndim)

print(arr2[0, 2])    # 첫번째 행의 세 번째 요소
print(arr2[:, 1:3])  # 모든 행, 두번째와 세번째 열
# 요소별 합
print(arr1 + arr1)
# 요소별 곱
print(arr1 * arr1)
# 집계 함수(합)
print(np.sum(arr2))
# 집계 함수(평균)
print(np.mean(arr2))
# axis 축 :0 행방향, 1 열방향
print(arr2.sum())
print(arr2.sum(axis=0))
print(arr2.sum(axis=1))
# 1차원 배열 생성
arr = np.arange(1, 10) # 1 ~ 9
print(arr)
# 리쉐입 3x3
print(arr.reshape(3, 3))
# dot product (두 배열의 대응하는 요소를 곱한 후 그 결과를 모두 더하는 연산)
print(np.dot(arr, arr))
arr4 = np.array([[1,2,3],[4,5,6],[7,8,9]])
print(arr4)  # arr4.T 아래와 같음
t_arr4 = arr4.transpose()
print(t_arr4)

# 5 x 5 행렬
matrix = np.array([
    [1, 2, 3, 4, 5],
    [5, 4, 3, 2, 1],
    [1, 2, 3, 4, 5],
    [5, 4, 3, 2, 1],
    [1, 2, 3, 4, 5]
])
# 2 x 2 필터
filter_ = np.array([
    [1, 0],
    [0, -1]
])
# 출력 행렬 초기화 (4, 4)
output = np.zeros((4, 4)) #0
# 컨볼루션 연산 수행
for i in range(4):
    for j in range(4):
        output[i, j] = np.sum(matrix[i:i+2, j:j+2] * filter_)
# 이미지로 출력
import matplotlib.pyplot as plt

plt.figure(figsize=(10, 4))
plt.subplot(1, 3, 1)
plt.imshow(matrix, cmap='gray')
plt.title('original')
plt.colorbar()

plt.subplot(1, 3, 2)
plt.imshow(filter_, cmap='gray')
plt.title('filter')
plt.colorbar()

plt.subplot(1, 3, 3)
plt.imshow(output, cmap='gray')
plt.title('conv result')
plt.colorbar()
plt.tight_layout()
plt.show()




