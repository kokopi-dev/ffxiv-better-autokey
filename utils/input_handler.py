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
	if len(args) > 1:
		profile = args[1]
	else:
		print(f"Macros: {list(s.PROFILES)}")
		profile = input()
	h.check_profile_exists(profile)
	return {"profile": profile}

def craft(args):
	"""Manual input: autocraft.py craft macro1 50 -repair"""
	if len(args) > 1:
		macro_name = args[1]
		h.check_profile_exists(macro_name)
		craft_amt = args[2]
		h.check_integer(craft_amt)
		craft_amt = int(craft_amt)
		options = args[3:]
		if options != []:
			h.check_options(options)
	else:
		print(f"Profiles: {list(s.PROFILES)}")
		macro_name = input(s.SELECT_MACRO)
		h.check_profile_exists(macro_name)
		craft_amt = input(s.CRAFT_AMT)
		h.check_integer(craft_amt)
		craft_amt = int(craft_amt)
		options = input(s.FLAGS_LIST).split()
		if options != []:
			h.check_options(options)
	return {"macro": s.PROFILES[macro_name], "amt": craft_amt, "opt": options}