#!/usr/bin/env python3
"""
implement later:
python main.py craft coolcraft1 50 -food -pot -repair
"""
import utils.autocrafter_funcs as func
import sys
COMMANDS = {
	"craft": func.use_macro,
	"create": func.create_macro,
	"delete": func.delete_macro,
	"list": func.list_macros
}


def parse(args: list):
	if len(args) == 0:
		print("ERROR: Please enter a command.")
		sys.exit()
	elif not COMMANDS.get(args[0], None):
		print(f"ERROR: {args[0]} is not a command.")
		sys.exit()
	else:
		COMMANDS[args[0]](args)