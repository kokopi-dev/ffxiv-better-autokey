#!/usr/bin/env python3
from collections import defaultdict
from colorama import init
from dataclasses import dataclass
init()

@dataclass
class Colors:
    RESET: str = "\033[0m"
    YEL: str = "\033[33m"
    GRE: str = "\033[32m"
    RED: str = "\033[31m"

class PrintColor:
    """Namespace for PrintColor"""

    @staticmethod
    def text(msg: str, color: str, bold=False):
        """Prints a colored text to stdout.
        Check tty_colors.Colors for a list of colors.
        """
        b = "" if not bold else ";1"
        print(f"{color}{b}{msg}{Colors.RESET}")

if __name__ == "__main__":
    pass
