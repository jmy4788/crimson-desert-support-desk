@echo off
setlocal

set "ROOT_DIR=%~dp0"
pushd "%ROOT_DIR%" >nul

python -c "import httpx, yaml, bs4" >nul 2>&1
if errorlevel 1 (
  echo [sync] Python dependencies not found. Installing...
  python -m pip install -e backend[dev]
  if errorlevel 1 (
    echo [sync] Dependency install failed.
    popd >nul
    exit /b 1
  )
)

echo [sync] Fetching official notices and importing them into the local database
python scripts\fetch_official_notices.py --locale ko-KR --pages 4 --clean-output --import-after-write

popd >nul
