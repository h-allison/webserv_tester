#! /usr/bin/python3

"""
PYTHON SERVER using socketserver Module

This is an another simple python server, which I am also using to quickly read
requests sent by the 42 tester. It uses the somewhat more complicated
socketserver Module instead of socket
"""

import socketserver
	
"""
MyTCPHandler is a request handler class for our server,
which will be instantiated once per connection.
It overrides the handle() method.

The handler can be used to receive data a couple ways:
	1) self.request = TCP socket connected to client
	2) self.rfile = "file-like" stream object

More info: https://docs.python.org/3/library/socketserver.html
	
"""

class MyTCPHandler(socketserver.BaseRequestHandler):


	def handle(self):
		
		msg = [b'']
		chunk = [b'']
		total_bytes_read = 0
		while b'\r\n\r\n' not in msg[-1] and total_bytes_read < 10_000:
			chunk = self.request.recv(2048)
			print("Received:\n\n", chunk, "\n\n")
			msg.append(chunk)
			total_bytes_read += len(msg[-1])
			# I am not sure about the use of -1 here
			# TODO why does it get stuck here?
			# Doesn't recognize that \r\n\r\n is now in msg, or not appending properly
		self.data = b''.join(msg)
		print("Full message:\n\n", self.data.decode("utf-8"), "\n\n")
		self.request.sendall(self.data.upper())
		# send something back to the client
		# can't just send back a string, requires a "bytes-like object"

if __name__ == "__main__":
	HOST, PORT = "localhost", 8082

with socketserver.TCPServer((HOST, PORT), MyTCPHandler) as server:
	server.serve_forever()

# Sources:
# https://www.tutorialspoint.com/python/python_socket_programming.htm
# https://docs.python.org/3/library/socketserver.html