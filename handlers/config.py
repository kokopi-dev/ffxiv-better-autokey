#!/usr/bin/env python3
from argparsers.config import MainArgsConfig, SingleArgsConfig, OptArgsConfig, ConfigLocation
from configs.config import Config
from configs.craft_config import CraftOptButtons
from enum import Enum
from handlers.base import BaseHandler
from typing import Callable, Dict, List
from utils.tty_colors import PrintColor as printc
from utils.tty_colors import Colors
from time import sleep
from utils.process import Process


class ConfigHandler(BaseHandler):
    """Handles all craft commands"""
    commands: Dict[Enum, Callable] = {}
    opt_commands: Dict[Enum, Callable] = {}

    def __init__(self):
        self.commands[SingleArgsConfig.listm] = self.run_listm
        super().__init__()

    def run_listm(self, config: Config):
        printc.text(f"Craft Opt Settings: {config.craft.opt_buttons}", Colors.GRE)
        printc.text(f"Craft Sleep Settings: {config.craft.sleeps}", Colors.GRE)

    def update_config(self, config: Config, args: MainArgsConfig):
        if args.opt == OptArgsConfig.buttons and args.location == ConfigLocation.craft:
            loc_data = config.craft.opt_buttons.dict()
            if args.key and args.value and loc_data.get(args.key, None):
                printc.text(f"Current Settings: {config.craft.opt_buttons}", Colors.YEL)
                new = config.craft.opt_buttons.construct(**{args.key: args.value})
                config.craft.opt_buttons = new
                printc.text(f"New Settings: {new}", Colors.GRE)
                config.craft.write_config()
            else:
                printc.text(f"{args.key} is not a valid key.", Colors.RED)
