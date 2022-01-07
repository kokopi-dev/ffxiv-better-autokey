#!/usr/bin/env python3
"""Handling all process related info"""
import re
import psutil
from pywinauto.application import Application
from pywinauto.keyboard import *
from utils.tty_colors import PrintColor as printc
from typing import Optional, List
from pydantic import BaseModel
PROCESS_TARGET = "ffxiv_dx11.exe"
WINDOW_TITLE = "FINAL FANTASY XIV"

class PID(BaseModel):
    id: int

class Process:
    """Gets PID of PROCESS_TARGET, then hooks onto the PID on init.
    Also contains key press sequences.
    """
    pid: Optional[int]
    app: Application
    all_pids: List

    def __init__(self):
        self.pid = self.find_pid()
        self.app = self.connect_to_pid()
        self.all_pids = []

    def find_pid(self):
        pid = None
        for p in psutil.process_iter():
            try:
                if p.name() == PROCESS_TARGET:
                    query = re.search("pid=(.+?), name=", str(p))
                    print(query)
                    pid = int(query.group(1))
                    printc.text(f"> Found FFXIV PID: {pid}", "gre")
            except psutil.AccessDenied:
                # Psutil cannot read system processes like CPU, so need this exception
                pass

        breakpoint()
        return pid

    def connect_to_pid(self):
        """Returns a pywinauto Application object created with find_pid()"""
        if not self.pid:
            printc.text(f"ERROR: Could not find process name: {PROCESS_TARGET}", "red")
            return None

        try:
            app = Application().connect(process=self.pid)
            printc.text(f"> Connected to FFXIV PID {self.pid}", "gre")
            return app
        except Exception as e:
            printc.text(f"> Could not connect to FFXIV PID {self.pid}", "red")
            printc.text(f"> {e}", "red")

        return None

    def press_key(self, key: str):
        """Presses a key. Refer to:
        https://pywinauto.readthedocs.io/en/latest/code/pywinauto.keyboard.html
        """
        self.app.window(title=WINDOW_TITLE).send_keystrokes(key)
        
    def press_char(self, char: str):
        """Types out a char"""
        self.app.window(title=WINDOW_TITLE).send_chars(char)
