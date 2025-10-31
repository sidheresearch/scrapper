@echo off
title Crystal Scraper - Installation Checker
color 0A

echo.
echo ========================================
echo   CRYSTAL SCRAPER - INSTALLATION CHECK
echo ========================================
echo.

echo [1/4] Checking Python...
python --version >nul 2>&1
if %errorlevel% equ 0 (
    echo [OK] Python is installed
    python --version
) else (
    echo [ERROR] Python is not installed!
    echo Please install Python from https://python.org
    goto :error
)

echo.
echo [2/4] Checking Node.js...
node --version >nul 2>&1
if %errorlevel% equ 0 (
    echo [OK] Node.js is installed
    node --version
) else (
    echo [ERROR] Node.js is not installed!
    echo Please install Node.js from https://nodejs.org
    goto :error
)

echo.
echo [3/4] Checking Python packages...
python -c "import flask" >nul 2>&1
if %errorlevel% equ 0 (
    echo [OK] Flask is installed
) else (
    echo [WARNING] Flask is not installed
    echo Run: pip install -r requirements.txt
)

python -c "import aiohttp" >nul 2>&1
if %errorlevel% equ 0 (
    echo [OK] aiohttp is installed
) else (
    echo [WARNING] aiohttp is not installed
    echo Run: pip install -r requirements.txt
)

echo.
echo [4/4] Checking Frontend dependencies...
if exist "frontend\node_modules\" (
    echo [OK] Frontend dependencies are installed
) else (
    echo [WARNING] Frontend dependencies not installed
    echo Run: cd frontend ^&^& npm install
)

echo.
echo ========================================
echo.
echo INSTALLATION STATUS:
echo ----------------------------------------
echo Backend Ready:     Check if Flask/aiohttp OK above
echo Frontend Ready:    Check if node_modules exists above
echo.
echo NEXT STEPS:
echo 1. Install missing dependencies if any
echo 2. Run: start_app.bat
echo 3. Open: http://localhost:3000
echo.
echo ========================================
echo.
pause
exit /b 0

:error
echo.
echo ========================================
echo Installation incomplete!
echo Please install the missing components.
echo ========================================
echo.
pause
exit /b 1
