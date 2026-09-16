@echo off
setlocal
cd /d "%~dp0"

echo ============================================
echo   SC2 Lobby Fact-Checker Bot
echo ============================================
echo.

if not exist "config\config.yaml" (
  echo [!] config\config.yaml not found.
  echo     Copying from config.example.yaml ...
  if not exist "config" mkdir config
  copy /Y "config\config.example.yaml" "config\config.yaml" >nul
  echo     Edit config\config.yaml and set your API key + OCR region.
  echo.
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
