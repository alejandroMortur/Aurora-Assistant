import time 
from gtts import gTTS
from SpeakModule import speak

def generateAudio(text, language):
    # Get the text to generate audio from
    text_to_generate = text
    
    # Create a gTTS object with the text and language
    tts = gTTS(text_to_generate, lang=language)
    
    # Save the generated audio as an mp3 file
    tts.save("./generatedVoices/voice.mp3")
    
    # Call the speak function to play the generated audio
    speak()
