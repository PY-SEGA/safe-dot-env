from ibm_watson import SpeechToTextV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator



apikey = '86PzL6eJhprtfm_q3uhayATvqBCU07pHCPQfRhb1zUoa'
url = 'https://api.eu-gb.speech-to-text.watson.cloud.ibm.com/instances/7dd3d9f3-1fe0-496b-ae56-3876034e7f42'

name = input('enter song name >')

authenticator = IAMAuthenticator(apikey)
stt = SpeechToTextV1(authenticator = authenticator)
stt.set_service_url(url)

import subprocess 
import os
command = f'ffmpeg -i {name}.wav -vn -ar 44100 -ac 2 -b:a 192k {name}.mp3'
subprocess.call(command, shell=True)
command = f'ffmpeg -i {name}.mp4 -map 0:a {name}.mp3'
subprocess.call(command, shell=True)
command = f'ffmpeg -i {name}.mp3 -f segment -segment_time 360 -c copy %03d.mp3'
subprocess.call(command, shell=True)


files = []
for filename in os.listdir('.'):
    if filename.endswith(".mp3") and filename !=f'{name}.mp3':
        files.append(filename)
files.sort()

print(files)


results = []
for filename in files:
    with open(filename, 'rb') as f:
        res = stt.recognize(audio=f, content_type='audio/mp3', model='en-US_NarrowbandModel',speech_detector_sensitivity=1.0,background_audio_suppression=0.5, continuous=True, \
                           inactivity_timeout=360).get_result()
        results.append(res)


text = []
for file in results:
    for result in file['results']:
        text.append(result['alternatives'][0]['transcript'].rstrip() + '.\n')


with open('output_vid.txt', 'w') as out:
    out.writelines(text)