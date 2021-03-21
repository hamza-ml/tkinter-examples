import time
import _thread
import tkinter as tk


class GUI(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        btn = tk.Button(self, text='start', command=self.start)
        btn.pack()
        btn2 = tk.Button(self, text='start2', command=self.start2)
        btn2.pack()

        self.indicator = tk.Frame(self, width=40, height=40, bg='green')
        self.indicator.pack()

    def start(self):
        _thread.start_new_thread(self.slow_function, ())

    def start2(self):
        _thread.start_new_thread(self.slow_function2, ())

    def slow_function(self):
        self.indicator.config(bg='red')
        time.sleep(10)  # lock up for 10 seconds
        self.indicator.config(bg='green')

    def slow_function2(self):
        self.indicator.config(bg='red')
        time.sleep(10)  # lock up for 10 seconds
        self.indicator.config(bg='green')


if __name__ == '__main__':
    root = tk.Tk()
    root.geometry("200x100")
    win = GUI(root)
    win.pack()
    root.mainloop()
