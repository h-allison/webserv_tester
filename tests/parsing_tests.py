#! /usr/bin/python3
import os
import subprocess

# my files
import defines
import color

def parsing_test_no_arg():

	print(defines.webserv)
	result = subprocess.run([defines.webserv],
	capture_output=True, text=True)
	res = result.stdout + result.stderr
	return res

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

