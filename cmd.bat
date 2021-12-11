@echo off
IF EXIST "venv\" (
  cd %CD%
  start cmd.exe /k "venv\scripts\activate.bat"^
    "&&python auto.py"
) ELSE (
  cd %CD%
  start cmd.exe /k "python -m venv venv"^
    "&&venv\Scripts\activate.bat"^
    "&&python -m pip install --upgrade pip"^
    "&&pip install -r requirements.txt"^
    "&&python auto.py"
)

