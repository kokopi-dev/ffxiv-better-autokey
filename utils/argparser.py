#!/usr/bin/env python3
"""
implement later:
python main.py craft coolcraft1 50 -food -pot -repair
"""
import utils.macro as macro
COMMANDS = {
	"make": macro.make_macro,
	"delete": macro.delete_macro,
	"craft": macro.use_macro,
	"list": macro.list_macros
}


def parse(args: list):
	if not COMMANDS.get(args[0], None):
		print(f"ERROR: {args[0]} is not a command.")
	if args[0] == "craft":
		profile = macro.read_macro(args[1])
		COMMANDS[args[0]](profile, int(args[2]))
	elif len(args) > 1:
		COMMANDS[args[0]](args[1])
	else:
		COMMANDS[args[0]]()