import time 
from gtts import gTTS

def generateAudio(text):
    texto = text
    tts = gTTS(texto, lang="es-us")
    tts.save("./generatedVoices/voice.mp3")
    