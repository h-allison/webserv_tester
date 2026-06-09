#! /usr/bin/python3
import os
import subprocess
import time
import sys
import datetime

# my files
import defines
import color

test_count = 0

def start_server(config_name):
	config_path = defines.configs + config_name
	print("./webserv ", config_name, "\n")
	os.makedirs(defines.logs, exist_ok=True) # create logs dir if doesn't exist
	log_file_name = defines.logs + "/webserv_" + datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".log"
	log_file = open(log_file_name, "w")
	server_proc = subprocess.Popen(
		[defines.webserv, config_path],
		stdout=log_file,
		stderr=log_file)
	time.sleep(0.2) # 200 milliseconds gives webserv time to start
	if server_proc.poll() is not None:
		log_file.close()
		print("\nwebserv failed to start with config " + config_path)
		print("Check the log file for details: " + log_file_name)
		sys.exit(1)
	return server_proc, log_file

def restart_if_needed(server_proc, config_name, log_file):
	time.sleep(0.5)
	if server_proc.poll() is not None:
		color.cprint("\nwebserv exited unexpectedly. restarting to continue tests...", "cyan")
		log_file.close()
		server_proc, log_file = start_server(config_name)
	return server_proc, log_file

def send_request_get_header(request_msg):
	printf_proc = subprocess.Popen(
		["printf", request_msg],
		stdout=subprocess.PIPE,
		text=True)
	
	nc_proc = subprocess.Popen(
		["nc", "localhost", defines.port],
		stdin=printf_proc.stdout,
		stdout=subprocess.PIPE,
		stderr=subprocess.STDOUT)
	
	printf_proc.stdout.close() # need to close this because netcat has it open
	output, _ = nc_proc.communicate()
	# communicate returns 2 values, but we've already merged stderr into stdout,
	#  the _ means 2nd value is ignored
	
	header = output.split(b"\r\n\r\n")[0].decode("utf-8")
	# previously utf-8 encoding was done by text=True in subprocess.Popen,
	# but commnuicate() will then not work when it's reading binary data from a file
	# that's not meant to be text, like a png file. So we're reading in binary
	# and converting just the header to text

	return header

"""
NOTE: send_request_get_response() returns the entire response, with NO ENCODING
	This is needed for testing binary files, or responses to HTTP 0.9  requests,
	but for most tests, send_request_get_header() should be used.
"""
def send_request_get_response(request_msg):
	printf_proc = subprocess.Popen(
		["printf", request_msg],
		stdout=subprocess.PIPE,
		text=True)
	
	nc_proc = subprocess.Popen(
		["nc", "localhost", defines.port],
		stdin=printf_proc.stdout,
		stdout=subprocess.PIPE,
		stderr=subprocess.STDOUT)
	
	printf_proc.stdout.close() # need to close this because netcat has it open
	output, _ = nc_proc.communicate()
	return output


def format_request(request_msg):
	return "\"" + request_msg.replace("\r\n", "\\r\\n") + "\""

def test_post_without_cgi(server):
	global test_count
	test_count += 1
	request_msg = "POST / HTTP/1.0\r\nContent-type: text/html\r\nContent-length: 5\r\n\r\nabc\r\n"
	header = send_request_get_header(request_msg)

	ok = header.startswith("TBD") and "Content-Type: TBD" in header
	msg_string = format_request(request_msg)
	color.print_test(f"Test {test_count}", msg_string,
					"TBD", ok)
	return 0 if ok else 1

def launcher():
	color.title_print("simple POST tests", "bold")
	server_proc, log_file = start_server("simple_allow_post_autoindex_off.conf")
	error = 0

	tests = [
		test_post_without_cgi, # ?
	]

	for test in tests:
		error += test(server_proc)
		server_proc, log_file = restart_if_needed(server_proc, "simple_allow_get_autoindex_off.conf", log_file)	
	log_file.close()
	server_proc.kill()

	return error
