#! /usr/bin/python3
import os
import subprocess
import time

# my files
import defines
import color

"""
Resources:

https://stackoverflow.com/questions/43274476/is-there-a-way-to-check-if-a-subprocess-is-still-running
"""

def parsing_test_no_arg():

	proc = subprocess.Popen([defines.webserv], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) #sends output to /dev/null to avoid clutter
	time.sleep(0.1) # 100 milliseconds
	is_finished = proc.poll()
	ok = is_finished is not None
	# poll return None if process is still running, or an exit code (0, 1, etc) if it's finished
	if not ok:
		proc.kill()
	color.print_test("Test 1", "./webserv <no arguments>", "Should exit immediately", ok)
	return 0 if ok else 1

def launcher():
	color.title_print("parsing tests", "bold")
	error = 0
	error += parsing_test_no_arg()
	return error

