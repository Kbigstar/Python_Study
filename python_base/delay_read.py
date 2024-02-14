f = open('delay.txt', 'r', encoding='utf8')
for line in f:
    print(line.strip()) # strip 공백제거
f.close()
with open('delay.txt', 'r', encoding='utf8') as f:
    for line in f:
        print(line.strip())  # strip 공백제거
# with는 사용이 끝나면 자동으로 닫음.