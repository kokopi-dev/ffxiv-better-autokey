#!/usr/bin/env python3
"""Do not use typing for older python3 compatability"""
from utils.process import Process
from time import sleep
from utils.remap import BUTTONS
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
        print("> Looking for FFXIV PID...")
        self.process = Process()

    def do_quit(self, arg):
        return True

    def do_EOF(self, arg):
        print()
        return True

    def do_emptyline(self):
        pass

    def do_key(self, arg):
        """Requires key:str and interval:int"""
        key, interval = do_key_input_check(arg)
        if not key or interval:
            return

        if key in BUTTONS:
            key = BUTTONS[key]

        print(f"Press CTRL+C to quit.\nInterval: {interval}s")
        while True:
            try:
                print(f"> Pressing {key}")
                self.process.press_key(key)
                sleep(interval)
            except KeyboardInterrupt:
                break

    def do_craft(self, arg):
        print(f"Press CTRL+C to quit.\n")


if __name__ == "__main__":
    comm = BetterAutoKey().cmdloop()
