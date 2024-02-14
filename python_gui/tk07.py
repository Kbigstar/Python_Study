from tkinter import *
from pythonProject.python_base.lotto_lib import fn_lotto
def append_text():
    txt.delete(1.0, END)
    cnt = int(entry.get())
    set_arr = fn_lotto(cnt)
    txt.insert(END, ("="*20)+' 행운의 로또 번호입니다 ^^' + '\n\n')
    for i in set_arr:
        txt.insert(END, str(list(i)) + '\n')
    entry.delete(0, 'end')
    txt.insert(END, ("="*20)+' 꼭 당첨 되세요!!!' + '\n')
    txt.see(END)

app = Tk()
entry = Entry(app)
entry.grid(row=0, column=0)
btn = Button(app, text='생성', command=append_text)
btn.grid(row=0, column=1)
txt = Text(app)
txt.grid(row=1, column=0, columnspan=2)
app.mainloop()
# 수량을 입력받아 Text 위젯에 입력받은 수량만큼 로또번호 출력
# 1.button event bind
# 2.entry value get
# 3.lotto 생성
# 생성 수량만큼 Text insert
