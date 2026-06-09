#! /usr/bin/python3
import os
import subprocess
import time
import sys

# my files
import defines
import color
import testserv

test_count = 0

def test_generate_index_in_subdirectory(server):
	global test_count
	test_count += 1
	request_msg = "GET /subdir/ HTTP/1.0\r\n\r\n"
	response = testserv.send_request_get_response(request_msg)

	header = response.split(b"\r\n\r\n")[0].decode("utf-8")
	body = response.split(b"\r\n\r\n")[1].decode("utf-8")
	ok = header.startswith("HTTP/1.0 200 OK") and "Content-Type: text/html" in header \
			and "hello.html" in body and "world.html" in body
	msg_string = testserv.format_request(request_msg)
	color.print_test(f"Test {test_count}", msg_string,
					"200 OK + text/html + file list", ok)
	return 0 if ok else 1

def test_generate_index(server):
	global test_count
	test_count += 1
	request_msg = "GET / HTTP/1.0\r\n\r\n"
	response = testserv.send_request_get_response(request_msg)

	header = response.split(b"\r\n\r\n")[0].decode("utf-8")
	body = response.split(b"\r\n\r\n")[1].decode("utf-8")
	ok = header.startswith("HTTP/1.0 200 OK") and "Content-Type: text/html" in header \
			and "A.html" in body and "B.txt" in body and "C.jpg" in body
	msg_string = testserv.format_request(request_msg)
	color.print_test(f"Test {test_count}", msg_string,
					"200 OK + text/html + file list", ok)
	return 0 if ok else 1

def test_get_index_in_subdirectory(server):
	global test_count
	test_count += 1
	request_msg = "GET /scripts/ HTTP/1.0\r\n\r\n"
	header = testserv.send_request_get_header(request_msg)

	ok = header.startswith("HTTP/1.0 200 OK") and "Content-Type: text/html" in header
	msg_string = testserv.format_request(request_msg)
	color.print_test(f"Test {test_count}", msg_string,
					"200 OK + text/html", ok)
	return 0 if ok else 1

def test_get_index(server):
	global test_count
	test_count += 1
	request_msg = "GET / HTTP/1.0\r\n\r\n"
	header = testserv.send_request_get_header(request_msg)

	ok = header.startswith("HTTP/1.0 200 OK") and "Content-Type: text/html" in header
	msg_string = testserv.format_request(request_msg)
	color.print_test(f"Test {test_count}", msg_string,
					"200 OK + text/html", ok)
	return 0 if ok else 1

def launcher():

	color.title_print("autoindex tests", "bold")
	
	error = 0

	# Testing first with config file that includes index.html file
	server_proc, log_file = testserv.start_server("simple_allow_get_autoindex_on.conf")
	tests = [
		test_get_index, # 200 OK
		test_get_index_in_subdirectory,
	]
	for test in tests:
		error += test(server_proc)
		server_proc, log_file = testserv.restart_if_needed(server_proc, "simple_allow_get_autoindex_on.conf", log_file)	
	log_file.close()
	server_proc.kill()

	print("")

	# Testing now with config file that does NOT include index.html file
	server_proc, log_file = testserv.start_server("autoindex_on_but_no_index.conf")
	tests = [
		test_generate_index, # 200 OK
		test_generate_index_in_subdirectory # 200 OK
	]
	for test in tests:
		error += test(server_proc)
		server_proc, log_file = testserv.restart_if_needed(server_proc, "autoindex_on_but_no_index.conf", log_file)	
	log_file.close()
	server_proc.kill()
	return error