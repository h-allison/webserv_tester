#! /usr/bin/python3
import os
from pathlib import Path

script_path = Path(__file__)
script_dir = script_path.parent

"""
cwd = os.getcwd()
webserv = cwd.removesuffix("/webserv_tester/tests") + "/webserv"
configs = cwd.removesuffix("/tests") + "/test_configs/"
configs_parsing = cwd.removesuffix("/tests") + "/test_configs/parsing/"
configs_networking_init = cwd.removesuffix("/tests") + "/test_configs/networking_init/"
configs_get = cwd.removesuffix("/tests") + "/test_configs/get/"
"""

webserv = str(script_dir.parent.parent / "webserv")
configs = str(script_dir.parent / "test_configs") + "/"
configs_parsing = str(script_dir.parent / "test_configs/parsing") + "/"
configs_networking_init = str(script_dir.parent / "test_configs/networking_init") + "/"
configs_get = str(script_dir.parent / "test_configs/get") + "/"

port = "8080"
