@echo off
title Crystal Scraper - Full Stack
echo ========================================
echo Crystal Scraper - Full Stack Launcher
echo ========================================
echo.
echo Starting both Backend and Frontend...
echo.

REM Start backend in a new window
start "Crystal Scraper - Backend API" cmd /k "python api.py"

REM Wait a moment for backend to start
timeout /t 3 /nobreak >nul

REM Start frontend in a new window
start "Crystal Scraper - Frontend" cmd /k "cd frontend && npm start"

echo.
echo ========================================
echo Both servers are starting!
echo ========================================
echo.
echo Backend API: http://localhost:5000
echo Frontend UI: http://localhost:3000
echo.
echo Press any key to close this window (servers will keep running)
pause >nul
