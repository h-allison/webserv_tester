#! /usr/bin/python3

# PYTHON CLIENT

def print_cyan(string):
	print("\033[96m{}\033[00m". format(string))

def get_ansi(color):
	
	if color == "bold":
		return "\033[1m{}\033[00m"

	if color == "cyan":
		return "\033[96m{}\033[00m"
	if color == "bold_cyan":
		return "\033[96;1m{}\033[00m"
	
	if color == "red":
		return "\033[91m {}\033[00m"
	if color == "green":
		return "\033[92m {}\033[00m"
	else:
		return "\033[00m"

def cprint(string, color):
	actual_color = get_ansi(color)
	print(actual_color.format(string))

def title_print(string, color):
	msg = ("---------------- " +
			string +
			" ---------------")
	cprint(msg, color)
	
