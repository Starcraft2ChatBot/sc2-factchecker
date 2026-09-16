@echo off
setlocal
cd /d "%~dp0"

echo ============================================
echo   SC2 Lobby Fact-Checker Bot
echo ============================================
echo.

if not exist "config\config.yml" (
  echo [!] config\config.yml not found.
  echo     Restore it from the repo ZIP.
  pause
  exit /b 1
)

where python >nul 2>&1
if errorlevel 1 (
  echo [!] Python not found on PATH. Install Python 3.10+
  pause
  exit /b 1
)

if not exist ".deps_installed" (
  echo Installing dependencies (first run)...
  python -m pip install -r requirements.txt
  if errorlevel 1 (
    echo [!] pip install failed
    pause
    exit /b 1
  )
  echo. > .deps_installed
)

echo Starting fact-checker...
python main.py
if errorlevel 1 (
  echo.
  echo Bot exited with an error. Check logs\ or the console above.
  pause
)
endlocal
