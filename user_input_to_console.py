from tkinter import *


def printtext():
    global e
    string = e.get()
    print(string)


root = Tk()

root.title('Name')
e = Entry(root)
e.pack()
e.focus_set()

b = Button(root, text='okay', command=printtext)
b.pack(side='bottom')
root.mainloop()
