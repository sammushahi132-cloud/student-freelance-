@echo off
echo =====================================================================
echo Pushing Student Freelance Marketplace to GitHub
echo Remote: https://github.com/sammushahi132-cloud/student-freelance-.git
echo =====================================================================
echo.

set GIT_PATH="C:\Users\SK Abdulsamadh\AppData\Local\GitHubDesktop\app-3.6.10\resources\app\git\cmd\git.exe"

cd /d "%~dp0"

echo Pushing committed code to GitHub origin main...
echo (If a GitHub sign-in window opens, click 'Sign in with your browser')
echo.

%GIT_PATH% push -u origin main

if errorlevel 1 (
    echo.
    echo =====================================================================
    echo If push failed, your GitHub repository may need to be force-pushed
    echo if it was initialized with a README on GitHub.
    echo To force push, you can run:
    echo   %GIT_PATH% push -u origin main --force
    echo =====================================================================
) else (
    echo.
    echo =====================================================================
    echo SUCCESS! Your code has been pushed to:
    echo https://github.com/sammushahi132-cloud/student-freelance-
    echo =====================================================================
)

pause
