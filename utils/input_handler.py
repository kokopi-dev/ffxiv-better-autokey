#!/usr/bin/env python3
import sys
import utils.settings as s
import utils.helpers as h


def create(args):
	if len(args) > 1:
		profile = args[1]
	else:
		profile = input(s.CREATE_MACRO)
	return profile

def delete(args):
	profile_list = h.read_json(s.PROFILES_PATH)
	if len(args) > 1:
		profile = args[1]
	else:
		print(f"Macros: {list(profile_list)}")
		profile = input()
	h.check_profile_exists(list(profile_list), profile)
	return {"profile": profile, "list": profile_list}

def craft(args):
	"""Manual input: autocraft.py craft macro1 50 -repair"""
	if len(args) > 1:
		macros = h.read_json(s.PROFILES_PATH)
		macro_name = args[1]
		h.check_profile_exists(list(macros), macro_name)
		craft_amt = args[2]
		h.check_integer(craft_amt)
		craft_amt = int(craft_amt)
		options = args[3:]
		if options != []:
			h.check_options(options)
	else:
		macros = h.read_json(s.PROFILES_PATH)
		print(f"Profiles: {list(macros)}")
		macro_name = input(s.SELECT_MACRO)
		h.check_profile_exists(list(macros), macro_name)
		craft_amt = input(s.CRAFT_AMT)
		h.check_integer(craft_amt)
		craft_amt = int(craft_amt)
		options = input(s.FLAGS_LIST).split()
		if options != []:
			h.check_options(options)
	return {"macro": macros[macro_name], "amt": craft_amt, "opt": options}