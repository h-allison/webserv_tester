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

"""
Interesting thing to note about this test & script:
To fulfill the post_body.sh script's expectations and successfully emulate a post request via the browser,
it is necessary to have a space between the CRLF and hello world. This also results in a space before
"hello world" (or whatever body we send) in the file created
"""

def test_post_with_post_body_script(server):
	global test_count
	test_count += 1
	
	request_msg = "POST /scripts/post_body.sh HTTP/1.0\r\nContent-Length: 12\r\n\r\n hello world"
	encoded_response = testserv.send_request_get_response(request_msg)
	response = encoded_response.decode("utf-8")
	
	# check if file is there and was written to
	file_path_with_pesky_newline = response.split("Written to: ")[1]
	file = file_path_with_pesky_newline.split("\n")[0]
	with open(file) as f:
		contents = f.read()
	f.close()
	ok = response.startswith("HTTP/1.0 200 Created") and "Content-Type: text/plain" in response and contents == " hello world"
	msg_string = testserv.format_request(request_msg)
	color.print_test(f"Test {test_count}", msg_string,
					"200 Created + text/html + file uploaded contains ' hello world'", ok)
	return 0 if ok else 1

def test_post_without_cgi(server):
	global test_count
	test_count += 1
	request_msg = "POST / HTTP/1.0\r\nContent-type: text/html\r\nContent-length: 5\r\n\r\nabc\r\n"
	header = testserv.send_request_get_header(request_msg)
	ok = header.startswith("HTTP/1.0 403 Forbidden") and "Content-Type: text/html" in header
	msg_string = testserv.format_request(request_msg)
	color.print_test(f"Test {test_count}", msg_string,
					"403 Forbidden + text/html", ok)
	return 0 if ok else 1

def launcher():
	color.title_print("POST tests", "bold")
	server_proc, log_file = testserv.start_server("demo_with_CGI.conf")
	error = 0

	tests = [
		test_post_without_cgi, # 403 Forbidden
		test_post_with_post_body_script, # 200 Created
	]

	for test in tests:
		error += test(server_proc)
		server_proc, log_file = testserv.restart_if_needed(server_proc, "demo_with_cgi.conf", log_file)	
	log_file.close()
	server_proc.kill()

	return error
