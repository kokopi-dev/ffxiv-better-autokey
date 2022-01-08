#!/usr/bin/env python3
from typing import List, Dict
from utils.tty_colors import PrintColor as printc
from utils.tty_colors import Colors
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
        keys, intervals = args[0].split(","), [float(i) for i in args[1].split(",")]
        return keys, intervals
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

    filename = args[0] if ".txt" in args[0] else args[0] + ".txt"
    # One of the commands
    if filename not in macro_list and args[0] in commands:
        command = args[0]
        return command, None, amt, opts

    if filename not in macro_list:
        printc.text(f"{args[0]} is not in macros folder.", Colors.RED)
        return None, None, None, None

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
    
    idx = macro_list.index(filename)

    if idx != None:
        return "craft", macro_list[idx], amt, opts

    print("Wrong input. Use craft help for details.")
    return None, None, None, opts
