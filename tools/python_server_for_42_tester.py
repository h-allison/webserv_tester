#! /usr/bin/python3

"""
PYTHON SERVER using socket Module

This is a python server designed to read requests from the 42 tester.
It sends back the expected input, in order to get the next request.
"""

import socket
import os
from pathlib import Path

this_script_path = Path(__file__)
this_dir = this_script_path.parent
canned_dir = str(this_dir) + "/canned_responses/"
test_count = 0


def expected_response():
	global test_count
	if test_count == 0:
		file_name = "test_0"
	elif test_count == 1:
		file_name = "test_1"
	else:
		return 'not handled yet'
	file_path = canned_dir + file_name
	with open(file_path, 'r') as file:
		file_content = file.read()
		print(file_content)
		return file_content

def handle_single_connection(c):
	global test_count
	msg = ''
	while (1):
		data = c.recv(2048).decode('utf-8')
		#data = c.recv(2048)
		if not data:
			break
		print ("from client: ")
		print (str(data), "\n\n")
		msg = msg + data
		if "\r\n\r\n" in msg:
			print ("full msg = ", msg)
			c.sendall(expected_response().encode())
			msg = ""
			break
	#c.sendall(expected_response().encode())
	#c.close()
	test_count += 1

def main():
	host = "127.0.0.1"
	port = 3491
	server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server.bind((host, port))
	server.listen()
	print("Python server is listening on port %s" %(port))

	# accept() returns BOTH
	# 1) a connection (usually, different socket on another port assigned by the kernel)
	# 2) address of the client

	while (1):
		c, addr = server.accept()
		print("Got connection from ", addr)
		handle_single_connection(c)

if __name__=="__main__":
	main()

# Sources:
# https://www.tutorialspoint.com/python/python_socket_programming.htm
