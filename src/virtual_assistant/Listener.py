# Listener.py

import speech_recognition as sr 
import pyttsx3
import pywhatkit

def listen(listener, name):
    rec = ""
    
    try:
        
        with sr.Microphone() as source:
            
            print("Escuchando....")
            pc = listener.listen(source)
            rec = listener.recognize_google(pc)
            rec = rec.lower()
            print("Texto reconocido:", rec)
            
            if name in rec:
                rec = rec.replace(name,'')
                
    except Exception as e:
        
        print("Error:", e)
        
    return rec
