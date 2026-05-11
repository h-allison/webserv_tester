#! /usr/bin/python3

import os

port = 3490
ip = 'localhost'
cwd = os.getcwd()
res_dir = cwd + "../test_resources/"

# RESOURCES
basic_html = res_dir + "basic.html"
basic_txt = res_dir + "basic.txt"
nonexistent_html = res_dir + "nonexistent.html"
