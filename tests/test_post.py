#! /usr/bin/python3
import os
import subprocess
import time
import sys
import datetime

# my files
import defines
import color
import testserv

test_count = 0

def test_post_without_cgi(server):
	global test_count
	test_count += 1
	request_msg = "POST / HTTP/1.0\r\nContent-type: text/html\r\nContent-length: 5\r\n\r\nabc\r\n"
	header = testserv.send_request_get_header(request_msg)

	ok = header.startswith("HTTP/1.0 403 Forbidden") and "Content-Type: text/html" in header
	msg_string = format_request(request_msg)
	color.print_test(f"Test {test_count}", msg_string,
					"TBD", ok)
	return 0 if ok else 1

def test_post_without_cgi(server):
	global test_count
	test_count += 1
	request_msg = "POST / HTTP/1.0\r\nContent-type: text/html\r\nContent-length: 5\r\n\r\nabc\r\n"
	header = testserv.send_request_get_header(request_msg)

	ok = header.startswith("HTTP/1.0 403 Forbidden") and "Content-Type: text/html" in header
	msg_string = testserv.format_request(request_msg)
	color.print_test(f"Test {test_count}", msg_string,
					"TBD", ok)
	return 0 if ok else 1

def launcher():
	color.title_print("simple POST tests", "bold")
	server_proc, log_file = testserv.start_server("simple_allow_post_autoindex_off.conf")
	error = 0

	tests = [
		test_post_without_cgi, # ?
	]

	for test in tests:
		error += test(server_proc)
		server_proc, log_file = testserv.restart_if_needed(server_proc, "simple_allow_get_autoindex_off.conf", log_file)	
	log_file.close()
	server_proc.kill()

	return error
