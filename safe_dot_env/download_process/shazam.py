from pydub import AudioSegment
import requests
import base64
import json
## load and convert
def shazam(audio):
    sound_from_mp3 = AudioSegment.from_mp3(f'{audio}.mp3').set_sample_width(2).set_frame_rate(44100).set_channels(1).split_to_mono()[0] 
    # - 44100 frame rate= (44.1kHz - CD audio)
    # - 1 channels 1 raw only (1 for mono and  2 for stereo)
    # - 2 for 16-bit (number of bytes per sample)
    ## encode
    base64_bytes = base64.b64encode(sound_from_mp3.raw_data)
    ## truncate
    payload = base64_bytes[:500000]
    # print(len(payload))
    ## request
    url = "https://shazam.p.rapidapi.com/songs/detect"
    # payload = "Generate one on your own for testing and send the body with the content-type as text/plain"
    headers = {
        'content-type': "text/plain",
        'x-rapidapi-key': "564627aea1mshad5378f2965a210p1a4b0fjsn4e9f05e4c654",
        'x-rapidapi-host': "shazam.p.rapidapi.com"
        }
    response = requests.request("POST", url, data=payload, headers=headers)
    # print(response.text)
    rt = json.loads(response.text)
    lyrics_list = rt["track"]["sections"][1]["text"]
    # lyrics_str= ""
    # for i in lyrics_list:
    #     lyrics_str += i  
    # artist_name = rt["track"]["subtitle"]
    # song_name = rt["track"]["title"]
    return lyrics_list
# print(lyrics_list)
# shazam(r"JustinBieberHoldOn")