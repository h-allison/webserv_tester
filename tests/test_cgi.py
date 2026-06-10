#! /usr/bin/python3
import os
import subprocess
import time
import sys
import datetime

# my files
import color
import defines
import testserv

test_count = 0

def test_get_date_py_script(server):
	global test_count
	test_count += 1
	request_msg = "GET /scripts/date.py HTTP/1.0\r\n\r\n"
	response = testserv.send_request_get_response(request_msg)
	ok = response.startswith(b"Content-Type: text/plain\n\n20")
	msg_string = testserv.format_request(request_msg)
	color.print_test(f"Test {test_count}",
					msg_string, "Content-Type: text/plain <date>", ok)
	return 0 if ok else 1	


def test_get_hello_world_py_script(server):
	global test_count
	test_count += 1
	request_msg = "GET /scripts/hello_world.py HTTP/1.0\r\n\r\n"
	response = testserv.send_request_get_response(request_msg)
	ok = response.startswith(b"hello world")
	msg_string = testserv.format_request(request_msg)
	color.print_test(f"Test {test_count}",
					msg_string, "hello world", ok)
	return 0 if ok else 1	

def launcher():
	color.title_print("CGI GET tests", "bold")
	server_proc, log_file = testserv.start_server("simple_CGI.conf")
	error = 0

	tests = [
		test_get_hello_world_py_script, # script responds with hello world
		#test_pause_py_script, # check full msg received after pause
	]

	for test in tests:
		error += test(server_proc)
		server_proc, log_file = testserv.restart_if_needed(server_proc, "simple_CGI.conf", log_file)	
	log_file.close()
	server_proc.kill()
	
	"""
	server_proc, log_file = start_server("simple_allow_post_autoindex_off.conf")
	error += test_get_not_allowed(server_proc) # 403 Forbidden
	log_file.close()
	server_proc.kill()
	"""
	
	return error

