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

timer1 = time.perf_counter_ns()


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

    guess_range = random.random()
    guess_range = str(guess_range).split(".")[1]
    guess_range = int(guess_range)
    print(guess_range)

    max_number = random.random()
    max_number = str(max_number).split(".")[1]
    max_number = int(max_number) + guess_range
    print(max_number)

    generated_numbers = []

    for number in range(2):
        number = random.randint(1, 2)
        # number = str(number).split(".")[1]

        generated_numbers.append(number)
        print(type(number))
    
    #print(number_list)
    yield generated_numbers

for item in generate_random_number():
    print(item)

### Compare random integer with corrected number


### Run comparision as multithread


### 


######################## End Code ########################