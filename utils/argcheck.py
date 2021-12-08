#!/usr/bin/env python3
"""Temporary arg check solution"""

def do_key_input_check(arg:str):
    args = arg.split()
    if len(args) != 2:
        print("Requires 2 inputs. key:str, interval:int")

    try:
        key, interval = args[0], int(args[1])
        return key, interval
    except:
        print("Interval needs to be an int.")

    return None, None

def do_craft_input_check(arg:str, macro_list:list):
    args = arg.split()
    commands = ["list"]
    if len(args) < 1:
        print("Requires atleast 1 input. Use craft help for details.")
        return None, None
    if args[0] not in macro_list and args[0] in commands:
        command = args[0]
        return command
    print("Wrong input. Use craft help for details.")
    return None, None
