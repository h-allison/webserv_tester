#! /usr/bin/python3
import os

cwd = os.getcwd()
webserv = cwd.removesuffix("/webserv_tester/tests") + "/webserv"
configs = cwd.removesuffix("/tests") + "/test_configs/"
configs_parsing = cwd.removesuffix("/tests") + "/test_configs/parsing/"
configs_networking_init = cwd.removesuffix("/tests") + "/test_configs/networking_init/"
configs_get = cwd.removesuffix("/tests") + "/test_configs/get/"
port = "8080"