#!/usr/bin/env python3
import re
import psutil
from pywinauto.application import Application
from pywinauto.keyboard import *
PROCESS_TARGET = "ffxiv_dx11.exe"
WINDOW_TITLE = "FINAL FANTASY XIV"


class Process:
    """Gets PID of PROCESS_TARGET, then hooks onto the PID on init.
    Also contains key press sequences.
    """
    def __init__(self):
        self.pid = self.find_pid()
        self.app = self.connect_to_pid()

    def find_pid(self):
        pid = None
        for p in psutil.process_iter():
            try:
                if p.name() == PROCESS_TARGET:
                    query = re.search("pid=(.+?), name=", str(p))
                    pid = int(query.group(1))
                    print(f"> Found FFXIV PID: {pid}")
            except psutil.AccessDenied:
                # Psutil cannot read system processes like CPU, so need this exception
                pass
        return pid

    def connect_to_pid(self):
        """Returns a pywinauto Application object created with find_pid()"""
        if not self.pid:
            print(f"ERROR: Could not find process name: {PROCESS_TARGET}")
            return None

        try:
            app = Application().connect(process=self.pid)
            print(f"> Connected to FFXIV PID {self.pid}")
            return app
        except:
            print(f"> Could not connect to FFXIV PID {self.pid}")

        return None

    def press_key(self, key: str):
        """Presses a key. Refer to:
        https://pywinauto.readthedocs.io/en/latest/code/pywinauto.keyboard.html
        """
        self.app.window(title=WINDOW_TITLE).send_keystrokes(key)
        
    def press_char(self, char: str):
        """Types out a char"""
        self.app.window(title=WINDOW_TITLE).send_chars(char)
