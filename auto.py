#!/usr/bin/env python3
"""Entry point"""
from configs.config import Config
try:
    from utils.process import Process
except Exception as e:
    print("> Ran into a pywinauto debug error.")
    print(f"{e}")
    Config().general.debug_check()

from utils.process import Process
from typing import Optional
from handlers.craft import CraftHandler
from handlers.key import KeyHandler
from handlers.config import ConfigHandler
from argparsers.craft_parse import parse as craft_parse
from argparsers.config_parse import parse as config_parse
from argparsers.key_parse import parse as key_parse
from argparsers.craft import MainArgsCraft
from argparsers.config import MainArgsConfig
from argparsers.key import MainArgsKey
from pywinauto.findwindows import ElementNotFoundError
import sys
import cmd
import logging

from utils.tty_colors import PrintColor as printc
from utils.tty_colors import Colors
logging_format = "%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s"
logging.basicConfig(format=logging_format)


class BetterAutoKey(cmd.Cmd):
    intro = ("\nCommands: craft|key|process|config|help\n" +
            "Run `help [COMMAND]` for more details.\n")
    prompt = "(BetterAutoKey) "
    process: Process
    config: Config
    craft_handler: CraftHandler
    config_handler: ConfigHandler
    key_handler: KeyHandler

    def onecmd(self, line):
        try:
            return super().onecmd(line)
        except ElementNotFoundError:
            print(f"FFXIV Not Found. Attemping to rehook... FFXIV\n")
            self.process = Process()
            if self.process.app:
                self.craft_handler.set_proc(self.process)
                self.key_handler.set_proc(self.process)
            return False

    def preloop(self):
        self.process = Process()
        self.config = Config()
        self.craft_handler = CraftHandler()
        self.key_handler = KeyHandler()
        self.config_handler = ConfigHandler()
        if self.process.app:
            self.craft_handler.set_proc(self.process)
            self.key_handler.set_proc(self.process)

    def do_quit(self, arg):
        """Quit the program."""
        return True

    def do_EOF(self, arg):
        self.do_process("")
        return True

    def do_emptyline(self):
        pass

    def do_precmd(self):
        pass

    def do_process(self, arg):
        """No args: Rehook the FFXIV process.
        Single Commands:
            list: List all FFXIV processes
        Option Commands:
            name NAME: Rename the current FFXIV process
            switch PID: Switch current FFXIV processes
        """
        args = arg.split()
        if len(args) > 0:
            if self.process:
                if args[0] == "name" and len(args) > 1:
                    self.process.change_current_name(args[1:])
                elif args[0] == "list":
                    print(f"{self.process.all_pids}")
                elif args[0] == "switch" and len(args) > 1:
                    self.process.switch_pids(int(args[1]))
            return
        if not self.process.app:
            self.process.check_pid_integrity()
        else:
            printc.text(f"> {self.process.pid}", Colors.GRE)
            printc.text("> FFXIV PID is already hooked.", Colors.GRE)

    def do_config(self, arg):
        """Edit configs:
        `refresh`: Reset config to defaults
        `list`
        `buttons [craft] [repair|item|food|pot] [key]`
        """
        args: Optional[MainArgsConfig] = config_parse(arg, self.config)
        if args:
            if args.single:
                self.config_handler.commands[args.single](self.config)
            else:
                self.config_handler.update_config(self.config, args)

    def do_key(self, arg):
        """Requires key:str and interval:int.
        Ex. To open and close character menu: c,c 0.5,500
        """
        if self.process.app:
            args: Optional[MainArgsKey] = key_parse(arg, self.config)
            if args:
                self.key_handler.key_sequence(args)

    def do_craft(self, arg):
        """Single commands: list
        Main command: craft
            Options: afk=true, repair=true, food=TIME_REMAINING*, pot=TIME_REMAINING*
        * Put your time remaining in minutes. Ex. 15m left on your food: food=15
        """
        if self.process.app:
            self.config.craft.check_modified_macros()
            args: Optional[MainArgsCraft] = craft_parse(arg, self.config.craft)
            if args:
                if args.single:
                    self.craft_handler.commands[args.single](args)
                else:
                    self.craft_handler.craft(args=args, config=self.config)
        else:
            print("Could not find FFXIV process")

    def do_debug(self, arg):
        """Developer command:
        `config`: Check the current loaded .*_config.json extension files.
        """
        pass

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
