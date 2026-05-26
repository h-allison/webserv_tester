#! /usr/bin/python3
import os
from pathlib import Path

script_path = Path(__file__)
script_dir = script_path.parent

webserv = str(script_dir.parent.parent / "webserv")
configs = str(script_dir.parent / "test_configs") + "/"
configs_parsing = str(script_dir.parent / "test_configs/parsing") + "/"
configs_networking_init = str(script_dir.parent / "test_configs/networking_init") + "/"
configs_get = str(script_dir.parent / "test_configs/get") + "/"
logs = str(script_dir.parent / "logs")

port = "8080"
