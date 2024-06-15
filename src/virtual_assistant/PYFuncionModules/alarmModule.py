import datetime # To work with dates and times
import time # To make the program wait
import simpleaudio as sa
import threading # To work with threads
import re # To work with regular expressions
import os

#local variable audio file
sound_file = "../resources/Sounds/alarm.wav"

def start_alarm_thread(alarm_time):
    
    """
    Starts a new thread to set and trigger the alarm at a specified time.
    
    Args:
    - alarm_time (str): The time in HH:MM format when the alarm should trigger.
    """

    alarm_thread = threading.Thread(target=set_alarm, args=(alarm_time,))
    alarm_thread.start()

def set_alarm(alarm_time):
    
    """
    Sets an alarm to trigger at a specified time and plays a sound when the time is reached.
    
    Args:
    - alarm_time (str): The time in HH:MM format when the alarm should trigger.
    """
    
    # Make sure the time is in HH:MM format
    alarm_time = datetime.datetime.strptime(alarm_time, '%H:%M').time()
    
    while True:
        
        current_time = datetime.datetime.now().time()
        
        if current_time >= alarm_time:
            
            print("---------------------------")
            print("¡Time to weak up!")
            print("---------------------------")
            
            wave_obj = sa.WaveObject.from_wave_file(sound_file)
            play_obj = wave_obj.play()
            play_obj.wait_done() 
            
            break
        
        time.sleep(1)  # Wait a second before checking the time again

def extract_time(response):
    
    """
    Extracts a time in HH:MM format from a given text response using regular expressions.
    
    Args:
    - response (str): The text response from which to extract the time.
    
    Returns:
    - str: The extracted time in HH:MM format if found, otherwise None.
    """
    
    # Defines a pattern to find times in HH:MM format
    pattern = r'\b([01]?[0-9]|2[0-3]):[0-5][0-9]\b'
    match = re.search(pattern, response)
    
    if match:
        return match.group()
    
    else:
        return None