"""
Date: 2020-08-26
The program will perform latest Pihole blacklist to Pihole server
(1) Create custom logging
(2) Download the latest Pihole blocklist and save it to local file
(3) Run nslookup commands on local Ubuntu machine using subprocess module
(4) Run multithread with subprocess module
(5) Run nslookup commands on remote machine via SSH pexpect
(6) Run multithread with pexpect
(7) Create generator to reduce RAM
"""

## Import modules
import pexpect
import logging
import time
import datetime
import subprocess
import requests
import concurrent.futures

## Create custom logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s--%(name)s--%(levelname)s---> %(message)s")
formatter2 = logging.Formatter("%(asctime)s--%(levelname)s---> %(message)s")
file_handler = logging.FileHandler("/home/do/Projects/Automation/Logs/6_pexpect_multithread_generator.log")
file_handler.setFormatter(formatter)
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter2)
logger.addHandler(file_handler)
logger.addHandler(console_handler)

## Download Pihole blacklist and save to local file
blocklist_url = "https://raw.githubusercontent.com/mhhakim/pihole-blocklist/master/list.txt"
pornlist_url = "https://raw.githubusercontent.com/mhhakim/pihole-blocklist/master/porn.txt"
youtube_ad_url = "https://www.sunshine.it/blacklist.txt"

blocklist_request = requests.get(blocklist_url)
pornlist_request = requests.get(pornlist_url)
youtube_ad_request = requests.get(youtube_ad_url)

logger.debug("Downloaded Pihole Blocklist")

save_file = "/home/do/Projects/Automation/DevOps/blocklist.txt"

with open(save_file, "w") as f:
    for line in youtube_ad_request.text.split("\r"):
        if "#" not in line:
            f.write(line)

logger.debug("Saved Pihole Blocklist To Local File")

## Perform nslookup
with open(save_file, "r") as f:
    blocklist_txt = f.read().splitlines()

def local_nslookup(domain):
    nslookup_cmd = subprocess.run(["nslookup", domain], capture_output=True)
    nslookup_cmd = nslookup_cmd.stdout.decode()

logger.debug("Start Nslookup")

with concurrent.futures.ThreadPoolExecutor() as executor:
    threads = executor.map(local_nslookup, blocklist_txt)

logger.debug("Completed Nslookup")

logger.debug("############################ END CODE ############################")