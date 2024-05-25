import os 
import sys
import random
import re
from dotenv import load_dotenv
from GenerateModule import generateAudio
from MicHandler import getVoice
from LLMModule import getLLMText
from TextHandler import read_file, read_word, read_lines,search_WeatherKeyword,  get_country_from_city
from PYFuncionModules.wikiModule import wiki_search
from PYFuncionModules.alarmModule import start_alarm_thread, extract_time
from PYFuncionModules.weatherModule import get_weather
from PYFuncionModules.programsHandlerModule import open_program, close_program

#load from .env file key_api for weather
load_dotenv()
apiWeather_Key = os.getenv('APIWEATHER_KEY')

#local variables
defaultLanguage = "en-US"
languague = "es"

File = [
    "../resources/Text/textResources/IntroText01.txt",
    "../resources/Text/textResources/ES/EsKeyWordsText02.json",
    "../resources/Text/textResources/ES/EsDefaultSentences01.json",
    "../resources/Text/textResources/EN/EnKeyWordsText02.json",
    "../resources/Text/textResources/EN/EnDefaultSentences01.json",
    "../resources/Text/textResources/cities.json"
]

#initial dialog load
content = read_file(File[0])
print("---------------------------")
print(content)
print("---------------------------")
generateAudio(content, defaultLanguage)

language = getVoice(defaultLanguage)

#-----------------------------setup on first run code --------------------------------------------
#default language set 
if language == "castellano" or language == "Castellano":
    
    defaultLanguage = "es-ES"
    generateAudio("Entendido, te hablaré en castellano a partir de ahora", defaultLanguage)
    language = "es"
    keyWords = read_word(File[1])
    defaultSentences = read_lines(File[2])
    print("---------------------------")
    print("Loaded data: " + str(keyWords) + "| " + str(defaultSentences))
    print("---------------------------")
elif language == "Inglés" or language == "English":
    
    defaultLanguage = "en-US"
    generateAudio("Got it, I will speak to you in English from now on", defaultLanguage)
    language = "en"
    keyWords = read_word(File[3])
    defaultSentences = read_lines(File[4])
    print("---------------------------")
    print("Loaded data: " + str(keyWords) + "| " + str(defaultSentences))
    print("---------------------------")
    
#---------------------------------------------------------------------------------------------------

#while loop for read responses
while True:
    response = getVoice(defaultLanguage).lower()

    if "aurora" in response:  
        response = response.replace("aurora", "")
        
        #module for onlineSearch (done) 
        if any(keyword in response for keyword in keyWords["onlineSearch"]):
            generateAudio(defaultSentences["onlineSearch"][0], defaultLanguage)
            respond = wiki_search(response,language,3)
            generateAudio(respond, defaultLanguage)
           
        #module for AlarmHandler  (done) 
        elif any(keyword in response for keyword in keyWords["putAlarm"]) and "alarma" in response:
            generateAudio(defaultSentences["putAlarm"][0], defaultLanguage)
            response = getVoice(defaultLanguage).lower()
            alarm_time  = extract_time(response)
            
            if defaultLanguage == "en-US":
                generateAudio("alarm "+alarm_time, defaultLanguage)
            elif defaultLanguage == "es-ES":
                generateAudio("alarma configurada "+alarm_time, defaultLanguage)
              
            start_alarm_thread(alarm_time)
          
        #module for weather handler  (done) 
        elif any(keyword in response for keyword in keyWords["wheaterUtilities"]):
            
            city = search_WeatherKeyword(response,File[5])#read the city from the json file
            print(city)
            if city == None:
                generateAudio("Lo siento pero no tengo soporte para la localidad mencionada", defaultLanguage)
            start_date = "today" # You can change the start date
            end_date = "today" # You can change the end date
            api_key = os.getenv("APIWEATHER_KEY") # Load the API key from the .env file

            if api_key:
                respond = get_weather(city, api_key, defaultLanguage)
                
                if respond:
                    generateAudio(respond, defaultLanguage)
                else:
                    print("Could not get time information.")
        
        #module for open programs (done)    
        elif any(keyword in response for keyword in keyWords["openUtilities"]):
            
            generateAudio(defaultSentences["openUtilities"][0], defaultLanguage)
      
            words = response.split()
            program_name = words[-1]
      
            open_program(program_name)
                 
        #module for close programs (done)
        elif any(keyword in response for keyword in keyWords["closeUtilities"]):
            
            generateAudio(defaultSentences["closeUtilities"][0], defaultLanguage)
            
            words = response.split()
            program_name = words[-1]
            
            close_program(program_name)
                 
        #module for greetings handler  (done)     
        elif any(keyword in response for keyword in keyWords["greeting"]):
            random_greeting = random.choice(defaultSentences["greeting"])
            generateAudio(random_greeting, defaultLanguage)
            
        #module of conversation with LLM (done)
        else: 
            textGenerated = getLLMText(response, 100,defaultLanguage)
            generateAudio(textGenerated, defaultLanguage)
        
    #module for nonUnderstood voice isue (done)  
    else:
        generateAudio(defaultSentences["notUnderstood"][0], defaultLanguage)
