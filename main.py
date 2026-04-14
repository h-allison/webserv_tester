#! /usr/bin/python3

def print_logo():
	file = open(".logo.txt")
	content = file.read()
	print(content)
	file.close()

error = 0
error += parsing_tests_launcher()
print_logo()
if error == 0:
	print("Congratulations! All tests passed.")
