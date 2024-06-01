import speech_recognition as sr
from GenerateModule import generateAudio

def getVoice(language):
    r = sr.Recognizer()

    # List available audio input devices
    # Replace 1 with the corresponding index of your microphone if it's not the default one
    print("---------------------------")
    print(sr.Microphone.list_microphone_names())
    print("---------------------------")
    
    with sr.Microphone() as source:
        # Adjust for ambient noise
        r.adjust_for_ambient_noise(source, duration=1)
        print("Recording voice: ")
        audio = r.listen(source)
        
        try:
            # Use Google Speech Recognition for speech recognition
            text = r.recognize_google(audio, language=language)
            print(text)
            return text
            
        except sr.UnknownValueError:
            
            if language == "es":
                print("---------------------------")
                print("Sorry, I didn't understand what you said.")
                print("---------------------------")
                generateAudio("Lo siento, No te he entendido")
            elif language == "en":
                print("---------------------------")
                print("Sorry, I didn't understand what you said.")
                print("---------------------------")
                generateAudio("Sorry, I didn't understand what you said.",language)
            return none
        
        except sr.RequestError as e:
            
            if language == "es":
                print("---------------------------")
                print("Could not complete the request; {0}".format(e))
                print("---------------------------")
                generateAudio("Lo siento se ha producido un error")
            elif language  == "en":
                print("---------------------------")
                print("Could not complete the request; {0}".format(e))
                print("---------------------------")
                generateAudio("sorry an error occurred",language)
            return none