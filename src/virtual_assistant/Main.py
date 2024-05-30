import os 
import sys
import random
import re
from dotenv import load_dotenv
from GenerateModule import generateAudio
from MicHandler import getVoice
from LLMModule import getLLMText
from TextHandler import read_file, read_word, read_lines,search_WeatherKeyword,  get_country_from_city, find_city_and_state_in_phrase
from PYFuncionModules.wikiModule import search_wikipedia_summary
from PYFuncionModules.alarmModule import start_alarm_thread, extract_time
from PYFuncionModules.weatherModule import get_weather
from PYFuncionModules.programsHandlerModule import open_program, close_program
from PYFuncionModules.newsModule import get_news_today

#load from .env file key_api for weather
load_dotenv()
api_key = os.getenv("APIWEATHER_KEY") # Load the API key from the .env file
apiNews_Key = os.getenv('APINEWS')# Load the API key from the .env file

#local variables
defaultLanguage = "en-US"
languague = "es"
location = []#array of locatión data of the user
newslock = False#Bool value for non location acepted by the user

# List of original files
files = [
    "../resources/Text/textResources/a.txt",
    "../resources/Text/textResources/ES/EsKeyWordsText02.json",
    "../resources/Text/textResources/ES/EsDefaultSentences01.json",
    "../resources/Text/textResources/ES/EsDefaultLoc03.txt",
    "../resources/Text/textResources/EN/EnKeyWordsText02.json",
    "../resources/Text/textResources/EN/EnDefaultSentences01.json",
    "../resources/Text/textResources/ES/EnDefaultLoc03.txt",
    "../resources/Text/textResources/cities.json"
]

# Normalize routes so that they work on any operating system and save to 'File'
File = [os.path.normpath(file) for file in files]

#initial dialog load
content = read_file(File[0])
print("---------------------------")
print(content)
print("---------------------------")
generateAudio(content, defaultLanguage)

language = getVoice(defaultLanguage)
while language == None:
    language = getVoice(defaultLanguage)

#-----------------------------setup on first run code --------------------------------------------
#default language set 
if "castellano" in language or "Castellano" in language:
    
    defaultLanguage = "es-ES"
    generateAudio("Entendido, te hablaré en castellano a partir de ahora", defaultLanguage)
    language = "es"
    keyWords = read_word(File[1])
    defaultSentences = read_lines(File[2])
    print("---------------------------")
    print("Loaded data: " + str(keyWords) + "| " + str(defaultSentences))
    print("---------------------------")
 
#default localication set spanish
    content = read_file(File[3])
    print("---------------------------")
    print(content)
    print("---------------------------")
    generateAudio(content, defaultLanguage)
    region = getVoice(defaultLanguage)
    while region == None:
        region = getVoice(defaultLanguage)
        
    if "no" in region or "No" in region:
        generateAudio("Entendido, el sistema de noticias queda deshabilitado", defaultLanguage)
        newslock = True
    else:
        location = find_city_and_state_in_phrase(region,File[7])
        generateAudio("Entendido, a si que vives en "+str(location[0])+", en el estado "+str(location[1])+", "+str(location[2]), defaultLanguage)
        print("location of user: "+str(location[0])+", en el estado "+str(location[1])+", "+str(location[2]))

elif "Inglés" in language or "English" in language:
    
    defaultLanguage = "en-US"
    generateAudio("Got it, I will speak to you in English from now on", defaultLanguage)
    language = "en"
    keyWords = read_word(File[4])
    defaultSentences = read_lines(File[5])
    print("---------------------------")
    print("Loaded data: " + str(keyWords) + "| " + str(defaultSentences))
    print("---------------------------")
  
#default localication set english
    content = read_file(File[6])
    print("---------------------------")
    print(content)
    print("---------------------------")
    generateAudio(content, defaultLanguage)
    region = getVoice(defaultLanguage)
    while region == None:
        region = getVoice(defaultLanguage)
        
    if "no" in region or "No" in region:
        generateAudio("Understood, the news system is disabled then", defaultLanguage)
        newslock = True
    else:
        location = find_city_and_state_in_phrase(region,File[7])
        generateAudio("Got it soo you live in "+str(location[0])+", in the state "+str(location[1])+", "+str(location[2]), defaultLanguage)
        print("location of user: "+str(location[0])+", en el estado "+str(location[1])+", "+str(location[2]))

#---------------------------------------------------------------------------------------------------

print(keyWords)   

#while loop for read responses
while True:
    response = getVoice(defaultLanguage).lower()

    if "aurora" in response or "Aurora" in response:  
        response = response.replace("aurora", "")
        
        #module for news handler  (done)     
        if any(keyword in response for keyword in keyWords["newsSearch"]) and newslock == False:
            print("------------------")
            print("News system:")
            print("------------------")
            
            #news = getVoice(defaultLanguage)

            if not api_key:
                print("Error: API key is not configured. Make sure the .env file contains the correct key.")
            else:
                query = "España"
                page_size = 7
                news_by_query = get_news_today(apiNews_Key, query,languague,page_size)
                print("Noticias por consulta en español:")
                for news in news_by_query:
                    print(news)
                print("-----------------------------------------")
        #module for onlineSearch (done) 
        elif any(keyword in response for keyword in keyWords["onlineSearch"]):
            print("------------------")
            print("Online search:")
            print("------------------")
            generateAudio(defaultSentences["onlineSearch"][0], defaultLanguage)
            respond = wiki_search(response,language,3)
            generateAudio(respond, defaultLanguage)
           
        #module for AlarmHandler  (done) 
        elif any(keyword in response for keyword in keyWords["putAlarm"]) and "alarma" in response:
            print("------------------")
            print("Alarm system:")
            print("------------------")
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
            print("------------------")
            print("Weather system:")
            print("------------------")
            city = search_WeatherKeyword(response,File[7])#read the city from the json file
            print(city)
            if city == None:
                generateAudio("Lo siento pero no tengo soporte para la localidad mencionada", defaultLanguage)
            else:
                start_date = "today" # You can change the start date
                end_date = "today" # You can change the end date

                if api_key:
                    respond = get_weather(city, api_key, defaultLanguage)
                    
                    if respond:
                        generateAudio(respond, defaultLanguage)
                    else:
                        print("Could not get time information.")
        
        #module for open programs (done)    
        elif any(keyword in response for keyword in keyWords["openUtilities"]):
            print("------------------")
            print("Open program system:")
            print("------------------")
            
            generateAudio(defaultSentences["openUtilities"][0], defaultLanguage)
      
            words = response.split()
            program_name = words[-1]
      
            open_program(program_name)
                 
        #module for close programs (done)
        elif any(keyword in response for keyword in keyWords["closeUtilities"]):
            print("------------------")
            print("Close program system:")
            print("------------------")
            
            generateAudio(defaultSentences["closeUtilities"][0], defaultLanguage)
            
            words = response.split()
            program_name = words[-1]
            
            close_program(program_name)
                 
        #module for greetings handler  (done)     
        elif any(keyword in response for keyword in keyWords["greeting"]):
            print("------------------")
            print("Greetings system:")
            print("------------------")
            random_greeting = random.choice(defaultSentences["greeting"])
            generateAudio(random_greeting, defaultLanguage)
                        
        #module of conversation with LLM (done)
        else: 
            print("------------------")
            print("LLM system:")
            print("------------------")
            textGenerated = getLLMText(response, 100,defaultLanguage)
            generateAudio(textGenerated, defaultLanguage)
        
    #module for nonUnderstood voice isue (done)  
    else:
        generateAudio(defaultSentences["notUnderstood"][0], defaultLanguage)