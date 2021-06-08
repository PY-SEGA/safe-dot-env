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
api_key = 'AIzaSyDnaMpaPAvgJfhbrTszGlA2tE8fVAKBN8c'
# youtube = build('youtube', 'v3', developerkey=api_key)
# ----- URL as user input
# ----- save all video details in data structure
# ----- method to check bad words
# ----- warning check
# ----- video description and insight
# ---------------------------------------------------------------
# **** translation , resolution  *****
list_of_details =[]


def download_method(ob):
    global list_of_details
    url = ob['url']
    myVideo = YouTube(url)
    # download video
    # for stream in myVideo.streams.filter(progressive=True, file_extension='mp4').order_by('resolution'):
    #     print(stream.resolution)
    print("start download")
    try:
        print("***************try*************************")
        caption = myVideo.captions.get_by_language_code('en')
        print("Video English Subtitle ")
        all = str(caption.generate_srt_captions())
        print(all)
        all = re.sub(r"[^A-z]", '', all)
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
        title = re.sub(r'^A-z0-9]', '_', myVideo.title)
        print(title)
        print("\nStart download!!!")
        myVideo.streams.filter(res=ob['resolution']).first().download(
            filename=title, output_path="downloads")
        print("download Done!!!")
        print(f"downloads/{myVideo.title}")
        clip = mp.VideoFileClip(fr"downloads/{title}.mp4")
        list_of_details.append(fr"downloads/{title}.mp4")
        clip.audio.write_audiofile(r"downloads/converted2.mp3")
        txt = ext_text()
        all_list_string = "--".join(all_list)
        list_of_details.append(all_list_string)
        return all_list
    except:
        print("*************** except *************************")
        title = re.sub(
                r'[^A-z0-9|\s]', '_', myVideo.title)
        print(title)
        print("\nStart download!!!")
        myVideo.streams.filter(res=ob['resolution']).first().download(
            filename=title, output_path="downloads")
        print("download Done!!!")
        print(f"downloads/{myVideo.title}")
        clip = mp.VideoFileClip(fr"downloads/{title}.mp4")
        list_of_details.append(fr"downloads/{title}.mp4")
        clip.audio.write_audiofile(r"downloads/converted2.mp3")
        txt = ext_text()
        # risk = {"text_predict":text_predict,"bad_words":bad_words}
        # risk = text_classifier(txt)
        # risk ={"text_predict":0.3,"bad_words":len(txt)/3}
        all_list_string = "--".join(txt)
        list_of_details.append(all_list_string)
        print(txt)
        return txt
    # if (risk.text_predict > 0.5 or risk.bad_words > len(txt)/2):
    #     user_res=input("warning don\'t bad contentet")
    #     if (user_res == "y"):
    #         # View content
    #         print("View content")
    #     else :
    #         # Delete contenet
    #         print("Delete contenet")
    # else :
    #     print ("safe go ahead ")
# myVideo.streams.filter(progressive=True, res="720p").download(output_path)
# print("Video is Downloaded!!")
# help(YouTube)
# print(YouTube.__dict__)
# Subtitle if Exist
# caption = myVideo.captions.get_by_language_code('en')
# print("Video English Subtitle ")
# print(caption.generate_srt_captions)
#######################################
# covert to wav


def warning(word):
    if word > 0.25:
        return True
    else:
        return False
# by line


def bad_word_percentage(text):
    counter = 0
    all_len = len(text)
    for words in text:
        if words.bad > 0:
            counter += 1
    return counter / all_len * 100
# by


def bad_word_counter(text):
    y = re.findall("([A-z]{1})?\*+", text)
    return len(y)


def run():
    print("********************** run **********************\n")
# run()

def search():
    global list_of_details
    con = sqlite3.connect('video_details.db')
    c = con.cursor()
    url = input("Enter URL ")
    c.execute("select * from videos where url=?",(url,))
    items = c.fetchall()
    print("here is the items",items)
    if len(items) == 0:
        print(items)
        myVideo = YouTube(url)
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
        comments_list = youtube_comments(url)
        # print("comments_list:joy::joy::joy::joy::joy::joy::joy::joy:" ,comments_list )
        list_of_details = list_of_details + [url,myVideo.title,myVideo.thumbnail_url , myVideo.author,
        myVideo.description,myVideo.rating,myVideo.views ]
        try:
            comments_results = comments_test(comments_list)
            good_result = format(comments_results['good_comments'], ".2f")
            bad_result = format(comments_results['bad_comments'], ".2f")
            print(comments_results)
            print(f"percentage of good comments : {float(good_result)*100} %")
            print(f"percentage of bad comments : {float(bad_result)*100} %")
            classifier_result = text_classifier(comments_list)
            print(f"percentage of profanity{classifier_result['text_predict']}")
            list_of_details = list_of_details + [good_result, bad_result , classifier_result['text_predict']]
            # print(f"number of bad words{classifier_result['bad_words']}")
        
        except:
            print(comments_list)
            list_of_details = list_of_details + ['None', 'None' , 0.0]
        
        res = []
    
        for stream in myVideo.streams.filter(progressive=True):
            res.append(stream.resolution)
            # print("Video resolutions : ",stream.resolution)
        subtitle_list = download_method({"url" : url , "resolution" : res[0] })
        print("\n\n***********************subtitle_list***********************")
        print(subtitle_list)
        classifier_result_vid = text_classifier(subtitle_list)
        print(f"percentage of profanity {classifier_result_vid['text_predict']}")
        print(f"number of bad words {classifier_result_vid['bad_words']}")
        res_string = ','.join(res)
        list_of_details = list_of_details + [classifier_result_vid['text_predict'],classifier_result_vid['bad_words'],res_string]
        # print(list_of_details)
        # sqlite_insert_query = """INSERT INTO vi
        #                       (id, name, email, joining_date, salary) 
        #                        VALUES 
        #                       (1,'James','james@pynative.com','2019-03-17',8000)"""
        insert_into = """INSERT INTO videos("url","title", "Thumbnail_image","author","description","rating","views" ,"good_comments","bad_comments", "profanity_comments" ,"path","subtitle","vid_text_predict"  ,"vid_bad_words" ,"resolution") 
        VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"""
        tuple_of_details = (list_of_details)
        c.execute(insert_into,tuple_of_details)
        c.execute("select * from videos where url=?",(url,))
        items = c.fetchall()
        print("here is the items" , items)
        con.commit()
        con.close()
        return {"url" : url , "resolution" : res[0] }
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
        print("from dic_items" , dic_items)
        return {"url" : dic_items['url'] , "resolution" : dic_items['resolution'] }
search()
