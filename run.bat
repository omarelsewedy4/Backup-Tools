@echo off
REM =========================================================================
REM Intelligent Backup Storage Management System - Launcher Script
REM =========================================================================
REM This batch file makes it easy to run the backup self-purge system
REM on Windows without opening a command prompt manually

REM Change to the directory where this script is located
cd /d "%~dp0"

REM Display welcome message
echo.
echo =========================================================================
echo Intelligent Backup Storage Management System - Self-Purge
echo =========================================================================
echo.
echo Checking Python installation...

REM Verify Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo.
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python from https://www.python.org/
    echo.
    pause
    exit /b 1
)

REM Check if psutil is installed
echo Checking required packages...
python -c "import psutil" >nul 2>&1
if errorlevel 1 (
    echo.
    echo Installing required package: psutil...
    echo.
    pip install psutil
    if errorlevel 1 (
        echo ERROR: Failed to install psutil
        pause
        exit /b 1
    )
)

REM Run the main script
echo.
echo =========================================================================
echo Starting Backup Self-Purge System...
echo =========================================================================
echo.

python backup_self_purge.py

REM Pause to let user see output
echo.
echo =========================================================================
echo Operation completed. Check backup_purge.log for details.
echo Press any key to exit...
echo =========================================================================
pause >nul
