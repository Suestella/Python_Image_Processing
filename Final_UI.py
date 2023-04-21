import tkinter as tk
from tkinter import ttk
import subprocess

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.program1_btn = ttk.Button(self)
        self.program1_btn["text"] = "Launch Program 1"
        self.program1_btn["command"] = self.launch_program1
        self.program1_btn.pack(side="top")

        self.program2_btn = ttk.Button(self)
        self.program2_btn["text"] = "Launch Program 2"
        self.program2_btn["command"] = self.launch_program2
        self.program2_btn.pack(side="top")

    def launch_program1(self):
        subprocess.Popen(['python', 'chat_test_final_0102.py'])

    def launch_program2(self):
        subprocess.Popen(['python', 'chat_test1expo.py'])

root = tk.Tk()
app = Application(master=root)
app.mainloop()