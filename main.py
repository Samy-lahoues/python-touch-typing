from tkinter import Tk
from tkinter import ttk
from random import shuffle
from clear_screen import clear
import time

clear()
root = Tk()
frame = ttk.Frame(root, padding=10, width=400, height=400);
frame.grid()
btn = ttk.Button(frame, text="Press any key").grid(column=10, row=0)
ttk.Label(frame, text="Hello world!").grid(column=0, row=1)
ttk.Button(frame, text="Quit", command=root.destroy).grid(column=1,row=1)
root.mainloop()

#! variables
index = 0
words_list = []
work_count = 10
file = open("words.txt", "r")
for line in file:
    words_list.append(line.strip())
shuffle(words_list)
