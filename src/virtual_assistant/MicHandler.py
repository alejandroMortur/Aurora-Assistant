import speech_recognition as sr
from GenerateModule import generateAudio

def getVoice():

    r = sr.Recognizer()
    print(sr.Microphone.list_microphone_names())

    with sr.Microphone() as source:
        
        r.adjust_for_ambient_noise(source,duration=1)
        print("say anything : ")
        audio= r.listen(source)
        
        try:
            
            text = r.recognize_google(audio)
            print(text)
            generateAudio("hola alejandro")
            
        except:   
            print("sorry, could not recognise")
            generateAudio("lo siento no te he entendido")