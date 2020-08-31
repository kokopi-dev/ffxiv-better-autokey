#!/usr/bin/env python3
import sys
from utils.argparser import parse
import utils.helpers as h
import utils.settings as s


def main():
    s.PROFILES = h.read_json(s.PROFILES_PATH)
    h.setup()
    h.refresh_timestamps()
    args = sys.argv[1:]
    parse(args)

if __name__ == '__main__':
    main()