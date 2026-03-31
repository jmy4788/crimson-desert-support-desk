@echo off
setlocal

set "ROOT_DIR=%~dp0"

echo Starting Crimson Desert Support Desk...
start "Crimson Desert Backend" cmd /k call "%ROOT_DIR%run_backend.bat"
start "Crimson Desert Frontend" cmd /k call "%ROOT_DIR%run_frontend.bat"

echo Backend:  http://127.0.0.1:8017
echo Frontend: http://127.0.0.1:4173
