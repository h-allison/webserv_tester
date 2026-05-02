#! /usr/bin/python3
import os
import subprocess
import time
import sys

# my files
import defines
import color

test_count = 0

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
	time.sleep(0.3) # 200 milliseconds gives webserv time to start
	if server_proc.poll() is not None:
		output = server_proc.stdout.read().decode()
		print("\nwebserv failed to start with config " + config_path)
		print(output)
		sys.exit(1)
	return server_proc

def get_test_1(server):
	global test_count
	test_count += 1
	request_msg = "GET /index.html HTTP/1.0\r\n\r\n"
	
	printf_proc = subprocess.Popen(
		["printf", request_msg],
		stdout=subprocess.PIPE,
		text=True)
	
	nc_proc = subprocess.Popen(
		["nc", "localhost", defines.port],
		stdin=printf_proc.stdout,
		stdout=subprocess.PIPE,
		stderr=subprocess.STDOUT,
		text=True)
	
	printf_proc.stdout.close() # need to close this because netcat has it open
	output, _ = nc_proc.communicate()
	# communicate returns 2 values, but we've already merged stderr into stdout,
	#  the _ means 2nd value is ignored

	ok = output.startswith("HTTP/1.0 200 OK")
	color.print_test(f"Test {test_count}", f"GET /index.html",
					"should return 200 OK", ok)
	return 0 if ok else 1


def launcher():
    color.title_print("simple GET tests", "bold")
    server_proc = start_server(defines.configs + "simple_example_allows_get.conf")
    error = 0
    error += get_test_1(server_proc)
    #error += get_test_2(server_proc)
    server_proc.kill()
    return error

