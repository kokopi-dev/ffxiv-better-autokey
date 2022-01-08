#!/usr/bin/env python3
from typing import List, Dict, Optional
from utils.tty_colors import PrintColor as printc
from utils.tty_colors import Colors
from pydantic import BaseModel
"""Temporary arg check solution"""


class CraftOptArgs(BaseModel):
    repair: Optional[bool]
    afk: Optional[bool]
    pot: Optional[int]
    food: Optional[int]

class CraftSingleArgs(BaseModel):
    listm: Optional[bool]

class CraftArgs(BaseModel):
    macro: Optional[str]
    amt: Optional[int]
    opts: Optional[CraftOptArgs]
    singles: Optional[CraftSingleArgs]
    opts_amt: int = 0

def create_craft_args(arg, macro_dict: Dict) -> CraftArgs:
    """Return None if error occured, prints a message if error"""
    valid_single_args = CraftSingleArgs.schema()["properties"]
    valid_opt_args = CraftOptArgs.schema()["properties"]
    args = arg.split()

    if len(args) == 0:
        printc.text("Need commands, run 'help craft' for info.", Colors.RED)

    opt_result = {}
    single_result = {}
    macro = None
    amt = None
    for a in args:
        pair = a.split("=")
        if len(pair) == 1:
            filename = a if ".txt" in a else a + ".txt"
            if filename in macro_dict:
                macro = filename
            elif valid_single_args.get(a):
                single_result[a] = True
            elif macro and a.isdigit():
                amt = a
        elif len(pair) == 2:
            if pair[0] not in valid_opt_args:
                printc.text(f"{pair} is not a valid option.", Colors.RED)
            else:
                opt_result[pair[0]] = pair[1]
        else:
            printc.text(f"{a} not a valid arg, run 'help craft' for info.", Colors.RED)

    try:
        singles = None if single_result == {} else CraftSingleArgs(**single_result)
        opts = None if opt_result == {} else CraftOptArgs(**opt_result)
        craft_args = CraftArgs(
            macro=macro,
            amt=amt,
            opts=opts,
            singles=singles,
            opts_amt=len(opt_result)
        )
    except Exception as e:
        printc.text(f"{e}", Colors.RED)
        craft_args = CraftArgs(**{})

    if not craft_args.singles and not craft_args.macro:
        printc.text("No commands ran. Use 'help craft' for more info.", Colors.RED)
    if not craft_args.macro:
        printc.text(f"Could not find macro {args[0]}.", Colors.RED)

    return craft_args

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
