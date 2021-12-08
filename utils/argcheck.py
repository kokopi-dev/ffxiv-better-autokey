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
