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

### Create Timer to track executing time
timer1 = time.time()

### Create custom logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s---> %(message)s")
file_handler = logging.FileHandler("7_Bot_Guessing_Game.log")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

### Create a log session whenever the program run = new game
logger.debug(f"########## New Game Starts on {time.ctime()} Pacific Time ##########")

### Create random integer with generator
def generate_numbers(gnumber):
    for number in range(gnumber):
        number = random.random()
        number = str(number).split(".")[1]
        number = str(number).split("e")[0]
        number = int(number)
        yield number

num_of_guesses = int(str(time.time()).split(".")[1])

random_numbers = generate_numbers(num_of_guesses) #Use num_of_guesses for argument

### Compare random integer with corrected number
def compare_numbers(guess):
    correct_number = random.random()
    correct_number = str(correct_number).split(".")[1]
    correct_number = str(correct_number).split("e")[0]
    correct_number = int(correct_number)

    cd_cmd = "cd /home/do/Projects/Automation/DevOps/"
    git_checkout_cmd = "git checkout master"
    git_add_cmd = "git add 7_Bot_Guessing_Game.log"
    git_commit_cmd = f"git commit -m 'Commit {guess} on {time.ctime()}'"
    git_push_cmd = "git push origin master"


    if guess == correct_number:
        print(f"The correct number {guess} takes {time.time() - timer1} seconds to find.")
        logger.debug(f"The correct number {guess} takes {time.time() - timer1} seconds to find.")
        subprocess.run(cd_cmd, shell=True)
        subprocess.run(git_checkout_cmd, shell=True)
        subprocess.run(git_add_cmd, shell=True)
        subprocess.run(git_commit_cmd, shell=True)
        subprocess.run(git_push_cmd, shell=True)

### Run comparision as multithread
# with concurrent.futures.ThreadPoolExecutor() as executor:
#     threads = executor.map(compare_numbers, random_numbers)

### Run in infinite loop with multithread
while True:
    with concurrent.futures.ThreadPoolExecutor() as executor:
        threads = executor.map(compare_numbers, random_numbers)

######################## End Code ########################