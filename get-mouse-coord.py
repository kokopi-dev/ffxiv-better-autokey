#!/usr/bin/python3
import pywinauto
import time
import win32api
"""
Gets mouse position by clicking any spot on your screen
"""


print('Press Ctrl-C to quit.')
try:
	while True:
		a = win32api.GetKeyState(0x01)
		if a < 0:
			x, y = win32api.GetCursorPos()
			print(x, y)
		time.sleep(0.0001)
except KeyboardInterrupt:
	print('\n')