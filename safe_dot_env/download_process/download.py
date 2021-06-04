from pytube import YouTube
import moviepy.editor as mp

myVideo = YouTube("https://www.youtube.com/watch?v=s7wmiS2mSXY&ab_channel=MuleSoftVideosMuleSoftVideos")
print("********************** Title **********************\n")
print("Video Title: " + myVideo.title)
# print(myVideo.captions)
# print("********************** Thumbnail image **********************\n")
# print("Video Thumbnail : " + myVideo.thumbnail_url)

# print("********************** Video Streams **********************\n")
# print("Video Thumbnail : " + myVideo.streams.all)


#download video 
for stream in myVideo.streams.filter() :
    print(stream)
myVideo.streams.first().download(output_path="downloads")
# myVideo.streams.filter(progressive=True, res="720p").download(output_path)
print("Video is Downloaded!!")

#Subtitle if Exist 
# caption = myVideo.captions.get_by_language_code('en')
# print("Video English Subtitle ")
# print(caption.generate_srt_captions)

#######################################

# covert to wav
clip = mp.VideoFileClip(r"downloads/What is an API.mp4") 
clip.audio.write_audiofile(r"downloads/converted2.wav")
