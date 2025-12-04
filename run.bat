@echo off
REM Gemini Fabric Telos OS - Launcher Script
REM Uses UV for fast Python environment management

echo ========================================
echo   Gemini Fabric - Telos OS Launcher
echo ========================================
echo.

REM Check if uv is installed
where uv >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] UV is not installed!
    echo.
    echo Please install UV first:
    echo   - Windows: powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
    echo   - Or visit: https://docs.astral.sh/uv/getting-started/installation/
    echo.
    pause
    exit /b 1
)

echo [1/4] Checking UV installation...
uv --version
echo.

REM Check if .venv exists
if exist ".venv\" (
    echo [2/4] Virtual environment found at .venv
) else (
    echo [2/4] Creating virtual environment with UV...
    uv venv
    if %ERRORLEVEL% NEQ 0 (
        echo [ERROR] Failed to create virtual environment
        pause
        exit /b 1
    )
    echo     Virtual environment created successfully!
)
echo.

REM Activate virtual environment and install/sync dependencies
echo [3/4] Installing dependencies with UV...
uv pip install -r requirements.txt
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Failed to install dependencies
    pause
    exit /b 1
)
echo     Dependencies installed successfully!
echo.

REM Check if .env exists
if not exist ".env" (
    echo [WARNING] .env file not found!
    echo.
    echo Please create a .env file with your Gemini API key:
    echo   GEMINI_API_KEY=your_api_key_here
    echo.
    echo You can copy .env.example to .env and edit it.
    echo.
    pause
)

REM Run Streamlit
echo [4/4] Starting Streamlit app...
echo.
echo ========================================
echo   App will open in your browser
echo   Press Ctrl+C to stop the server
echo ========================================
echo.

uv run streamlit run app.py

REM If streamlit exits, pause so user can see any errors
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [ERROR] Streamlit exited with an error
    pause
)
