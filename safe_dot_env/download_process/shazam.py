# import requests
# url = "https://shazam.p.rapidapi.com/songs/detect"

# payload = "HoldOn"
# headers = {
#     'content-type': "text/plain",
#     'x-rapidapi-key': "564627aea1mshad5378f2965a210p1a4b0fjsn4e9f05e4c654",
#     'x-rapidapi-host': "shazam.p.rapidapi.com"
#     }

# response = requests.request("POST", url, data=payload, headers=headers)

# print(response.text)
# print(response.text.matches)

# import requests

# url = "https://shazam.p.rapidapi.com/auto-complete"

# querystring = {"term":"kiss the","locale":"en-US"}

# headers = {
#     'x-rapidapi-key': "564627aea1mshad5378f2965a210p1a4b0fjsn4e9f05e4c654",
#     'x-rapidapi-host': "shazam.p.rapidapi.com"
#     }

# response = requests.request("GET", url, headers=headers, params=querystring)

# print(response.text)
# from pydub import AudioSegment

## convert the wav to raw
# import wave
# import audioop


# wav_file = wave.open("loseyourself.wav")
# print(audioop.avg(wav_file.readframes(wav_file.getnframes()), wav_file.getsampwidth()))
# get_frag = audioop.avg(wav_file.readframes(wav_file.getnframes()), wav_file.getsampwidth())
# # print(wav_file.getnframes()) ## Returns number of audio frames.
# # print(wav_file.readframes((wav_file.getnframes())))
# # print(wav_file.getsampwidth()) ## Returns sample width in bytes.
# raw_file = open("Raw.txt", "w")
# raw_file.write(str(get_frag))

## convert mp3 to raw 
# from pydub import AudioSegment

# sound = AudioSegment.from_mp3("hold.mp3")

# # sound._data is a bytestring
# raw_data = sound._data
# print(type(raw_data))
# data_list = list(raw_data)
# new_file = open("new.raw", "w")
# new_file.write(str(raw_data))
# import base64
# import requests
# import json


# # file_path="Raw.raw"
# url = "https://rapidapi.p.rapidapi.com/songs/detect"
# encode_string = base64.b64encode(data_list) ## read in a binary mode
# # encode_string = base64.b64encode(open(file_path, "rb").read()) ## read in a binary mode

# payload=encode_string
# # print(type(payload))
# # row = {
# #     raw_data
# # }
# new_file = open("text.txt", "w")
# new_file.write(payload.decode())

# headers = {
#     'content-type': "text/plain",
#     'x-rapidapi-key': "564627aea1mshad5378f2965a210p1a4b0fjsn4e9f05e4c654",
#     'x-rapidapi-host': "shazam.p.rapidapi.com"
#     }

# response = requests.request("POST", url, data=payload, headers=headers)
# # print(response.json()["matches"])
# # print(response.json())
# # print(payload)
# print(response.text)
from numpy import source
from scipy.io.wavfile import read, write
import io
from os import path
from pydub import AudioSegment
import json
import base64
## This may look a bit intricate/useless, considering the fact that scipy's read() and write() function already return a
## numpy ndarray, but the BytesIO "hack" may be useful in case you get the wav not through a file, but trough some websocket or
## HTTP Post request. This should obviously work with any other sound format, as long as you have the proper decoding function
src = "3s.mp3"
dst = "input_wav.wav"
sound = AudioSegment.from_mp3(src)
sound.export(dst, format="wav")
with open("input_wav.wav", "rb") as wavfile:
    input_wav = wavfile.read()
# here, input_wav is a bytes object representing the wav object
rate, data = read(io.BytesIO(input_wav))
# data is a numpy ND array representing the audio data. Let's do some stuff with it
reversed_data = data[::-1] #reversing it
#then, let's save it to a BytesIO object, which is a buffer for bytes object
bytes_wav = bytes()
byte_io = io.BytesIO(bytes_wav)
write(byte_io, rate, reversed_data)
output_wav = byte_io.read() # and back to bytes, tadaaa
# output_wav can be written to a file, of sent over the network as a binary
a=output_wav
b = list(a)
data = b
dataStr = json.dumps(data)
base64EncodedStr = base64.b64encode(dataStr.encode('utf-8'))
# print(base64EncodedStr)
with open('output64.txt', 'w') as out:
         out.write(str(base64EncodedStr))
# print('decoded', base64.b64decode(base64EncodedStr))
# with open('output64.txt', 'w') as out:
#         out.writelines(base64EncodedStr)
# print(output_wav)


# print(json.dumps(json.loads(response.text)))

# import requests
# import base64
# import json

# def shazam(payload):
#     url = "https://shazam.p.rapidapi.com/songs/detect"

#     payload = open(payload,"rb").read()
#     payload = base64.b64encode(payload)
#     payload = str(payload)
#     headers = {
#     'x-rapidapi-host': "shazam.p.rapidapi.com",
#     'x-rapidapi-key':"564627aea1mshad5378f2965a210p1a4b0fjsn4e9f05e4c654",
#     'content-type': "text/plain",
#     'accept': "text/plain"
#     }

#     response = requests.request("POST", url, data=payload, headers=headers)

#     # print(response.text)
#     print(json.dumps(json.loads(response.text)))

# shazam("coldplay.mp3")

