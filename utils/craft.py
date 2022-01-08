#!/usr/bin/env python3
"""Crafting related functionalities"""
import os
from pathlib import PurePath
from time import sleep
import re
from typing import Optional, List
from utils.argcheck import CraftArgs
from utils.tty_colors import PrintColor as printc
from utils.tty_colors import Colors
from utils.craft_options import CraftOpts
from config import conf, buttons, opt_buttons



class Craft:
    def __init__(self):
        self.OPTIONS = CraftOpts

    def _estimate_time_completion(self, amt:int, macro) -> float:
        result = 0
        sleep_buffers = sum(list(conf.config["craft"]["sleeps"].values()))
        step_sleep = sum(macro["wait"])
        result = amt * (sleep_buffers + step_sleep)
        return result / 60 # in minutes

    def run(self, proc, args: CraftArgs):
        prestart = conf.config["craft"]["sleeps"]["prestart"]
        poststep = conf.config["craft"]["sleeps"]["poststep"]
        postfinish = conf.config["craft"]["sleeps"]["postfinish"]

        name = str(PurePath(conf.craft_folder, args.macro))
        macro = conf.config["craft"]["macros"][name]

        count = 1
        run_opts = False

        printc.text(f">>> Press CTRL+C to quit.\n", Colors.YEL)

        if args.opts_amt > 0:
            run_opts = True
            print(f">>> Options selected: {args.opts.schema().keys()}")

        if not args.amt:
            printc.text(f">>> Amount not specified, running until CTRL+C is pressed.", Colors.YEL)
        else:
            print(f">>> Amount specified: {args.amt} crafts.")
            est = self._estimate_time_completion(args.amt, macro)
            print(f">>> Estimated completion time: {est:.2f}m")

        print(f">>> Using macro: {name}")
        while True:
            try:
                if run_opts == True:
                    for k, v in args.opts.dict().items():
                        opt_func = getattr(self.OPTIONS, k)
                        opt_func(proc, count)

                if args.amt and count > args.amt:
                    printc.text(">> Crafts finished.", Colors.GRE)
                    break

                print(f"> Craft #{count}")
                for _ in range(4):
                    proc.press_key(buttons.select)
                sleep(prestart) # sleep prestart

                for step in range(len(macro["keys"])):
                    key, wait = macro["keys"][step], macro["wait"][step]
                    print(f">> Pressing {key}")
                    proc.press_key(key)
                    print(f">> Waiting {wait}s")
                    sleep(wait + poststep) # sleep + select padding
                count += 1
                sleep(postfinish) # sleep post craft finish
            except KeyboardInterrupt:
                print("> Stopping craft")
                break
