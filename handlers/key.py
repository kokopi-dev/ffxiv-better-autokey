#!/usr/bin/env python3
from handlers.base import BaseHandler
from utils.tty_colors import PrintColor as printc
from utils.tty_colors import Colors
from time import sleep
from typing import Callable, Dict
from enum import Enum
from argparsers.key import MainArgsKey


class KeyHandler(BaseHandler):
    """Handles all key commands"""
    commands: Dict[Enum, Callable] = {}

    def __init__(self):
        super().__init__()

    def key_sequence(self, args: MainArgsKey):
        printc.text(f"Press CTRL+C to quit.\nInterval: {args.intervals} in secs", Colors.YEL)
        while True:
            try:
                for idx in range(len(args.keys)):
                    print(f"> Pressing {args.keys[idx]}", end="")
                    self.proc.press_key(args.keys[idx])
                    print(f" <wait.({args.intervals[idx]})>")
                    sleep(args.intervals[idx])
            except KeyboardInterrupt:
                printc.text(f"\n> Stopping key", Colors.YEL)
                break
