#!/usr/bin/env python3

from datetime import datetime

import sys
import time

print('HI! This is the script running', file=sys.stderr)
print("Content-Type: text/plain")
print()
print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

print("abc")
