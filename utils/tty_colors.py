#!/usr/bin/env python3
from collections import defaultdict
from colorama import init
init()

class PrintColor:
    colors = defaultdict(None, {
        "reset": "\033[0m",
        "yel": "\033[33m",
        "gre": "\033[32m",
        "red": "\033[31m"
    })

    @staticmethod
    def text(msg, color, bold=False):
        b = "" if not bold else ";1"
        print(f"{PrintColor.colors[color]}{b}{msg}{PrintColor.colors['reset']}")
