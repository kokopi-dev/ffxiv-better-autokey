#!/usr/bin/env python3
from utils.process import Process

class BaseHandler:
    proc: Process

    def set_proc(self, proc: Process):
        self.proc = proc
