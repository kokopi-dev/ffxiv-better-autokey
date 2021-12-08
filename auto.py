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
    intro = "Commands: key [KEY] [INTERVAL]"
    prompt = "(BetterAutoKey) "
    process = None
    config = None

    def preloop(self):
        print("> Initializing configs...")
        self.config = BAKConfig()
        self.do_process("")

    def do_quit(self, arg):
        return True

    def do_EOF(self, arg):
        print()
        return True

    def do_emptyline(self):
        pass

    def do_process(self, arg):
        """Rehook FFXIV PID again."""
        if not self.process or not self.process.app:
            # Importing here due to initializing a new venv debug issue
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
                break

    def do_craft(self, arg):
        """craft [OPT:edit|delete] [macro_name]"""
        print(f"Press CTRL+C to quit.\n")
        # parse command arg if there is command
        # check if command arg is in macro list
        # run macro


if __name__ == "__main__":
    comm = BetterAutoKey().cmdloop()
