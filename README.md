![github version](https://d25lcipzij17d.cloudfront.net/badge.svg?id=gh&type=6&v=2.0.0&x2=0)
# FFXIV Auto Crafter
Terminal tool for FFXIV crafting

---

## Setup :wrench:
Install Python for Windows
https://www.python.org/downloads/windows/

### Download 64 bit and run it
```Download Windows x86-64 executable installer```

### Check PATH during installation
![path_check](../assets/pythonpathcheck.PNG)

### Requirements
Run/double-click `cmd.bat`

It should make an env\ folder and install python requirements

---

## Instructions
#### Make a text file in the macros\\ folder with the key you press for your macro, and the macro below it like in the image below:
![demo1](../assets/demo1.PNG)

### Creating a macro profile
The text file you created is the macro profie
List your profiles with:
```
python main.py list
```

### Updating a macro profile
Update the text file, it will immediately change after saving the file


### Deleting a macro profile
To delete a profile, delete the text file.

### Crafting with a macro profile
Start crafting with this command in cmd:
```
python main.py craft whitescripts 8
```
* python main.py craft PROFILE_NAME CRAFT_AMOUNT


### Crafting options
WIP

---

## Author
* [kai-dg](https://github.com/kai-dg)
