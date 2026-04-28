#! /usr/bin/python3
import os
import subprocess
import time

# my files
import defines
import color

"""
Resources:
https://www.datacamp.com/tutorial/python-subprocess
https://stackoverflow.com/questions/6809590/merging-a-python-scripts-subprocess-stdout-and-stderr-while-keeping-them-disti
"""

"""
def get_test_simple_0():

	color.cprint("Test 1", "bold")
	server_proc = subprocess.run([defines.webserv, config_path], capture_output=True, text=True)
"""

def start_server(config_path):
	
	print("./webserv ", config_path)
	server_proc = subprocess.Popen(
		[defines.webserv, config_path],
		stdout=subprocess.PIPE,
		stderr=subprocess.STDOUT)

	request_msg = "GET /example/index.html\r\n\r\n"
	printf_proc = subprocess.Popen(
		["printf", request_msg], stdout=subprocess.PIPE, text=True)
	nc_proc = subprocess.Popen(
		["nc", "localhost", "3490"],
		stdin=printf_proc.stdout, stdout=subprocess.PIPE,
		text=True)
	
	printf_proc.stdout.close()
	output, error = nc_proc.communicate()
	
	print(output)
	print(error)

def launcher():
	color.title_print("simple GET tests", "bold")

	config_path = defines.configs + "simple_0.txt"
	start_server(config_path)

	#get_test_simple_0()
	return 0

