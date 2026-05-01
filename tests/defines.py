#! /usr/bin/python3
import os

cwd = os.getcwd()
webserv = cwd.removesuffix("/webserv_tester/tests") + "/webserv"
configs = cwd.removesuffix("/tests") + "/test_configs/"
port = "8080"