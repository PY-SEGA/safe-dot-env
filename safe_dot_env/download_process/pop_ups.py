import re
from re import L
from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter.font import BOLD, Font
from PIL import ImageTk,Image
import threading
import requests
from io import BytesIO
import textwrap
from safe_dot_env.download_process.download import *
# from safe_dot_env.download_process.download import insert_to_db
from safe_dot_env.download_process.root import root

alert_font = Font(
    size=9,
    weight='bold'
)

def pop_up():
    '''This function is for the invalid input popup'''
    global pop
    pop = Toplevel(root)
    pop.overrideredirect(1)
    pop.title('Invalid input')
    pop.geometry('250x170+700+500')
    pop.config(bg=('#2b2929'))
    
    global err
    err = PhotoImage(file='assets/error2.png')
    pop_label = Label(pop, text='Please add a valid youtube URL!',bg='#2b2929', fg='white', font=alert_font)
    pop_label.pack(pady=10)

    err_pic = Label(pop, image=err,borderwidth=0, bg='yellow')
    err_pic.pack(pady=10)

    ok = Button(pop, text='OK', command=pop.destroy, bg='grey', width=10, height=5)
    ok.pack(pady=10)


def cancel_download(title):
    import os
    os.remove(f'downloads/{title}.mp4')
    pop2.destroy()

    insert_to_db()


def continue_download():
    pop2.destroy()
    download_complete()

    insert_to_db()


def pop_up_unsafe(title):
    '''This function is for the unsafe content warning'''
    global pop2
    pop2 = Toplevel(root)
    pop2.overrideredirect(0.2)
    pop2.title('Unsafe Content')
    pop2.geometry('350x250+700+500')
    pop2.config(bg=('#2b2929'))
    
    
    global err
    err = PhotoImage(file='assets/error2.png')

    err_pic = Label(pop2, image=err,borderwidth=0, bg='yellow')
    err_pic.pack(pady=10)

    pop2_label = Label(pop2, text='This video contains unsafe content',bg='#2b2929', fg='white', font=alert_font)
    pop2_label.pack(pady=10)

    no = Button(pop2, text='Cancel', command=lambda: cancel_download(title), bg='grey')
    no.pack(pady=10)
  
    yes = Button(pop2, text='Continue', command=continue_download, bg='grey')
    yes.pack(pady=10)


def pop_up_safe():
    '''This function is for the safe content warning'''
    global pop4
    pop4 = Toplevel(root)
    pop4.overrideredirect(0.2)
    pop4.title('Content safe')
    pop4.geometry('350x250+700+500')
    pop4.config(bg=('#2b2929'))
    
    
    # global err
    # err = PhotoImage(file='assets/error2.png')

    # err_pic = Label(pop4, image=err,borderwidth=0, bg='yellow')
    # err_pic.pack(pady=10)

    pop4_label = Label(pop4, text='Download complete\n  your video is safe',bg='#2b2929', fg='white', font=15)
    pop4_label.pack(pady=10)

    k = Button(pop4, text='OK', command=pop4.destroy, bg='grey')
    k.pack(pady=10)



def download_complete():
    '''This function is for the unsafe content warning'''
    global pop3
    pop3 = Toplevel(root)
    pop3.overrideredirect(0.2)
    pop3.title('Download Complete')
    pop3.geometry('350x250+700+500')
    pop3.config(bg=('#2b2929'))
    
    
    global done
    done = PhotoImage(file='assets/error2.png')

    # done_pic = Label(pop3, image=done,borderwidth=0, bg='yellow')
    # done_pic.pack(pady=10)

    pop3_label = Label(pop3, text='Download complete',bg='#2b2929', fg='white', font=alert_font)
    pop3_label.pack(pady=10)

    # no = Button(pop3, text='Cancel', command=pop3.destroy, bg='grey')
    # no.pack(pady=10)
  
    k = Button(pop3, text='OK', command=pop3.destroy, bg='grey')
    k.pack(pady=10)
