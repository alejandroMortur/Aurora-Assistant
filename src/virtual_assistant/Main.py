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
        "../resources/Text/textResources/EN/EnDefaultLoc03.txt",
        "../resources/Text/textResources/EN/EnUse04.txt",
        "../resources/Text/textResources/cities.json",
        "../resources/Logs/Data.log"
    ]

    #Log system run
    queue, log_process = start_logger(File[10])
    queue.put("-----------------------------")
    queue.put("Aurora system start")#First log system flag

    print("---------------------------")
    print("Log system activated, registered")
    print("---------------------------")

    try:
        
        #initial dialog load
        content = read_file(File[0])
        print("---------------------------")
        print(content)
        print("---------------------------")
        generateAudio(content, defaultLanguage)#generate audio from text introduction file 

        language = ""
        language = getVoice(defaultLanguage)
        while language == None:
            language = getVoice(defaultLanguage)

        #-----------------------------setup on first run code --------------------------------------------
        #default language set 
        if "castellano" in language or "Castellano" in language:
            
            queue.put("Castellano for default language choosen")#log system flag for language set
            
            #set default language system for the Micmodule system
            defaultLanguage = "es-ES"
            language = "es"
            
            generateAudio("Entendido, te hablaré en castellano a partir de ahora", defaultLanguage)
            
            #load keyword and default sentences
            keyWords = read_word(File[1])
            defaultSentences = read_lines(File[2])
            
            queue.put("Correct default keyword and sentences lecture")#log system flag for keyword and default sentences
            
            print("---------------------------")
            print("Loaded data: " + str(keyWords) + "| " + str(defaultSentences))
            print("---------------------------")
        
        #default localication set spanish
            content = read_file(File[3])#load loc dialog fro file
            print("---------------------------")
            print(content)
            print("---------------------------")
            generateAudio(content, defaultLanguage)#generate audio from text loc file 
            
            #code to get respond from the user
            region = ""
            region = getVoice(defaultLanguage)
            while region == "":
                region = getVoice(defaultLanguage)
                
            #if user had said no , the assistant will block de news system (because not loc seted)
            if "no" in region or "No" in region:
                generateAudio("Entendido, el sistema de noticias queda deshabilitado", defaultLanguage)
                queue.put("No location set")#log system flag for block news system
                newslock = True#set bool block true
                
            #if user had said a loc, then we find the loc in the loc file and we save it
            else:
                location = find_city_and_state_in_phrase(region,File[9])
                generateAudio("Entendido, a si que vives en "+str(location[0])+", en el estado "+str(location[1])+", "+str(location[2]), defaultLanguage)#generate confirmation voice
                queue.put("Location set: "+str(location))#log system flag for loc set
                print("location of user: "+str(location))
                
            #get final tutorial dialog for user
            content = read_file(File[4])
            print("---------------------------")
            print(content)
            print("---------------------------")
            generateAudio(content, defaultLanguage)#generate final tutorial voice from text


        elif "Inglés" in language or "English" in language:
            
            queue.put("English for default language choosen")#log system flag for language set
            
            #set default language system for the Micmodule system
            defaultLanguage = "en-US"
            language = "en"
            
            #log system flag for keyword and default sentences
            keyWords = read_word(File[5])
            defaultSentences = read_lines(File[6])
            
            generateAudio("Got it, I will speak to you in English from now on", defaultLanguage)
            
            print("---------------------------")
            print("Loaded data: " + str(keyWords) + "| " + str(defaultSentences))
            print("---------------------------")
        
        #default localication set english
            content = read_file(File[7])#load loc dialog fro file
            print("---------------------------")
            print(content)
            print("---------------------------")
            generateAudio(content, defaultLanguage)#generate audio from text loc file 
            
            #code to get respond from the user
            #while loop used to get al the time the voice if is an error during record
            region = ""
            region = getVoice(defaultLanguage)
            while region == "":
                region = getVoice(defaultLanguage)
                
            #if user had said no , the assistant will block de news system (because not loc seted)
            if "no" in region or "No" in region:
                generateAudio("Understood, the news system is disabled then", defaultLanguage)
                queue.put("No location set")#log system flag for block news system
                newslock = True#set bool block true
                
            #if user had said a loc, then we find the loc in the loc file and we save it
            else:
                location = find_city_and_state_in_phrase(region,File[9])
                generateAudio("Got it soo you live in "+str(location[0])+", in the state "+str(location[1])+", "+str(location[2]), defaultLanguage)#generate confirmation voice
                queue.put("Location set by user")#log system flag for loc set
                print("location of user: "+str(location[0])+", en el estado "+str(location[1])+", "+str(location[2]))
                
            #get final tutorial dialog for user
            content = read_file(File[8])
            print("---------------------------")
            print(content)
            print("---------------------------")
            generateAudio(content, defaultLanguage)#generate final tutorial voice from text

        #---------------------------------------------------------------------------------------------------

        #while loop for read responses from the user
        while True:
            
            #while loop used to get al the time the voice if is an error during record
            response = ""
            response = getVoice(defaultLanguage).lower()
            while response == "":
                response = getVoice(defaultLanguage).lower()

            #If in the record is the name aurora the assistant starts to prepare to work
            if "aurora" in response or "Aurora" in response:  
                response = response.replace("aurora", "")
                
                # Module for news handler:  (done)  
                # This module handles news-related queries. If the user request includes any of the specified keywords for news search,
                # the system checks if the news feature is locked.:
                # 
                # ->If it is locked, an audio message indicating the lock status is generated and logged, and the access attempt is noted in the queue. 
                # ->If the feature is not locked and the API key is configured: 
                # The system proceeds to fetch news based on the user's location. It then selects two random news items, cleans the text for the
                # title and content, generates audio for the cleaned text, and outputs it. The system also logs relevant actions and errors
                # into the queue for tracking purposes.   
                if any(keyword in response for keyword in keyWords["newsSearch"]):
                    
                    
                    if newslock == True:
                        
                        generateAudio(defaultSentences["newsLock"][0]+str(location), defaultLanguage)
                        print("------------------")
                        print("News system lock")
                        print("------------------")
                        
                        queue.put("News system lock, user try to access")#log system flag for lock news
                        
                    else:
                        print("------------------")
                        print("News system:")
                        print("------------------")
                        
                        queue.put("Entry to News system module") #log system flag for access to the news block
                        
                        if not api_key:
                            print("Error: API key is not configured. Make sure the .env file contains the correct key.")
                            queue.put("Error: API key is not configured. Make sure the .env file contains the correct key.")
                        else:
                            query = location[0]
                            generateAudio(defaultSentences["news"][0]+str(location), defaultLanguage) #generate voice from default sentences
                            page_size = 7
                            news_by_query = get_news_today(apiNews_Key, query,languague,page_size,queue)
                            print("News for consultation in: "+str(location))

                            # Select two unique random indexes
                            random_indices = random.sample(range(len(news_by_query)), 2)
                            queue.put("News data received correctly")#log system flag for correct data

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

                                generateAudio(concatenated_content, defaultLanguage)#generate voice from the respond 

                                print()
                            
                            print("-----------------------------------------")
                            
                            generateAudio(defaultSentences["news"][1], defaultLanguage) #generate voice from the default sentences
                        
                # Module for onlineSearch (done) 
                # This module handles online search queries. If the user request includes any of the specified keywords for online search:
                # 
                # -> The system logs the entry into the online search module and generates an audio message indicating the start of the search.
                # -> It performs a Wikipedia summary search based on the user's query. If a response is received, it generates an audio message
                #    with the search result and logs the successful data retrieval. If no response is received, it logs an error message.

                elif any(keyword in response for keyword in keyWords["onlineSearch"]):
                    print("------------------")
                    print("Online search:")
                    print("------------------")
                    
                    queue.put("Entry yo Online search module") #log system flag for access to the online search module
                    
                    generateAudio(defaultSentences["onlineSearch"][0], defaultLanguage) #generate voice from the default sentences
                    respond =  search_wikipedia_summary(response,language,queue,3)
                    if respond != "":
                        generateAudio(respond, defaultLanguage) #generate voice from the respond
                        queue.put("Correct search online data") #log system flag for correct data
                    else: 
                        queue.put("Error: search online data") #log system flag an error
                
                # Module for AlarmHandler (done)
                # This module handles alarm-setting queries. If the user request includes any of the specified keywords for setting an alarm and the word "alarma":
                # 
                # -> The system logs the entry into the alarm module and generates an audio message indicating the start of the alarm setup.
                # -> It then captures the user's voice input for the alarm time, extracts the time from the input, and sets the alarm accordingly.
                # -> Based on the default language, it generates an appropriate audio message confirming the alarm time.
                # -> Finally, it starts the alarm thread and logs the successful alarm setup.
                elif any(keyword in response for keyword in keyWords["putAlarm"]) and "alarma" in response:
                    print("------------------")
                    print("Alarm system:")
                    print("------------------")
                    
                    queue.put("Entry to alarm module") #log system flag access to the alarm block
                    
                    generateAudio(defaultSentences["putAlarm"][0], defaultLanguage) #generate voice from the default sentences
                    response = ""
                    response = getVoice(defaultLanguage).lower()
                    alarm_time  = extract_time(response)
                    
                    if defaultLanguage == "en-US":
                        generateAudio("alarm "+alarm_time, defaultLanguage) #generate voice from the default sentences in Es

                    elif defaultLanguage == "es-ES":
                        generateAudio("alarma configurada "+alarm_time, defaultLanguage) #generate voice from the default sentences in En

                    
                    start_alarm_thread(alarm_time)
                    queue.put("Correct alarm set") #log system flag for alarm set
                
                # Module for weather handler (done)
                # This module handles weather-related queries. If the user request includes any of the specified keywords for weather utilities:
                # 
                # -> The system logs the entry into the weather module and attempts to identify the city from the user's query using a JSON file.
                # -> If no city is found in the query, it defaults to the user's registered location. If no location is available, it generates an 
                #    audio message indicating the error and logs it.
                # -> If a city is identified and the API key is configured, it fetches weather data for the specified city, logs the successful data 
                #    retrieval, generates an audio message with the weather information, and logs the error if the data retrieval fails.
                elif any(keyword in response for keyword in keyWords["wheaterUtilities"]):
                    print("------------------")
                    print("Weather system:")
                    print("------------------")
                    
                    queue.put("Entry to Weather module") #log system flag for access to the weather module
                    
                    city = search_WeatherKeyword(response,File[9])#read the city from the json file
                    print(city)
                    if city == "":
                        
                        city = location[0] #in case of no location in sentence , auto add location fron register
                        
                        if location == "":
                            generateAudio(defaultSentences["wheaterNotLoc"][0], defaultLanguage) #generate voice from the default sentences
                            queue.put("Error: local data not seted in scope") #log system flag for error if is not loc
                            
                    else:
                        start_date = "today" # start date
                        end_date = "today" # end date

                        if api_key:
                            respond = get_weather(city, api_key, defaultLanguage,queue)
                            queue.put("Weather correct data ") #log system flag correct data get
                            
                            if respond:
                                generateAudio(respond, defaultLanguage) #generate voice from the respond
                            else:
                                print("Could not get time information.")
                                queue.put("Could not get time information.") #log system flag for error of data
                
                # Module for open programs (done)
                # This module handles queries to open programs. If the user request includes any of the specified keywords for opening utilities:
                # 
                # -> The system logs the entry into the open programs module and generates an audio message indicating the start of the program opening process.
                # -> It then extracts the program name from the user's query, which is assumed to be the last word in the response.
                # -> Finally, it calls a function to open the specified program and logs the action.            
                elif any(keyword in response for keyword in keyWords["openUtilities"]):
                    print("------------------")
                    print("Open program system:")
                    print("------------------")
                    
                    queue.put("Entry to open programs module") #log system flag for access to the open program module
                    
                    generateAudio(defaultSentences["openUtilities"][0], defaultLanguage) #generate voice from the default sentences
            
                    words = response.split()
                    program_name = words[-1]
            
                    open_program(program_name,queue)
                        
                # Module for close programs (done)
                # This module handles queries to close programs. If the user request includes any of the specified keywords for closing utilities:
                # 
                # -> The system logs the entry into the close programs module and generates an audio message indicating the start of the program closing process.
                # -> It then extracts the program name from the user's query, which is assumed to be the last word in the response.
                # -> Finally, it calls a function to close the specified program and logs the action.
                elif any(keyword in response for keyword in keyWords["closeUtilities"]):
                    print("------------------")
                    print("Close program system:")
                    print("------------------")
                    
                    queue.put("Entry to Close programs module") #log system flag for access to the close program module
                    
                    generateAudio(defaultSentences["closeUtilities"][0], defaultLanguage) #generate voice from the default sentences
                    
                    words = response.split()
                    program_name = words[-1]
                    
                    close_program(program_name,queue)
                        
                # Module for greetings handler (done)
                # This module handles greeting-related queries. If the user request includes any of the specified keywords for greetings:
                # 
                # -> The system logs the entry into the greetings module and generates an audio message indicating the start of the greetings process.
                # -> It selects a random greeting from the predefined list of greetings and generates an audio message with the selected greeting.
                    
                elif any(keyword in response for keyword in keyWords["greeting"]):
                    print("------------------")
                    print("Greetings system:")
                    print("------------------")
                    
                    queue.put("Entry to Greetings module")  #log system flag for access to the greetings system module
                    
                    random_greeting = random.choice(defaultSentences["greeting"])
                    generateAudio(random_greeting, defaultLanguage) #generate voice from the random greetings
                                
                # Module for LLM system (done)
                # This module handles general queries that do not match any specific keywords and are passed to the language model (LLM) for processing:
                # 
                # -> The system logs the entry into the LLM module and generates an audio message indicating the start of the LLM process.
                # -> It generates a response text using the LLM based on the user's query, with a specified maximum length.
                # -> Finally, it generates an audio message with the generated text and logs the action.
                else: 
                    print("------------------")
                    print("LLM system:")
                    print("------------------")
                    
                    queue.put("Entry to LLM module") #log system flag for access to the LLM module
                    
                    textGenerated = getLLMText(response, 100,defaultLanguage,queue)
                    generateAudio(textGenerated, defaultLanguage,queue) #generate voice from the respond
                
            # Module for non-understood voice issue (done)
            # This module handles cases where the user's query does not match any known keywords or commands:
            # 
            # -> The system generates an audio message indicating that it did not understand the user's request using a predefined message.
            else:
                generateAudio(defaultSentences["notUnderstood"][0], defaultLanguage)
        

    except (KeyboardInterrupt, EOFError):
        # If a KeyboardInterrupt or EOFError is raised during execution:
        print("---------------------------")
        print("Keyboard interrupt detected.")
        print("---------------------------")
        log_process.terminate()  # Ensure the logger process is terminated
        log_process.join()  # Wait for the logger process to join
        sys.exit(0)
        
    finally:
        # Regardless of whether an exception was raised or not, execute the following block of code
        log_process.terminate()  # Ensure the logger process is terminated
        log_process.join()  # Wait for the logger process to join
        print("---------------------------")
        print("Logger finish.")
        print("---------------------------")
