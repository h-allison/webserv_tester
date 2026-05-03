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

def start_server(config_name):
	config_path = defines.configs + config_name
	print("./webserv ", config_name, "\n")
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

def restart_if_needed(server_proc, config_name):
	time.sleep(0.2)
	if server_proc.poll() is not None:
		color.cprint("\nwebserv exited unexpectedly. restarting to continue tests...", "cyan")
		server_proc = start_server(config_name)
	return server_proc

def send_request(request_msg):
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
	return output

def format_request(request_msg):
	return "\"" + request_msg.replace("\r\n", "\\r\\n") + "\""

def test_get_index(server):
	global test_count
	test_count += 1
	request_msg = "GET /index.html HTTP/1.0\r\n\r\n"
	output = send_request(request_msg)

	ok = output.startswith("HTTP/1.0 200 OK")
	msg_string = format_request(request_msg)
	color.print_test(f"Test {test_count}", msg_string,
					"200 OK", ok)
	return 0 if ok else 1

def test_get_root_without_autoindex(server):
	global test_count
	test_count += 1
	request_msg = "GET / HTTP/1.0\r\n\r\n"
	output = send_request(request_msg)
	ok = output.startswith("HTTP/1.0 403 Forbidden")
	msg_string = format_request(request_msg)
	color.print_test(f"Test {test_count}",
					msg_string, "403 Forbidden", ok)
	return 0 if ok else 1

def test_nonexistent_file(server):
	global test_count
	test_count += 1
	request_msg = "GET /nonexistent.html HTTP/1.0\r\n\r\n"
	output = send_request(request_msg)
	ok = output.startswith("HTTP/1.0 404 Not Found")
	msg_string = format_request(request_msg)
	color.print_test(f"Test {test_count}",
					msg_string, "404 Not Found", ok)
	return 0 if ok else 1

def launcher():
	color.title_print("simple GET tests", "bold")
	server_proc = start_server("simple_allow_get_autoindex_off.conf")
	error = 0
	
	error += test_get_index(server_proc)
	server_proc = restart_if_needed(server_proc, "simple_allow_get_autoindex_off.conf")

	error += test_get_root_without_autoindex(server_proc)
	server_proc = restart_if_needed(server_proc, "simple_allow_get_autoindex_off.conf")
	
	error += test_nonexistent_file(server_proc)
	server_proc = restart_if_needed(server_proc, "simple_allow_get_autoindex_off.conf")	
	
	server_proc.kill()
	return error

