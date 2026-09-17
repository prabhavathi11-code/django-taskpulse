@echo off
title TaskPulse - Django + Cloudflare Tunnel

echo ============================================
echo  Starting Django Server...
echo ============================================
start "Django Server" cmd /k "cd /d %~dp0 && .venv\Scripts\activate && python manage.py runserver"

timeout /t 3 /nobreak >nul

echo ============================================
echo  Starting Cloudflare Tunnel...
echo ============================================
start "Cloudflare Tunnel" cmd /k "cd /d %~dp0 && cloudflared.exe tunnel --url http://localhost:8000"

echo.
echo Both services started!
echo Look at the Cloudflare Tunnel window for your public URL.
echo.
pause
