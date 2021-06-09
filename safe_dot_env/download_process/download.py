from pickle import GLOBAL
from pytube import YouTube
import moviepy.editor as mp
import re
from safe_dot_env.download_process.extract_text import *
from safe_dot_env.download_process.extract_text import *
# from profanity_check import predict, predict_prob
from test_text_classifier.test import *
from googleapiclient.discovery import build
from safe_dot_env.download_process.youtube_commnets import *
# from safe_dot_env.download_process.sqlite import c, con
import sqlite3
api_key = 'AIzaSyDnaMpaPAvgJfhbrTszGlA2tE8fVAKBN8c'

list_of_details =[]


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
        try:
            txt = shazam(r"downloads/converted2")
            # print(txt)
            return txt
        except:
            txt = ext_text()
            # risk = {"text_predict":text_predict,"bad_words":bad_words}
            # risk = text_classifier(txt)
            # risk ={"text_predict":0.3,"bad_words":len(txt)/3}
            all_list_string = "--".join(txt)
            list_of_details.append(all_list_string)
            print(txt)
            return txt








def search(gui_url):
# dictionary of: url(str), resolution(list), myVideo (object)
    global list_of_details
    con = sqlite3.connect('video_details.db')
    c = con.cursor()
    url = gui_url
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
        list_of_details = list_of_details + [url,myVideo.title,myVideo.thumbnail_url , myVideo.author,myVideo.description,myVideo.rating,myVideo.views ]



        res = []
        for stream in myVideo.streams.filter(progressive=True):
            res.append(stream.resolution)


        con.commit()
        con.close()
        sub_extract(url, res)
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


def sub_extract(url_input, resolution):
    global list_of_details

    con = sqlite3.connect('video_details.db')
    c = con.cursor()
    url = url_input

    c.execute("select * from videos where url=?",(url,))
    items = c.fetchall()


    vid = search(url)
    res = resolution
    title = re.sub(r'[W|\s|?|#|:|!|@|#|$|\'|%|^|&|*|+|=|\|/|*]', '_', vid['my_video'].title)
    
    subtitle_list = download_method({"url" : url , "resolution" : res[0] })
    classifier_result_vid = text_classifier(subtitle_list)


    res_string = ','.join(res)
    list_of_details = list_of_details + [classifier_result_vid['text_predict'],classifier_result_vid['bad_words'],res_string]

    print(f"percentage of profanity {classifier_result_vid['text_predict']}")
    print(f"number of bad words {classifier_result_vid['bad_words']}")


    comments_list = youtube_comments(url)
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
    except:
        print(comments_list)
        list_of_details = list_of_details + ['None', 'None' , 0.0]
    
    # if classifier_result_vid['text_predict'] > 0.5:
    #     pop_up_unsafe(title)
    # else:
    #     pop_up_safe()

    return {'profanity': classifier_result_vid['text_predict'], 'bad':classifier_result_vid['bad_words'], 'good_comments':f'{float(good_result)*100}%', 'bad_comments':f'{float(bad_result)*100}%', 'profanity_comments':classifier_result['text_predict'], 'bad_word_comments':classifier_result['bad_words'] }

