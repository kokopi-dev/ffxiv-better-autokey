#!/usr/bin/env python3
"""
implement later:
python main.py craft coolcraft1 50 -food -pot -repair
"""
import utils.autocrafter_funcs as func
import sys
import utils.settings as s
COMMANDS = {
    "craft": func.use_macro,
    "list": func.list_macros,
    "leve": func.auto_leve,
}


def parse(args: list):
    if len(args) == 0:
        sys.stderr.write(s.ERROR_ENTRY_0)
        sys.exit()
    elif not COMMANDS.get(args[0], None):
        sys.stderr.write(s.ERROR_ENTRY_1.format(args[0]))
        sys.exit()
    else:
        COMMANDS[args[0]](args)
