#! /usr/bin/python3

# PYTHON CLIENT

import socket
import time

cyan = str(36)

port = 3490
ip = 'localhost'
resource = "/home/hallison/webserv/randomHTMLfile.html"

def print_cyan(string):
	print("\033[96m{}\033[00m". format(string))

def basic_get(resource, http_version):
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # socket object
	s.connect((ip, port))
	request = "GET " + resource + " HTTP/" + str(http_version) + "\r\n\r\n"
	print_cyan("client: " + request)
	s.send(request.encode())
	data = s.recv(1024).decode() # try different bytes as well
	print(data)
	s.close()

def fragmented_get_2(resource, http_version):
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # socket object
	s.connect((ip, port))
	request_half_0 = "GET "
	request_half_1 = resource + " HTTP/" + str(http_version) + "\r\n\r\n"
	print_cyan(("client (sending in 3 pieces):\n" + request_half_0 + "\n" + request_half_1))
	s.send(request_half_0.encode())
	s.send(request_half_1.encode())
	data = s.recv(1024).decode()
	print(data)
	s.close()

basic_get(resource, 1.0)
time.sleep(1)
fragmented_get_2(resource, 1.0)
