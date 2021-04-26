#!/usr/bin/env python3
import sys
import utils.settings as s
import utils.helpers as h


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

def leve(*args, **kwargs):
    """This input acts as a check before running the leve loop"""
    print("Is Eirikur your current target?")
    print("Is Moyce your focus target?")
    print("Do you have key 1 and key 2 with the correct macros?")
    confirm = input("Enter anything to continue... ")
    amt = int(input(" > How many leves? (1-100) "))
    if 0 < amt < 100:
        return amt
    else:
        print("ERROR: Choose 1-100")
        sys.exit(1)
