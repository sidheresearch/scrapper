@echo off
echo ========================================
echo Crystal Scraper - Starting Frontend
echo ========================================
echo.
cd frontend
echo Installing dependencies (first time only)...
if not exist "node_modules\" (
    call npm install
)
echo.
echo Starting React development server...
echo Frontend will be available at http://localhost:3000
echo.
call npm start
pause
