@echo off
setlocal
cd /d "%~dp0"

echo ============================================
echo   SC2 Lobby Fact-Checker Bot
echo ============================================
echo.

if not exist "config\config.yml" (
  echo [!] config\config.yml not found.
  echo     Create it or restore it from the repo.
  pause
  exit /b 1
)

where python >nul 2>&1
if errorlevel 1 (
  echo [!] Python not found on PATH. Install Python 3.10+ or use the portable build.
  pause
  exit /b 1
)

echo Starting fact-checker...
python main.py
if errorlevel 1 (
  echo.
  echo Bot exited with an error. Check logs\ or the console above.
  pause
)
endlocal
