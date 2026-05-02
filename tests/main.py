#! /usr/bin/python3
import os
import sys

# my files
import defines
import color
import parsing_tests
import networking_init_tests
import get_tests

def print_logo():
	file = open(".logo.txt")
	content = file.read()
	print(content)
	file.close()

def file_exists():
	if not os.path.isfile(defines.webserv):
		color.cprint("No executable found at \"" + defines.webserv + "\"", "red")
		color.cprint("Did you forget to build webserv?", "red")
		return False
	return True

def main():
	error = 0
	print_logo()
	if file_exists() == False:
		sys.exit(1)
	error += parsing_tests.launcher()
	error += networking_init_tests.launcher()
	error += get_tests.launcher()
	if error == 0:
		print("\nCongratulations! All tests passed.")
	else:
		sys.exit(1)

# means only run main() if the script is executed directly as opposed to imported as a module
if __name__=="__main__":
	main()
