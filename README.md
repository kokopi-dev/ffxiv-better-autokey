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
Run `cmd.bat`

Type and enter `setup.bat` in cmd

If it doesn't download, re-read the top of this README.

---

## Instructions
Make a text file in the auto crafter folder with the key you press for your macro, and the macro below it like in the image below:
![demo1](../assets/demo1.PNG)

### Creating a macro profile
Make a macro profile with this command in the cmd:
```
python main.py make whitescripts.txt
```
* Your filename will become the macro profile's name

### Deleting a macro profile
Delete a macro profile with this command in cmd:
```
python main.py delete whitescripts
```

### Listing macro profiles
List all profiles saved with this command in cmd:
```
python main.py list
```

### Crafting with a macro profile
Start crafting with this command in cmd:
```
python main.py craft whitescripts 8
```
* python main.py craft PROFILE_NAME CRAFT_AMOUNT
