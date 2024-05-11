import os 
import sys
from GenerateModule import generateAudio
from MicHandler import getVoice
from LLMModule import getLLMText
from TextHandler import read_file, read_word
defautLanguange = "es-ES"

File = [
    
    "./textResources/IntroText01.txt",
    "./textResources/ES/EsKeyWordsText02.txt",
    "./textResources/ES/EsDefaultSentences01.txt",
    "./textResources/EN/EnKeyWordsText02.txt",
    "./textResources/EN/EnDefaultSentences01.txt"
    
]

content = read_file(File[0])
print(content)
generateAudio(content,defautLanguange)

languague = getVoice(defautLanguange)
if languague == "castellano":
    
    generateAudio("Entendido te hablare en castellano a partir de ahora",defautLanguange)
    defautLanguange = "es-ES"
    keyWords =  read_word(File[1])
    defaultSentences =  read_word(File[2])
    print(keyWords,defaultSentences)
    
else:
    generateAudio("Got it from now on i will speak to you in english",defautLanguange)
    defautLanguange = "en-US"
    keyWords =  read_word(File[3])
    defaultSentences =  read_word(File[4])
    print(keyWords,defaultSentences)

while True:
    respond = getVoice(defautLanguange)
    respond = respond.lower()
    if "aurora" in respond:  
        respond = respond.replace("aurora","")
        if keyWords[0] in respond and keyWords[1] in respond or keyWords[2] in respond:
            generateAudio("Claro dime que quieres que busque por ti",defautLanguange)
        elif keyWords[3] in respond:
            generateAudio("Claro que programa quieres abrir?",defautLanguange)
        elif keyWords[4] in respond:
            generateAudio("Claro ahora te digo, dejame pensar",defautLanguange)
            textGenerated = getLLMText(respond,100)
            generateAudio(textGenerated,defautLanguange)
            generateAudio("¿Te ha sido util esta informacion? o quieres mas?",defautLanguange)
            moreText = ""
            while keyWords[5] not in moreText: 
                moreText = getVoice(defautLanguange)
                moreText = respond.lower()
                if keyWords[6] in moreText or keyWords[7] in moreText or keyWords[8] in moreText:
                    textGenerated = getLLMText(respond,200)
                    generateAudio(textGenerated,defautLanguange)
                    
        elif keyWords[9] in respond:
            generateAudio("Claro que programa quieres que cierre?",defautLanguange)
        elif keyWords[10] in respond and "alarma" in respond:
            generateAudio("Claro puedo hacerte una alarma, cuando la quieres?",defautLanguange)
        elif keyWords[11] in respond:
            generateAudio("Buenas!!!",defautLanguange)
        else:
            generateAudio("Lo siento no te he entendido",defautLanguange)
    else:
        generateAudio("Lo siento no te he entendido",defautLanguange)