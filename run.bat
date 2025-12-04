@echo off
REM Gemini Fabric Telos OS - Launcher Script
REM Supports both UV (system-wide) and pip (venv) installations

echo ========================================
echo   Gemini Fabric - Telos OS Launcher
echo ========================================
echo.

REM Check if .venv exists
if exist ".venv\" (
    echo [1/4] Virtual environment found at .venv
    
    REM Check if UV is available in venv
    if exist ".venv\Scripts\uv.exe" (
        echo [2/4] Using UV from virtual environment...
        call .venv\Scripts\activate.bat
        uv --version
    ) else (
        REM Check if UV is available system-wide
        where uv >nul 2>nul
        if %ERRORLEVEL% EQU 0 (
            echo [2/4] Using system UV...
            uv --version
        ) else (
            echo [2/4] UV not found, using pip...
            call .venv\Scripts\activate.bat
            python --version
        )
    )
) else (
    REM No venv exists - check for UV to create one
    where uv >nul 2>nul
    if %ERRORLEVEL% EQU 0 (
        echo [1/4] Creating virtual environment with UV...
        uv venv
        if %ERRORLEVEL% NEQ 0 (
            echo [ERROR] Failed to create virtual environment
            pause
            exit /b 1
        )
        echo     Virtual environment created successfully!
        echo [2/4] UV ready
        uv --version
    ) else (
        echo [1/4] Creating virtual environment with Python...
        python -m venv .venv
        if %ERRORLEVEL% NEQ 0 (
            echo [ERROR] Failed to create virtual environment
            pause
            exit /b 1
        )
        echo     Virtual environment created successfully!
        call .venv\Scripts\activate.bat
        echo [2/4] Installing UV in virtual environment...
        pip install uv
        if %ERRORLEVEL% NEQ 0 (
            echo [WARNING] Failed to install UV, will use pip instead
        )
    )
)
echo.

REM Install dependencies
echo [3/4] Installing dependencies...
if exist ".venv\Scripts\uv.exe" (
    call .venv\Scripts\activate.bat
    uv pip install -r requirements.txt
) else (
    where uv >nul 2>nul
    if %ERRORLEVEL% EQU 0 (
        uv pip install -r requirements.txt
    ) else (
        call .venv\Scripts\activate.bat
        pip install -r requirements.txt
    )
)

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

REM Activate venv if not already active
if not defined VIRTUAL_ENV (
    call .venv\Scripts\activate.bat
)

REM Run with UV if available, otherwise use python directly
where uv >nul 2>nul
if %ERRORLEVEL% EQU 0 (
    uv run streamlit run app.py
) else (
    python -m streamlit run app.py
)

REM If streamlit exits, pause so user can see any errors
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [ERROR] Streamlit exited with an error
    pause
)
