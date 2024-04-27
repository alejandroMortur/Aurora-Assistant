import os
import sys

# Set the Python search path to include the dependencies folder
dependencies_path = os.path.abspath('./src/resources/dependences')
sys.path.insert(0, dependencies_path)

# Then import your necessary modules and run your main code
import speech_recognition as sr
import pyttsx3, pywhatkit
from src.virtual_assistant import Main

Main.main(sr, pyttsx3, pywhatkit)