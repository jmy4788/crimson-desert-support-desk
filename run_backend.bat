@echo off
setlocal

set "ROOT_DIR=%~dp0"
pushd "%ROOT_DIR%" >nul

python -c "import fastapi, sqlmodel, uvicorn" >nul 2>&1
if errorlevel 1 (
  echo [backend] Python dependencies not found. Installing...
  python -m pip install -e backend[dev]
  if errorlevel 1 (
    echo [backend] Dependency install failed.
    popd >nul
    exit /b 1
  )
)

python -c "import sys, urllib.request; urllib.request.urlopen('http://127.0.0.1:8017/api/health', timeout=2); sys.exit(0)" >nul 2>&1
if not errorlevel 1 (
  echo [backend] API already running at http://127.0.0.1:8017
  popd >nul
  exit /b 0
)

echo [backend] Starting API at http://127.0.0.1:8017
python scripts\run_backend_server.py

popd >nul
