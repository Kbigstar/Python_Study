# _*_ coding: utf-8 _*_
# w rite, a ppend, r ead
f = open("delay.txt", 'a', encoding='utf8')
f.write('오늘의 지각자\n')
while True:
    n = input("오늘 지각한 사람!!(종료:q)")
    if 'q' == n:
        break
    f.write(n)
    f.writelines('\n')
f.close()
