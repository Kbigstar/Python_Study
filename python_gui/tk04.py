from tkinter import *


app = Tk()
canvas = Canvas(app, width=400, height=300)
canvas.pack()
x_size = 20
y_size = 20

def create_ball(context):
    canvas.create_oval(100, 150, 150, 200, fill='red', tag='redball')
def move_left(event):
    canvas.move('redball', -x_size, 0)
    canvas.after(1)
    canvas.update()
def move_right(event):
    canvas.move('redball', x_size, 0)
    canvas.after(1)
    canvas.update()
def move_up(event):
    canvas.move('redball', 0, -y_size)
    canvas.after(1)
    canvas.update()
def move_down(event):
    canvas.move('redball', 0, y_size)
    canvas.after(1)
    canvas.update()
create_ball(canvas)
canvas.bind('<Left>', move_left)
canvas.bind('<Right>', move_right)
canvas.bind('<Up>', move_up)
canvas.bind('<Down>', move_down)
canvas.focus_set()
canvas.pack()
app.mainloop()

