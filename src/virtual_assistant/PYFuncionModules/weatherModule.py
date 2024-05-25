import requests
from dotenv import load_dotenv
import os

def get_weather(city,api_key,defaultLanguage):
    # URL for the current weather
    url = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{city}?unitGroup=metric&key={api_key}&contentType=json"

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
            
            if defaultLanguage == "en-US":
                
                # Generate the phrase with the current weather data
                phrase = f"At this moment in {current_weather['city']}, it is {current_weather['temperature']} degrees Celsius, with a humidity of {current_weather['humidity']}% and a wind speed of {current_weather['wind']} km/h."
                print("---------------------------")
                print(phrase)
                print("---------------------------")
                
            elif defaultLanguage == "es-ES": 
                # Generate the phrase with the current weather data
                phrase = f"En este momento en {current_weather['city']}, hay {current_weather['temperature']} grados Celsius, con una humedad del {current_weather['humidity']}% y una velocidad del viento de {current_weather['wind']} km/h."
                print("---------------------------")
                print(phrase)
                print("---------------------------")
            
            return phrase
        else:
            print("No current weather information found.")
            return None
    else:
        print(f"Error: {response.status_code}")
        try:
            # Attempt to print the response content
            error_data = response.json()
            print("Error content:")
            print(error_data)
        except:
            # If it cannot be loaded as JSON, print the content as text
            print("Error content:")
            print(response.text)
        return None
