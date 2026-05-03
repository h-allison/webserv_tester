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
	
	if color == "gray":
		return "\033[90m{}\033[00m"
	if color == "red":
		return "\033[91m{}\033[00m"
	if color == "green":
		return "\033[92m{}\033[00m"
	else:
		return "\033[00m"

def cprint(string, color, end="\n"):
	ansi_color = get_ansi(color)
	print(ansi_color.format(string), end=end)

def title_print(string, color):
	msg = ("\n---------------- " +
			string +
			" ------------------------------\n")
	cprint(msg, color)

def print_test(title, request, expected, ok):
    cprint(title, "bold", end="\t")
    print(request, "... Expected =", expected, end=" ... ")
    if ok:
        cprint("OK", "green")
    else:
        cprint("FAIL","red")