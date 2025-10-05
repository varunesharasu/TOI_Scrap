@echo off
REM Installs dev dependencies and runs pytest for this project (Windows cmd)
SET PY=python
IF NOT "%1"=="" (
  SET PY=%1
)
%PY% -m pip install -r "%~dp0dev-requirements.txt"
%PY% -m pytest -q "%~dp0tests"

pause
