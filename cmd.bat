@echo off
python --version >nul 2>&1 && (
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
) || (
  start cmd.exe /k "echo Python Status: Not Found"^
    "&&echo Please follow the README.md of this folder to install Python"
)

