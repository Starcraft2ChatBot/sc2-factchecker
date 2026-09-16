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
  echo [ERROR] main.py not found. Run this from the project root.
  goto :end
)
if not exist "config\config.yml" (
  echo [ERROR] config\config.yml not found.
  goto :end
)
if not exist "src\bot.py" (
  echo [ERROR] src\bot.py missing — incomplete download.
  goto :end
)

set "PYEXE="
where py >nul 2>&1
if not errorlevel 1 (
  py -3.12 -c "import sys" >nul 2>&1 && set "PYEXE=py -3.12"
  if not defined PYEXE py -3.11 -c "import sys" >nul 2>&1 && set "PYEXE=py -3.11"
  if not defined PYEXE py -3.13 -c "import sys" >nul 2>&1 && set "PYEXE=py -3.13"
  if not defined PYEXE set "PYEXE=py -3"
)
if not defined PYEXE where python >nul 2>&1 && set "PYEXE=python"
if not defined PYEXE (
  echo [ERROR] Python not found. Install 3.12 and enable PATH.
  goto :end
)

echo Using: %PYEXE%
%PYEXE% --version
if errorlevel 1 (
  echo [ERROR] Could not run Python.
  goto :end
)

%PYEXE% -c "import sys; raise SystemExit(0 if sys.version_info < (3,14) else 1)"
if errorlevel 1 (
  echo [ERROR] Python 3.14+ is not supported yet. Use 3.12.
  echo         py -3.12 -m pip install -r requirements.txt
  echo         py -3.12 -u main.py
  goto :end
)
echo.

if exist "requirements.txt" (
  echo Installing / checking dependencies with this Python...
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
  if "%ERR%"=="-1073741819" (
    echo         Windows native crash. Use Python 3.12 and try chat_backend: simulated first.
  )
) else (
  echo Bot stopped normally.
)

:end
echo.
echo --------------------------------------------
pause
endlocal
