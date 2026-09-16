@echo off
setlocal EnableExtensions
cd /d "%~dp0"

echo ============================================
echo   SC2 Lobby Fact-Checker Bot
echo ============================================
echo.
echo Folder: %CD%
echo.

if not exist "main.py" (
  echo [ERROR] main.py not found in this folder.
  echo         Extract the full ZIP and run start.bat from the project root.
  goto :end
)

if not exist "config\config.yml" (
  echo [ERROR] config\config.yml not found.
  echo         Restore config\config.yml from the repo.
  goto :end
)

if not exist "src\bot.py" (
  echo [ERROR] src\bot.py missing — incomplete download.
  echo         Re-download the full repository ZIP from GitHub.
  goto :end
)

REM Prefer the Python launcher, then python, then python3
set "PYEXE="
where py >nul 2>&1 && set "PYEXE=py -3"
if not defined PYEXE (
  where python >nul 2>&1 && set "PYEXE=python"
)
if not defined PYEXE (
  where python3 >nul 2>&1 && set "PYEXE=python3"
)
if not defined PYEXE (
  echo [ERROR] Python was not found on PATH.
  echo         Install Python 3.10+ from https://www.python.org/downloads/
  echo         During setup, check "Add python.exe to PATH".
  goto :end
)

echo Using: %PYEXE%
%PYEXE% --version
if errorlevel 1 (
  echo [ERROR] Could not run Python. Install Python 3.10+ and enable PATH.
  goto :end
)
echo.

if not exist "requirements.txt" (
  echo [WARN] requirements.txt missing — skipping dependency install.
) else (
  echo Checking / installing dependencies...
  %PYEXE% -m pip install -r requirements.txt
  if errorlevel 1 (
    echo [ERROR] pip install failed.
    goto :end
  )
  echo.
)

echo Starting fact-checker...
echo (Press Ctrl+C to stop)
echo.
%PYEXE% -u main.py
set "ERR=%ERRORLEVEL%"
echo.
if not "%ERR%"=="0" (
  echo [ERROR] Bot exited with code %ERR%.
  echo         Common causes: missing API key in config\config.yml, missing packages, incomplete src\.
) else (
  echo Bot stopped normally.
)

:end
echo.
echo --------------------------------------------
pause
endlocal
