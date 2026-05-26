#! /usr/bin/python3
import os
import sys

# my files
import defines
import color
import test_parsing
import test_networking_init
import test_get
import test_index_generation
import test_autoindex
import test_cgi

def print_logo():
	logo_path = os.path.join(defines.script_dir, '.logo.txt')
	file = open(logo_path)
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
	error += test_parsing.launcher()
	error += test_networking_init.launcher()
	error += test_get.launcher()
	error += test_autoindex.launcher()
	error += test_index_generation.launcher()
	error += test_cgi.launcher()
	if error == 0:
		print("\nCongratulations! All tests passed.")
	else:
		sys.exit(1)

# means only run main() if the script is executed directly as opposed to imported as a module
if __name__=="__main__":
	main()
