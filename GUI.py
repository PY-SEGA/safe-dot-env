import tkinter as tk
from tkinter import *
from tkinter.font import BOLD
import tkinter.ttk as ttk
from ttkthemes import ThemedStyle

class App(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        # self.pack()
    
my_app = App()

def print_result(url):
    '''this function is to test the button and print the input to the shell'''
    result = url.get() #This gets the input as a string
    print(result)

url = StringVar() 

label = Label(my_app.master, text='Video URL', font=("Helvetica", 18, BOLD), width=15).grid(row=0, column=0)

label_progress= Label(my_app.master)
label_progress.grid(row=7,column=2)

entry_url = Entry(my_app.master, textvariable=url, width=50).grid(row=0,column=1)

button_function = Button(my_app.master, text='Download',command=lambda:print_result(url), font=(20), width=20, bg='blue').grid(row=0,column=2) #This button calles the function 




my_app.master.title("Safe-Dot-Env")
my_app.master.geometry('1000x700')


my_app.mainloop()
