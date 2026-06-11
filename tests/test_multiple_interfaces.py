#! /usr/bin/python3
import os
import subprocess
import time

# my files
import color
import defines
import testserv

test_count = 0

def test_get_index_with_port(port):
	global test_count
	test_count += 1
	request_msg = "GET / HTTP/1.0\r\n\r\n"
	header = testserv.send_request_get_header_with_port(request_msg, port)
	ok = header.startswith("HTTP/1.0 200 OK") and "Content-Type: text/html" in header
	print("\n", header, "\n")
	msg_string = testserv.format_request(request_msg)
	color.print_test(f"Test {test_count}", msg_string,
					"on port " + str(port), ok)
	return 0 if ok else 1

def launcher():
	color.title_print("tests for multiple IP:port pairs", "bold")
	color.cprint("\tEach of the following tests uses a unique IP:port", "bold")
	color.cprint("\tbut all requests are sent to ONE instance of webserv, using ONE config.", "bold")
	color.cprint("\tTo prove support of multiple interfaces, all tests must pass.", "bold")
	color.cprint("\tUnique index.html files can be demonstrated manually.\n", "bold")
	server_proc, log_file = testserv.start_server("multiple_interfaces.conf")
	error = 0
	error += test_get_index_with_port(8080)
	error += test_get_index_with_port(8081)
	error += test_get_index_with_port(8082)
	error += test_get_index_with_port(8083)
	log_file.close()
	server_proc.kill()
	return error

