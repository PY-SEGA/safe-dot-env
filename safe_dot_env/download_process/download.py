# from numpy import extract
from pytube import YouTube
import moviepy.editor as mp
import re
from safe_dot_env.download_process.extract_text import *
# from profanity_check import predict, predict_prob
from test_text_classifier.test import * 
from googleapiclient.discovery import build
api_key = 'AIzaSyDnaMpaPAvgJfhbrTszGlA2tE8fVAKBN8c'
# youtube = build('youtube', 'v3', developerkey=api_key)
# ----- URL as user input 
# ----- save all video details in data structure 
# ----- method to check bad words
# ----- warning check
# ----- video description and insight 
# ---------------------------------------------------------------
# **** translation , resolution  *****
def download_method(ob):
    url = ob['url']
    myVideo = YouTube(url)
    #download video 
    # for stream in myVideo.streams.filter(progressive=True, file_extension='mp4').order_by('resolution'):
    #     print(stream.resolution)
    print("start download")
    try:
        caption = myVideo.captions.get_by_language_code('en')
        print("Video English Subtitle ")
        all =caption.generate_srt_captions()
        print (all)
    except:
        title = re.sub(r'[(|)|\s|]', '_', myVideo.title) 
        print(title)
        myVideo.streams.filter(res=ob['resolution']).first().download(filename=title, output_path="downloads")
        print("download Done!!!")
        print(f"downloads/{myVideo.title}")
        clip = mp.VideoFileClip(fr"downloads/{title}.mp4")
        clip.audio.write_audiofile(r"downloads/converted2.mp3")
        txt=ext_text()
        # risk = {"text_predict":text_predict,"bad_words":bad_words}
        # risk = text_classifier(txt)
        # risk ={"text_predict":0.3,"bad_words":len(txt)/3}
        print(txt)
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
#Subtitle if Exist 
# caption = myVideo.captions.get_by_language_code('en')
# print("Video English Subtitle ")
# print(caption.generate_srt_captions)
#######################################
# covert to wav
def warning(word):
    if word > 0.25:
        return True
    else :
        return False
# by line
def bad_word_percentage(text):
    counter=0
    all_len= len(text)
    for words in text :
        if words.bad > 0 :
            counter += 1
    return counter / all_len *100
# by 
def bad_word_counter(text):
    y = re.findall("([A-z]{1})?\*+", text)
    return len(y)
def run():
    print("********************** run **********************\n")
# run()
def search():
    url = input("Enter URL ")
    myVideo = YouTube(url)
    print("********************** Title **********************\n")
    print("Video Title: " , myVideo.title)
    # print(myVideo.captions)
    print("********************** Thumbnail image **********************\n")
    print("Video Thumbnail : " , myVideo.thumbnail_url)
    print("********************** author **********************\n")
    print("Video Thumbnail : " , myVideo.author)
    print("********************** description **********************\n")
    print("Video description : " , myVideo.description)
    print("********************** rating **********************\n")
    print("Video rating : " , myVideo.rating)
    print("********************** views **********************\n")
    print("Video views : " , myVideo.views)
    print("********************** Video resolution **********************\n")

    res = []
    for stream in myVideo.streams.filter(progressive=True):
        res.append(stream.resolution)
        # print("Video resolutions : ",stream.resolution)
    download_method({"url" :url ,"resolution" :res[0] })
    # return {"url" :url ,"resolution" :res[4] }
search()
