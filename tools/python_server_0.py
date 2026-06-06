#! /usr/bin/python3

# PYTHON SERVER

import socket

host = "127.0.0.1"
port = 3490
# backlog = 10

# socket.socket (socket_family, socket_type, protocol=0)
# family -- "AF_INET by default" .. no option for AF_UNSPEC?
# type = SOCK_STREAM,SOCK_DGRAM, SOCK_RAW, etc.
# protocol - "number is usually zero and maybe omitted."
# does 0 = TCP?

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))

server.listen()
print("Python server is listening on port %s" %(port))

# accept() returns BOTH
# 1) a connection (usually, different socket on another port assigned by the kernel)
# 2) address of the client
c, addr = server.accept()
print("Got connection from ", addr)

while (1):
	data = c.recv(2048).decode()
	if not data:
		break
	print ("from client:\n")
	print (str(data))

c.close()

# Sources:
# https://www.tutorialspoint.com/python/python_socket_programming.htm
