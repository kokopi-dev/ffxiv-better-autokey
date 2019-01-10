#!/usr/bin/python3
"""
DEBUGGING: CHECK COMMENT BLOCKS BELOW AND MAKE SURE INPUTS ARE CORRECT
Use the example to calculate sleep time:
YOUR_MACRO_WAIT_TOTAL + 5

Example:
time.sleep(1)
MACRO_1
time.sleep(39)
MACRO_2
...
"""
import json
import os
import sys
import psutil
import re
import time
from pywinauto.application import Application
from pywinauto.keyboard import *


# Intro
current_path = os.path.dirname(os.path.abspath(__file__))
# Opening json data file to read
with open(("%s/ffxiv-autocraft_data.json" % current_path), "r") as time_data:
	macro_time = json.load(time_data)
# Dsiplaying current macro timers
m_list = [macro_time["m1"], macro_time["m2"], macro_time["m3"], macro_time["m4"]]
print("The current macro timers are:\n")
print("M1\tM2\tM3\tM4")
print(*m_list, sep='\t')

# argc, argv
argv = sys.argv[1:]
argc = len(argv)

# argument checker
if argc > 1:
	print("  <Error: Too many arguments (must be one).>")
	sys.exit()

if argc == 1 and sys.argv[1] != "edit":
	print("  <Error: %s command not found.>" % sys.argv[1])

editor = ""
editedCount = 0
# Editing macro timers
try:
	if sys.argv[1] == "edit":
		editor = "y"
		while editor == "y":
			print("\nFormat example: m1 35")
			print("Which macro timer do you want to edit?")
			editThis = input()
		
			if editThis == "":
				print("  <Error: input cannot be none, try again.>")
				sys.exit()

			try:
				mtime = int(editThis[3:])
				m = editThis[:2]
			except:
				print("Wrong format.\nFormat example: m1 35")
				sys.exit()

			if editThis[2] != ' ':
				print("Wrong format.\nFormat example: m1 35")
				sys.exit()
			if m[0] != 'm':
				print("Wrong format.\nFormat example: m1 35")
				sys.exit()
			if mtime < 0 or mtime > 300:
				print("Wrong format.\nFormat example: m1 35\nTime limit is 300")
				sys.exit()

			# Temp adding to json
			with open("%s/ffxiv-autocraft_data.json" % current_path) as add_time_data:
				add_time = json.load(add_time_data)

			print("  ... editing requested macro timer.")
			add_time[m] = mtime

			# Saving to json
			with open(("%s/ffxiv-autocraft_data.json" % current_path), "w") as save_time_data:
				json.dump(add_time, save_time_data)
			# Rereading json
			with open(("%s/ffxiv-autocraft_data.json" % current_path), "r") as time_data:
				macro_time = json.load(time_data)
				print("  ... saving data...rereading data...done.")

			# Increment times edited
			editedCount += 1

			# continue or exit
			print("\nDo you want to edit another macro timer? (y/n)")
			editor = input()
			if editor == "y":
				pass
			elif editor == "n":
				print("  ... Program will continue to auto craft")
				break
			else:
				print(" <Error: input needs to be 'y' or 'n'.>")
				sys.exit()
except IndexError:
	pass

# Displaying new timers if edited
if editedCount > 0:
	m_list = [macro_time["m1"], macro_time["m2"], macro_time["m3"], macro_time["m4"]]
	print("\nThe new macro timers are:\n")
	print("M1\tM2\tM3\tM4")
	print(*m_list, sep='\t')

# Task Manager -> Right click FFXIV -> Go to details
process_name = "ffxiv_dx11.exe"

# AUTO PID
for proc in psutil.process_iter():
    if proc.name() == process_name:
        findingPID = re.search('pid=(.+?), name=', str(proc))
        ffxiv_pid = int(findingPID.group(1))

if not findingPID:
	print("  <Error: Process name not found, try changing it.>")
	sys.exit()

# If auto PID doesnt work, then add process manually `connect(process=1234)`
app = Application().connect(process=ffxiv_pid)

# Setup sleep times accordingly, and your keystrokes
print('\nPress Ctrl-C to quit crafting.')
try:
	while True:
		time.sleep(2)
		# SELECT "SYNTHESIZE"
		app.window(title='FINAL FANTASY XIV').send_keystrokes('{VK_NUMPAD0}')
		print("  ... Selecting the button 'Synthesize'.")
		time.sleep(3)
		# PRESS "SYNTHESIZE"
		app.window(title='FINAL FANTASY XIV').send_keystrokes('{VK_NUMPAD0}')
		print("  ... Pressing the button 'Synthesize'.")
		time.sleep(3)
		# CRAFTING MACRO 1
		app.window(title='FINAL FANTASY XIV').send_keystrokes('1')
		print("  ... Pressing macro 1 ... <wait.{:d}>.".format(macro_time["m1"]))
		time.sleep(macro_time["m1"])
		# CRAFTING MACRO 2
		app.window(title='FINAL FANTASY XIV').send_keystrokes('2')
		print("  ... Pressing macro 2 ... <wait.{:d}>.".format(macro_time["m2"]))
		time.sleep(macro_time["m2"])
except KeyboardInterrupt:
	print("Program has stopped.")
