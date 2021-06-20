@echo off
IF EXIST "env\" (
  cd %CD%
  start cmd.exe /k "env\scripts\activate.bat"^
    "&&echo Autocraft Commands: craft refresh leve"
) ELSE (
  cd %CD%
  start cmd.exe /k "python -m venv env"^
    "&&env\Scripts\activate.bat"^
    "&&pip install -r requirements.txt"^
    "&&echo Autocraft Commands: craft refresh leve"
)
