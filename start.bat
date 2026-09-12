@echo off
echo Starting Car Reseller System...
echo.

echo Step 1: Initializing database...
cd backend
python init_db.py
echo.

echo Step 2: Starting API server...
start "API Server" cmd /k "python main.py"
echo API server started on http://localhost:8000
echo.

echo Step 3: Starting Telegram Bot...
start "Telegram Bot" cmd /k "python start_bot.py"
echo Telegram Bot started
echo.

echo Step 4: Starting Frontend...
cd ../frontend
start "Frontend" cmd /k "npm run dev"
echo Frontend started on http://localhost:5173
echo.

echo All services started!
echo.
echo API: http://localhost:8000
echo Frontend: http://localhost:5173
echo.
echo Press any key to stop all services...
pause >nul

echo Stopping all services...
taskkill /FI "WINDOWTITLE eq API Server*" /T /F >nul 2>&1
taskkill /FI "WINDOWTITLE eq Telegram Bot*" /T /F >nul 2>&1
taskkill /FI "WINDOWTITLE eq Frontend*" /T /F >nul 2>&1
echo All services stopped.
