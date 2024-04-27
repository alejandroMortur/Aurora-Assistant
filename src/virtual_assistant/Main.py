def main(sr, pyttsx3, pywhatkit):
    name = "Aurora"
    listener = sr.Recognizer()
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)
    
    try:
        rec = listen(listener,sr)
        if 'reproduce' in rec:
            music = rec.replace('reproduce','')
            print("Reproduciendo: " + music)
            talk(engine, "Reproduciendo: " + music)
            pywhatkit.playonyt(music)
    except Exception as e:
        print("Error:", e)

def talk(engine, text):
    engine.say(text)
    engine.runAndWait()
    
def listen(listener,sr):
    rec = ""  # Inicializa rec con un valor predeterminado
    try:
        with sr.Microphone() as source:
            print("Escuchando....")
            pc = listener.listen(source)
            rec = listener.recognize_google(pc)
            rec = rec.lower()
            if name in rec:
                rec = rec.replace(name,'')
    except sr.UnknownValueError:
        print("No se pudo entender el audio")
    except sr.RequestError as e:
        print("Error en la solicitud de reconocimiento de voz; {0}".format(e))
    except Exception as e:
        print("Error:", e)
    return rec


if __name__ == "__main__":
    main()
