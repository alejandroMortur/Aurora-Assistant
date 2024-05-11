import os 
import sys
from GenerateModule import generateAudio
from MicHandler import getVoice
from LLMModule import getLLMText
from TextHandler import read_file, read_word

# Default language setting
defaultLanguage = "es-ES"

# File paths for different resources
File = [
    "./textResources/IntroText01.txt",        # Introduction text
    "./textResources/ES/EsKeyWordsText02.txt",# Spanish keywords
    "./textResources/ES/EsDefaultSentences01.txt", # Default Spanish sentences
    "./textResources/EN/EnKeyWordsText02.txt",# English keywords
    "./textResources/EN/EnDefaultSentences01.txt"  # Default English sentences
]

# Read intro text from file
content = read_file(File[0])
print(content)
generateAudio(content, defaultLanguage)

# Get user's preferred language through voice input
language = getVoice(defaultLanguage)

# Set language based on user input
if language == "castellano":
    generateAudio("Entendido, te hablaré en castellano a partir de ahora", defaultLanguage)
    defaultLanguage = "es-ES"
    keyWords = read_word(File[1])  # Load Spanish keywords
    defaultSentences = read_word(File[2])  # Load default Spanish sentences
    print(keyWords, defaultSentences)
else:
    generateAudio("Got it, from now on I will speak to you in English", defaultLanguage)
    defaultLanguage = "en-US"
    keyWords = read_word(File[3])  # Load English keywords
    defaultSentences = read_word(File[4])  # Load default English sentences
    print(keyWords, defaultSentences)

# Main loop for voice interaction
while True:
    # Get user's response through voice input
    response = getVoice(defaultLanguage)
    response = response.lower()  # Convert response to lowercase for easier comparison
    
    # Check if the wake word "aurora" is in the response
    if "aurora" in response:
        # Remove the wake word "aurora" from the response
        response = response.replace("aurora", "")
        
        # Check for various commands based on keywords
        if keyWords[0] in response and keyWords[1] in response or keyWords[2] in response:
            generateAudio("Sure, tell me what you want me to search for you", defaultLanguage)
        elif keyWords[3] in response:
            generateAudio("Sure, which program do you want to open?", defaultLanguage)
        # Additional commands can be added similarly
        
    else:
        generateAudio("Sorry, I didn't understand you", defaultLanguage)

