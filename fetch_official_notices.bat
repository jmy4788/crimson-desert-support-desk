@echo off
setlocal

set "ROOT_DIR=%~dp0"
pushd "%ROOT_DIR%" >nul

python -c "import httpx, yaml, bs4" >nul 2>&1
if errorlevel 1 (
  echo [fetch] Python dependencies not found. Installing...
  python -m pip install -e backend[dev]
  if errorlevel 1 (
    echo [fetch] Dependency install failed.
    popd >nul
    exit /b 1
  )
)

echo [fetch] Fetching official notices into raw_sources\\incoming\\auto
python scripts\fetch_official_notices.py --locale ko-KR --pages 4 --clean-output --validate-only

popd >nul
