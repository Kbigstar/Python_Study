class Rectangle:
    count = 0   # 클래스 변수

    def __init__(self, w, h):
        self.witdh = w
        self.height = h

    # 인스턴스 메서드
    def clacArea(self):
        area = self.witdh * self.height
        return  area

    @staticmethod
    def isSquare():
        print("정적 메서드")

    @classmethod
    def printCount(cls):
        cls.count += 1
        print(cls.count)

a = Rectangle(10, 20)
b = Rectangle(50, 100)
print(a.clacArea())
print(b.clacArea())
# Rectangle.clacArea() # 오류발생 인스턴스 메서드이기 때문.
Rectangle.isSquare()    # 정적 메서드 사용

Rectangle.printCount()  # 클래스 메서드 사용 (클래스 변수 접근)
Rectangle.printCount()

