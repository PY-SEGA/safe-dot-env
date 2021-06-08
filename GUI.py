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
# class App(tk.Frame):
#     def __init__(self, master=None):
#         super().__init__(master)
#         # self.pack()
    
# my_app = App()

# def print_result(url):
#     '''this function is to test the button and print the input to the shell'''
#     result = url.get() #This gets the input as a string
#     print(result)

# url = StringVar() 

# label = Label(my_app.master, text='Video URL', font=("Helvetica", 18, BOLD), width=15).grid(row=0, column=0)

# label_progress= Label(my_app.master)
# label_progress.grid(row=7,column=2)

# entry_url = Entry(my_app.master, textvariable=url, width=50).grid(row=0,column=1)

# button_function = Button(my_app.master, text='Download',command=lambda:print_result(url), font=(20), width=20, bg='blue').grid(row=0,column=2) #This button calles the function 




# my_app.master.title("Safe-Dot-Env")
# my_app.master.geometry('1000x700')


# my_app.mainloop()


# WINDOW CONFIGURATION
root = Tk()
root.title("Safe-dot-env")
root.minsize(1100, 760)
root.configure(background="#2b2929")
root.attributes('-zoomed', True)


# FONTS
heading_font = Font(
    family="Noto Sans Mono CJK SC",
    size=60, weight="bold", slant="roman", underline=0, overstrike=0
)

info_font = Font(
    size =22,
    underline=0,
    overstrike=0
)

alert_font = Font(
    size=9,
    weight='bold'
)


# FUNCTIONS:
def show_image(image_url):

    '''This function shows the thumbnail image of the video'''

    url = image_url
    response = requests.get(url)
    raw_data = response.content
    response.close()

    fixed_height = 512
    im = Image.open(BytesIO(raw_data))
    height_percent = (fixed_height/float(im.size[1]))
    width_size = int((float(im.size[0])*float(height_percent)))
    im = im.resize((width_size, fixed_height), Image.NEAREST)
    photo = ImageTk.PhotoImage(im)

    return photo

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

def pop_up_unsafe():
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

    no = Button(pop2, text='Cancel', command=pop2.destroy, bg='grey')
    no.pack(pady=10)
  
    yes = Button(pop2, text='Continue', command=pop2.destroy, bg='grey')
    yes.pack(pady=10)


def thread_search():
    '''This function is for the search button, either sends the url to the (search_video) function, or
    states that the url is invalid'''

    pattern = '^(https?\:\/\/)?(www\.youtube\.com|youtu\.?be)\/.+$'
    match = re.match(pattern, url_entry.get())
    
    if url_entry.get():
    # if bool(match):
        # search_button['state'] = DISABLED
        threading.Thread(target=search_video).start()
    else:
        pop_up()


def show_result_frame(root_window, *args, **kwargs):
    ''' This function adds the content of the video to the application'''

    result_frame = Frame(root_window, bg='#2b2929')
    result_frame.grid(row=3, column=0, rowspan=3, columnspan=4)


    title_frame = Frame(result_frame, borderwidth=0, highlightthickness=0)
    title_frame.configure(background="#2b2929")
    title_frame.grid(row=3, column=0, padx=(0, 10), rowspan=4)   

    title = Label(title_frame, text=kwargs["title"], font=("bold", 30), bg="#2b2929", fg="white", width= 20)
    title.grid(row=0, column=0, pady=(40, 10))

    thumb_frame = Frame(root_window, bg='#2b2929')
    thumb_frame.grid(row=6, column=0, padx=(150,0))

    thumbnail = show_image(image_url=kwargs["thumbnail_url"])
    thumbnail_label = Label(thumb_frame, image=thumbnail)
    thumbnail_label.image = thumbnail
    thumbnail_label.grid(row=0, column=2, pady=(0,100))



    resolution_options = ['720p', '1080p', '420p'] #place holder
    resolution_frame = Frame(root_window, bg='#2b2929')
    resolution_frame.grid(row=2,)

    resolution_label = Label(resolution_frame, text="Resolution", font=('bold', 14), bg="#2b2929", fg="white")
    resolution_label.grid(row=2, column=0, pady=8, padx=(30,30))

    resolution_dropdown_value = StringVar()
    resolution_dropdown = ttk.Combobox(resolution_frame, textvariable=resolution_dropdown_value, width=33, font=('bold', 14))
    resolution_dropdown ['value'] = [k for k in resolution_options]
    resolution_dropdown.grid(row=2, column=1)

    author_frame = Frame(root_window, bg='#2b2929')
    author_frame.grid(row=7, column=0) 
    author_label = Label(author_frame, text= 'Author:', fg="white", bg='#2b2929', font=info_font, padx= 50,pady=15)
    author_label.grid(row=0, column=0)
    author = Label(author_frame, text=kwargs['author'], bg='#2b2929', fg="white", font=(20)).grid(row=0, column=1)

    description_label = Label(author_frame, text="Description:", bg= '#2b2929', fg='white', font=info_font, padx= 50,pady=15).grid(row=1,column=0)
    description = Label(author_frame, text=kwargs['description'], bg='#2b2929',fg="white", font=(20))
    description.grid(row=1, column=1)

    views_label = Label(author_frame, text= "Views:", font=info_font, bg= '#2b2929', fg='white',pady=15).grid(row=2, column=0)
    views = Label(author_frame, text= kwargs['views'], font=(20), bg = '#2b2929', fg='white').grid(row=2, column=1)

    rating_label = Label(author_frame, text= "Rating:", font=info_font, bg= '#2b2929', fg='white',pady=15).grid(row=3, column=0)
    rating = Label(author_frame, text= kwargs['rating'], font=(20), bg = '#2b2929', fg='white').grid(row=3, column=1)

    download_frame = Frame(root_window, bg='#2b2929')
    download_frame.grid(row=8, column=0, pady=(20,40), padx=(150,0))
    download = Button(download_frame, bg='#941D12', fg = '#ffffff', text='Download', width=15, font=13).grid(row=0, column=2)


def search_video():

    ''' This function gathers the information of the video and sends them to the (show_result_frame) function'''

    video_url = url_entry.get()
    if video_url:
        # Creating the Frame from the available data to download the video
        show_result_frame(root_window=second_frame,
                          #available_stream=res["streams"],                          
                        #   originalStream=res["originalStream"],
                          #thumbnail_url=res["thumbnail_url"]
                          thumbnail_url = 'https://i.pinimg.com/originals/be/b8/5d/beb85da5406bbd3fb982a8d78d923dc7.jpg',
                          #title=res["title"],
                          title = 'Versus',
                        #   video_url=video_url,
                          search_button=search_button,
                          url_entry=url_entry,
                          author = 'Author',
                          description = 'hello, this is the description of the video\n so here you will find some\n lines that describe this video',
                          views = 222202.0,
                          rating = 5.6
                          )


#Search Window Configuration

#main frame that contains everything
main_frame = Frame(root)
main_frame.pack(fill=BOTH, expand=1)

#main canvas
my_canvas = Canvas(main_frame, bg='#2b2929')
my_canvas.pack(side=LEFT, fill= BOTH, expand=1)

#scrollbar
my_scrollbar = tk.Scrollbar(main_frame, orient=VERTICAL, command=my_canvas.yview)
my_scrollbar.pack(side=RIGHT, fill=Y)

#canvas configure
my_canvas.configure(yscrollcommand=my_scrollbar.set)
my_canvas.bind('<Configure>', lambda e: my_canvas.configure(scrollregion= my_canvas.bbox("all")))

def _on_mouse_wheel(event):
    '''This function is for the mouse wheel to scroll'''
    my_canvas.yview_scroll(-1 * int((event.delta / 120)), "units")
my_canvas.bind_all("<MouseWheel>", _on_mouse_wheel)


second_frame = Frame(my_canvas, bg='#2b2929')
my_canvas.create_window((0,0), window=second_frame, anchor='nw')



frame1 = Frame(second_frame, bg='#2b2928')
frame1.grid(row=0,column=0 , columnspan=3, pady=(50,50), padx=(100,0))

image = ImageTk.PhotoImage(Image.open("assets/yt.png"))
imageLabel = Label(frame1, image=image, bg="#2b2929")
imageLabel.grid(row=0, column=0, padx=(75,0))
heading = Label(frame1, text='Video Downloader', font=heading_font, bg="#2b2929", fg="white")
heading.grid(row=0, column=1,columnspan=2, padx=(110,0))

frame2 = Frame(second_frame, bg='#2b2929')
frame2.grid(row=1, column=0, columnspan=2, padx=(60,0), pady=(50,50))

url_label = Label(frame2, text='Video URL', font=('bold', 14), bg="#2b2929", fg="white")
url_label.pack(side=LEFT, padx=(100, 50))
url_text = StringVar()
url_entry = Entry(frame2, textvariable=url_text, width=70, borderwidth=1, font=('bold', 20))
url_entry.pack(side=LEFT)

# frame3 = Frame(second_frame, bg='#2b2929')
# frame3.grid(row=1, column=3, columnspan=2, pady= (50,50), padx=(0,0))

search_button = Button(frame2, text='Search', bg='#941D12', command=thread_search,fg='#ffffff', font=('bold', 13), width=15)
search_button.pack(side=LEFT, padx=(40,0))





#The Main Loop That Runs The App
root.mainloop()
