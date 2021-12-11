#!/usr/bin/env python3
"""Entry point"""
from time import sleep
from utils.config import BAKConfig
import cmd
import logging
from utils.argcheck import (
    do_key_input_check,
    do_craft_input_check,
    do_config_input_check
)
from utils.craft import Craft
logging_format = "%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s"
logging.basicConfig(format=logging_format)


class BetterAutoKey(cmd.Cmd):
    intro = "\nCommands: craft|key|process|help\nRun `[COMMAND] help` for more details.\n"
    prompt = "(BetterAutoKey) "
    process = None
    config = None

    def preloop(self):
        self.config = BAKConfig()
        self.do_process("") # Creating ffxiv process hook

    def do_quit(self, arg):
        """Quit the program."""
        breakpoint()
        return True

    def do_EOF(self, arg):
        print()
        return True

    def do_emptyline(self):
        pass

    def do_process(self, arg):
        """Rehook FFXIV PID again."""
        if not self.process or not self.process.app:
            # Importing here due to initializing a new venv debug check
            from utils.process import Process
            print("> Looking for FFXIV PID...")
            self.process = Process()

    def do_config(self, arg):
        """Edit configs."""
        keys, value = do_config_input_check(arg)
        if keys and value:
            self.config.config_nested_keys_set(keys, value)
            self.config.write_config("craft_filename", "craft")

    def do_key(self, arg):
        """Requires key:str and interval:int"""
        key, interval = do_key_input_check(arg)
        if not key or not interval:
            return

        if key in self.config.buttons:
            key = self.config.buttons[key]

        print(f"Press CTRL+C to quit.\nInterval: {interval}s")
        while True:
            try:
                print(f"> Pressing {key}")
                self.process.press_key(key)
                sleep(interval)
            except KeyboardInterrupt:
                print(f"> Stopping key")
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

        command, macro_name, amt = do_craft_input_check(arg, macros_list)

        if command == "list":
            print(f"{macros_list}")
        elif command == "craft":
            print(f">>> Press CTRL+C to quit.\n")
            Craft.run(self.process, self.config, macro_name, amt)
        # parse command arg if there is command
        # check if command arg is in macro list
        # run macro


if __name__ == "__main__":
    try:
        comm = BetterAutoKey().cmdloop()
    except KeyboardInterrupt:
        print("\nRun `python auto.py` to enter the cmd again.")
