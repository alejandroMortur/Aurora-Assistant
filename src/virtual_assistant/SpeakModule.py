from playsound import playsound
import os

def speak():
    
    """
    Function to play the generated voice audio file and remove it afterward.

    Raises:
    - Exception: If there is an error during audio playback or file removal.
    """
    
    try:
        # Play the generated voice audio file
        playsound(r"../resources/Sounds/generatedVoices/voice.mp3")
        
        # Remove the generated voice audio file after playing
        os.remove("../resources/Sounds/generatedVoices/voice.mp3")
    
    except Exception as e:
        print("An error occurred:", e)
