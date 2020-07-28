#!/usr/bin/env python3
import sys
from utils.argparser import parse


def main():
    args = sys.argv[1:]
    parse(args)

if __name__ == '__main__':
    main()