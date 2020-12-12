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
i1 = random.random()
# print(i1)


def generate_random_number():

    guess_range = time.time()
    guess_range = str(guess_range).split(".")
    guess_range = int(guess_range[0]) - int(guess_range[1])
    print(f"Guess range {guess_range}")

    generated_numbers = []

    count = 0

    for number in range(10): # Replace (2) with guess_range
        number = random.randint(1,10)
        # number = random.random()
        # number = str(number).split(".")[1]

        generated_numbers.append(number)
        # print(type(number))
        # count += 1
        # print(count)
        # yield number

    print(f"generated_numbers {generated_numbers}")
    yield generated_numbers


### Compare random integer with corrected number
correct_number = random.randint(1,2)
# correct_number = random.random()
# correct_number = int(str(correct_number).split(".")[1])
# correct_number = int(correct_number)
print(f"correct_number {correct_number}")

# count = 0
for guessed_number in generate_random_number():
    print(guessed_number)
    # count +=1 
    # print(count)
    # print(guessed_number)
    # if guessed_number == correct_number:
    #     print(guessed_number)
    # else:
    #     print("OUCH", guessed_number)


### Run comparision as multithread


### 


######################## End Code ########################