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

	"""
	print("./webserv <no arguments>")
	result = subprocess.run([defines.webserv],
	capture_output=True, text=True)
	res = 
	print(result.stdout)
	print(result.stderr)
	"""
	
	color.cprint("Test 1", "bold")
	print("./webserv <no arguments>")
	proc = subprocess.Popen([defines.webserv])
	time.sleep(0.1)
	is_finished = proc.poll()
	# poll == 0 means subprocess is alive
	try:
		assert is_finished != 0
	except AssertionError as e:
		print("incorrect")

	"""
	cmd = '/home/hallison/webserv'
	pid = os.fork()
	if pid == 0:
		print("child process")
		os._exit(0)
	else:
		print("parent process")
		os.wait()
	#os.execl(cmd, cmd)
	"""

def launcher():
	color.title_print("parsing tests", "bold")
	parsing_test_no_arg()
	return 0

