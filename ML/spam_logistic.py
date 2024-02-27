# 예시 데이터
texts = ["당신에게 특별한 제안이 있습니다."
         ,"회원님 당첨되셨어요"
         ,"회의 일정을 확인 해주세요"
         ,"50% 할인 쿠폰을 드립니다!"
         ,"어제 먹은 점심메뉴 말고 오늘은 다른.."
         ,"당신의 계좌로 입금 되었습니다."]
labels = [1, 1, 0, 1, 0, 0]
# 정상 : 0, 스팸 : 1
from sklearn.feature_extraction.text import TfidfVectorizer
vec = TfidfVectorizer()
# text to vector
x = vec.fit_transform(texts).toarray()
y = labels
from sklearn.linear_model import LogisticRegression
model = LogisticRegression()
model.fit(x, y)

# test
mail = [""]
mail = vec.transform(mail)
pred = model.predict(mail)

if pred == 0:
    print("정상")
else:
    print("스팸이다 !!")