@echo off
setlocal

rem Double-click this file to refresh the Belay dashboard.
rem
rem It re-runs scripts/status.py against the current state of the repository,
rem then opens the resulting page in your default browser. Nothing to type.
rem
rem "cd /d %~dp0" moves to the folder this file lives in, so the script works
rem no matter where it is launched from - including a desktop shortcut.

cd /d "%~dp0"

echo Refreshing Belay status...
echo.

python scripts\status.py
set RESULT=%errorlevel%

if not exist "reports\generated\status.html" (
    echo.
    echo ---------------------------------------------------------------
    echo Could not build the dashboard.
    echo.
    echo Most likely cause: Python is not on your PATH, so the "python"
    echo command above did not run. The error text above will say so.
    echo ---------------------------------------------------------------
    echo.
    pause
    exit /b 1
)

start "" "reports\generated\status.html"

if %RESULT% neq 0 (
    echo.
    echo ---------------------------------------------------------------
    echo The dashboard opened, but the test suite is NOT passing.
    echo Details are on the page and in the output above.
    echo ---------------------------------------------------------------
    echo.
    pause
)
