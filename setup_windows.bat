@echo off
REM CSMAR Data Download - Windows Setup Script
REM This script installs all dependencies and prepares the environment

echo ======================================================================
echo CSMAR DATA DOWNLOAD - WINDOWS SETUP
echo ======================================================================
echo.

REM Check Python installation
echo [1/5] Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH!
    echo.
    echo Please install Python 3.8+ from: https://www.python.org/downloads/
    echo IMPORTANT: Check "Add Python to PATH" during installation
    pause
    exit /b 1
)

python --version
echo ✅ Python is installed
echo.

REM Check pip
echo [2/5] Checking pip...
pip --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: pip is not installed!
    echo.
    echo Please reinstall Python with pip included
    pause
    exit /b 1
)

pip --version
echo ✅ pip is installed
echo.

REM Install dependencies
echo [3/5] Installing Python dependencies...
echo This may take a few minutes...
echo.

pip install urllib3 websocket websocket_client pandas prettytable python-dotenv

if errorlevel 1 (
    echo.
    echo ERROR: Failed to install dependencies!
    echo Please check your internet connection and try again
    pause
    exit /b 1
)

echo.
echo ✅ All dependencies installed successfully!
echo.

REM Create .env file if it doesn't exist
echo [4/5] Setting up credentials file...

if exist .env (
    echo ℹ️  .env file already exists - skipping
) else (
    if exist .env.example (
        copy .env.example .env >nul
        echo ✅ Created .env file from template
        echo.
        echo ⚠️  IMPORTANT: Edit .env file and add your CSMAR credentials!
        echo    Open with Notepad: notepad .env
    ) else (
        echo ⚠️  WARNING: .env.example not found!
        echo    Please create .env file manually with your credentials
    )
)
echo.

REM Check CSMAR API installation
echo [5/5] Checking CSMAR API installation...

python -c "import csmarapi" >nul 2>&1
if errorlevel 1 (
    echo ❌ CSMAR API not installed yet
    echo.
    echo ========================================================================
    echo NEXT STEP: Install CSMAR-PYTHON Library
    echo ========================================================================
    echo.
    echo 1. Download from: https://data.csmar.com/static/python_3.6.0.rar
    echo    ^(Login required^)
    echo.
    echo 2. Extract the RAR file
    echo.
    echo 3. Find your Python site-packages folder:
    echo    python -c "import site; print(site.getsitepackages()[0])"
    echo.
    echo 4. Copy the 'csmarapi' folder from extracted RAR to site-packages
    echo.
    echo 5. Verify installation:
    echo    python -c "import csmarapi; print('Success!')"
    echo.
    echo 6. Run this setup script again after installation
    echo.
    echo ========================================================================
    pause
    exit /b 0
) else (
    echo ✅ CSMAR API is installed
    echo.
)

REM Run test script
echo ======================================================================
echo RUNNING INSTALLATION TEST
echo ======================================================================
echo.

python test_csmar_api.py

if errorlevel 1 (
    echo.
    echo ⚠️  Some tests failed - please fix issues above before downloading
    pause
    exit /b 1
)

echo.
echo ======================================================================
echo ✅ SETUP COMPLETE!
echo ======================================================================
echo.
echo Next steps:
echo   1. Edit .env file with your CSMAR credentials: notepad .env
echo   2. Run download script: python download_csmar_classifications.py
echo   3. Wait for download to complete (15-30 minutes)
echo   4. Transfer CSV files back to Mac
echo.
echo ======================================================================
pause
