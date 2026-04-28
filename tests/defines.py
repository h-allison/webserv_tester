#! /usr/bin/python3
import os

cwd = os.getcwd()
webserv = cwd.removesuffix("/unit_tests/tests") + "/webserv"
configs = cwd.removesuffix("/tests") + "/test_configs/"
