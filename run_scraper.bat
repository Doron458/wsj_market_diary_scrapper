@echo off
setlocal ENABLEDELAYEDEXPANSION

REM Resolve project directory to this script's location
set "SCRIPT_DIR=%~dp0"
cd /d "%SCRIPT_DIR%"

echo WSJ Market Diary Scraper
echo ========================
echo.

REM Check for Python via the Windows launcher
where py >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo Python was not found on this system.
    echo.
    echo Please install Python 3 and ensure the "py" launcher is available in PATH.
    echo - Download: https://www.python.org/downloads/
    echo - During install, check "Add python.exe to PATH".
    echo.
    echo After installing, re-run this script.
    pause
    exit /b 1
)

REM Create virtual environment if missing
if not exist ".venv" (
    echo Creating virtual environment...
    py -3 -m venv .venv
    if %ERRORLEVEL% neq 0 (
        echo Failed to create virtual environment.
        pause
        exit /b 1
    )
)

REM Activate virtual environment
call ".venv\Scripts\activate.bat"
if %ERRORLEVEL% neq 0 (
    echo Failed to activate virtual environment.
    pause
    exit /b 1
)

echo Installing dependencies...
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
if %ERRORLEVEL% neq 0 (
    echo Failed to install dependencies.
    pause
    exit /b 1
)

echo.
echo Starting scraper...
python "%SCRIPT_DIR%wsj_market_diary_scraper.py"
set RUN_EXIT=%ERRORLEVEL%
echo.
if %RUN_EXIT% neq 0 (
    echo Scraper exited with code %RUN_EXIT%.
) else (
    echo Scraping completed. Check the output folder for CSV files.
)
echo.
pause
endlocal
