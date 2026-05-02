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

def networking_test_bad_config(config_path):
	global test_count
	test_count += 1
	if config_path.endswith("bad_port_requires_root.conf"):
		if os.getuid() == 0:
			color.cprint("Test " + str(test_count) +
						"\tSkipping because webserv is running as root and the test is irrelevant",
						"cyan")
			return 0
	proc = subprocess.Popen(
		[defines.webserv, config_path],
		stdout=subprocess.DEVNULL,
		stderr=subprocess.DEVNULL) #sends output to /dev/null to avoid clutter
	time.sleep(0.2) # 100 milliseconds
	is_finished = proc.poll()
	ok = is_finished is not None
	if not ok:
		proc.kill()
	color.print_test(f"Test {test_count}", f"./webserv {config_path}", "should exit", ok)
	return 0 if ok else 1

def launcher():
	color.title_print("networking init tests", "bold")
	error = 0
	error += networking_test_bad_config(defines.configs_networking_init + "no_listen.conf")
	error += networking_test_bad_config(defines.configs_networking_init + "bad_port_requires_root.conf")
	error += networking_test_bad_config(defines.configs_networking_init + "bad_port_too_big.conf")
	return error

