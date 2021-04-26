#!/usr/bin/env python3
import re
import psutil
from pywinauto.application import Application
from pywinauto.keyboard import *
from utils.kb import Keyboard
import utils.autoleve_settings as asettings
from time import sleep
import sys
PROCESS_TARGET = "ffxiv_dx11.exe"
WINDOW_TITLE = "FINAL FANTASY XIV"


class Process:
    """Gets PID of PROCESS_TARGET, then hooks onto the PID on init"""
    def __init__(self):
        self.pid = self.find_pid()
        self.app = self.connect_to_pid()
        self.kbd = Keyboard()

    def find_pid(self) -> int:
        pid = None
        for p in psutil.process_iter():
            try:
                if p.name() == PROCESS_TARGET:
                    query = re.search("pid=(.+?), name=", str(p))
                    pid = int(query.group(1))
            except psutil.AccessDenied:
                # Psutil cannot read system processes like CPU, so need this exception
                pass
        return pid

    def connect_to_pid(self):
        """Returns a pywinauto Application object created with find_pid()"""
        if not self.pid:
            return f"ERROR: Could not find process name: {PROCESS_TARGET}."
        app = Application().connect(process=self.pid)
        return app

    def press_key(self, key: str):
        """Presses a key. Refer to:
        https://pywinauto.readthedocs.io/en/latest/code/pywinauto.keyboard.html
        """
        self.app.window(title=WINDOW_TITLE).send_keystrokes(key)
        
    def press_char(self, char: str):
        """Types out a char"""
        self.app.window(title=WINDOW_TITLE).send_chars(char)

    def press_tnpc_macro(self):
        """Presses key 1. Map key 1 to a macro with `/tnpc`"""
        self.press_key("1")
        self.press_key("1")

    def press_tfocus_macro(self):
        """Presses key 2. Map key 1 to a macro with `/ta <f>`"""
        self.press_key("2")
        self.press_key("2")

    def press_to_leve_menu_seq(self):
        self.press_key(self.kbd.select)
        sleep(0.8)
        self.press_key(self.kbd.select)
        sleep(0.5)
        self.press_key(self.kbd.down)
        self.press_key(self.kbd.select)
        sleep(1.2)

    def press_leve_menu_seq(self, index: int):
        sleep(0.6)
        if index == 0:
            pass
        elif index == 1:
            self.press_key(self.kbd.down)
        elif index == 2:
            self.press_key(self.kbd.down)
            sleep(0.3)
            self.press_key(self.kbd.down)
        elif index == -1:
            print("ERROR: Could not find quest in window region, check window position setting.")
        else:
            print("ERROR: Index has to be 0, 1, or 2.")
            sys.exit(1)
        self.press_key(self.kbd.select)
        sleep(1)
        self.press_key(self.kbd.select)
        sleep(0.5)
        self.press_key(self.kbd.select)
        sleep(1.3)
        self.press_key(self.kbd.esc)
        sleep(0.5)
        self.press_key(self.kbd.esc)
        sleep(1.1)

    def press_leve_quest_seq(self):
        amt = 9
        lastamt = 8
        sleep(0.1)
        self.press_key(self.kbd.select)
        sleep(1)
        self.press_key(self.kbd.select)
        if asettings.LANG == "Japanese":
            sleep(0.3)
            self.press_key(self.kbd.select)
            sleep(0.3)
            lastamt = 5
        for i in range(3):
            sleep(2.6)
            self.press_key(self.kbd.submenu)
            self.press_key(self.kbd.submenu)
            self.press_key(self.kbd.submenu)
            if i == 2:
                amt = lastamt
            for _ in range(amt):
                sleep(0.3)
                self.press_key(self.kbd.select)
        sleep(2)
