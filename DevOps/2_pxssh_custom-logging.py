"""
Date: 2020-07-20
(1) Create custom loggin to avoid shared "root" account
(2) SSH to Arista device with pxssh module
(3) SSH to new Arista device with new SSH key
"""

## Required modules
import logging
from pexpect import pxssh
import time
import getpass

## Create custom logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter("%(asctime)s--%(levelname)s:%(lineno)d--->%(message)s")

log_file = "2_pxssh_custom-logging.log"

file_handle = logging.FileHandler(log_file)
file_handle.setFormatter(formatter)

logger.addHandler(file_handle)


## Define hostname and credential
hostname = "192.168.0.1"
username = "admin"
password = "devops"


## SSH to device
try:
    ssh = pxssh.pxssh()

    logger.debug("Begin SSH to Arista")
    ssh.login("192.168.0.1", "admin", "devops") #pxssh to Arista does not work
    logger.debug("SSH to Arista Successfully")

    logger.debug("CLI show uptime")
    ssh.sendline("show uptime")
    ssh.prompt()
    logger.debug(ssh.before)
    print(ssh.before)
    print(ssh.after)

    logger.debug("CLI show clock")
    ssh.sendline("show clock")
    ssh.prompt()
    print(ssh.before)
    print(ssh.after)

    ssh.close()

except:
    logger.exception("##### SSH FAILED ######")
    print("##### SSH FAILED ######")

    ssh.close()