#!/usr/bin/env python3
import sys
import os
import subprocess
from utils.process import Process
from utils.autoleve_settings import LANG, WINDOW_POS
import base64


def _find_jp(out: list) -> int:
    idx = 0
    indicators = {"大", "！", "キ", "!"}
    print(out)
    for quest in out:
        if any(indicator in quest for indicator in indicators):
            return idx
        idx += 1
    return -1

def _find_en(out: list) -> int:
    return max(enumerate(out), key=lambda x: len(x[1]))[0]

def get_quest_index() -> int:
    path = os.path.join("utils", "Capture2Text_v4.6.2_64bit", "Capture2Text", "Capture2Text_CLI.exe")
    command = f' --screen-rect "{WINDOW_POS}" -l {LANG} --b'
    pipe = subprocess.Popen((path + command), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out = pipe.communicate()[0].decode("utf-8").split("\n")
    if LANG == "English":
        return _find_en(out)
    elif LANG == "Japanese":
        return _find_jp(out)
    else:
        print("ERROR: Language not selected.")

if __name__ == "__main__":
    pass
