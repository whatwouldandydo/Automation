"""
Date: 2020-12-05
This Python script will do the following:
(1) Use Generator to store large data of random numbers
(2) Compare each random number from the Generator with the Correct number
(3) If the comparison is a match, log the number, date/time, and how long was the guess
(4) Then autosave the log file to Github
(5) Autoload the Python script when the system started with crontab
"""

### Import modules
import pexpect
import logging
import time
import datetime
import concurrent.futures
import subprocess
import random

timer1 = time.perf_counter()

### Create custom logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s---> %(message)s")
file_handler = logging.FileHandler("Bot_Guessing_Game.log")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

### Create random integer with generator
i1 = random.random()
# print(i1)

def generate_random_number():
    number_list = []

    for line in range(10):
        line = random.random()
        number_list.append(line)
    
    #print(number_list)
    yield number_list

for item in generate_random_number():
    print(item)

### Compare random integer with corrected number


### Run comparision as multithread


### 


######################## End Code ########################