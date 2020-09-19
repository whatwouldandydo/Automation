"""
Date: 2020-08-12
Summary: The function of this program is to (1) create customer logging and save logs to a file,
(2) Open network devices from a file,
(3) Connect to each network device via SSH,
(4) Apply network commands from a file,
(5) Run all network devices at the same time.
"""

## Import modules
import pexpect
import concurrent.futures
import time
import datetime
import getpass
import logging


## Create custome logging and save log to file
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter("%(asctime)s--%(name)s--%(levelname)s---> %(message)s")
formatter2 = logging.Formatter("%(asctime)s--%(levelname)s---> %(message)s")

log_handler = logging.FileHandler("/home/do/Desktop/Projects/Logs/5_pexpect_multhread_log_cli-file.log")
log_handler.setFormatter(formatter)

console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter2)

logger.addHandler(log_handler)
logger.addHandler(console_handler)


## Open network devices from file
devices_file = "/home/do/Desktop/Projects/DevOps/devices.txt"

with open(devices_file, "r") as f:
    devices_txt = f.read().splitlines() #print ['10.10.10.201', '10.10.10.202', '10.10.10.203', '10.10.10.204']
    # devices_txt = f.read()
    """print
    10.10.10.201
    10.10.10.202
    10.10.10.203
    10.10.10.204
    """
    # devices_txt = f.read().split() #print ['10.10.10.201', '10.10.10.202', '10.10.10.203', '10.10.10.204']
    # devices_txt = f.readline() #print 10.10.10.201
    # devices_txt = f.readlines() #print ['10.10.10.201\n', '10.10.10.202\n', '10.10.10.203\n', '10.10.10.204\n']

## Open network commands from a file
commands_file = "/home/do/Desktop/Projects/DevOps/commands.txt"
with open(commands_file, "r") as f:
    commands_txt = f.read().splitlines()


## Login credential and device expected prompt
# username = input("Username: ")
# password = getpass.getpass()
username = "admin"
password = "devops"

read_prompt = ">"
enable_prompt = "#"
invalid_cli_prompt = "%.*"


## Connect to network devices and apply configurations
def network_devices(hostname):
    try:
        ssh_net_connect = pexpect.spawn(f"ssh {username}@{hostname}", timeout=5, maxread=1)
        device_prompt = ssh_net_connect.expect(["\(yes/no/\[fingerprint\]\)\?", "Pass.*", "pass.*", pexpect.EOF])
        logger.debug(f"===== {hostname} SSH Initiate ======")

        if device_prompt == 0:
            ssh_net_connect.sendline("yes")
            device_prompt = ssh_net_connect.expect([read_prompt, "Pass.*", "pass.*"])
            logger.debug(f"{hostname} Accepted SSH Key")
            ssh_net_connect.sendline(password)
            device_prompt = ssh_net_connect.expect([read_prompt, "Pass.*", "pass.*"])
            logger.debug(f"{hostname} SSH Established")
        else: 
            ssh_net_connect.sendline(password)
            device_prompt = ssh_net_connect.expect([read_prompt, enable_prompt])
            logger.debug(f"{hostname} SSH Established")

        ssh_net_connect.sendline("enable")
        device_prompt = ssh_net_connect.expect([read_prompt, enable_prompt])
        print(ssh_net_connect.before)
        ssh_net_connect.sendline("term len 0")
        device_prompt = ssh_net_connect.expect([read_prompt, enable_prompt])
        print(ssh_net_connect.before)

        ## Configure network commands from a file
        logger.debug(f"{hostname} Applying Configurations")

        for cmd in commands_txt:
            ssh_net_connect.sendline(cmd)
            device_prompt = ssh_net_connect.expect([invalid_cli_prompt, enable_prompt])

            if device_prompt == 0:
                logger.debug(f"{hostname} Invalid Commands!!!")
                logger.debug(ssh_net_connect.before.decode("utf-8").splitlines())

        logger.debug(f"{hostname} Completed Configurations")

        ## Save configuration to network devices
        ssh_net_connect.sendline("end")
        device_prompt = ssh_net_connect.expect(enable_prompt)
        ssh_net_connect.sendline("write mem")
        device_prompt = ssh_net_connect.expect(enable_prompt)

        ## Display network device's current running-config
        ssh_net_connect.sendline("show runn")
        device_prompt = ssh_net_connect.expect(enable_prompt)
        # logger.debug(ssh_net_connect.before)
        print(ssh_net_connect.before)

        logger.debug(f"===== Closed SSH Connect to {hostname} =====")
        ssh_net_connect.close()

    except:
        logger.exception(f"{hostname} ERROR")
        ssh_net_connect.close()


## This function allows multi thread by running multiple devices at the same time
with concurrent.futures.ThreadPoolExecutor() as executor:
    threads = executor.map(network_devices, devices_txt)

logger.debug("############################ END CODE ############################")

## End Code