# Imports of test modules 
from testBlockScripts.test_alarm import *
from testBlockScripts.test_news import *
from testBlockScripts.test_programs_open import *
from testBlockScripts.test_weather import *
from testBlockScripts.test_wiki import *
from testBlockScripts.test_LLM import *
import pytest
import subprocess
import os

def run_pytest():
    result = subprocess.run(["pytest", "-v", "-rA"], capture_output=True, text=True)
    print(result.stdout)
    if result.stderr:
        print(result.stderr)

if __name__ == "__main__":
    run_pytest()
