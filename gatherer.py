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


class AutoGather:
    def __init__(self, arg):
        self.ffxiv = self.setup()
        if self.ffxiv:
            self.autogather(arg)
        else:
            print("Error: Could not find json_data.")

    def setup(self):
        json_data = json_reader()
        ffxiv = None
        if json_data:
            ffxiv = Process(json_data["process_name"])
        return ffxiv

    def reduction(self):
        print("  -> Pressing Aetherial Menu")
        self.ffxiv.press_key("4")
        sleep(0.5)
        print("  -> Pressing 0")
        self.ffxiv.press_key("{VK_NUMPAD0}")
        sleep(0.5)
        while True:
            print("  -> Pressing 0")
            self.ffxiv.press_key("{VK_NUMPAD0}")
            print("  -> Pressing left")
            self.ffxiv.press_key("{VK_NUMPAD6}")
            sleep(0.2)
            print("  -> Pressing 0")
            self.ffxiv.press_key("{VK_NUMPAD0}")
            sleep(3.5)
            print("  -> Pressing 0")
            self.ffxiv.press_key("{VK_NUMPAD0}")
            sleep(0.5)
        quit()

    def fishing_reg(self):
        for i in range(6):
            print("  -> Pressing Gather")
            self.ffxiv.press_key("1")
            sleep(9)

    def fishing(self):
        print("  -> Pressing 0")
        self.ffxiv.press_key("{VK_NUMPAD0}")
        sleep(0.5)
        print("  -> Pressing 0")
        self.ffxiv.press_key("{VK_NUMPAD0}")
        sleep(3.5)
        print("  -> Pressing Identical Gig")
        self.ffxiv.press_key("2")
        sleep(2)
        print("  -> Pressing Calm Waters")
        self.ffxiv.press_key("3")
        sleep(2.5)
        for i in range(6):
            print("  -> Pressing Gather")
            self.ffxiv.press_key("1")
            sleep(2)
            print("  -> Pressing 0")
            self.ffxiv.press_key("{VK_NUMPAD0}")
            sleep(1)
            print("  -> Pressing 0")
            self.ffxiv.press_key("{VK_NUMPAD0}")
            sleep(7)
        quit()

    def bountiful(self):
        self.ffxiv.press_key("{VK_NUMPAD0}")
        print("  -> Pressing 0")
        sleep(0.6)
        for i in range(6):
            self.ffxiv.press_key("1")
            print("  -> Pressing Bountiful")
            sleep(2)
            self.ffxiv.press_key("{VK_NUMPAD0}")
            print("  -> Pressing 0")
            sleep(3)
        quit()

    def regular(self):
        self.ffxiv.press_key("{VK_NUMPAD0}")
        for i in range(6):
            print("  -> Pressing 0")
            self.ffxiv.press_key("{VK_NUMPAD0}")
            sleep(2.5)
        quit()

    def autogather(self, arg):
        if arg == ["spear"]:
            self.fishing_reg()
        if arg == ["fish"]:
            self.fishing()
        if arg == ["reduc"]:
            self.reduction()
        if arg == ["boun"]:
            self.bountiful()
        if arg == []:
            self.regular()

if __name__ == "__main__":
    arg = sys.argv[1:]
    autogather = AutoGather(arg)
