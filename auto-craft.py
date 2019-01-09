#!/usr/bin/python3
import time
from pywinauto.application import Application
from pywinauto.keyboard import *
"""
DEBUGGING: CHECK COMMENT BLOCKS BELOW AND MAKE SURE INPUTS ARE CORRECT
Use the example to calculate sleep time:
YOUR_MACRO_WAIT_TOTAL + 5

Example:
time.sleep(1)
MACRO_1
time.sleep(39)
MACRO_2
time.sleep(46)
...
"""


# Setup FFXIV here, change PID process=YOURNUMBER
app = Application().connect(process=3376)

# Setup sleep times accordingly, and your keystrokes
print('Press Ctrl-C to quit.')
try:
	while True:
		time.sleep(2)
		# SELECT "SYNTHESIZE"
		app.window(title='FINAL FANTASY XIV').send_keystrokes('{VK_NUMPAD0}')
		time.sleep(1)
		# PRESS "SYNTHESIZE"
		app.window(title='FINAL FANTASY XIV').send_keystrokes('{VK_NUMPAD0}')
		time.sleep(3)
		# CRAFTING MACRO 1
		app.window(title='FINAL FANTASY XIV').send_keystrokes('{VK_NUMPAD0}')
		time.sleep(39)
		# CRAFTING MACRO 2
		app.window(title='FINAL FANTASY XIV').send_keystrokes('{VK_NUMPAD0}')
		time.sleep(46)
except KeyboardInterrupt:
	print('\n')
