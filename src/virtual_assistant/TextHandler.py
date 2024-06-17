import json
import re
import os
from unidecode import unidecode
import pickle

def read_file(file_path):
    
    """
    Reads the entire content of a file and returns it as a single string.

    Parameters:
    - file_path (str): The path to the file to read.

    Returns:
    - file_content (str): The concatenated string of all lines in the file.
    """
    
    # Initialize a list to store the lines of the file
    lines = []
    
    # Open the file in read mode
    with open(file_path, 'r') as file:
        # Read each line of the file and add it to the list
        for line in file:
            lines.append(line.strip())  # Remove leading and trailing whitespace from the line
            
    # Concatenate all lines into a single string separated by newline characters
    file_content = '\n'.join(lines)
    
    return file_content

def read_word(file_path):
    
    """
    Reads keywords from a JSON file and organizes them into a dictionary.

    Parameters:
    - file_path (str): The path to the JSON file containing keywords.

    Returns:
    - words (dict): A dictionary where keys are category names and values are lists of keywords.
    """
    
    words = {}

    # Open the JSON file
    with open(file_path, "r") as f:
        # Load JSON data
        data = json.load(f)
        
        # Check if 'keywords' key exists in JSON data
        if 'keywords' in data:
            # Get the dictionary of keywords from the JSON data
            keywords = data['keywords']
            
            # Iterate over each keyword category
            for category, category_keywords in keywords.items():
                # Add the category and its keywords to the words dictionary
                words[category] = category_keywords
            
    return words

import json

def read_lines(file_path):
    
    """
    Reads dialog lines from a JSON file and organizes them into a dictionary.

    Parameters:
    - file_path (str): The path to the JSON file containing dialog lines.

    Returns:
    - responses (dict): A dictionary where keys are category names and values are lists of dialog responses.
    """
    
    responses = {}

    # Open the JSON file
    with open(file_path, "r") as f:
        # Load JSON data
        data = json.load(f)
        
        # Check if 'responses' key exists in JSON data
        if 'responses' in data:
            # Get the dictionary of responses from the JSON data
            response_dict = data['responses']
            
            # Iterate over each category in the response dictionary
            for category, category_responses in response_dict.items():
                # Add the category and its responses to the responses dictionary
                responses[category] = category_responses
            
    return responses

def search_weather_keyword(input_text, keyword_data):
    
    """
    Searches for a weather keyword (city name) in user input using a JSON file.

    Parameters:
    - input_text (str): The user input text to search for keywords.
    - keyword_data (str): The path to the JSON file containing keyword data.

    Returns:
    - city_name (str or None): The matched city name if found, otherwise None.
    """
    
    # Load keyword data from JSON file
    with open(keyword_data, 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    # Split user input into words
    input_words = set(input_text.lower().split())
    
    # Search for keyword (city name) in user input
    for entry in data:
        city_name = entry.get("name", "").lower()
        
        if city_name in input_words:
            return entry["name"]
    
    # If no keyword found
    return None

def get_country_from_city(city_name, cities_data):
    
    """
    Retrieves the country name associated with a given city name from a JSON file.

    Parameters:
    - city_name (str): The name of the city to search for.
    - cities_data (str): The path to the JSON file containing city data.

    Returns:
    - country_name (str or None): The country name of the city if found, otherwise None.
    """
    
    # Load cities data from JSON file
    with open(cities_data, 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    # Search for city name in user input
    for city_info in data:
        if city_info.get("name", "").lower() == city_name.lower():
            return city_info.get("country_name")
    
    # If city not found
    return None


def find_city_and_state_in_phrase(phrase, cities_data):
    
    """
    Finds city and state names in a given phrase using a JSON file containing city data.

    Parameters:
    - phrase (str): The phrase to search for city and state names.
    - cities_data (str): The path to the JSON file containing city data.

    Returns:
    - city_info (list): A list containing city name, state name, and country name if found; empty list if not found.
    """
    
    # Load cities data from JSON file
    with open(cities_data, 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    # Normalize the phrase to avoid case sensitivity and accent sensitivity issues
    normalized_phrase = unidecode(phrase.lower())
    
    # Search for each city and state in the phrase
    for city_info in data:
        city_name = unidecode(city_info.get("name", "").lower())
        state_name = unidecode(city_info.get("state_name", "").lower())
        
        # Check if both city name and state name are in the phrase
        if re.search(r'\b' + re.escape(city_name) + r'\b', normalized_phrase) and \
           re.search(r'\b' + re.escape(state_name) + r'\b', normalized_phrase):
            return [city_info["name"], city_info["state_name"], city_info.get("country_name")]
    
    # If no city and state are found
    return []

def text_cleaner(text, max_length=200):
    
    """
    Cleans text by removing HTML tags, special characters, and limiting its length.

    Parameters:
    - text (str): The text to clean.
    - max_length (int): The maximum allowed length of the cleaned text. Default is 200 characters.

    Returns:
    - clean_text (str): The cleaned text.
    """
    
    # Remove HTML/XML tags
    clean_text = re.sub(r'<.*?>', '', text)
    
    # Remove character count indicators
    clean_text = re.sub(r'\[\+\d+ chars\]', '', clean_text)
    
    # Remove special characters except space, letters, and commas
    clean_text = re.sub(r'[^\w\s,]', '', clean_text)
    
    if len(clean_text) <= max_length:
        return clean_text.strip()
    
    # Cut the text at the last period found or at an incomplete word
    last_period_index = clean_text.rfind('.')
    
    if last_period_index != -1:  # If a period is found in the text
        clean_text = clean_text[:last_period_index + 1]  # Keep only up to the last period and the following space
        
    else:
        
        # If no periods are found in the text, find the closest space before the maximum allowed length
        closest_space_index = max_length
        
        for i in range(max_length // 2, max_length):
            if clean_text[i] == ' ':
                closest_space_index = i
                break
            
        # Cut the text up to the closest space
        clean_text = clean_text[:closest_space_index]
        
        # Remove the last word if it's incomplete
        last_space_index = clean_text.rfind(' ')
        
        if last_space_index != -1:
            clean_text = clean_text[:last_space_index]
        
    return clean_text.strip()  # Remove leading and trailing spaces

def save_user_data(location, default_Language, language, news_lock, filename):
    """
    Saves the given data to a binary file using pickle.

    Parameters:
    - location (tuple): The location data to be saved. Can be None.
    - default_Language (str): The default language setting.
    - language (str): The language setting.
    - news_lock (bool): The news lock status.
    - filename (str): The name of the file to save the data. Default is 'data.bin'.

    Returns:
    - None
    """
    
    # Ensure the directory exists
    os.makedirs(os.path.dirname(filename), exist_ok=True)   
    
    data = {
        'location': location,
        'default_Language': default_Language,
        'language': language,
        'news_lock': news_lock
    }
    with open(filename, 'wb') as file:
        pickle.dump(data, file)

def load_user_data(filename='data.bin'):
    """
    Loads data from a binary file using pickle.

    Parameters:
    - filename (str): The name of the file to load the data from. Default is 'data.bin'.

    Returns:
    - tuple: A tuple containing the location, default_Language, language, and news_lock.
    """
    with open(filename, 'rb') as file:
        data = pickle.load(file)
        return data['location'], data['default_Language'], data['language'], data['news_lock']

