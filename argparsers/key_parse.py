#!/usr/bin/env python3
from utils.tty_colors import PrintColor as printc
from utils.tty_colors import Colors
from argparsers.key import MainArgsKey
from configs.config import Config
from typing import List


def parse(arg: str, config: Config):
    """Takes in Cmd format"""
    args = arg.split()

    if len(args) != 2:
        printc.text("Only 2 inputs required: keys and intervals. Ex: c,c 0.5,5", Colors.RED)
        return
    
    keys: List = args[0].split(",")
    intervals_str: List = args[1].split(",")

    # check intervals are floats
    try:
        intervals = [float(i) for i in intervals_str]
    except Exception as e:
        printc.text(f"{intervals_str} -> All intervals need to be a number", Colors.RED)
        printc.text(f"{e}", Colors.RED)
        return

    # modify keys if needed
    filtered_keys = []
    buttons = config.buttons.dict()
    for k in keys:
        match = buttons.get(k)
        if match:
            filtered_keys.append(match)
        else:
            filtered_keys.append(k)

    result = MainArgsKey(keys=filtered_keys, intervals=intervals)
    return result
