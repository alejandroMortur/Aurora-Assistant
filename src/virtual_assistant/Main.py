import os 
import sys
import random
import re
import time
from dotenv import load_dotenv
from GenerateModule import generateAudio
from MicHandler import getVoice
from LLMModule import getLLMText
from TextHandler import read_file, read_word, read_lines,search_weather_keyword,  get_country_from_city, find_city_and_state_in_phrase, text_cleaner
from pyfuncionmodules.wikiModule import search_wikipedia_summary
from pyfuncionmodules.alarmModule import start_alarm_thread, extract_time
from pyfuncionmodules.weatherModule import get_weather
from pyfuncionmodules.programsHandlerModule import open_program, close_program
from pyfuncionmodules.newsModule import get_news_today
from Security.LogHandler import start_logger

if __name__ == "__main__":
    
    #load from .env file key_api for weather
    load_dotenv()

    API_KEY = os.getenv("APIWEATHER_KEY")  # Load the API key from the .env file
    API_NEWS_KEY = os.getenv('APINEWS')   # Load the API key from the .env file

    #local variables
    default_Language = "en-US"
    language = "es"
    location = []#array of location data of the user
    news_lock = False#Bool value for non location accepted by the user

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

        generateAudio(content, default_Language)#generate audio from text introduction file 
        language = ""
        language = getVoice(default_Language)

        while language == None:
            language = getVoice(default_Language)

        #-----------------------------setup on first run code --------------------------------------------
        #default language set 

        if "castellano" in language or "Castellano" in language:
            
            queue.put("Castellano for default language chosen")#log system flag for language set
    
            #set default language system for the MicModule system
            default_Language = "es-ES"
            language = "es"
            
            generateAudio("Entendido, te hablaré en castellano a partir de ahora", default_Language)
            
            #load keyword and default sentences
            keyWords = read_word(File[1])
            default_sentences = read_lines(File[2])
            
            queue.put("Correct default keyword and sentences lecture")#log system flag for keyword and default sentences
            
            print("---------------------------")
            print("Loaded data: " + str(keyWords) + "| " + str(default_sentences))
            print("---------------------------")
        
            #default location set spanish
            content = read_file(File[3])#load loc dialog fro file

            print("---------------------------")
            print(content)
            print("---------------------------")

            generateAudio(content, default_Language)#generate audio from text loc file 
            
            #code to get respond from the user
            region = ""
            region = getVoice(default_Language)

            while region == "":
                region = getVoice(default_Language)
                
            #if user had said no , the assistant will block de news system (because not loc seted)
            if "no" in region or "No" in region:
                
                generateAudio("Entendido, el sistema de noticias queda deshabilitado", default_Language)
                queue.put("No location set")#log system flag for block news system
                news_lock = True#set bool block true
                
            #if user had said a loc, then we find the loc in the loc file and we save it
            else:
                
                location = find_city_and_state_in_phrase(region,File[9])
                
                #generate confirmation voice
                generateAudio("Entendido, a si que vives en "+str(location[0])+", en el estado "+str(location[1])+", "+str(location[2]), default_Language)
                
                queue.put("Location set: "+str(location))#log system flag for loc set
                print("location of user: "+str(location))
                
            #get final tutorial dialog for user
            content = read_file(File[4])
            
            print("---------------------------")
            print(content)
            print("---------------------------")
            
            generateAudio(content, default_Language)#generate final tutorial voice from text
            
        elif "Inglés" in language or "English" in language:
            
            queue.put("English for default language choosen")#log system flag for language set
            
            #set default language system for the MicModule system
            default_Language = "en-US"
            language = "en"
            
            #log system flag for keyword and default sentences
            keyWords = read_word(File[5])
            default_sentences = read_lines(File[6])
            
            generateAudio("Got it, I will speak to you in English from now on", default_Language)
            
            print("---------------------------")
            print("Loaded data: " + str(keyWords) + "| " + str(default_sentences))
            print("---------------------------")
            
        #default location set english
            content = read_file(File[7])#load loc dialog fro file
            
            print("---------------------------")
            print(content)
            print("---------------------------")
            
            generateAudio(content, default_Language)#generate audio from text loc file 
            
            #code to get respond from the user
            #while loop used to get al the time the voice if is an error during record
            region = ""
            region = getVoice(default_Language)
            
            while region == "":
                region = getVoice(default_Language)
                
            #if user had said no , the assistant will block de news system (because not loc seted)
            if "no" in region or "No" in region:
                
                generateAudio("Understood, the news system is disabled then", default_Language)
                queue.put("No location set")#log system flag for block news system
                news_lock = True#set bool block true
                
            #if user had said a loc, then we find the loc in the loc file and we save it
            else:
                
                location = find_city_and_state_in_phrase(region,File[9])
                
                #generate confirmation voice
                generateAudio("Got it soo you live in "+str(location[0])+", in the state "+str(location[1])+", "+str(location[2]), default_Language)
                queue.put("Location set by user")#log system flag for loc set
                
                print("location of user: "+str(location[0])+", en el estado "+str(location[1])+", "+str(location[2]))
                
            #get final tutorial dialog for user
            content = read_file(File[8])
            
            print("---------------------------")
            print(content)
            print("---------------------------")
            
            generateAudio(content, default_Language)#generate final tutorial voice from text
            
        #---------------------------------------------------------------------------------------------------
        
        #while loop for read responses from the user
        while True:
        
            #while loop used to get al the time the voice if is an error during record
            response = ""
            response = getVoice(default_Language).lower()
            
            while response == "":
                response = getVoice(default_Language).lower()

            #If in the record is the name aurora the assistant starts to prepare to work
            if "aurora" in response or "Aurora" in response:  
                
                response = response.replace("aurora", "")
                                
                if any(keyword in response for keyword in keyWords["newsSearch"]):
                    
                    """
                    Module for news handler.

                    This module handles news-related queries. If the user's request includes any of the specified keywords for news search,
                    the system checks if the news feature is locked.

                    If the news feature is locked:
                        - An audio message indicating the lock status is generated and logged.
                        - The access attempt is noted in the queue.

                    If the news feature is not locked and the API key is configured:
                        - The system fetches news based on the user's location.
                        - It selects two random news items, cleans the text for the title and content, generates audio for the cleaned text, and outputs it.
                        - The system logs relevant actions and errors into the queue for tracking purposes.
                    """
                    
                    if news_lock == True:
                        
                        generateAudio(default_sentences["newsLock"][0]+str(location), default_Language)
                        
                        print("------------------")
                        print("News system lock")
                        print("------------------")
                        
                        queue.put("News system lock, user try to access")#log system flag for lock news
                        
                    else:
                        
                        print("------------------")
                        print("News system:")
                        print("------------------")
                        
                        queue.put("Entry to News system module") #log system flag for access to the news block
                        
                        if not API_NEWS_KEY:
                            
                            print("Error: API key is not configured. Make sure the .env file contains the correct key.")
                            queue.put("Error: API key is not configured. Make sure the .env file contains the correct key.")
                            
                        else:
                            
                            query = location[0]
                            generateAudio(default_sentences["news"][0]+str(location), default_Language) #generate voice from default sentences
                            page_size = 7
                            news_by_query = get_news_today(API_NEWS_KEY, query,language,page_size,queue)
                            
                            print("News for consultation in: "+str(location))
                            
                            # Select two unique random indexes
                            random_indices = random.sample(range(len(news_by_query)), 2)
                            queue.put("News data received correctly")#log system flag for correct data
                            
                            # Iterate over random indices and concatenate titles and contents
                            for i in random_indices:
                                concatenated_content = ""
                                news = news_by_query[i]
                                
                                print("News:", i + 1)
                                
                                # Clean and print the title
                                clean_title = text_cleaner(news['title'])
                                print("Title:", clean_title)
                                concatenated_content += clean_title + " "  # Add the clean title to the concatenated string
                                
                                # Clean and print the content
                                clean_content = text_cleaner(news['content'])
                                print("Content:", clean_content)
                                concatenated_content += clean_content + " "  # Add the clean content to the concatenated string
                                
                                # Generate audio from the concatenated content
                                generate_audio(concatenated_content, default_language)

                            print("-----------------------------------------")

                            # Generate audio from the default sentence
                            generate_audio(default_sentences["news"][1], default_language)
                            
            elif any(keyword in response for keyword in keyWords["onlineSearch"]):

                """
                Module for online search.

                This module handles online search queries. If the user's request includes any of the specified keywords for online search:

                1. The system logs the entry into the online search module and generates an audio message indicating the start of the search.
                2. It performs a Wikipedia summary search based on the user's query.
                - If a response is received, it generates an audio message with the search result and logs the successful data retrieval.
                - If no response is received, it logs an error message.
                """
                
                print("------------------")
                print("Online search:")
                print("------------------")
                    
                queue.put("Entry yo Online search module") #log system flag for access to the online search module
                generateAudio(default_sentences["onlineSearch"][0], default_Language) #generate voice from the default sentences

                respond =  search_wikipedia_summary(response,language,queue,3)
                
                if respond != "":
                    
                    generateAudio(respond, default_Language) #generate voice from the respond
                    queue.put("Correct search online data") #log system flag for correct data

                else: 
                    
                    queue.put("Error: search online data") #log system flag an error
                
            elif any(keyword in response for keyword in keyWords["putAlarm"]) and "alarma" in response:

                """
                Module for AlarmHandler.

                This module handles alarm-setting queries. If the user's request includes any of the specified keywords for setting an alarm and the word "alarma":

                1. The system logs the entry into the alarm module and generates an audio message indicating the start of the alarm setup.
                2. It captures the user's voice input for the alarm time, extracts the time from the input, and sets the alarm accordingly.
                3. Based on the default language, it generates an appropriate audio message confirming the alarm time.
                4. Finally, it starts the alarm thread and logs the successful alarm setup.
                """

                print("------------------")
                print("Alarm system:")
                print("------------------")
                    
                queue.put("Entry to alarm module") #log system flag access to the alarm block
                    
                generateAudio(default_sentences["putAlarm"][0], default_Language) #generate voice from the default sentences
                
                response = ""
                response = getVoice(default_Language).lower()
                alarm_time  = extract_time(response)
                    
                if default_Language == "en-US":
                    
                    generateAudio("alarm "+alarm_time, default_Language) #generate voice from the default sentences in Es
                    
                elif default_Language == "es-ES":
                    
                    generateAudio("alarma configurada "+alarm_time, default_Language) #generate voice from the default sentences in En
                    start_alarm_thread(alarm_time)
                    queue.put("Correct alarm set") #log system flag for alarm set
                
            elif any(keyword in response for keyword in keyWords["weatherUtilities"]):

                """
                Module for weather handler.

                This module handles weather-related queries. If the user's request includes any of the specified keywords for weather utilities:

                1. The system logs the entry into the weather module and attempts to identify the city from the user's query using a JSON file.
                2. If no city is found in the query, it defaults to the user's registered location. If no location is available, it generates an audio message indicating the error and logs it.
                3. If a city is identified and the API key is configured:
                - It fetches weather data for the specified city.
                - Logs the successful data retrieval.
                - Generates an audio message with the weather information.
                - Logs the error if the data retrieval fails.
                """

                print("------------------")
                print("Weather system:")
                print("------------------")
                    
                queue.put("Entry to Weather module") #log system flag for access to the weather module
                    
                city = search_weather_keyword(response,File[9])#read the city from the json file
                print(city)

                if city == "":
                        
                    city = location[0] #in case of no location in sentence , auto add location fron register
                        
                    if location == "":
                        
                        generateAudio(default_sentences["weatherNotLoc"][0], default_Language) #generate voice from the default sentences
                        queue.put("Error: local data not set in scope") #log system flag for error if is not loc
                            
                    else:
                        
                        start_date = "today" # start date
                        end_date = "today" # end date

                        if API_KEY :
                            
                            respond = get_weather(city,API_KEY,language,queue)
                            queue.put("Weather correct data ") #log system flag correct data get
                            
                            if respond:
                                generateAudio(respond, default_Language) #generate voice from the respond
                                
                            else:
                                
                                print("Could not get time information.")
                                queue.put("Could not get time information.") #log system flag for error of data
                
                elif any(keyword in response for keyword in keyWords["openUtilities"]):

                    """
                    Module for opening programs.

                    This module handles queries to open programs. If the user's request includes any of the specified keywords for opening utilities:

                    1. The system logs the entry into the open programs module and generates an audio message indicating the start of the program opening process.
                    2. It extracts the program name from the user's query, which is assumed to be the last word in the response.
                    3. It calls a function to open the specified program and logs the action.
                    """
                    
                    print("------------------")
                    print("Open program system:")
                    print("------------------")
                    
                    queue.put("Entry to open programs module") #log system flag for access to the open program module
                    
                    generateAudio(default_sentences["openUtilities"][0], default_Language) #generate voice from the default sentences
            
                    words = response.split()
                    program_name = words[-1]
                    open_program(program_name,queue)
                        
                elif any(keyword in response for keyword in keyWords["closeUtilities"]):

                    """
                    Module for closing programs.

                    This module handles queries to close programs. If the user's request includes any of the specified keywords for closing utilities:

                    1. The system logs the entry into the close programs module and generates an audio message indicating the start of the program closing process.
                    2. It extracts the program name from the user's query, which is assumed to be the last word in the response.
                    3. It calls a function to close the specified program and logs the action.
                    """

                    print("------------------")
                    print("Close program system:")
                    print("------------------")
                    
                    queue.put("Entry to Close programs module") #log system flag for access to the close program module
                    generateAudio(default_sentences["closeUtilities"][0], default_Language) #generate voice from the default sentences
                    
                    words = response.split()
                    program_name = words[-1]
                    
                    close_program(program_name,queue)
                        
                elif any(keyword in response for keyword in keyWords["greeting"]):

                    """
                    Module for greetings handler.

                    This module handles greeting-related queries. If the user's request includes any of the specified keywords for greetings:

                    1. The system logs the entry into the greetings module and generates an audio message indicating the start of the greetings process.
                    2. It selects a random greeting from the predefined list of greetings and generates an audio message with the selected greeting.
                    """
                    
                    print("------------------")
                    print("Greetings system:")
                    print("------------------")
                    
                    queue.put("Entry to Greetings module")  #log system flag for access to the greetings system module
                    random_greeting = random.choice(default_sentences["greeting"])
                    generateAudio(random_greeting, default_Language) #generate voice from the random greetings
                                
                else: 
                    
                    """
                    Module for LLM system.

                    This module handles general queries that do not match any specific keywords and are passed to the language model (LLM) for processing:

                    1. The system logs the entry into the LLM module and generates an audio message indicating the start of the LLM process.
                    2. It generates a response text using the LLM based on the user's query, with a specified maximum length.
                    3. Finally, it generates an audio message with the generated text and logs the action.
                    """

                    print("------------------")
                    print("LLM system:")
                    print("------------------")
                    
                    queue.put("Entry to LLM module") #log system flag for access to the LLM module
                    textGenerated = getLLMText(response, 100,default_Language,queue)
                    
                    generateAudio(textGenerated, default_Language) #generate voice from the respond
                
            else:

                """
                Module for non-understood voice issue.

                This module handles cases where the user's query does not match any known keywords or commands:

                - The system generates an audio message indicating that it did not understand the user's request using a predefined message.
                """
                
                generateAudio(default_sentences["notUnderstood"][0], default_Language)
                
    except (KeyboardInterrupt, EOFError):

        # If a KeyboardInterrupt or EOFError is raised during execution:
        print("---------------------------")
        print("Keyboard interrupt detected.")
        print("---------------------------")
        
        log_process.terminate()  # Ensure the logger process is terminated
        log_process.join()  # Wait for the logger process to join
        sys.exit(0)
        
    finally:
        
        # Regardless of whether an exception was raised or not, execute the following block of cod
        log_process.terminate()  # Ensure the logger process is terminated
        log_process.join()  # Wait for the logger process to join
        
        print("---------------------------")
        print("Logger finish.")
        print("---------------------------")