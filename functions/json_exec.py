"""
json_writer contains a class with functions to help
read, write, save, and re-read the json files
"""
import json
import os
import sys
import re

class JsonExec:
    """ JsonExec
    """
    current_path = os.path.dirname(os.path.abspath(__file__))

    def __init__(self):
        self.json_file_name = json_file_name
        JsonExec.current_path = current_path

    @property
    def getJsonFileName(self):
        """ Getting json file name
        """
        return self.json_file_name

    @getJsonFileName.setter
    def getJsonFileName(self, name_string):
        """ Setting json file name
            Must be a type string
        """
        if not isinstance(name_string, str):
            raise TypeError("Json file variable must be a type string.")
        self.json_file_name = name_string

    def reading_from_json(json_file_name):
        """ Reads the json file and returns a var that allows data access to the
            ... latest read dictionary
        """
        with open(("{:s}/{:s}".format(JsonExec.current_path, json_file_name)), "r") as time_data:
            json_data = json.load(time_data)
        return json_data

    def adding_to_json(json_file_name):
        """ Opens the json file and returns a var that allows adding to the dictionary
        """
        with open("{:s}/{:s}".format(JsonExec.current_path, json_file_name)) as add_data:
            add_time = json.load(add_data)
        return add_time

    def saving_to_json(json_file_name, data_to_add):
        """ Opens the json file and overwrites the entire file with newly added data from
              ... adding_to_json
            Relies on returned value from adding_to_json
            Prints save message for debugging purposes
        """
        with open(("{:s}/{:s}".format(JsonExec.current_path, json_file_name)), "w") as save_data:
            json.dump(data_to_add, save_data)
        print("  ... saving data", end='')
