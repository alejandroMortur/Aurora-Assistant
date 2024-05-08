import os 
import sys
from GenerateModule import generateAudio
from MicHandler import getVoice
from LLMModule import getLLMText

text = "hola buenos dias soy aurora"

text = getLLMText()

generateAudio(text)
#getVoice()


