from tkinter import *
from tkinter import messagebox
from pythonProject.python_base.lotto_lib import fn_lotto
app = Tk()
lab = Label(app, text='로또 수량')
lab.grid(row=0, column=0)
txt = Entry(app)
txt.grid(row=0, column=1)
def fn_click():
    cnt = int(txt.get())
    arr = fn_lotto(cnt)
    messagebox.showinfo("행운의 숫자는:", arr)
btn = Button(app, text='ok', command=fn_click)
btn.grid(row=1, column=1)
app.mainloop()