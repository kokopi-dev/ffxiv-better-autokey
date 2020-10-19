@echo off
IF EXIST "env\" (
  cd %CD%
  start cmd.exe /k env\scripts\activate.bat
) ELSE (
  cd %CD%
  start cmd.exe /k "python -m venv env&&env\Scripts\activate.bat&&pip install -r requirements.txt"
)