"""
Date: 2020-08-03
(1) Create custom logging and save to file
(2) Open devices from a file
(3) Create a function for connect network device with error handling and configure SVIs
(4) Create multi threading with Concurrent module
"""

## Import modules
import pexpect
import logging
import concurrent.futures
import getpass
import time
import datetime

## Create custom logging and save logging to file
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s--%(name)s--%(levelname)s---> %(message)s")
file_handler = logging.FileHandler("/home/do/Desktop/Projects/Logs/4_pexpect_multithread_logger.log")
file_handler.setFormatter(formatter)
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
logger.addHandler(file_handler)
logger.addHandler(console_handler)

## Network access credential
username = input("Username: ")
password = getpass.getpass()

## Open network devices from a file
device_file = "/home/do/Desktop/Projects/DevOps/devices.txt"

with open(device_file) as f:
    devices_txt = f.read().splitlines()

## Connect to network devices and configure SVI
read_mode = ">"
exec_mode = "#"
invalid_cmd = "% .*" #Regex .+ matches anything after % (% Invalid, % Incomplete)
log_invalid_cmds = "{hostname} Invalid Command {ssh.before} {ssh.after}"

def connect_network_devices(hostname):
    try:
        ssh = pexpect.spawn(f"ssh {username}@{hostname}")
        output = ssh.expect(["\(yes/no/\[fingerprint\]\)\?", "Pass.*", "pass.*", pexpect.EOF])
        logger.debug(f"Connect to {hostname} via SSH")
            
        if output == 0:
            cli = ssh.sendline("yes")
            output = ssh.expect([read_mode, "Pass.*", "pass.*"])
            logger.debug(f"Save {hostname} key to known_hosts file")

        ssh.sendline(password)
        output = ssh.expect(read_mode)
        logger.debug(f"{hostname} Password Accepted")

        ssh.sendline("term len 0")
        output = ssh.expect(read_mode)
        logger.debug(f"{hostname} Disable Terminal Lenght")

        ssh.sendline("enable")
        output = ssh.expect(exec_mode)
        logger.debug(f"{hostname} Enable Execution Mode")

        ssh.sendline("config t")
        output = ssh.expect(exec_mode)
        logger.debug(f"{hostname} Enable Configuration Mode")

        ## Configure SVI interfaces and IP address
        for svi in range(101):
            ssh.sendline(f"interface vlan {svi}")
            output = ssh.expect([exec_mode, invalid_cmd])
            if output == 1:
                logger.exception(f"{hostname} Invalid Command {ssh.before} {ssh.after}")
                # logger.exception(f"{log_invalid_cmds}")

            ssh.sendline(f"description SVI_{svi}")
            output = ssh.expect([exec_mode, invalid_cmd])
            if output == 1:
                logger.exception(f"{hostname} Invalid Command {ssh.before} {ssh.after}")
                # logger.exception(f"{log_invalid_cmds}")

            ssh.sendline(f"ip address 10.10.{svi}.1 255.255.255.0")
            output = ssh.expect([exec_mode, invalid_cmd])
            if output == 1:
                logger.exception(f"{hostname} Invalid Command {ssh.before} {ssh.after}")
                # logger.exception(f"{log_invalid_cmds}")

            logger.debug(f"{hostname} Configure SVI Interface {svi}")

        ## Delete SVI interfaces
        for rm_svi in range(101):
            ssh.sendline(f"no interface vlan {rm_svi}")
            output = ssh.expect([exec_mode, invalid_cmd])

            if output == 1:
                logger.exception(f"{hostname} Invalid Command {ssh.before} {ssh.after}")

            if rm_svi == 100:
                logger.debug(f"{hostname} Remove all SVI Interfaces")

        ## Save Router Config
        ssh.sendline("end")
        output = ssh.expect(exec_mode)
        ssh.sendline("write mem")
        time.sleep(2)
        output = ssh.expect(exec_mode)
        logger.debug(f"{hostname} Save Configuration")

        ssh.sendline("show run")
        time.sleep(1)
        output = ssh.expect([read_mode, exec_mode])
        logger.debug(ssh.before) #Does not log show run output
        print(ssh.before) #Does not disply show run output

        ## Close SSH connection
        ssh.close()
        logger.debug(f"{hostname} Close Connection")

    except:
        logger.exception(f"{hostname} Encounter ERROR")
        ssh.close()

## This function allows configuration to multiple network devices as the same time
with concurrent.futures.ThreadPoolExecutor() as executor:
    threads = executor.map(connect_network_devices, devices_txt)

logger.debug("############################ END CODE ############################")

## End Code
