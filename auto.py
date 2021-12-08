#!/usr/bin/env python3
"""Do not use typing for older python3 compatability"""
from time import sleep
from utils.config import BAKConfig
import cmd
import os
import logging
from utils.argcheck import do_key_input_check, do_craft_input_check
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
        """craft [OPT:delete|list] [macro_name]"""
        # Check for modified macros before running
        (has_changed, last_mod_config,
        macros_config, macros_list) = self.config.check_modified_macros()

        if has_changed:
            self.config.config["craft"]["last_modified"] = last_mod_config
            self.config.config["craft"]["macros"] = macros_config
            self.config.config["craft"]["macros_list"] = macros_list
            # write new configs
            self.config.write_config("craft_filename", "craft")

        command, macro_name = do_craft_input_check(arg, macros_list)

        if command == "list":
            print(f"{macros_list}")
        elif command == "craft":
            print(f">>> Press CTRL+C to quit.\n")
            buttons = self.config.buttons
            name = os.path.join(self.config.craft_folder, macro_name)
            macro = self.config.config["craft"]["macros"][name]
            amt = 5
            count = 0
            print(f">>> Using macro: {name}")
            while True:
                try:
                    if amt and count > amt:
                        break
                    for _ in range(4):
                        self.process.press_key(buttons["select"])
                    # sleep
                    for step in range():
                        pass
                    count += 1
                except KeyboardInterrupt:
                    print("> Stopping craft")
                    break
        else:
            return
        # parse command arg if there is command
        # check if command arg is in macro list
        # run macro


if __name__ == "__main__":
    try:
        comm = BetterAutoKey().cmdloop()
    except KeyboardInterrupt:
        print("\nRun python auto.py to enter the cmd again.")
