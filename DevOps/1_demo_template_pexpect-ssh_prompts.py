"""
Date: 2020-07-13
Summary: This a demo and template for ...
(1) SSH with pexpect
(2) Expected prompt from remote device or child
(3) The use of a list of expected prompts from ssh.expect([])
(4) Print out results that matched ssh.expect([])
(5) Config VLANs with for loop
(6) Send information to log
"""

## Import Modules
import pexpect
import time
import datetime
import getpass
import logging

## Enable logging
log_file = "1_demo_template_pexpect-ssh_prompts.log"
logging.basicConfig(filename=log_file, level=logging.DEBUG,
                    format="%(asctime)s--%(levelname)s:%(lineno)d-->%(message)s")

## Define hostname, username, and password
hostname = "192.168.0.1"
# username = input("Enter Username: ")
# password = getpass.getpass()
username = "admin"
password = "devops"

## Expect prompt from remote device
read_mode = ">"
exec_mode = "#"

## Setup SSH access
t1 = time.perf_counter()

ssh = pexpect.spawn(f"ssh {username}@{hostname}")
result = ssh.expect(["Username:", ":", "password", "Password", pexpect.EOF, "Password:"])

if result == 0:
    print("ssh PROMPT index 0")
    print(ssh.before)
    print(ssh.after)
elif result == 1:
    print("ssh PROMPT index 1")
    print(ssh.before)
    print(ssh.after)
elif result == 2:
    print("ssh PROMPT index 2")
    print(ssh.before)
    print(ssh.after)
elif result == 3: # ssh.expect matched "Password"
    print("ssh PROMPT index 3")
    logging.debug(ssh.before)
    print(ssh.before)
    print(ssh.after)
elif result == 4:
    print("ssh PROMPT index 4")
    print(ssh.before)
    print(ssh.after)
else:
    print("ssh PROMPT NOT MATCH")
    print(ssh.before)
    print(ssh.after)
print()

ssh.sendline(password)
result = ssh.expect([read_mode, exec_mode, pexpect.EOF])

if result == 0: # ssh.expect matched read_mode
    print("After password Prompt index 0")
    logging.debug(ssh.before)
    print(ssh.before)
    print(ssh.after)
elif result == 1:
    print("After password Prompt index 1")
    print(ssh.before)
    print(ssh.after)
elif result == 2:
    print("After password Prompt index 2")
    print(ssh.before)
    print(ssh.after)
else:
    print("After password Prompt NO Matched")
    print(ssh.before)
    print(ssh.after)
print()

ssh.sendline("enable")
result == ssh.expect([read_mode, exec_mode, pexpect.EOF])

if result == 0: # ssh.expect matched read_mode
    print("Enable mode prompt index 0")
    logging.debug(ssh.before)
    print(ssh.before)
    print(ssh.after)
elif result == 1:
    print("Enable mode prompt index 1")
    print(ssh.before)
    print(ssh.after)
elif result == 2:
    print("Enable mode prompt index 2")
    print(ssh.before)
    print(ssh.after)
else:
    print("Enable mode prompt NO Matched")
    print(ssh.before)
    print(ssh.after)
print()

ssh.sendline("term len 0")
result = ssh.expect([read_mode, exec_mode, pexpect.EOF])

if result == 0:
    print("Term Len 0 prompt index 0")
    print(ssh.before)
    print(ssh.after)
elif result == 1: # ssh.expect matched exec_mode
    print("Term Len 0 prompt index 1")
    logging.debug(ssh.before)
    print(ssh.before)
    print(ssh.after)
elif result == 2:
    print("Term Len 0 prompt index 2")
    print(ssh.before)
    print(ssh.after)
else:
    print("Term Len 0 prompt NO Matched")
    print(ssh.before)
    print(ssh.after)
print()

ssh.sendline("config t")
result = ssh.expect([read_mode, exec_mode, pexpect.EOF])

if result == 0:
    print("config t Prompt index 0")
    print(ssh.before)
    print(ssh.after)
elif result == 1: # ssh.expect matched exec_mode
    print("config t Prompt index 1")
    logging.debug(ssh.before)
    print(ssh.before)
    print(ssh.after)
elif result == 2:
    print("config t Prompt index 2")
    print(ssh.before)
    print(ssh.after)
else:
    print("config t Prompt index NO Matched")
    print(ssh.before)
    print(ssh.after)
print()

for vlan in range(10):
    if result == 0:
        print(f"READ VLAN {vlan}")
        ssh.sendline("config t")
        print(ssh.before)
        print(ssh.after)
    elif result == 1:
        print(f"CONFIGURE VLAN {vlan}")
        ssh.sendline(f"vlan {vlan}")
        logging.debug(ssh.before)
        print(ssh.before)
        print(ssh.after)
    else:
        print("ERROR CONFIGURE VLAN")

for rm_vlan in range(10):
    if result == 0:
        print(f"RM_VLAN {rm_vlan}")
        ssh.sendline("config f")
    elif result == 1:
        print(f"REMOVE VLAN {rm_vlan}")
        ssh.sendline(f"no vlan {rm_vlan}")
        logging.debug(ssh.before)
    else:
        print("ERROR REMOVE VLANs")
print()

ssh.sendline("end")
ssh.expect([read_mode, exec_mode, pexpect.EOF])

ssh.sendline("write mem")
result = ssh.expect([read_mode, exec_mode, pexpect.EOF])

if result == 0:
    print("write mem Prompt Index 0")
    print(ssh.before)
    print(ssh.after)
elif result == 1: # ssh.expect matched exec_mode
    print("write mem Prompt Index 1")
    logging.debug(ssh.before)
    print(ssh.before)
    print(ssh.after)
elif result == 2:
    print("write mem Prompt Index 2")
    print(ssh.before)
    print(ssh.after)
else:
    print("write mem Prompt Index NO Matched")
    print(ssh.before)
    print(ssh.after)
print()

ssh.sendline("show run")
ssh.expect([read_mode, exec_mode, pexpect.EOF])
print("SHOW RUN")
logging.debug(ssh.before)
print(ssh.before) # Did not display the entire config
print(ssh.after)

ssh.close()

t2 = time.perf_counter()

delta_time = t2 - t1

logging.debug(f"###### {__name__} runs {delta_time} Seconds #####")
print(f"################### {delta_time} Seconds ###################")
