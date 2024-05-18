from playsound import playsound
import os

def speak():
    # Play the generated voice audio file
    playsound(r"../resources/Sounds/generatedVoices/voice.mp3")
    
    # Remove the generated voice audio file after playing
    os.remove("../resources/Sounds/generatedVoices/voice.mp3")
