#!/usr/bin/env python3

def place(tk_obj, h, w, x, y, a=""):
    """Place order: relheight, relwidth, relx, rely.
    Wrapper for helping make the code more readable.
    Positions can be skipped with empty str.
    """
    if a != "":
        return tk_obj.place(relheight=h, relwidth=w, relx=x, rely=y, anchor=a)
    return tk_obj.place(relheight=h, relwidth=w, relx=x, rely=y)