#!/usr/bin/env python3
import tkinter as tk
from tkinter import ttk
import ui.settings as s
import ui.tk_helper as tkh
import utils.macro_exe as crafter
from time import sleep
import multiprocessing as m


class CraftTab:
    def __init__(self, notebook):
        self.frame = tk.Frame(notebook, padx=10, pady=10, bg=s.BG1)
        self.craft_check = False
        self.init_vars()
        self.init_displays()
        self.init_entries()
        self.init_dropdowns()
        self.init_buttons()
        if type(s.FFXIV.app) == str:
            self.display1["text"] = self.ffxiv.app
        else:
            self.display1["text"] = s.CONNECTED

    def init_vars(self):
        self.collect_flag = tk.IntVar()
        self.status = tk.IntVar()

    def input_checker(self, data):
        try:
            temp = int(data["amt"])
            data["amt"] = temp
        except ValueError:
            self.display2["text"] = s.ERR_CRAFT_AMT
            return False
        return True

    def clear_display(self):
        self.display1["text"] = ""
        self.display2["text"] = ""

    def init_displays(self):
        self.display1 = tk.Label(self.frame, bg=s.BG2, fg=s.FG1)
        self.display2 = tk.Label(self.frame, bg=s.BG2, fg=s.FG1)
        tkh.place(self.display1, h=0.05, w=1, x=0, y=0)
        tkh.place(self.display2, h=0.05, w=1, x=0, y=0.05)

    def init_entries(self):
        self.craft_amt = tk.Entry(self.frame)
        self.craft_amt_l = tk.Label(self.frame, text=s.CRAFT_AMT_LABEL, anchor="w", bg=s.BG1, fg=s.FG1)
        tkh.place(self.craft_amt_l, h=0.03, w=0.15, x=0, y=0.29)
        tkh.place(self.craft_amt, h="", w=0.05, x=0.15, y=0.29)

    def init_dropdowns(self):
        s.MACRO_LIST_CRAFT_TAB = ttk.Combobox(self.frame, value=list(s.MACRO_LIST))
        s.MACRO_LIST_CRAFT_TAB["state"] = "readonly"
        self.macro_list_l = tk.Label(self.frame, text=s.MACRO_LIST_LABEL, anchor="w", bg=s.BG1, fg=s.FG1)
        tkh.place(self.macro_list_l, h=0.03, w=0.09, x=0, y=0.2)
        tkh.place(s.MACRO_LIST_CRAFT_TAB, h="", w=0.3, x=0.09, y=0.2)

    def init_buttons(self):
        self.craft_b = tk.Button(self.frame, text="Craft", bg=s.B1, command=lambda: self.exec_craft())
        self.collect_cb = tk.Checkbutton(self.frame, text="Collectable",
                                        variable=self.collect_flag,
                                        anchor="w", activebackground=s.BG1, activeforeground=s.FG1, bg=s.BG1, fg=s.FG1, selectcolor="black")
        tkh.place(self.collect_cb, h=0.08, w=0.2, x=0, y=0.1)
        tkh.place(self.craft_b, h=0.07, w=0.3, x=0.02, y=0.37)

    def create_flags(self) -> dict:
        flags = {
            "collect": False
        }
        temp = self.collect_flag.get()
        if temp == 1:
            flags["collect"] = True
        return flags

    def exec_craft(self):
        self.display2["text"] = ""
        data = {}
        amt = self.craft_amt.get()
        data["amt"] = amt
        name = s.MACRO_LIST_CRAFT_TAB.get()
        data["macro"] = s.MACRO_LIST[name]
        craft_check = self.input_checker(data)
        if craft_check:
            flags = self.create_flags()
            total_time = crafter.get_time_estimation(data["macro"], data["amt"])
            p1 = m.Process(target=crafter.use_macro, args=(data["macro"], data["amt"], flags))
            p1.start()
            p1.join()
            self.display2["text"] = f"{data['amt']} crafts finished."
        self.collect_cb.deselect()