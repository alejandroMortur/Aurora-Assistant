from playsound import playsound
import os

def speak():
    playsound(r"./generatedVoices/voice.mp3")
    os.remove("./generatedVoices/voice.mp3")
