@echo off
setlocal

set "ROOT_DIR=%~dp0"
pushd "%ROOT_DIR%frontend" >nul
set "VITE_API_BASE_URL=http://127.0.0.1:8017"

if not exist "node_modules" (
  echo [frontend] node_modules not found. Installing...
  call npm install
  if errorlevel 1 (
    echo [frontend] npm install failed.
    popd >nul
    exit /b 1
  )
)

echo [frontend] Starting Vite at http://127.0.0.1:4173
call npm run dev

popd >nul
