#!/usr/bin/env python3
"""Entry point for autocraft"""
import sys
from utils.argparser import parse
import utils.helpers as h
import utils.conf.settings as s


def main():
    h.setup()
    s.PROFILES = h.read_json(s.PROFILES_PATH)
    s.LOGS = h.read_json(s.LOGS_PATH)
    h.scan_macros()
    args = sys.argv[1:]
    parse(args)

if __name__ == '__main__':
    main()
