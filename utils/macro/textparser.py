#!/usr/bin/env python3


def parse_wait(line):
    """Regex to find wait time on macro line
    Returns:
        Int if regex found
        None if newline
    """
    timer = s.RE_WAIT.findall(line)
    if timer != []:
        return int(timer[0])

def parse_key(line):
    """Regex to find wait time on macro line
    Returns:
        str if regex found
        None if not a KEY
    """
    check = s.RE_KEY.findall(line)
    if check != []:
        key = line.split()[1]
        return key
