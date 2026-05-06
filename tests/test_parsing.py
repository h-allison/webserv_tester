#! /usr/bin/python3
import os
import subprocess
import time

# my files
import defines
import color

test_count = 0

"""
Resources:

https://stackoverflow.com/questions/43274476/is-there-a-way-to-check-if-a-subprocess-is-still-running
"""

def test_no_arg():
	global test_count
	test_count += 1
	proc = subprocess.Popen([defines.webserv], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) #sends output to /dev/null to avoid clutter
	time.sleep(0.2) # 100 milliseconds
	is_finished = proc.poll()
	ok = is_finished is not None
	# poll return None if process is still running, or an exit code (0, 1, etc) if it's finished
	if not ok:
		proc.kill()
	color.print_test(f"Test {test_count}", "./webserv <no arguments>", "exit(1)", ok)
	return 0 if ok else 1

def test_malformed_config(config_name):
	global test_count
	test_count += 1
	config_path = defines.configs_parsing + config_name
	proc = subprocess.Popen(
		[defines.webserv, config_path],
		stdout=subprocess.DEVNULL,
		stderr=subprocess.DEVNULL) #sends output to /dev/null to avoid clutter
	time.sleep(0.2) # 100 milliseconds
	is_finished = proc.poll()
	ok = is_finished is not None
	if not ok:
		proc.kill()
	color.print_test(f"Test {test_count}", f"./webserv {config_name}", "exit(1)", ok)
	return 0 if ok else 1

def launcher():
	color.title_print("parsing tests", "bold")
	error = 0
	error += test_no_arg()
	error += test_malformed_config("bad_ip_1.conf")
	error += test_malformed_config("bad_ip_2.conf")
	error += test_malformed_config("bad_ip_3.conf")
	error += test_malformed_config("bad_port_1.conf")
	return error

