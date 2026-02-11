@echo off
echo Starting MarketMind Platform...

:: Start Backend
start "MarketMind Backend" cmd /k "cd backend && venv\Scripts\activate && uvicorn main:app --reload --port 8000"

:: Start Frontend
start "MarketMind Frontend" cmd /k "cd frontend && npm run dev"

echo.
echo ========================================================
echo   Servers are starting!
echo   Once loaded, access the app at: http://localhost:5173
echo ========================================================
echo.
pause
