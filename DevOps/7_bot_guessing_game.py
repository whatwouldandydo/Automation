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

timer1 = time.time()
t2 = time.time()
# print(timer1, t2)


### Create custom logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s---> %(message)s")
file_handler = logging.FileHandler("Bot_Guessing_Game.log")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

### Create random integer with generator
def generate_numbers(gnumber):
    for number in range(gnumber):
        number = random.random()
        number = str(number).split(".")[1]
        number = str(number).split("e")[0]
        # number = int(str(number).split(".")[1])
        # number = random.randint(1,10)
        number = int(number)
        yield number

num_of_guesses = int(time.time_ns())
# print(num_of_guesses)
        
random_numbers = generate_numbers(10) #Use num_of_guesses for argument
# print(next(random_numbers))


### Compare random integer with corrected number
def compare_numbers(cnumber):
    correct_number = random.random()
    correct_number = str(correct_number).split(".")[1]
    correct_number = str(correct_number).split("e")[0]
    correct_number = int(correct_number)
    # correct_number = random.randint(1,10)
    print(f"correct_number {correct_number}")

    for guess in cnumber:
        # print(guess)
        if guess == correct_number:
            logger.debug(f"It takes {time.time() - timer1} to guess the correct number {guess}")
            # print(f"guess, correct_number {guess} {correct_number}")
        else:
            print(f"WRONG {guess} It takes {time.time() - timer1}")

compare = compare_numbers(random_numbers)


### Run comparision as multithread


### 


######################## End Code ########################