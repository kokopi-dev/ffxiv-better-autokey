#!/usr/bin/env python3
from utils.tty_colors import PrintColor as printc
from utils.tty_colors import Colors
from argparsers.config import MainArgsConfig, SingleArgsConfig, ConfigLocation, OptArgsConfig
from configs.config import Config
from typing import Optional


def parse(arg, config: Config) -> Optional[MainArgsConfig]:
    """Takes in Cmd arg format"""
    args = arg.split()
    
    # single arg
    if len(args) == 1:
        try:
            single = SingleArgsConfig(args[0])
            return MainArgsConfig(single=single)
        except ValueError:
            printc.text(f"{args[0]} is not a valid arg.", Colors.RED)
            return

    # need opt and location
    if len(args) == 4:
        try:
            opt = OptArgsConfig(args[0])
            location = ConfigLocation(args[1])
            key = args[2]
            value = args[3]
            return MainArgsConfig(
                location=location,
                opt=opt,
                key=key,
                value=value
            )
        except ValueError:
            printc.text(f"{args[0]} or {args[1]} are not a valid arg", Colors.RED)
            return

    printc.text("Not valid args were inputted. Use help config for info.", Colors.RED)
    return
