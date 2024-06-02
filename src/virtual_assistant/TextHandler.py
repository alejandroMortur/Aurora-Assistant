import json
import re
from unidecode import unidecode

#code block for read initial dialog
def read_file(file_path):
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

#code block for read vocie keywords
def read_word(file_path):
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

#code block for read dialog setences
def read_lines(file_path):
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

#code block for read cities
def search_WeatherKeyword(input_text, keyword_data):
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
    # Load cities data from JSON file
    with open(cities_data, 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    # Search for city name in user input
    for city_info in data:
        if city_info.get("name", "").lower() == city_name.lower():
            return city_info.get("country_name")
    
    # If city not found
    return None

#Get localitation module
def find_city_and_state_in_phrase(phrase, cities_data):
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

