:: language: Batch, file: phase2_dependencies.cmd, target: Windows 10 CMD
@echo off
title IDM By Rashid - Phase 2 Dependencies and Binaries
color 0B

cd /d "%~dp0"

echo ===================================================
echo   IDM By Rashid - Phase 2: Engine and Library Setup
echo ===================================================
echo.

:: 1. Locate Installed Python
set "PY_CMD="

python --version >nul 2>&1
if %errorlevel% equ 0 set "PY_CMD=python"

if not defined PY_CMD (
    py --version >nul 2>&1
    if %errorlevel% equ 0 set "PY_CMD=py"
)

if not defined PY_CMD (
    for /d %%I in ("%LocalAppData%\Programs\Python\Python3*") do (
        if exist "%%~I\python.exe" set "PY_CMD=%%~I\python.exe"
    )
)

if not defined PY_CMD (
    for /d %%I in ("C:\Python3*" "C:\Program Files\Python3*") do (
        if exist "%%~I\python.exe" set "PY_CMD=%%~I\python.exe"
    )
)

if not defined PY_CMD (
    color 0C
    echo [ERROR] Could not locate python.exe.
    echo Re-run your Python installer, select "Modify", and check "Add python.exe to PATH".
    pause
    exit /b
)

echo   + Using Python: %PY_CMD%

:: 2. Create Virtual Environment (venv)
echo.
echo [1/4] Creating Python Virtual Environment (venv)...
if not exist "venv\Scripts\python.exe" (
    "%PY_CMD%" -m venv venv
    echo   + Virtual environment created.
) else (
    echo   - Virtual environment already exists.
)

:: 3. Install Python Libraries directly into venv
echo.
echo [2/4] Installing required Python packages...
"venv\Scripts\python.exe" -m pip install --upgrade pip
"venv\Scripts\pip.exe" install -r requirements.txt
echo   + Python packages installed.

:: 4. Download and Extract aria2c.exe (For Torrents and 16x Speed)
echo.
echo [3/4] Checking for aria2c.exe in bin\ folder...
if not exist "bin\aria2c.exe" (
    echo   * Downloading aria2c 64-bit Windows...
    curl -L "https://github.com/aria2/aria2/releases/download/release-1.37.0/aria2-1.37.0-win-64bit-build1.zip" -o "bin\aria2.zip"
    
    echo   * Extracting aria2c.exe...
    powershell -NoProfile -Command "Expand-Archive -Path 'bin\aria2.zip' -DestinationPath 'bin\aria2_temp' -Force; Get-ChildItem -Path 'bin\aria2_temp' -Filter 'aria2c.exe' -Recurse | Copy-Item -Destination 'bin\aria2c.exe' -Force; Remove-Item 'bin\aria2_temp' -Recurse -Force; Remove-Item 'bin\aria2.zip' -Force"
    echo   + aria2c.exe installed in bin\
) else (
    echo   - bin\aria2c.exe already exists.
)

:: 5. Download and Extract ffmpeg.exe (For 4K Video/Audio Merging)
echo.
echo [4/4] Checking for ffmpeg.exe in bin\ folder...
if not exist "bin\ffmpeg.exe" (
    echo   * Downloading FFmpeg Essentials (approx. 109 MB, please wait)...
    curl -L "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip" -o "bin\ffmpeg.zip"
    
    echo   * Extracting ffmpeg.exe and ffprobe.exe...
    powershell -NoProfile -Command "Expand-Archive -Path 'bin\ffmpeg.zip' -DestinationPath 'bin\ffmpeg_temp' -Force; Get-ChildItem -Path 'bin\ffmpeg_temp' -Include 'ffmpeg.exe','ffprobe.exe' -Recurse | Copy-Item -Destination 'bin\' -Force; Remove-Item 'bin\ffmpeg_temp' -Recurse -Force; Remove-Item 'bin\ffmpeg.zip' -Force"
    echo   + ffmpeg.exe and ffprobe.exe installed in bin\
) else (
    echo   - bin\ffmpeg.exe already exists.
)

echo.
echo ===================================================
echo   Verifying Engine Binaries...
echo ===================================================
if exist "venv\Scripts\python.exe" (echo   [OK] venv\Scripts\python.exe is ready.) else (echo   [MISSING] venv failed.)
if exist "bin\aria2c.exe" (echo   [OK] bin\aria2c.exe is ready.) else (echo   [MISSING] aria2c.exe failed to download.)
if exist "bin\ffmpeg.exe" (echo   [OK] bin\ffmpeg.exe is ready.) else (echo   [MISSING] ffmpeg.exe failed to download.)

echo.
echo ===================================================
echo   Phase 2 Complete! Ready for Phase 3.
echo ===================================================
pause