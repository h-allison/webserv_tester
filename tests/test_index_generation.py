#! /usr/bin/python3
import os
import subprocess
import time
import sys

# my files
import defines
import color

test_count = 0


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

"""
def test_get_image_png(server):
	global test_count
	test_count += 1
	request_msg = "GET /minirt.png HTTP/1.0\r\n\r\n"
	header = send_request_get_header(request_msg)
	ok = header.startswith("HTTP/1.0 200 OK") and "Content-Type: image/png" in header
	color.print_test(f"Test {test_count}", format_request(request_msg), "200 OK + image/png", ok)
	return 0 if ok else 1

def test_get_image_gif(server):
	global test_count
	test_count += 1
	request_msg = "GET /minishell.gif HTTP/1.0\r\n\r\n"
	header = send_request_get_header(request_msg)
	ok = header.startswith("HTTP/1.0 200 OK") and "Content-Type: image/gif" in header
	color.print_test(f"Test {test_count}", format_request(request_msg), "200 OK + image/gif", ok)
	return 0 if ok else 1

def test_get_image_jpg(server):
	global test_count
	test_count += 1
	request_msg = "GET /disarray_0.jpg HTTP/1.0\r\n\r\n"
	header = send_request_get_header(request_msg)
	ok = header.startswith("HTTP/1.0 200 OK") and "Content-Type: image/jpeg" in header
	# nginx treats jpg and jpeg as the same type, and returns image/jpeg for both
	color.print_test(f"Test {test_count}", format_request(request_msg), "200 OK + image/jpeg", ok)
	return 0 if ok else 1

def test_get_image_jpeg(server):
	global test_count
	test_count += 1
	request_msg = "GET /disarray_1.jpeg HTTP/1.0\r\n\r\n"
	header = send_request_get_header(request_msg)
	ok = header.startswith("HTTP/1.0 200 OK") and "Content-Type: image/jpeg" in header
	color.print_test(f"Test {test_count}", format_request(request_msg), "200 OK + image/jpeg", ok)
	return 0 if ok else 1

def test_get_unknown_extension(server):
	global test_count
	test_count += 1
	request_msg = "GET /some_file.unknown HTTP/1.0\r\n\r\n"
	header = send_request_get_header(request_msg)
	if "Content-Type: application/octet-stream" in header:
		our_type = "application/octet-stream"
	elif "Content-Type: text/plain" in header:
		our_type = "text/plain"
	else:
		our_type = "neither"
	ok = header.startswith("HTTP/1.0 200 OK") and ("Content-Type: application/octet-stream" in header or "Content-Type: text/plain" in header)
	color.print_test(f"Test {test_count}", format_request(request_msg), "200 OK + application/octet-stream or text/plain", ok)
	color.cprint("\n\tNote: nginx returns text/plain for unknown extensions, but RFC 2046 (Section 5.2.4.)\n\tsays application/octet-stream is the default for unknown types.", "gray")
	color.cprint(f"\tWebserv responded with: {our_type}\n", "gray")
	return 0 if ok else 1

def test_get_root_without_autoindex(server):
	global test_count
	test_count += 1
	request_msg = "GET / HTTP/1.0\r\n\r\n"
	header = send_request_get_header(request_msg)
	ok = header.startswith("HTTP/1.0 403 Forbidden")
	msg_string = format_request(request_msg)
	color.print_test(f"Test {test_count}",
					msg_string, "403 Forbidden", ok)
	return 0 if ok else 1

def test_get_missing_http_version(server):
	global test_count
	test_count += 1
	request_msg = "GET /hello_world.txt\r\n\r\n"
	response = send_request_get_response(request_msg)
	ok = response.startswith(b"hello world")
	msg_string = format_request(request_msg)
	color.print_test(f"Test {test_count}", format_request(request_msg), "requested file with no headers (HTTP 0.9)", ok)
	return 0 if ok else 1

def test_nonexistent_file(server):
	global test_count
	test_count += 1
	request_msg = "GET /nonexistent.html HTTP/1.0\r\n\r\n"
	header = send_request_get_header(request_msg)
	ok = header.startswith("HTTP/1.0 404 Not Found")
	msg_string = format_request(request_msg)
	color.print_test(f"Test {test_count}",
					msg_string, "404 Not Found", ok)
	return 0 if ok else 1
"""

def test_generate_index(server):
	global test_count
	test_count += 1
	request_msg = "GET / HTTP/1.0\r\n\r\n"
	response = send_request_get_response(request_msg)

	header = response.split(b"\r\n\r\n")[0].decode("utf-8")
	body = response.split(b"\r\n\r\n")[1].decode("utf-8")
	ok = header.startswith("HTTP/1.0 200 OK") and "Content-Type: text/html" in header \
			and "A.html" in body and "B.txt" in body and "C.jpg" in body
	msg_string = format_request(request_msg)
	color.print_test(f"Test {test_count}", msg_string,
					"200 OK + text/html + file list", ok)
	return 0 if ok else 1


def launcher():
	color.title_print("auto-generation of index.html tests", "bold")
	error = 0
	
	server_proc = start_server("autoindex_on_but_no_index.conf")
	tests = [
		test_generate_index, # 200 OK
		# test_get_image_png, # 200 OK
		# test_get_image_gif, # 200 OK
		# test_get_image_jpg, # 200 OK
		# test_get_image_jpeg, # 200 OK
		# test_get_unknown_extension, # 200 OK + application/octet-stream or text/plain
		# test_get_missing_http_version, # treats as HTTP 0.9
		# test_get_root_without_autoindex, # 403 Forbidden
		# test_nonexistent_file, # 404 Not Found
	]
	for test in tests:
		error += test(server_proc)
		server_proc = restart_if_needed(server_proc, "autoindex_on_but_no_index.conf")	
	
	server_proc.kill()
	return error

