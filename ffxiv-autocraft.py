#!/usr/bin/python3
"""
Use the example to calculate sleep time:
YOUR_MACRO_WAIT_TOTAL + 5

You can manually edit the timers and keystrokes
in the .json file
"""
import os
import sys
import re
import time
from functions.json_exec import JsonExec
from functions.format_checker import FormatCheck
from functions.process_exec import ProcessExec

# This is the name of the json dictionary
json_file = "ffxiv-autocraft_data.json"

# Reading json file to use and display timers/keystroke info
json_data = JsonExec.reading_from_json(json_file)

#############
### Intro ###
#############
# Displaying current macro timers
m_list = [json_data["m1"], json_data["m2"], json_data["m3"], json_data["m4"]]
print("The current macro timers are:\n")
print("m1\tm2\tm3\tm4")
print(*m_list, sep='\t')
# Displaying current keystrokes
k_list = [json_data["k1"], json_data["k2"], json_data["k3"], json_data["k4"], json_data["k5"]]
print("\nThe current keystrokes are:\n")
print("k1\tk2\tk3\tk4\tk5")
print(*k_list, sep='\t')

# argc, argv
argv = sys.argv[1:]
argc = len(argv)

# argument checker
acceptedArguments = ["edit", "editkeys", "editprocess", "autobuff"]
if argc > 1:
    print("  <Error: Too many arguments (must be one).>")
    sys.exit()

if argc == 1 and sys.argv[1] not in acceptedArguments:
    print("  <Error: {:s} command not found.>".format(sys.argv[1]))
    sys.exit()

editor = ""
editedTimerCount = 0
editedKeyCount = 0
editedProcessCount = 0
try:
    # EDITING MACRO TIMERS
    if sys.argv[1] == "edit":
        editor = "y"
        while editor == "y":
            print("\nFormat example: m1 35")
            # User input
            editThis = input("Which macro timer do you want to edit?\n")

            # Format checker for macro timer on user input
            editThis = FormatCheck.timer_format(editThis)

            # Splitting input
            temp_list = FormatCheck.input_splitter(editThis)
            m = temp_list[1]
            mtime = temp_list[0]

            # Returns a variable that allows adding to json file
            add_timer = JsonExec.adding_to_json(json_file)

            # Adding user input's timer to json dictionary
            add_timer[m] = mtime
            print("  ... editing requested macro timer.")

            # Saving to json using the above 'add_this'
            JsonExec.saving_to_json(json_file, add_timer)

            # Rereading json
            json_data = JsonExec.reading_from_json(json_file)
            print("  ...rereading data...done.")

            # Increment times edited
            editedTimerCount += 1

            # Continue or exit
            acceptedOptions = ["y", "n"]
            editor = input("\nDo you want to edit another macro timer? (y/n)\n")
            while editor not in acceptedOptions:
                print("  ... You need to input 'y' or 'n' only.")
                editor = input("\nDo you want to edit another macro timer? (y/n)\n")

            if editor == "n":
                print("  ... Program will continue to auto craft")
                break
    # EDITING KEYS
    if sys.argv[1] == "editkeys":
        editor = "y"
        while editor == "y":
            print("\nFormat example: k1 1")
            # User input
            editThis = input("Which keystroke do you want to edit?\n")
            print()

            # Format checker for keystrokes on user input
            editThis = FormatCheck.keystroke_checker(editThis)

            # Splitting input into keys and keystrokes
            temp_list = FormatCheck.input_splitter(editThis)
            k = temp_list[1]
            kstroke = temp_list[0]

            # Returns a variable that allows adding to json file
            add_key = JsonExec.adding_to_json(json_file)

            # Adding user input's keystroke to json dictionary
            add_key[k] = kstroke
            print("  ... editing requested keystrokes.")

            # Saving to json using the above 'add_key'
            JsonExec.saving_to_json(json_file, add_key)

            # Rereading json
            json_data = JsonExec.reading_from_json(json_file)
            print("  ...rereading data...done.")

            # Increment times edited
            editedKeyCount += 1

            # Continue or exit
            acceptedOptions = ["y", "n"]
            editor = input("\nDo you want to edit another keystroke? (y/n)\n")
            while editor not in acceptedOptions:
                print("  ... You need to input 'y' or 'n' only.")
                editor = input("\nDo you want to edit another keystroke? (y/n)\n")
                
            if editor == "n":
                print("  ... Program will continue to auto craft")
                break
            
    # EDITING PROCESS NAME
    if sys.argv[1] == "editprocess":
        editor = "y"
        while editor == "y":
            print("\nProcess name should end with a '.exe'")
            # User input for new process name
            editThis = input("Enter your new process name:\n")

            # Format check for new process name
            editThis = FormatCheck.processname_checker(editThis)

            # Returns a variable that allows adding to json file
            add_process = JsonExec.adding_to_json(json_file)

            # Saving to json using the above 'add_key'
            JsonExec.saving_to_json(json_file, add_process)

            add_process["process_name"] = editThis
            print("  ... editing requested process name.")

            # Rereading json
            json_data = JsonExec.reading_from_json(json_file)
            print("  ...rereading data...done.")

            # Increment times edited
            editedProcessCount += 1

            # Continue or exit
            acceptedOptions = ["y", "n"]
            editor = input("\nDo you want to re-edit the process name? (y/n)\n")
            while editor not in acceptedOptions:
                print("  ... You need to input 'y' or 'n' only.")
                editor = input("\nDo you want to re-edit the process name? (y/n)\n")
                
            if editor == "n":
                print("  ... Program will continue to auto craft")
                break

    # AUTO FOOD POT OPTION
    if sys.argv[1] == "autobuff":
        editor = "y"
        while editor == "y":
            # User input for food and pot timers, and if there is an extender buff on
            foodBuff = input("\nEnter your current food buff timer in minutes:\n")
            potBuff = input("\nEnter your current pot timer in minutes:\n")
            extenderBuff = input("\nDo you have a 10m food timer extender buff on? (y/n):\n")

            # y/n format checker, passes to auto_craft_buff()
            acceptedOptions = ["y", "n"]
            while extenderBuff not in acceptedOptions:
                print("  ... You need to input 'y' or 'n' only.")
                extenderBuff = input("\nDo you have a 10m food timer extender buff on? (y/n):\n")

            # Format checker for both food and pot timers
            temp_list = FormatCheck.autobuff_checker( [foodBuff, potBuff] )

            # Splitting food and pot after checking format
            foodBuff = temp_list[0]
            potBuff = temp_list[1]

            # Calculating when to execute auto food and auto pot
            print("  ... Calculating food and pot timers.")
            foodBufft = (foodBuff * 60) - 40
            potBufft = (potBuff * 60) - 40
            print("  ... Your food buff will wear off in {:d} seconds".format(foodBufft))
            print("  ... Your pot buff will wear off in {:d} seconds".format(potBufft))
            print("  ... Proceeding to craft.")

            # Process name: editable through program arugment `editprocess`
            process_name = json_data["process_name"]

            # AUTO PID: Returns the PID of process
            ffxiv_pid = ProcessExec.auto_pid(process_name)

            # Connecting to process's PID
            opened_process = ProcessExec.connect_process(ffxiv_pid)

            # Auto Craft Loop w/ Auto Buff: takes in connected process and json dict
            # Tracks food and pot timers with foodBufft and potBufft
            # Tracks if extenderBuff is 'y' or 'n'
            print('\nPress Ctrl-C to quit crafting.')
            try:
                ProcessExec.auto_craft_buff(opened_process, json_data, foodBufft, potBufft, extenderBuff)
            except KeyboardInterrupt:
                print("Program has stopped.")
                sys.exit()
except IndexError:
    pass

# Displaying new timers if edited
if editedTimerCount > 0:
    m_list = [json_data["m1"], json_data["m2"], json_data["m3"], json_data["m4"]]
    print("\nThe new macro timers are:\n")
    print("m1\tm2\tm3\tm4")
    print(*m_list, sep='\t')

# Displaying new timers if edited
if editedKeyCount > 0:
    k_list = [json_data["k1"], json_data["k2"], json_data["k3"], json_data["k4"], json_data["k5"]]
    print("\nThe new keystrokes are:\n")
    print("k1\tk2\tk3\tk4\tk5")
    print(*k_list, sep='\t')

# Displaying new process if edited
if editedProcessCount > 0:
    print("The new process is {:s}".format(json_data["process_name"]))

# Process name: editable through program arugment `editprocess`
process_name = json_data["process_name"]

# AUTO PID: Returns the PID of process
ffxiv_pid = ProcessExec.auto_pid(process_name)

# Connecting to process's PID
opened_process = ProcessExec.connect_process(ffxiv_pid)

# Auto Craft Loop: takes in connected process and json dict
print('\nPress Ctrl-C to quit crafting.')
try:
    ProcessExec.auto_craft(opened_process, json_data)
except KeyboardInterrupt:
    print("Program has stopped.")
    sys.exit()
