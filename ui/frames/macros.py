#!/usr/bin/env python3
import tkinter as tk
from tkinter import ttk
import ui.settings as s
import ui.tk_helper as tkh

class MacrosTab:
    def __init__(self, notebook):
        self.frame = tk.Frame(notebook, bg=s.BG1)
        self.temp_frame = None

    def create_temp_frame(self):
        self.temp_frame = tk.Frame(self.frame, bg=s.BG1, padx=10, pady=10)
        tkh.place(self.temp_frame, h=1, w=1, x=0, y=0)

    def destroy_temp_frame(self):
        self.temp_frame.destroy()

    def edit_or_create(self):
        self.create_temp_frame()
        create_b = tk.Button(self.temp_frame, text="Create Macro", command=lambda: self.create_frame())
        tkh.place(create_b, h=0.05, w=0.3, x=0.15, y=0.2)
        edit_b = tk.Button(self.temp_frame, text="Edit Macro", command=lambda: self.edit_frame())
        tkh.place(edit_b, h=0.05, w=0.3, x=0.55, y=0.2)

    def edit_frame(self):
        self.destroy_temp_frame()
        self.create_temp_frame()
        s.MACRO_LIST_MACRO_TAB = ttk.Combobox(self.temp_frame, value=s.MACRO_LIST)
        s.MACRO_LIST_MACRO_TAB["state"] = "readonly"
        s.MACRO_LIST_MACRO_TAB.bind("<<ComboboxSelected>>", self.check_macro)
        dropdown_l = tk.Label(self.temp_frame, text=s.MACRO_LIST_LABEL, anchor="w", bg=s.BG1, fg=s.FG1)
        tkh.place(dropdown_l, h=0.03, w=0.09, x=0, y=0.01)
        tkh.place(s.MACRO_LIST_MACRO_TAB, h="", w=0.3, x=0.09, y=0.01)
        self.create_textboxes()
        reset_b = tk.Button(self.temp_frame, text="Reset")
        edit_b = tk.Button(self.temp_frame, text="Edit")
        tkh.place(reset_b, h=0.05, w=0.2, x=0.25, y=0.76)
        tkh.place(edit_b, h=0.05, w=0.2, x=0.0, y=0.76)

    def check_macro(self, e):
        macro = e.widget.get()
        print(macro)

    def delete_macro(self):
        s.MACRO_LIST_MACRO_TAB.config(value=s.MACRO_LIST)

    def edit_create_macro(self):
        pass

    def clear_text(self):
        pass

    def create_frame(self):
        self.destroy_temp_frame()
        self.create_temp_frame()
        self.name = tk.Entry(self.temp_frame)
        name_l = tk.Label(self.temp_frame, text="Macro Name:", bg=s.BG1, fg=s.FG1)
        tkh.place(self.name, h="", w=0.3, x=0.15, y=0.01)
        tkh.place(name_l, h=0.03, w=0.15, x=0, y=0.01)
        self.create_textboxes()
        clear_b = tk.Button(self.temp_frame, text="Clear")
        create_b = tk.Button(self.temp_frame, text="Create")
        tkh.place(clear_b, h=0.05, w=0.2, x=0.25, y=0.76)
        tkh.place(create_b, h=0.05, w=0.2, x=0.0, y=0.76)

    def create_textboxes(self):
        self.key1 = tk.Entry(self.temp_frame)
        tkh.place(self.key1, h="", w=0.05, x=0.15, y=0.09)
        key1_l = tk.Label(self.temp_frame, text="Macro 1 Key:", bg=s.BG1, fg=s.FG1)
        tkh.place(key1_l, h=0.03, w=0.15, x=0, y=0.09)
        self.text1 = tk.Text(self.temp_frame)
        tkh.place(self.text1, h=0.57, w=0.4, x=0, y=0.16)
        self.key2 = tk.Entry(self.temp_frame)
        tkh.place(self.key2, h="", w=0.05, x=0.58, y=0.09)
        key2_l = tk.Label(self.temp_frame, text="Macro 2 Key:", bg=s.BG1, fg=s.FG1)
        tkh.place(key2_l, h=0.03, w=0.15, x=0.43, y=0.09)
        self.text2 = tk.Text(self.temp_frame)
        tkh.place(self.text2, h=0.57, w=0.4, x=0.43, y=0.16)