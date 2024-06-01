# Importamos los módulos de prueba manualmente
from testBlockScripts.test_alarm import *
from testBlockScripts.test_news import *
from testBlockScripts.test_programs_open import *
from testBlockScripts.test_weather import *
from testBlockScripts.test_wiki import *
from testBlockScripts.test_LLM import *
import subprocess

def run_pytest():
    # Run all tests and print verbose output with extra information
    subprocess.run(["pytest", "-v", "-rA"])

if __name__ == "__main__":
    run_pytest()
