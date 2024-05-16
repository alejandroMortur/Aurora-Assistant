import os 
import sys
import random
from GenerateModule import generateAudio
from MicHandler import getVoice
from LLMModule import getLLMText
from TextHandler import read_file, read_word, read_lines

defaultLanguage = "es-ES"

File = [
    "./textResources/a.txt",
    "./textResources/ES/EsKeyWordsText02.json",
    "./textResources/ES/EsDefaultSentences01.json",
    "./textResources/EN/EnKeyWordsText02.json",
    "./textResources/EN/EnDefaultSentences01.json"
]

content = read_file(File[0])
print(content)
generateAudio(content, defaultLanguage)

language = getVoice(defaultLanguage)
if language == "castellano":
    
    generateAudio("Entendido, te hablaré en castellano a partir de ahora", defaultLanguage)
    defaultLanguage = "es-ES"
    keyWords = read_word(File[1])
    defaultSentences = read_lines(File[2])
    print(keyWords,defaultSentences)
else:
    
    generateAudio("Got it, I will speak to you in English from now on", defaultLanguage)
    defaultLanguage = "en-US"
    keyWords = read_word(File[3])
    defaultSentences = read_lines(File[4])
    print(keyWords,defaultSentences)

while True:
    response = getVoice(defaultLanguage).lower()

    if "aurora" in response:  
        response = response.replace("aurora", "")
        
        if any(keyword in response for keyword in keyWords["onlineSearch"]):
            generateAudio(defaultSentences["onlineSearch"][0], defaultLanguage)
            
        elif any(keyword in response for keyword in keyWords["openUtilities"]):
            generateAudio(defaultSentences["openUtilities"][0], defaultLanguage)
            
        elif any(keyword in response for keyword in keyWords["LLMUtilities"]):
            generateAudio(defaultSentences["LLMUtilities"][0], defaultLanguage)
            textGenerated = getLLMText(response, 100)
            generateAudio(textGenerated, defaultLanguage)
            generateAudio(defaultSentences["moreInfo"][0], defaultLanguage)
            moreText = ""
            
            while all(keyword not in moreText for keyword in keyWords["moreInfo"]): 
                moreText = getVoice(defaultLanguage).lower()
                
                if any(keyword in moreText for keyword in keyWords["moreInfo"]):
                    textGenerated = getLLMText(response, 200)
                    generateAudio(textGenerated, defaultLanguage)
                    
        elif any(keyword in response for keyword in keyWords["closeUtilities"]):
            generateAudio(defaultSentences["closeUtilities"][0], defaultLanguage)
            
        elif any(keyword in response for keyword in keyWords["putAlarm"]) and "alarma" in response:
            generateAudio(defaultSentences["putAlarm"][0], defaultLanguage)
            
        elif any(keyword in response for keyword in keyWords["greeting"]):
            random_greeting = random.choice(defaultSentences["greeting"])
            generateAudio(random_greeting, defaultLanguage)
            
        else:
            generateAudio(defaultSentences["notUnderstood"][0], defaultLanguage)
    else:
        generateAudio(defaultSentences["notUnderstood"][0], defaultLanguage)