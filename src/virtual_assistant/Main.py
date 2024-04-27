# Main.py

import Imports

import Listener
import Talker

def main():
    
    name = "Aurora"
    listener = Listener.sr.Recognizer()  
    engine = Listener.pyttsx3.init()     
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)
    
    try:
        
        rec = Listener.listen(listener, name) 
        
        if 'reproduce' in rec:
            music = rec.replace('reproduce','')
            print("Reproduciendo: " + music)
            Talker.talk(engine, "Reproduciendo: " + music)   
            Listener.pywhatkit.playonyt(music)     
                      
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    main()
