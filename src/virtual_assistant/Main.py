import os 
import sys
import random
from GenerateModule import generateAudio
from MicHandler import getVoice
from LLMModule import getLLMText
from TextHandler import read_file, read_word, read_lines
from PYFuncionModules.wikiModule import wiki_search
from PYFuncionModules.alarmModule import start_alarm_thread, extract_time

#local variables
defaultLanguage = "es-ES"
languague = "es"

File = [
    "../resources/Text/textResources/a.txt",
    "../resources/Text/textResources/ES/EsKeyWordsText02.json",
    "../resources/Text/textResources/ES/EsDefaultSentences01.json",
    "../resources/Text/textResources/EN/EnKeyWordsText02.json",
    "../resources/Text/textResources/EN/EnDefaultSentences01.json"
]

content = read_file(File[0])
print(content)
generateAudio(content, defaultLanguage)

language = getVoice(defaultLanguage)

#default language set 
if language == "castellano":
    
    generateAudio("Entendido, te hablaré en castellano a partir de ahora", defaultLanguage)
    defaultLanguage = "es-ES"
    language = "es"
    keyWords = read_word(File[1])
    defaultSentences = read_lines(File[2])
    print(keyWords,defaultSentences)
else:
    
    generateAudio("Got it, I will speak to you in English from now on", defaultLanguage)
    defaultLanguage = "en-US"
    language = "en"
    keyWords = read_word(File[3])
    defaultSentences = read_lines(File[4])
    print(keyWords,defaultSentences)

#while loop for read responses
while True:
    response = getVoice(defaultLanguage).lower()

    if "aurora" in response:  
        response = response.replace("aurora", "")
        
        #module for onlineSearch
        if any(keyword in response for keyword in keyWords["onlineSearch"]):
            generateAudio(defaultSentences["onlineSearch"][0], defaultLanguage)
            respond = wiki_search(response,language,3)
            generateAudio(respond, defaultLanguage)
           
        #module for AlarmHandler    
        elif any(keyword in response for keyword in keyWords["putAlarm"]) and "alarma" in response:
            generateAudio(defaultSentences["putAlarm"][0], defaultLanguage)
            response = getVoice(defaultLanguage).lower()
            alarm_time  = extract_time(response)
            
            if defaultLanguage == "en-US":
                generateAudio("alarm "+alarm_time, defaultLanguage)
            elif defaultLanguage == "es-ES":
                generateAudio("alarma configurada "+alarm_time, defaultLanguage)
              
            start_alarm_thread(alarm_time)
          
        #module for LLM(AI) handler                
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
                    
        elif any(keyword in response for keyword in keyWords["openUtilities"]):
            generateAudio(defaultSentences["openUtilities"][0], defaultLanguage)
                    
        elif any(keyword in response for keyword in keyWords["closeUtilities"]):
            generateAudio(defaultSentences["closeUtilities"][0], defaultLanguage)
                 
        #module for greetings handler       
        elif any(keyword in response for keyword in keyWords["greeting"]):
            random_greeting = random.choice(defaultSentences["greeting"])
            generateAudio(random_greeting, defaultLanguage)
            
        else:
            generateAudio(defaultSentences["notUnderstood"][0], defaultLanguage)
