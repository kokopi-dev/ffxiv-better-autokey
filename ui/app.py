#!/usr/bin/env python3
import tkinter as tk
from tkinter import ttk
import ui.settings as s
from ui.frames.craft import CraftTab
from ui.frames.macros import MacrosTab
import utils.macro_exe as crafter
from utils.process import Process
s.MACRO_LIST = crafter.read_json()
s.FFXIV = Process()


class App:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title(s.TITLE)
        self.root.geometry(f"{s.W_HEIGHT}x{s.W_WIDTH}")
        self.root.minsize(s.W_HEIGHT, s.W_WIDTH)
        self.init_notebook()
        self.root.mainloop()

    def selected_tab(self, e):
        tab = e.widget.index(e.widget.select())
        if tab == 0:
            if self.macro_f.temp_frame:
                self.macro_f.destroy_temp_frame()
        if tab == 1:
            self.macro_f.edit_or_create()

    def init_notebook(self):
        self.notebook = ttk.Notebook(self.root)
        self.craft_f = CraftTab(self.notebook)
        self.macro_f = MacrosTab(self.notebook)
        self.notebook.add(self.craft_f.frame, text="Craft")
        self.notebook.add(self.macro_f.frame, text="Macros")
        self.notebook.pack(expand=1, fill="both")
        self.notebook.bind("<<NotebookTabChanged>>", self.selected_tab)
