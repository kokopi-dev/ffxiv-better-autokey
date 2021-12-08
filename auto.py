#!/usr/bin/env python3
"""Do not use typing for older python3 compatability"""
from time import sleep
from utils.config import BAKConfig
import cmd
import logging
from utils.argcheck import do_key_input_check
logging_format = "%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s"
logging.basicConfig(format=logging_format)


class BetterAutoKey(cmd.Cmd):
    intro = "\nCommands: craft|key|process|help\nRun [COMMAND] help for more details.\n"
    prompt = "(BetterAutoKey) "
    process = None
    config = None

    def preloop(self):
        self.config = BAKConfig()
        print("> Initialized configs...")
        self.do_process("")

    def do_quit(self, arg):
        """Quit the program."""
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

    def do_key(self, arg):
        """Requires key:str and interval:int"""
        key, interval = do_key_input_check(arg)
        if not key or not interval:
            return

        if key in self.config.buttons_remap:
            key = self.config.buttons_remap[key]

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
        """craft [OPT:delete|list] [macro_name]"""
        print(f"Press CTRL+C to quit.\n")

        # Check for modified macros before running
        has_changed, last_mod_config, macros_config = self.config.check_modified_macros()
        if has_changed:
            self.config.config["craft"]["last_modified"] = last_mod_config
            self.config.config["craft"]["macros"] = macros_config
            # write new configs
            self.config.write_config("craft_filename", "craft")
        # parse command arg if there is command
        # check if command arg is in macro list
        # run macro


if __name__ == "__main__":
    try:
        comm = BetterAutoKey().cmdloop()
    except KeyboardInterrupt:
        print("\nRun python auto.py to enter the cmd again.")
