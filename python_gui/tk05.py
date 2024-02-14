from tkinter import *

def fn_select(event):
    print("선택됨")
    selection = event.widget.curselection()
    if selection:
        idx = selection[0]
        value = event.widget.get(idx)
        print(value)
app = Tk()
app.geometry("200x200")
listbox = Listbox(app)
listbox.pack()
for i in ['첫번째', '두번째', '세번째', '네번째']:
    listbox.insert(END, i)
listbox.bind('<<ListboxSelect>>', fn_select)
app.mainloop()
