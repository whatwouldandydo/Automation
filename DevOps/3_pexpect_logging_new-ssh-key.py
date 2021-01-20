"""
Date: 2020-07-24
(1) Create custom logging. Save logs to file. Display log to console
(2) First time SSH and accept RSA key
(3) Config VLANs
(4) Open devices from a text file
(5) From a device file, loop through each IP, SSH to each IP, configure VLANs for each IP
"""

## Import modules
import pexpect
import logging
import time
import datetime
import getpass
import pprint

## Create custom logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter("%(asctime)s--%(name)s--%(levelname)s--> %(message)s")
log_file = "3_pexpect_ssh-new-key.log"
file_handler = logging.FileHandler(log_file)
file_handler.setFormatter(formatter)

console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(console_handler)

## Credential to access network devices
# username = input("Username: ")
# password = getpass.getpass()
username = "admin"
password = "devops"

## Open devices from a file
device_file = "devices.txt"
with open(device_file) as f:
    devices_txt = f.read().splitlines()

## Expect outputs return from network devices
read_mode = ">"
exec_mode = "#"

## Connect to network devices
def network_device(hostname):
    try:
        ssh = pexpect.spawn(f"ssh {username}@{hostname}")
        result = ssh.expect(["\(yes/no/\[fingerprint\]\)\?", "Password", "password",
                            "Password:", "password:", pexpect.EOF])
        if result == 0:
            logger.debug(f"First time SSH to {hostname}")
            ssh.sendline("yes")
            result = ssh.expect(["Password", "password", "Password:", "password", pexpect.EOF])

        logger.debug(f"Connect to {hostname}")
        ssh.sendline(password)
        logger.debug(f"{hostname} Enter password")
        result = ssh.expect(read_mode)
        # print(ssh.before, ssh.after)

        ssh.sendline("enable")
        logger.debug(f"{hostname} Enable Exec Mode")
        result = ssh.expect(exec_mode)
        # print(ssh.before, ssh.after)

        ssh.sendline("term len 0")
        logger.debug(f"{hostname} Disable terminal length")
        result = ssh.expect(exec_mode)

        ssh.sendline("config t")
        logger.debug(f"{hostname} Enter configuration mode")
        result = ssh.expect(exec_mode)

        ## Configure VLAN
        for vlan in range(99):
            ssh.sendline(f"vlan {vlan}")
            logger.debug(f"{hostname} Configure VLAN {vlan}")
            result = ssh.expect(exec_mode)
            ssh.sendline(f"name DevOps_VLAN_{vlan}")
            result = ssh.expect(exec_mode)

        # Remove VLANs
        # for vlan in range(99):
        #     ssh.sendline(f"no vlan {vlan}")
        #     result = ssh.expect(exec_mode)
        #     print(f"Remove VLAN {vlan}")

        ## Save config
        ssh.sendline("end")
        result = ssh.expect(exec_mode)
        ssh.sendline("write mem")
        logger.debug(f"{hostname} Save config")
        result = ssh.expect(exec_mode)

        ## Show run config
        ssh.sendline("show run")
        time.sleep(1)
        result = ssh.expect(exec_mode)
        print(ssh.before, ssh.after)
        
        ssh.close()

    except:

        ssh.close()
        logger.exception(f"Cannot SSH to {hostname}")

## Loop through each IP, SSH to each IP, configure each IP
for ip in devices_txt:
    network_device(ip)


## End Code