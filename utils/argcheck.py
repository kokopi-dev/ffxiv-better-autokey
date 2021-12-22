#!/usr/bin/env python3
from typing import List, Dict
"""Temporary arg check solution"""


def check_float(name, value):
    try:
        value = float(value)
        return value
    except ValueError:
        print(f"> {name} specified needs to be a float (ex. 1.0).")
        return None

def check_int(name, value):
    try:
        value = int(value)
        return value
    except ValueError:
        print(f"> {name} specified needs to be a number (ex. 5).")
        return None

def do_key_input_check(arg:str):
    args = arg.split()
    if len(args) != 2:
        print("Requires 2 inputs. key, interval (seconds)")

    try:
        keys, interval = args[0].split(","), float(args[1])
        return keys, interval
    except:
        print("Interval needs to be an int or float.")

    return None, None

def do_craft_input_check(arg: str, macro_list: List, options: Dict):
    """Return: (str|None, str|None, int|None)"""
    args = arg.split()
    amt = None
    commands = ["list"]
    opts = []
    if len(args) < 1:
        print("Requires atleast 1 input. Use craft help for details.")
        return None, None, None, None

    # One of the commands
    if args[0] not in macro_list and args[0] in commands:
        command = args[0]
        return command, None, amt, opts

    # Formatting
    if ".txt" not in args[0]:
        idx = macro_list.index((args[0] + ".txt"))
    else:
        idx = macro_list.index(args[0])

    # Amount detected
    if len(args) > 1:
        try:
            amt = int(args[1])
        except:
            print("Amt needs to be a number.")
            return None, None, None, opts

    if len(args) > 2:
        opts = args[2:]
        for item in opts:
            if item not in options:
                if "--" not in item:
                    print(f"Try using --{item} instead of {item}.")
                else:
                    print(f"{item} is not an option.")
                return None, None, None, []
    
    if idx != None:
        return "craft", macro_list[idx], amt, opts

    print("Wrong input. Use craft help for details.")
    return None, None, None, opts
