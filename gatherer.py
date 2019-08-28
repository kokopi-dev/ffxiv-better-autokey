#!/usr/bin/env python3
"""Entry point for semi-autogathering.

File arguments:
    fish: Auto spearfishes after getting first collectable menu.
    boun: Auto gathers with bountiful on gather menu.
    reduc: Auto aetherial reduction for fishes mainly.
    no args: Auto gathers on gather menu.

Setup:
    Fisher: Hotkey 1 = Gig, Hotkey 2 = Identitcal Gig, Hotkey 3 = Calm Waters,
    Hotkey 4 = Aetherial Reduction Menu
    Mining/Botany: Hotkey 1 = Bountiful II
"""
import sys
from json_editor import json_reader
from process import Process
from time import sleep


def reduction(ffxiv):
    print("  -> Pressing Aetherial Menu")
    ffxiv.press_key("4")
    sleep(0.5)
    print("  -> Pressing 0")
    ffxiv.press_key("{VK_NUMPAD0}")
    sleep(0.5)
    while True:
        print("  -> Pressing 0")
        ffxiv.press_key("{VK_NUMPAD0}")
        sleep(0.5)
        print("  -> Pressing left")
        ffxiv.press_key("{VK_NUMPAD6}")
        sleep(0.5)
        print("  -> Pressing 0")
        ffxiv.press_key("{VK_NUMPAD0}")
        sleep(4)
        print("  -> Pressing 0")
        ffxiv.press_key("{VK_NUMPAD0}")
        sleep(0.5)

def fishing(ffxiv):
    print("  -> Pressing 0")
    ffxiv.press_key("{VK_NUMPAD0}")
    sleep(0.5)
    print("  -> Pressing 0")
    ffxiv.press_key("{VK_NUMPAD0}")
    sleep(3.5)
    print("  -> Pressing Identical Gig")
    ffxiv.press_key("2")
    sleep(2)
    print("  -> Pressing Calm Waters")
    ffxiv.press_key("3")
    sleep(2.5)
    for i in range(5):
        print("  -> Pressing Gather")
        ffxiv.press_key("1")
        sleep(2)
        print("  -> Pressing 0")
        ffxiv.press_key("{VK_NUMPAD0}")
        sleep(1)
        print("  -> Pressing 0")
        ffxiv.press_key("{VK_NUMPAD0}")
        sleep(7)

def bountiful(ffxiv):
    ffxiv.press_key("{VK_NUMPAD0}")
    print("  -> Pressing 0")
    sleep(0.6)
    for i in range(6):
        ffxiv.press_key("1")
        print("  -> Pressing Bountiful")
        sleep(2)
        ffxiv.press_key("{VK_NUMPAD0}")
        print("  -> Pressing 0")
        sleep(3)

def regular(ffxiv):
    ffxiv.press_key("{VK_NUMPAD0}")
    for i in range(6):
        print("  -> Pressing 0")
        ffxiv.press_key("{VK_NUMPAD0}")
        sleep(2.5)

if __name__ == "__main__":
    json_data = json_reader()
    ffxiv = Process(json_data["process_name"])
    args = sys.argv[1:]
    if len(args) == 0:
        regular(ffxiv)
    if args[0] == "reduc":
        reduction(ffxiv)
    if args[0] == "fish":
        fishing(ffxiv)
    if args[0] == "boun":
        bountiful(ffxiv)
