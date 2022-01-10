#!/usr/bin/env python3
from argparsers.craft import OptArgsCraft, SingleArgsCraft, MainArgsCraft
from configs.config import Config
from enum import Enum
from handlers.base import BaseHandler
from typing import Callable, Dict, List
from utils.tty_colors import PrintColor as printc
from utils.tty_colors import Colors
from time import sleep
from utils.process import Process

class CraftOptsHandler:
    """Namespace for craft opt functions"""
    @staticmethod
    def repair(proc: Process, args: MainArgsCraft, config: Config, count: int):
        if count % config.craft.opt_buttons.repair_threshold == 0:
            print("> Repairing...", end="")
            buttons = config.buttons
            opt_buttons = config.craft.opt_buttons
            sequence = [
                buttons.esc,
                opt_buttons.repair,
                buttons.left,
                buttons.select,
                buttons.left,
                buttons.select,
                buttons.esc
            ]
            for key in sequence:
                proc.press_key(key)
                sleep(0.6)
            sleep(3) # repair animation
            proc.press_key(opt_buttons.craft_item) # craft item button
            print("done.")

    @staticmethod
    def food(proc: Process, args: MainArgsCraft, config: Config, count: int):
        pass

    @staticmethod
    def pot(proc: Process, args: MainArgsCraft, config: Config, count: int):
        pass

    @staticmethod
    def afk(proc: Process, args: MainArgsCraft, config: Config, count: int):
        if args.amt < count:
            printc.text(">> Crafts have finished, starting afk sequence. CTRL+C to quit:", Colors.GRE)
            try:
                while True:
                    print("> Pressing c,c <wait.(500)>")
                    proc.press_key("c")
                    sleep(0.3)
                    proc.press_key("c")
                    sleep(500)
            except KeyboardInterrupt:
                printc.text("> Stopping afk", Colors.YEL)
                raise KeyboardInterrupt # break craft sequence

class CraftHandler(BaseHandler):
    """Handles all craft commands"""
    commands: Dict[Enum, Callable] = {}
    opt_commands: Dict[Enum, Callable] = {}

    def __init__(self):
        self.commands[SingleArgsCraft.listm] = self.run_listm
        self.opt_commands[OptArgsCraft.repair] = CraftOptsHandler.repair
        self.opt_commands[OptArgsCraft.food] = CraftOptsHandler.food
        self.opt_commands[OptArgsCraft.pot] = CraftOptsHandler.pot
        self.opt_commands[OptArgsCraft.afk] = CraftOptsHandler.afk
        super().__init__()

    def run_listm(self, args: MainArgsCraft):
        if args.macros_dict:
            print(f"{list(args.macros_dict)}")

    def craft(self, args: MainArgsCraft, config: Config):
        def _estimate_time_completion(amt:int, macro) -> float:
            result = 0
            sleep_buffers = sum(config.craft.sleeps.dict().values())
            step_sleep = sum(macro["wait"])
            result = amt * (sleep_buffers + step_sleep)
            return result / 60 # in minutes

        def _print_opt_messages(opts: List[OptArgsCraft], config: Config) -> None:
            for a in opts:
                printc.text(f"> Options selected: {a.name}", Colors.GRE)
                if a.name == "repair":
                    printc.text(f">> Repair keys:", Colors.YEL)
                    printc.text(f">>> Repair: {config.craft.opt_buttons.repair}", Colors.YEL)
                    printc.text(f">>> Craft Item Key: {config.craft.opt_buttons.craft_item}", Colors.YEL)
                if a.name == "food":
                    printc.text(f">> Food Key: {config.craft.opt_buttons.food}", Colors.YEL)
                if a.name == "pot":
                    printc.text(f">> Pot Key: {config.craft.opt_buttons.pot}", Colors.YEL)

        # START
        count = 1
        printc.text(f">>> Press CTRL+C to quit.\n", Colors.YEL)
        if args.opts:
            _print_opt_messages(args.opts, config)

        if not args.amt:
            printc.text(f">>> Amount not specified, running until CTRL+C is pressed.", Colors.YEL)
        else:
            print(f">>> Amount specified: {args.amt} crafts.")
            est = _estimate_time_completion(args.amt, args.macro)
            print(f">>> Estimated completion time: {est:.2f}m")

        print(f">>> Using macro: {args.macro_name}")

        while True:
            try:
                if args.opts:
                    for o in args.opts:
                        self.opt_commands[o](
                            proc=self.proc,
                            args=args,
                            config=config,
                            count=count
                        )

                if args.amt and count > args.amt:
                    printc.text(">> Crafts finished.", Colors.GRE)
                    break

                print(f"> Craft #{count}")
                for _ in range(4):
                    self.proc.press_key(config.buttons.select)
                sleep(config.craft.sleeps.prestart) # sleep prestart

                for step in range(len(args.macro["keys"])):
                    key, wait = args.macro["keys"][step], args.macro["wait"][step]
                    print(f">> Pressing {key}")
                    self.proc.press_key(key)
                    print(f">> Waiting {wait}s")
                    sleep(wait + config.craft.sleeps.poststep) # sleep + select padding
                count += 1
                sleep(config.craft.sleeps.postfinish) # sleep post craft finish
            except KeyboardInterrupt:
                print("> Stopping craft")
                break