#!/usr/bin/env python3
from utils.tty_colors import PrintColor as printc
from utils.tty_colors import Colors
from argparsers.craft import MainArgsCraft, SingleArgsCraft, OptArgsCraft
from configs.craft_config import CraftConfig
from typing import Optional


def parse(arg, config: CraftConfig) -> Optional[MainArgsCraft]:
    """Takes in Cmd arg format"""
    def get_name_and_filename(name):
        name = args[0] if ".txt" not in args[0] else args[0].replace(".txt", "")
        filename = args[0] if ".txt" in args[0] else args[0] + ".txt"
        return name, filename

    macro = None
    args = arg.split()

    # if singles then return
    if len(args) == 1:
        # check if macro
        name, filename = get_name_and_filename(args[0])
        macro = config.macros.macros.get(filename, None)
        if not macro:
            try:
                single = SingleArgsCraft(args[0])
                return MainArgsCraft(
                    single=single,
                    macros_dict=config.macros.macros,
                )
            except ValueError:
                printc.text(f"{args[0]} is not a valid arg", Colors.RED)
                return

        return MainArgsCraft(macro_name=name, macro_file=filename, macro=macro)

    # check for macro
    if len(args) > 0 and not macro:
        name, filename = get_name_and_filename(args[0])
        macro = config.macros.macros.get(filename, None)
        if not macro:
            printc.text(f"{args[0]} not in macros/", Colors.RED)
            return

    # check for amt
    result = MainArgsCraft(macro_name=name, macro_file=filename, macro=macro)
    amt = 0
    if len(args) > 1:
        if args[1].isdigit():
            amt = int(args[1])
        result.amt = amt

    # check for opts
    idx = 1
    if amt != 0 and len(args) > 2:
        idx = 2
    opt_args = args[idx:]
    if len(opt_args) == 0:
        return result

    if len(opt_args) > 0:
        for o in opt_args:
            pair = o.split("=")
            if len(pair) != 2:
                printc.text(f"> {o} is an incorrect option format or not an option", Colors.RED)
                return
            try:
                op = OptArgsCraft(pair[0])
                if result.opts:
                    result.opts.append(op)
                else:
                    result.opts = [op]
            except ValueError:
                printc.text(f"> {o} is not an option", Colors.RED)
                return

            try:
                if op == OptArgsCraft.food:
                    result.food_count = int(pair[1])
                elif op == OptArgsCraft.pot:
                    result.pot_count = int(pair[1])
            except ValueError:
                printc.text(f"> {pair[0]}: {pair[1]} needs to be a number", Colors.RED)
                return

    return result
