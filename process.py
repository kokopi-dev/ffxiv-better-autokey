#!/usr/bin/env python3
import re
import psutil
from pywinauto.application import Application
from pywinauto.keyboard import *

class Process:
    """Data related to Windows processes."""

    def __init__(self, process_input):
        self.process_name = process_input
        self.process_pid = self.find_pid()
        self.app = self.connect_process()

    def find_pid(self):
        """Finds the PID of the process name.

        Returns:
            pid (int): The PID of the process name.
        """
        pid = None
        for process in psutil.process_iter():
            if process.name() == self.process_name:
                searcher = re.search("pid=(.+?), name=", str(process))
                pid = int(searcher.group(1))
        return pid

    def connect_process(self):
        app = None
        try:
            app = Application().connect(process=self.process_pid)
        except:
            print("  -> ERROR: Process not found. Change process name with json_editor.py.")
            quit()
        return app

    def press_key(self, key):
        """Presses the key given"""
        ffxiv = self.app
        ffxiv.window(title="FINAL FANTASY XIV").send_keystrokes(key)
