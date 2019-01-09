#!/usr/bin/python3
import psutil
import re
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


# Task Manager -> Right click FFXIV -> Go to details
process_name = "ffxiv_dx11.exe"

# AUTO PID
for proc in psutil.process_iter():
    if proc.name() == process_name:
        findingPID = re.search('pid=(.+?), name=', str(proc))
        ffxiv_pid = int(findingPID.group(1))

if not findingPID:
    print('Error: Process name not found, try changing it.')

# If auto PID doesnt work, then add process manually `connect(process=1234)`
app = Application().connect(process=ffxiv_pid)

# Setup sleep times accordingly, and your keystrokes
print('Press Ctrl-C to quit crafting.')
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