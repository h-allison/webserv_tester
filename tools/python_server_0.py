#! /usr/bin/python3

"""
PYTHON SERVER using socket Module

This is an extremely simple python server, which I am using to quickly read
requests sent by the 42 tester. Right now it can only handle one connection
"""

import socket

host = "127.0.0.1"
port = 3490
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()
print("Python server is listening on port %s" %(port))

# accept() returns BOTH
# 1) a connection (usually, different socket on another port assigned by the kernel)
# 2) address of the client

c, addr = server.accept()
print("Got connection from ", addr)
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
		print("got delimiter")
		print ("full msg = ", msg)
		break
	#c.sendall(b'HTTP/1.0 200 OK\r\n\r\n')

c.close()

# Sources:
# https://www.tutorialspoint.com/python/python_socket_programming.htm
