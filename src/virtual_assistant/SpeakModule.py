from playsound import playsound
import os

def speak():
    # Play the generated voice audio file
    playsound(r"./generatedVoices/voice.mp3")
    
    # Remove the generated voice audio file after playing
    os.remove("./generatedVoices/voice.mp3")
