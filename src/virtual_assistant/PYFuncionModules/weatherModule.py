import requests
import os

def get_weather(city,API_KEY,default_language,queue):
    
    """
    Retrieves current weather information for a specified city using an API call.
    
    Args:
    - city (str): Name of the city to fetch weather data for.
    - API_KEY (str): API key for accessing the weather API.
    - default_language (str): Default language for generating weather phrases ('en-US' or 'es-ES').
    - queue (multiprocessing.Queue): Queue for logging messages from the function.
    
    Returns:
    - str or None: Phrase describing current weather in the specified language, or None if data retrieval fails.
    """
    
    # URL for the current weather
    url = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{city}?unitGroup=metric&key={API_KEY}&contentType=json"

    # Make the GET request
    response = requests.get(url)
    
    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()
        
        # Print the complete JSON response for analysis
        print("Complete JSON response:")
        
        # Extract and format the relevant information
        current_conditions = data.get('currentConditions', {})
        
        if current_conditions:
            current_weather = {
                "city": city,
                "temperature": current_conditions.get("temp"),
                "humidity": current_conditions.get("humidity"),
                "wind": current_conditions.get("windspeed")
            }
            
            if default_language == "en-US":
                
                # Generate the phrase with the current weather data
                phrase = f"At this moment in {current_weather['city']}, it is {current_weather['temperature']} degrees Celsius, with a humidity of {current_weather['humidity']}% and a wind speed of {current_weather['wind']} km/h."
                print("---------------------------")
                print(phrase)
                print("---------------------------")
                
            elif default_language == "es-ES": 
                # Generate the phrase with the current weather data
                phrase = f"En este momento en {current_weather['city']}, hay {current_weather['temperature']} grados Celsius, con una humedad del {current_weather['humidity']}% y una velocidad del viento de {current_weather['wind']} km/h."
                print("---------------------------")
                print(phrase)
                print("---------------------------")
            
            queue.put("Weather information found correctly")
            return phrase
        
        else:
            
            print("No current weather information found.")
            queue.put("No current weather information found.")
            
            return None
        
    else:
        
        print(f"Error: {response.status_code}")
        
        try:
            
            # Attempt to print the response content
            error_data = response.json()
            print("---------------------------")
            print("Error content:")
            print(error_data)
            queue.put(error_data)
            print("---------------------------")
            
        except:
            
            # If it cannot be loaded as JSON, print the content as text
            print("---------------------------")
            print("Error content:")
            print(response.text)
            queue.put("Error content:"+str(response.text))
            print("---------------------------")
            
        return None
