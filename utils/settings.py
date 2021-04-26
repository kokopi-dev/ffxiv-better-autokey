import re
import os
from pathlib import Path
# BUTTONS
REPAIR = "4"
CRAFT_ITEM = "5"
FOOD_KEY = ""
POTION_KEY = ""
ESC = "{VK_ESCAPE}"
LEFT = "{LEFT}"
RIGHT = "{RIGHT}"
SELECT = "{VK_NUMPAD0}"

# SETTINGS
REPAIR_COUNTER = 85
TIME_PADDING_0 = 3 # Time padding for in between pressing keys
CRAFT_SLEEPS = {
    "step1": 0.5,
    "step2": 1,
    "input1": 1,
    "input2": 2.5
}
CRAFT_OPTS = {
    "-repair": False,
    "-food": False,
    "-pot": False
}

# SYSTEM
RE_WAIT = re.compile(r"<wait.(.+?)>")
RE_KEY = re.compile(r"KEY")
FILENAME_MACROS = ".profiles.json"
FILENAME_LOGS = ".logs.json"
CWDPATH = os.getcwd()
ABSPATH = os.path.dirname(os.path.realpath(__file__))
PROFILES_PATH = os.path.join(Path(ABSPATH).parent, FILENAME_MACROS)
LOGS_PATH = os.path.join(Path(ABSPATH).parent, FILENAME_LOGS)
MACROS_FOLDER = "macros"
FLAGS = ["-repair", "-food", "-pot"]
PROFILES = {}
LOGS = {}

# MESSAGES
PROMPT = " > "
SELECT_MACRO = f"Macro profile name:\n{PROMPT}"
CRAFT_AMT = f"\nHow many crafts?\n{PROMPT}"
FLAGS_LIST = f"\nAvailable options: {FLAGS}\nLeave blank if none\n{PROMPT}"
DELETE_MACRO = f"Which macro do you want to delete?\n{PROMPT}"
CREATE_MACRO = f"What is the filename in the macros folder?\n{PROMPT}"
ERROR_ENTRY_0 = "ERROR: Please enter a command."
ERROR_ENTRY_1 = "ERROR: {} is not a command."
ERROR_CHECK_0 = "ERROR: {} does not exist, try creating it."
ERROR_CHECK_1 = "ERROR: Please enter a positive number."
ERROR_CHECK_2 = "ERROR: {} is not an option."
ERROR_CHECK_3 = "ERROR: No profiles have been made. Create one in macros\ folder"
