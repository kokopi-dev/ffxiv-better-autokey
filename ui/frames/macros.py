#!/usr/bin/env python3
import tkinter as tk
from tkinter import ttk
import ui.settings as s
import ui.tk_helper as tkh
import re
import utils.macro_exe as crafter


def key_check(key):
    if key == "" or len(key) != 1:
        return False
    return True

def name_check(name):
    if len(name.split()) != 1:
        return False
    return True

def check_wait(text):
    if "wait" not in text:
        return False
    return True

def parse_wait(text) -> int:
    wait = 3
    re_wait = re.compile(r"<wait.(.+?)>")
    for line in text.strip().split("\n"):
        timer = re_wait.findall(line)
        try:
            wait += int(timer[0])
        except IndexError:
            pass
    return wait

class MacrosTab:
    def __init__(self, notebook):
        self.frame = tk.Frame(notebook, bg=s.BG1)
        self.temp_frame = None
        self.mode = None
        self.target = ""

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
        self.mode = "edit"
        self.target = ""
        self.destroy_temp_frame()
        self.create_temp_frame()
        s.MACRO_LIST_MACRO_TAB = ttk.Combobox(self.temp_frame, value=list(s.MACRO_LIST))
        s.MACRO_LIST_MACRO_TAB["state"] = "readonly"
        s.MACRO_LIST_MACRO_TAB.bind("<<ComboboxSelected>>", self.load_macro)
        dropdown_l = tk.Label(self.temp_frame, text=s.MACRO_LIST_LABEL, anchor="w", bg=s.BG1, fg=s.FG1)
        tkh.place(dropdown_l, h=0.03, w=0.09, x=0, y=0.01)
        tkh.place(s.MACRO_LIST_MACRO_TAB, h="", w=0.3, x=0.09, y=0.01)
        self.create_textboxes()
        reset_b = tk.Button(self.temp_frame, text="Reset", command=lambda: self.reset_text())
        delete_b = tk.Button(self.temp_frame, text="Delete", command=lambda: self.delete_macro())
        edit_b = tk.Button(self.temp_frame, text="Edit", command=lambda: self.edit_create_macro())
        tkh.place(reset_b, h=0.05, w=0.2, x=0.25, y=0.76)
        tkh.place(edit_b, h=0.05, w=0.2, x=0.0, y=0.76)
        tkh.place(delete_b, h=0.05, w=0.2, x=0.5, y=0.76)

    def load_macro(self, e):
        macro = e.widget.get()
        self.target = macro
        data = s.MACRO_LIST[self.target]
        if data.get("key1", "") != "":
            self.key1.insert(0, data["key1"])
            self.text1.insert(tk.INSERT, data["text1"])
        if data.get("key2", "") != "":
            self.key1.insert(0, data["key2"])
            self.text1.insert(tk.INSERT, data["text2"])

    def delete_macro(self):
        if self.target != "":
            del s.MACRO_LIST[self.target]
            s.MACRO_LIST_MACRO_TAB.config(value=s.MACRO_LIST)
            crafter.write_json(s.MACRO_LIST)
            s.MACRO_LIST_MACRO_TAB.set("")
            self.clear_text()
        self.target = ""

    def edit_create_macro(self):
        if self.mode == "create":
            self.target = self.name.get()
        if not name_check(self.target):
            print("have not selected a macro name")
        else:
            data = self.get_text()
            if key_check(data["key1"]):
                data["wait1"] = parse_wait(data["text1"])
                s.MACRO_LIST[self.target] = {
                    "key1": data["key1"],
                    "wait1": data["wait1"],
                    "text1": data["text1"]
                }
            if key_check(data["key2"]):
                data["wait2"] = parse_wait(data["text2"])
                s.MACRO_LIST[self.target]["key2"] = data["key2"]
                s.MACRO_LIST[self.target]["wait2"] = data["wait2"]
                s.MACRO_LIST[self.target]["text2"] = data["text2"]
            self.clear_text()
            crafter.write_json(s.MACRO_LIST)
            s.MACRO_LIST_CRAFT_TAB.config(value=list(s.MACRO_LIST))

    def clear_text(self):
        self.key1.delete(0, "end")
        self.text1.delete("1.0", "end")
        self.key2.delete(0, "end")
        self.text2.delete("1.0", "end")

    def reset_text(self):
        self.clear_text()
        original = s.MACRO_LIST[self.target]
        self.key1.insert(0, original["key1"])
        self.text1.insert(tk.INSERT, original["text1"])
        if original.get("key2", "") != "":
            self.key2.insert(0, original["key2"])
            self.text2.insert(tk.INSERT, original["text2"])

    def create_frame(self):
        self.mode = "create"
        self.target = ""
        self.destroy_temp_frame()
        self.create_temp_frame()
        self.name = tk.Entry(self.temp_frame)
        name_l = tk.Label(self.temp_frame, text="Macro Name:", bg=s.BG1, fg=s.FG1)
        tkh.place(self.name, h="", w=0.3, x=0.15, y=0.01)
        tkh.place(name_l, h=0.03, w=0.15, x=0, y=0.01)
        self.create_textboxes()
        clear_b = tk.Button(self.temp_frame, text="Clear")
        create_b = tk.Button(self.temp_frame, text="Create", command=lambda: self.edit_create_macro())
        tkh.place(clear_b, h=0.05, w=0.2, x=0.25, y=0.76)
        tkh.place(create_b, h=0.05, w=0.2, x=0.0, y=0.76)

    def get_text(self) -> dict:
        data = {
            "key1": self.key1.get(),
            "key2": self.key2.get(),
            "text1": self.text1.get("1.0", tk.END),
            "text2": self.text2.get("1.0", tk.END)
        }
        return data

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