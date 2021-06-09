from pickle import GLOBAL
from pytube import YouTube
import moviepy.editor as mp
import re
from safe_dot_env.download_process.extract_text import *
# from profanity_check import predict, predict_prob
from test_text_classifier.test import *
from googleapiclient.discovery import build
from safe_dot_env.download_process.youtube_commnets import *
# from safe_dot_env.download_process.sqlite import c, con
import sqlite3
# from safe_dot_env.download_process.pop_ups import pop2, pop, pop3, pop4, pop_up, pop_up_safe, pop_up_unsafe, pop_up_unsafe
from pathlib import Path
from safe_dot_env.download_process.shazam import *
from tkinter import *
from safe_dot_env.download_process.root import root
from tkinter.font import BOLD, Font
from PIL import ImageTk,Image

# api_key = 'AIzaSyDnaMpaPAvgJfhbrTszGlA2tE8fVAKBN8c'
api_key = 'AIzaSyDGfngFMxQiVAweRw7ae4BqM_cgDEZBSmo'

list_of_details =[]
title = ''


#######################################################
alert_font = Font(
    size=9,
    weight='bold'
)

def cancel_download(title):
    import os
    os.remove(f'downloads/{title}.mp4')
    pop2.destroy()
    global list_of_details
    print(list_of_details, 'gllllllllloballlllllllllll')
    insert_to_db()


def continue_download():
    pop2.destroy()
    download_complete()

    


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
    
    insert_to_db()    
    # global err
    # err = PhotoImage(file='assets/error2.png')

    # err_pic = Label(pop4, image=err,borderwidth=0, bg='yellow')
    # err_pic.pack(pady=10)

    pop4_label = Label(pop4, text='Download complete\n  your video is safe',bg='#2b2929', fg='white', font=15)
    pop4_label.pack(pady=10)

    k = Button(pop4, text='OK', command=pop4.destroy, bg='grey')
    k.pack(pady=10)




def download_complete():
    '''This function is for download is complete'''
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

    insert_to_db()
#######################################################





def download_method(ob):
    global list_of_details
    url = ob['url']
    myVideo = YouTube(url)

    print("start download")
    try:
        print("***************try*************************")
        
        caption = myVideo.captions.get_by_language_code('en')
        print("Video English Subtitle ")
        all = str(caption.generate_srt_captions())
        # print(all)
        all = re.sub(r"[^A-z|\s]", '', all)
        all_list = all.split("\n")
        length = len(all_list)  # 100
        flag = 0
        while(flag < length):
                if all_list[flag] == "" or all_list[flag] == " " or all_list[flag] == "  ":
                    length -= 1
                    all_list.pop(flag)
                else:
                    flag += 1
        print(all_list)
        title = re.sub(r'[^A-z0-9]', '_', myVideo.title)
        print(title)
        print("\nStart download!!!")
        myVideo.streams.filter(res=ob['resolution']).first().download(filename=title, output_path="downloads")
        print("download Done!!!")
        print(f"downloads/{myVideo.title}")
        clip = mp.VideoFileClip(fr"downloads/{title}.mp4")
        print(type(clip), 'this is clip')
        list_of_details.append(fr"downloads/{title}.mp4")
        # print(clip, 'clip in the append')
        clip.audio.write_audiofile(r"downloads/converted2.mp3")
        txt = ext_text()
        li = []
        for i in all_list:
            li.append(i)

        all_list_string = "--".join(all_list)
        list_of_details.append(all_list_string)
        print(li, 'li******************************')
        return li
    except:
        print("*************** except *************************")
        title = re.sub(
                r'[^A-z0-9]', '_', myVideo.title)
        print(title)
        print("\nStart download!!!")
        myVideo.streams.filter(res=ob['resolution']).first().download(filename=title, output_path="downloads")
        print("download Done!!!")
        print(f"downloads/{myVideo.title}")
        clip = mp.VideoFileClip(fr"downloads/{title}.mp4")
        print(type(clip), 'this is clip in the shazam')
        list_of_details.append(fr"downloads/{title}.mp4")
        print('123456')
        clip.audio.write_audiofile(r"downloads/converted2.mp3")

        try:
            txt = shazam(r"downloads/converted2")
            # print(txt)
            all_list_string = "--".join(txt)
            list_of_details.append(all_list_string)
            li = []
            for i in txt:
                li.append(i)
            return li
        except:
            txt = ext_text()
            # risk = {"text_predict":text_predict,"bad_words":bad_words}
            # risk = text_classifier(txt)
            # risk ={"text_predict":0.3,"bad_words":len(txt)/3}
            all_list_string = "--".join(txt)
            list_of_details.append(all_list_string)
            print(txt)
            li = []
            for i in txt:
                li.append(i)
            return li



# print(download_method({'url':'https://www.youtube.com/watch?v=xh1ROLEDyP4&t=228s&ab_channel=UniversalPictures', 'resolution':'360p'}))




def search(gui_url):
# dictionary of: url(str), resolution(list), myVideo (object)
    global list_of_details
    con = sqlite3.connect('video_details.db')
    c = con.cursor()
    url = gui_url
    c.execute("select * from videos where url=?",(url,))
    items = c.fetchall()
    # print("here is the items",items)
    
    myVideo = YouTube(url)

    global title
    title = re.sub(r'[^A-z0-9]', '_', myVideo.title)

    print('==this is the title==', title)
    
    if len(items) == 0:
        print(items)
        print("********************** Title **********************\n")
        print("Video Title: ", myVideo.title)
        print("********************** Thumbnail image **********************\n")
        print("Video Thumbnail : ", myVideo.thumbnail_url)
        print("********************** author **********************\n")
        print("Video Thumbnail : ", myVideo.author)
        print("********************** description **********************\n")
        print("Video description : ", myVideo.description)
        print("********************** rating **********************\n")
        print("Video rating : ", myVideo.rating)
        print("********************** views **********************\n")
        print("Video views : ", myVideo.views)
        print("********************** Video resolution **********************\n")
        list_of_details = list_of_details + [url,myVideo.title,myVideo.thumbnail_url , myVideo.author,myVideo.description,myVideo.rating,myVideo.views ]



        res = []
        for stream in myVideo.streams.filter(progressive=True):
            res.append(stream.resolution)



        # sub_extract(url, res)
        return {"url" : url , "resolution" : res, "my_video": myVideo}
    else:
        print("hi I am here finally")
        print(items)

        dic_items = {
            "url" : items[0][0],
            "title": items[0][1],
             "Thumbnail_image": items[0][2],
             "author": items[0][3],
             "description": items[0][4],
             "rating": items[0][5],
             "views" : items[0][6],
             "good_comments": items[0][7],
             "bad_comments": items[0][8],
             "profanity_comments" : items[0][9],
             "path": items[0][10],
             "subtitle": items[0][11],
             "vid_text_predict" : items[0][12] ,
             "vid_bad_words" : items[0][13],
             "resolution" : items[0][14]
        }
        # print("from dic_items" , dic_items)
        return {"url" : dic_items['url'] , "resolution" : dic_items['resolution'].split(','), "my_video": myVideo }



def insert_to_db():
    global list_of_details
    print('from insert to db', list_of_details)
    insert_into = """INSERT INTO videos("url","title", "Thumbnail_image","author","description","rating","views","path" ,"subtitle","vid_text_predict"  ,"vid_bad_words","resolution" ,"good_comments","bad_comments", "profanity_comments" )         VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"""        
    tuple_of_details = (list_of_details)
    con = sqlite3.connect('video_details.db')
    # create a cursor
    c = con.cursor()        
    c.execute(insert_into,tuple_of_details)        
    c.execute("select * from videos where url=?",(url,))        
    items = c.fetchall()        
    print("here is the items" , items)    

    con.commit()        
    con.close()

# @pysnooper.snoop()
def sub_extract(url_input, resolution):


    """good_comments text,
    bad_comments text, 
    profanity_comments real,
    path text,
    subtitle text,
    vid_text_predict real ,
    vid_bad_words integer,
    resolution text
    )
    """
    global list_of_details

    con = sqlite3.connect('video_details.db')
    c = con.cursor()
    url = url_input
    myVideo = YouTube(url)

    c.execute("select * from videos where url=?",(url,))
    items = c.fetchall()


    res = resolution
    title = re.sub(r'[^A-z0-9]', '_', myVideo.title)
    
    subtitle_list = download_method({"url" : url , "resolution" : res })
    classifier_result_vid = text_classifier(subtitle_list)
    print(subtitle_list, 'This is subtitle list 11111111111111')

    # res_string = ','.join(res)
    list_of_details = list_of_details + [classifier_result_vid['text_predict'],classifier_result_vid['bad_words'],res]

    print(f"percentage of profanity {classifier_result_vid['text_predict']}")
    print(f"number of bad words {classifier_result_vid['bad_words']}")


    comments_list = youtube_comments(url)

    try:
        print(comments_list,'commmmmmmmments')
        comments_results = comments_test(comments_list)
        print('after line341')
        good_result = format(comments_results['good_comments'], ".2f")
        print('after line343')
        bad_result = format(comments_results['bad_comments'], ".2f")
        print(comments_results, 'in the try')
        print(f"percentage of good comments : {float(good_result)*100} %")
        print(f"percentage of bad comments : {float(bad_result)*100} %")
        classifier_result = text_classifier(comments_list)
        print(f"percentage of profanity{classifier_result['text_predict']}")
        list_of_details = list_of_details + [good_result, bad_result , classifier_result['text_predict']]
    except:
        print(comments_list, 'in the except')
        good_result = '0.0'
        bad_result = '0.0'
        classifier_result = {'text_predict':0.0, 'bad_words':0.0}
        list_of_details = list_of_details + ['0.0', '0.0', classifier_result['text_predict']]
    
    # print('++++++++++++()()()()()()()++++++++',classifier_result_vid['text_predict'] )
    if classifier_result_vid['text_predict'] > 0.15:
        pop_up_unsafe(title)
    else:
        pop_up_safe()

    # print(list_of_details, '-------------------------------------------+++++++++++++')
    # insert_into = """INSERT INTO videos("url","title", "Thumbnail_image","author","description","rating","views","path" ,"subtitle","vid_text_predict"  ,"vid_bad_words","resolution" ,"good_comments","bad_comments", "profanity_comments" )         VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"""        
    # tuple_of_details = (list_of_details)        
    # c.execute(insert_into,tuple_of_details)        
    # c.execute("select * from videos where url=?",(url,))        
    # items = c.fetchall()        
    # print("here is the items" , items)    

    # con.commit()        
    # con.close()

    print(classifier_result_vid)

    return {'profanity': classifier_result_vid['text_predict'], 'bad':classifier_result_vid['bad_words'], 'good_comments':f'{good_result}%', 'bad_comments':f'{bad_result}%', 'profanity_comments':classifier_result['text_predict'], 'bad_word_comments':classifier_result['bad_words'] }

def call_res(url , res):
    con = sqlite3.connect('video_details.db')
    c = con.cursor()
    c.execute("select * from videos where url=?",(url,))
    items = c.fetchall()
    print("here is the items\n***************************************************************",len(items))


    if len(items)==0:
        print(":inside ")
        contents =  sub_extract(url, res)
        return contents


    else:
        global title
        my_file = Path(fr"downloads/{title}.mp4")
        print('title inside extract', title)
        print('if the file is in the downloads',my_file.is_file())

        if not my_file.is_file():
           sub_extract(url, res)
            
        print("hi I am here finally")
        print(items)
        dic_items = {
            "url" : items[0][0],
            "title": items[0][1],
             "Thumbnail_image": items[0][2],
             "author": items[0][3],
             "description": items[0][4],
             "rating": items[0][5],
             "views" : items[0][6],
             "good_comments": items[0][7],
             "bad_comments": items[0][8],
             "profanity_comments" : items[0][9],
             "path": items[0][10],
             "subtitle": items[0][11],
             "vid_text_predict" : items[0][12] ,
             "vid_bad_words" : items[0][13],
             "resolution" : items[0][14]
        }
        # print(dic_items)
        return {'profanity': dic_items['vid_text_predict'], 'bad':dic_items['vid_bad_words'], 'good_comments':dic_items['good_comments'], 'bad_comments':dic_items['bad_comments'], 'profanity_comments':dic_items['profanity_comments'], 'bad_word_comments':dic_items['bad_comments'] }