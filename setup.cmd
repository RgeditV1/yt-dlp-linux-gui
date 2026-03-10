@echo off
setlocal

cd /d "%~dp0"

set "PY_CMD="
where py >nul 2>nul
if %errorlevel%==0 (
  set "PY_CMD=py -3"
) else (
  where python >nul 2>nul
  if %errorlevel%==0 (
    set "PY_CMD=python"
  ) else (
    echo ERROR: Python not found. Install Python 3 (or the 'py' launcher^) and retry.
    exit /b 1
  )
)

if not exist ".venv" (
  %PY_CMD% -m venv .venv
  if %errorlevel% neq 0 exit /b %errorlevel%
)

if exist ".venv\Scripts\python.exe" (
  set "VENV_PY=.venv\Scripts\python.exe"
) else (
  echo ERROR: venv python not found under .venv\Scripts. venv creation may have failed.
  exit /b 1
)

"%VENV_PY%" -m pip install --upgrade pip
if %errorlevel% neq 0 exit /b %errorlevel%

"%VENV_PY%" -m pip install -r requirements.txt
if %errorlevel% neq 0 exit /b %errorlevel%

echo OK: venv ready.

