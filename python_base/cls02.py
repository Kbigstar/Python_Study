# 상속 (python은 다중 상속가능)
class Animal:
    def __init__(self, name):
        self.name = name
    def move(self):
        print("move!!")
    def speak(self):
        pass
class Dog(Animal):
    def speak(self):
        print('bark!!')
class Duck(Animal):
    def speak(self):
        print("quack!!")
dog = Dog("doggy")
print(dog.name)
dog.move()
dog.speak()
duck = Duck('donalde')
print(duck.name)
duck.speak()