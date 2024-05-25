import datetime # To work with dates and times
import time # To make the program wait
import simpleaudio as sa
import threading # To work with threads
import re # To work with regular expressions
import os

#local variable audio file
sound_file = "../resources/Sounds/alarm.wav"

def start_alarm_thread(alarm_time):
    alarm_thread = threading.Thread(target=set_alarm, args=(alarm_time,))
    alarm_thread.start()

def set_alarm(alarm_time):
    # Make sure the time is in HH:MM format
    alarm_time = datetime.datetime.strptime(alarm_time, '%H:%M').time()
    
    while True:
        current_time = datetime.datetime.now().time()
        if current_time >= alarm_time:
            print("---------------------------")
            print("¡Es hora de despertar!")
            print("---------------------------")
            wave_obj = sa.WaveObject.from_wave_file(sound_file)
            play_obj = wave_obj.play()
            play_obj.wait_done() 
            break
        time.sleep(1)  # Wait a second before checking the time again

def extract_time(response):
    # Defines a pattern to find times in HH:MM format
    pattern = r'\b([01]?[0-9]|2[0-3]):[0-5][0-9]\b'
    match = re.search(pattern, response)
    if match:
        return match.group()
    else:
        return None