#!/usr/bin/env python3
"""Edits the json keys"""
import json

def json_reader():
    try:
        with open("settings.json", "r") as f:
            data = json.load(f)
            return data
    except FileNotFoundError:
        return None

def json_writer(key, value, data):
    data[key] = value
    with open("settings.json", "w+") as f:
        json.dump(data, f)
    return data

def value_checker(key, value, data):
    data_keys = list(data)
    int_value_key_list = ["m1", "m2", "m3", "m4"]
    int_value = None

    if key not in data_keys:
        print("    -> Incorrect key name, check the key list and restart the json_editor.")
        quit()

    for i in int_value_key_list:
        if i == key:
            try:
                int_value = int(value)
                return int_value
            except ValueError:
                print("    -> A timer needs to be a number. Restart the json_editor.py.")
                quit()

if __name__ == "__main__":
    print("Editing settings.json...")
    print("  -> Type quit whenever to quit.")
    print("  -> (Note) Macro timer calculator: (total <wait>) + (5)\n")

    json_data = json_reader()

    if json_data != None:
        user_input = None
        json_keys = list(json_data)
        while True:
            print("What do you want to change? (Type in a key listed below)")
            user_input = input("{}\n".format(json_keys))
            if user_input in json_keys:
                print("  -> What do you want to change {} to?".format(user_input))
                new_value = input()
                new_checked_value = value_checker(user_input, new_value, json_data)
                json_data = json_writer(user_input, new_checked_value, json_data)
                print("{} was changed to {}.\n".format(user_input, new_value))
            elif user_input == "quit":
                print("Quitting...")
                quit()
            else:
                print("\nYour input was not listed in the keys. Try again.\n")
