#!/usr/bin/env python3
"""Entry point"""
from time import sleep
import sys
from utils.config import BAKConfig
import cmd
import logging
from utils.argcheck import (
    do_key_input_check,
    do_craft_input_check,
    check_float,
    check_int
)
from utils.craft import Craft
from utils.tty_colors import PrintColor as printc
logging_format = "%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s"
logging.basicConfig(format=logging_format)


class BetterAutoKey(cmd.Cmd):
    intro = ("\nCommands: craft|key|process|config|help\n" +
            "Run `help [COMMAND]` for more details.\n")
    prompt = "(BetterAutoKey) "
    process = None
    config = None
    craft_service = None

    def preloop(self):
        self.config = BAKConfig()
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

    def do_process(self, arg):
        """Try to rehook FFXIV PID again."""
        if not self.process or not self.process.app:
            # Importing here due to initializing a new venv debug check
            from utils.process import Process
            printc.text("> Looking for FFXIV PID...", "yel")
            self.process = Process()
        else:
            printc.text("> FFXIV PID is already hooked.", "gre")

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
                printc.text("> Needs 2 inputs. Check `help config` for details.", "red")
                return
            if section == "sleeps":
                if not check_float("interval", value):
                    return

                check = self.config.config["craft"]["sleeps"].get(key, None)
                if check:
                    self.config.config["craft"]["sleeps"][key] = float(value)
            elif section == "buttons":
                check = self.config.config["craft"]["opt_buttons"].get(key, None)
                if check:
                    self.config.config["craft"]["opt_buttons"][key] = value
            elif section == "repair":
                if not check_int("threshold", value):
                    return
                real_key = "repair_" + key
                check = self.config.config["craft"]["opt_buttons"].get(real_key, None)
                if check:
                    self.config.config["craft"]["opt_buttons"][real_key] = int(value)

            print(f"> Config set: {key} to {value}.")

            # Currently, all config opts are craft opts
            self.config.write_config("craft_filename", "craft")
        except:
            printc.text("Invalid input.", "red")

    def do_key(self, arg):
        """Requires key:str and interval:int"""
        keys, interval = do_key_input_check(arg)
        if not keys or not interval:
            return

        modded_keys = []
        for k in keys:
            if k in self.config.buttons:
                modded_keys.append(self.config.buttons[k])
            else:
                modded_keys.append(k)

        printc.text(f"Press CTRL+C to quit.\nInterval: {interval}s", "yel")
        while True:
            try:
                for k in modded_keys:
                    print(f"> Pressing {k}")
                    self.process.press_key(k)
                    sleep(interval)
            except KeyboardInterrupt:
                printc.text(f"> Stopping key", "yel")
                break

    def do_craft(self, arg):
        """craft [OPT:delete|list] [macro_name].
        Add macro text files to the macros/ folder.
        Check the readme on repo's github for how to configure macros in detail.
        """
        # Check for modified macros before running
        (has_changed, last_mod_config,
        macros_config, macros_list) = self.config.check_modified_macros()

        if has_changed:
            self.config.config["craft"]["last_modified"] = last_mod_config
            self.config.config["craft"]["macros"] = macros_config
            self.config.config["craft"]["macros_list"] = macros_list
            self.config.write_config("craft_filename", "craft")

        command, macro_name, amt, opts = do_craft_input_check(
            arg, macros_list, self.craft_service.OPTIONS
        )

        if command == "list":
            print(f"{macros_list}")
        elif command == "craft":
            printc.text(f">>> Press CTRL+C to quit.\n", "yel")
            self.craft_service.run(self.process, self.config, macro_name, amt, opts)
            if opts and "--afk" in opts:
                self.do_key("c 500")
        # parse command arg if there is command
        # check if command arg is in macro list
        # run macro

    def do_debug(self, arg):
        """Developer command:
        `config`: Check the current loaded .*_config.json extension files.
        """
        args = arg.split()
        try:
            command = args[0]
            if command == "config":
                print(f"{self.config.config}")
        except Exception as e:
            printc.text(f"Invalid Input: {e}", "red")


if __name__ == "__main__":
    python_version = f"{sys.version_info[0]}.{sys.version_info[1]}"
    if float(python_version) < 3.8:
        printc.text("Please install python version 3.8+", "red")
        printc.text("Refer to the README.md of this folder to manage your python versions on windows.", "red")
    else:
        printc.text(f"> Python version detected: {python_version}", "gre")
        try:
            comm = BetterAutoKey().cmdloop()
        except KeyboardInterrupt:
            printc.text("\nRun `python auto.py` to enter the cmd again.", "yel")
