#!/usr/bin/env python3
"""Entry point"""
from config import conf, buttons
from time import sleep
import sys
import cmd
import logging
from utils.argcheck import (
    create_craft_args,
    do_key_input_check,
    check_float,
    check_int
)
from handlers.craft_singles import CraftSinglesHandler
from utils.craft import Craft
from utils.fccraft import FCCraft
from utils.tty_colors import PrintColor as printc
from utils.tty_colors import Colors
logging_format = "%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s"
logging.basicConfig(format=logging_format)


class BetterAutoKey(cmd.Cmd):
    intro = ("\nCommands: craft|key|process|config|help\n" +
            "Run `help [COMMAND]` for more details.\n")
    prompt = "(BetterAutoKey) "
    process = None
    config = None
    craft_service: Craft

    def preloop(self):
        self.craft_service = Craft()
        self.do_process("") # Creating ffxiv process hook

    def do_quit(self, arg):
        """Quit the program."""
        return True

    def do_EOF(self, arg):
        print()
        return True

    def do_emptyline(self):
        pass

    def do_precmd(self):
        # check integrity of process, if it cannot find ffxiv, rehook process
        pass

    def do_process(self, arg):
        """Try to rehook FFXIV PID again."""
        args = arg.split()
        if len(args) > 0:
            if self.process:
                if args[0] == "name" and len(args) > 1:
                    self.process.change_current_name(args[1])
                elif args[0] == "list":
                    print(f"{self.process.all_pids}")
                elif args[0] == "switch" and len(args) > 1:
                    self.process.switch_pids(int(args[1]))
            return
        if not self.process or not self.process.app:
            # Importing here due to initializing a new venv debug check
            from utils.process import Process
            printc.text("> Looking for FFXIV PID...", Colors.YEL)
            self.process = Process()
        else:
            printc.text(f"> {self.process.pid}", Colors.GRE)
            printc.text("> FFXIV PID is already hooked.", Colors.GRE)

    def do_config(self, arg):
        """Edit configs:
        `sleeps [prestart|poststep|postfinish] [interval]`
        `buttons [repair|craft_item] [key]`
        `repair [threshold] [amount]`
        """
        args = arg.split()
        try:
            section, key, value = args[0], args[1], args[2]
            if len(args) != 3:
                printc.text("> Needs 2 inputs. Check `help config` for details.", Colors.RED)
                return
            if section == "sleeps":
                if not check_float("interval", value):
                    return

                check = conf.config["craft"]["sleeps"].get(key, None)
                if check:
                    conf.config["craft"]["sleeps"][key] = float(value)
            elif section == "buttons":
                check = conf.config["craft"]["opt_buttons"].get(key, None)
                if check:
                    conf.config["craft"]["opt_buttons"][key] = value
            elif section == "repair":
                if not check_int("threshold", value):
                    return
                real_key = "repair_" + key
                check = conf.config["craft"]["opt_buttons"].get(real_key, None)
                if check:
                    conf.config["craft"]["opt_buttons"][real_key] = int(value)

            print(f"> Config set: {key} to {value}.")

            # Currently, all config opts are craft opts
            conf.write_config("craft_filename", "craft")
        except:
            printc.text("Invalid input.", Colors.RED)

    def do_key(self, arg):
        """Requires key:str and interval:int"""
        keys, intervals = do_key_input_check(arg)
        if not arg or not keys or not intervals:
            return

        modded_keys = []
        valid_keys = buttons.dict()
        for k in keys:
            mod = valid_keys.get(k)
            if mod:
                modded_keys.append(mod)
            else:
                modded_keys.append(k)

        multi_interval = False
        # TODO move to interval checking function
        if len(intervals) > 1 and len(intervals) == len(keys):
            multi_interval = True
        elif len(intervals) > 1 and len(intervals) != len(keys):
            printc.text(f"> Number of keys do not match number of intervals.", Colors.RED)
            printc.text(f"> Setting interval to first interval\n", "yel")

        printc.text(f"Press CTRL+C to quit.\nInterval: {intervals} in secs", Colors.YEL)
        while True:
            try:
                for idx in range(len(modded_keys)):
                    print(f"> Pressing {modded_keys[idx]}", end="")
                    self.process.press_key(modded_keys[idx])
                    if multi_interval:
                        sleep(intervals[idx])
                        print(f" <wait.({intervals[idx]})>")
                    else:
                        sleep(intervals[0])
                        print(f" <wait.({intervals[0]})>")
            except KeyboardInterrupt:
                printc.text(f"\n> Stopping key", Colors.YEL)
                break

    def do_craft(self, arg):
        (has_changed, last_mod_config,
        macros_config, macros_dict) = conf.check_modified_macros()

        # TODO change configs to callables
        if has_changed:
            conf.config["craft"]["last_modified"] = last_mod_config
            conf.config["craft"]["macros"] = macros_config
            conf.config["craft"]["macros_list"] = macros_dict
            conf.write_config("craft_filename", "craft")

        craft_args = create_craft_args(arg, macros_dict)
        if craft_args.singles:
            for k, v in craft_args.singles.dict().items():
                if v == True:
                    command = getattr(CraftSinglesHandler, k)
                    command(macros_dict)
        elif craft_args.macro:
            self.craft_service.run(self.process, craft_args)

    def do_debug(self, arg):
        """Developer command:
        `config`: Check the current loaded .*_config.json extension files.
        """
        args = arg.split()
        try:
            command = args[0]
            if command == "config":
                print(f"{conf.config}")
        except Exception as e:
            printc.text(f"Invalid Input: {e}", Colors.RED)

    def do_update(self, arg):
        """Updates this program if there is a new update."""
        pass

    def do_fccraft(self, arg):
        args = arg.split()
        command = args[0]
        amt = int(args[1])
        if command == "pilgram":
            FCCraft.pilgram(self.process, amt)

if __name__ == "__main__":
    python_version = f"{sys.version_info[0]}.{sys.version_info[1]}"
    if float(python_version) < 3.8:
        printc.text("Please install python version 3.8+", Colors.RED)
        printc.text("Refer to the README.md of this folder to manage your python versions on windows.", Colors.RED)
    else:
        printc.text(f"> Python version detected: {python_version}", Colors.GRE)
        try:
            comm = BetterAutoKey().cmdloop()
        except KeyboardInterrupt:
            printc.text("\nRun `python auto.py` to enter the cmd again.", Colors.YEL)
