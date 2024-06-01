import os 
import sys
import random
import re
import time
from dotenv import load_dotenv
from GenerateModule import generateAudio
from MicHandler import getVoice
from LLMModule import getLLMText
from TextHandler import read_file, read_word, read_lines,search_WeatherKeyword,  get_country_from_city, find_city_and_state_in_phrase, text_cleaner
from PYFuncionModules.wikiModule import search_wikipedia_summary
from PYFuncionModules.alarmModule import start_alarm_thread, extract_time
from PYFuncionModules.weatherModule import get_weather
from PYFuncionModules.programsHandlerModule import open_program, close_program
from PYFuncionModules.newsModule import get_news_today
from Security.LogHandler import start_logger

if __name__ == "__main__":
    
    #load from .env file key_api for weather
    load_dotenv()
    api_key = os.getenv("APIWEATHER_KEY") # Load the API key from the .env file
    apiNews_Key = os.getenv('APINEWS')# Load the API key from the .env file

    #local variables
    defaultLanguage = "en-US"
    languague = "es"
    location = []#array of locatión data of the user
    newslock = False#Bool value for non location acepted by the user

    # List of files
    File = [
        "../resources/Text/textResources/IntroText01.txt",
        "../resources/Text/textResources/ES/EsKeyWordsText02.json",
        "../resources/Text/textResources/ES/EsDefaultSentences01.json",
        "../resources/Text/textResources/ES/EsDefaultLoc03.txt",
        "../resources/Text/textResources/ES/EsUse04.txt",
        "../resources/Text/textResources/EN/EnKeyWordsText02.json",
        "../resources/Text/textResources/EN/EnDefaultSentences01.json",
        "../resources/Text/textResources/ES/EnDefaultLoc03.txt",
        "../resources/Text/textResources/EN/EnUse04.txt",
        "../resources/Text/textResources/cities.json",
        "../resources/Logs/Data.log"
    ]

    queue, log_process = start_logger(File[10])
    queue.put("-----------------------------")
    queue.put("Aurora system start")

    print("---------------------------")
    print("Log system activated, registered")
    print("---------------------------")

    try:
        
        #initial dialog load
        content = read_file(File[0])
        print("---------------------------")
        print(content)
        print("---------------------------")
        generateAudio(content, defaultLanguage)
        
        queue.put("Correct default keyword and sentences lecture")

        language = getVoice(defaultLanguage)
        while language == None:
            language = getVoice(defaultLanguage)

        #-----------------------------setup on first run code --------------------------------------------
        #default language set 
        if "castellano" in language or "Castellano" in language:
            
            queue.put("Castellano for default language choosen")
            
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
            while region == "":
                region = getVoice(defaultLanguage)
                
            if "no" in region or "No" in region:
                generateAudio("Entendido, el sistema de noticias queda deshabilitado", defaultLanguage)
                queue.put("No location set")
                newslock = True
            else:
                location = find_city_and_state_in_phrase(region,File[9])
                generateAudio("Entendido, a si que vives en "+str(location[0])+", en el estado "+str(location[1])+", "+str(location[2]), defaultLanguage)
                queue.put("Location set: "+str(location))
                print("location of user: "+str(location))
                
            content = read_file(File[4])
            print("---------------------------")
            print(content)
            print("---------------------------")
            generateAudio(content, defaultLanguage)


        elif "Inglés" in language or "English" in language:
            
            queue.put("Inglés for default language choosen")
            
            defaultLanguage = "en-US"
            generateAudio("Got it, I will speak to you in English from now on", defaultLanguage)
            language = "en"
            keyWords = read_word(File[5])
            defaultSentences = read_lines(File[6])
            print("---------------------------")
            print("Loaded data: " + str(keyWords) + "| " + str(defaultSentences))
            print("---------------------------")
        
        #default localication set english
            content = read_file(File[7])
            print("---------------------------")
            print(content)
            print("---------------------------")
            generateAudio(content, defaultLanguage)
            region = getVoice(defaultLanguage)
            while region == "":
                region = getVoice(defaultLanguage)
                
            if "no" in region or "No" in region:
                generateAudio("Understood, the news system is disabled then", defaultLanguage)
                queue.put("No location set")
                newslock = True
            else:
                location = find_city_and_state_in_phrase(region,File[9])
                generateAudio("Got it soo you live in "+str(location[0])+", in the state "+str(location[1])+", "+str(location[2]), defaultLanguage)
                queue.put("Location set by user")
                print("location of user: "+str(location[0])+", en el estado "+str(location[1])+", "+str(location[2]))
                
            content = read_file(File[8])
            print("---------------------------")
            print(content)
            print("---------------------------")
            generateAudio(content, defaultLanguage)

        #---------------------------------------------------------------------------------------------------

        print(keyWords)   

        #while loop for read responses
        while True:
            response = getVoice(defaultLanguage).lower()

            if "aurora" in response or "Aurora" in response:  
                response = response.replace("aurora", "")
                
                #module for news handler  (done)     
                if any(keyword in response for keyword in keyWords["newsSearch"]):
                    
                    
                    if newslock == True:
                        
                        generateAudio(defaultSentences["newsLock"][0]+str(location), defaultLanguage)
                        print("------------------")
                        print("News system lock")
                        print("------------------")
                        
                        queue.put("News system lock, user try to access")
                        
                    else:
                        print("------------------")
                        print("News system:")
                        print("------------------")
                        
                        queue.put("Entry to News system module")
                        
                        if not api_key:
                            print("Error: API key is not configured. Make sure the .env file contains the correct key.")
                            queue.put("Error: API key is not configured. Make sure the .env file contains the correct key.")
                        else:
                            query = location[0]
                            generateAudio(defaultSentences["news"][0]+str(location), defaultLanguage)
                            page_size = 7
                            news_by_query = get_news_today(apiNews_Key, query,languague,page_size,queue)
                            print("News for consultation in: "+str(location))

                            # Select two unique random indexes
                            random_indices = random.sample(range(len(news_by_query)), 2)
                            queue.put("News data received correctly")

                            # Iterate over random indexes and concatenate titles and contents
                            for i in random_indices:
                                concatenated_content = ""
                                news = news_by_query[i]
                                print("New:", i+1)

                                clean_title = text_cleaner(news['title'])
                                print("Title:", clean_title)
                                concatenated_content += clean_title + "     "  # Add the clean content to the concatenated string

                                clean_content = text_cleaner(news['content'])
                                print("Content:", clean_content)
                                concatenated_content += clean_content + " "  # Add the clean content to the concatenated string

                                generateAudio(concatenated_content, defaultLanguage)

                                print()
                            
                            print("-----------------------------------------")
                            
                            generateAudio(defaultSentences["news"][1], defaultLanguage)
                        
                #module for onlineSearch (done) 
                elif any(keyword in response for keyword in keyWords["onlineSearch"]):
                    print("------------------")
                    print("Online search:")
                    print("------------------")
                    
                    queue.put("Entry yo Online search module")
                    
                    generateAudio(defaultSentences["onlineSearch"][0], defaultLanguage)
                    respond =  search_wikipedia_summary(response,language,queue,3)
                    if respond != "":
                        generateAudio(respond, defaultLanguage)
                        queue.put("Correct search online data")
                    else: 
                        queue.put("Error: search online data")
                
                #module for AlarmHandler  (done) 
                elif any(keyword in response for keyword in keyWords["putAlarm"]) and "alarma" in response:
                    print("------------------")
                    print("Alarm system:")
                    print("------------------")
                    
                    queue.put("Entry to alarm module")
                    
                    generateAudio(defaultSentences["putAlarm"][0], defaultLanguage)
                    response = getVoice(defaultLanguage).lower()
                    alarm_time  = extract_time(response)
                    
                    if defaultLanguage == "en-US":
                        generateAudio("alarm "+alarm_time, defaultLanguage)

                    elif defaultLanguage == "es-ES":
                        generateAudio("alarma configurada "+alarm_time, defaultLanguage)

                    
                    start_alarm_thread(alarm_time)
                    queue.put("Correct alarm set")
                
                #module for weather handler  (done) 
                elif any(keyword in response for keyword in keyWords["wheaterUtilities"]):
                    print("------------------")
                    print("Weather system:")
                    print("------------------")
                    
                    queue.put("Entry to Weather module")
                    
                    city = search_WeatherKeyword(response,File[9])#read the city from the json file
                    print(city)
                    if city == "":
                        
                        city = location[0] #in case of no location in sentence , auto add location fron register
                        
                        if location == "":
                            generateAudio(defaultSentences["wheaterNotLoc"][0], defaultLanguage)
                            queue.put("Error: local data not seted in scope")
                            
                    else:
                        start_date = "today" # start date
                        end_date = "today" # end date

                        if api_key:
                            respond = get_weather(city, api_key, defaultLanguage,queue)
                            queue.put("Weather correct data ")
                            
                            if respond:
                                generateAudio(respond, defaultLanguage)
                            else:
                                print("Could not get time information.")
                                queue.put("Could not get time information.")
                
                #module for open programs (done)    
                elif any(keyword in response for keyword in keyWords["openUtilities"]):
                    print("------------------")
                    print("Open program system:")
                    print("------------------")
                    
                    queue.put("Entry to open programs module")
                    
                    generateAudio(defaultSentences["openUtilities"][0], defaultLanguage)
            
                    words = response.split()
                    program_name = words[-1]
            
                    open_program(program_name,queue)
                        
                #module for close programs (done)
                elif any(keyword in response for keyword in keyWords["closeUtilities"]):
                    print("------------------")
                    print("Close program system:")
                    print("------------------")
                    
                    queue.put("Entry to Close programs module")
                    
                    generateAudio(defaultSentences["closeUtilities"][0], defaultLanguage)
                    
                    words = response.split()
                    program_name = words[-1]
                    
                    close_program(program_name,queue)
                        
                #module for greetings handler  (done)     
                elif any(keyword in response for keyword in keyWords["greeting"]):
                    print("------------------")
                    print("Greetings system:")
                    print("------------------")
                    
                    queue.put("Entry to Greetings module")
                    
                    random_greeting = random.choice(defaultSentences["greeting"])
                    generateAudio(random_greeting, defaultLanguage)
                                
                #module of conversation with LLM (done)
                else: 
                    print("------------------")
                    print("LLM system:")
                    print("------------------")
                    
                    queue.put("Entry to LLM module")
                    
                    textGenerated = getLLMText(response, 100,defaultLanguage)
                    generateAudio(textGenerated, defaultLanguage,queue)
                
            #module for nonUnderstood voice isue (done)  
            else:
                generateAudio(defaultSentences["notUnderstood"][0], defaultLanguage)
        

    except (KeyboardInterrupt, EOFError):
        print("---------------------------")
        print("Keyboard interrupt detected.")
        print("---------------------------")
        log_process.terminate()  # Ensure the logger process is terminated
        log_process.join()  # Wait for the logger process to join
        sys.exit(0)
        
    finally:
        log_process.terminate()  # Ensure the logger process is terminated
        log_process.join()  # Wait for the logger process to join
        print("---------------------------")
        print("Logger finish.")
        print("---------------------------")