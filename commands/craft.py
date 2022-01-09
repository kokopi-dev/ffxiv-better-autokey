#!/usr/bin/env python3
"""Models for identifying and containing craft args"""
from enum import Enum
from pydantic import BaseModel
from typing import List, Optional, Dict


class CraftSingles(Enum):
    """Single arg commands, args with opts are in Args class."""
    listm = "list"

class CraftOpts(Enum):
    """Optional arg commands"""
    repair = "repair"
    afk = "afk"
    food = "food"
    pot = "pot"

class CraftArgs(BaseModel):
    """Main args container"""
    macro_name: Optional[str]
    macro_file: Optional[str]
    amt: int = 0
    opts_amt: int = 0
    singles: Optional[List[CraftSingles]] = None
    opts: Optional[List[CraftOpts]] = None

def parse(arg, macro_dict: Dict) -> Optional[CraftArgs]:
    """Takes in Cmd arg format"""
    args = arg.split()
    # check singles then return
    if len(args) == 1:
        singles = CraftSingles(args[0])
        if command:
            return CraftArgs(singles=singles)
    # find macro, then check amt, then get opts
    if len(args) > 0:
        macro = macro_dict.get(args[0], None)
        if not macro:
            print(f"{args[0]} not in macros/")
            return
        name = args[0] if ".txt" not in args[0] else args[0].replace(".txt", "")
        filename = args[0] if ".txt" in args[0] else args[0] + ".txt"
    result = CraftArgs(macro_name=name, macro_file=filename)
    if len(args) > 1:
        if args[1].isdigit():
            amt = int(args[1])
        else:
            amt = 0
        result.amt = amt
    idx = 2
    if amt != 0 and len(args) > 2:
        idx = 3
    opt_args = args[idx:]
    if len(opt_args) > 0:
        pass
            
if __name__ == "__main__":
    # craft parse return Args
    arg = "craft 80dura 5"
    breakpoint()
