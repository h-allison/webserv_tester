#! /usr/bin/python3
import os
import parsing_tests

# my files
import defines
import color

def print_logo():
	file = open(".logo.txt")
	content = file.read()
	print(content)
	file.close()

def file_exists():
	if not os.path.isfile(defines.webserv):
		color.cprint("No executable found at \"" + defines.webserv + "\"", "red")
		color.cprint("Did you remember to run make?", "red")
		return False
	return True

def main():
	error = 0
	print_logo()
	if file_exists() == False:
		return 0
	error += parsing_tests.launcher()
	if error == 0:
		print("\nCongratulations! All tests passed.")
	return 0

if __name__=="__main__":
	main()
