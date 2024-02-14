from tkinter import *
from tkinter import messagebox

app = Tk()  # T 대문자, k소문자
lab = Label(app, text='이름')
lab.grid(row=0, column=0)
txt = Entry(app)
txt.grid(row=0, column=1)
def fn_click():
    name = txt.get()
    messagebox.showinfo("이름은:", name)
btn = Button(app, text='ok', command=fn_click)
btn.grid(row=1, column=1)
app.mainloop()