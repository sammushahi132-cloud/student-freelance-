@echo off
echo =====================================================================
echo Starting Student Freelance Marketplace Web Application
echo Python Full Stack Internship Project
echo =====================================================================
echo.

cd /d "%~dp0\freelance_marketplace"

echo Checking system environment...
python --version
if errorlevel 1 (
    echo [ERROR] Python is not installed or not added to your system PATH.
    echo Please install Python from https://www.python.org/
    pause
    exit /b 1
)

echo Starting Django Development Server...
echo.
echo Application will be available at:
echo   Main Website:      http://127.0.0.1:8000/
echo   Admin Panel:       http://127.0.0.1:8000/admin/
echo   Admin Dashboard:   http://127.0.0.1:8000/admin-dashboard/
echo.
echo Demo Credentials:
echo   Superuser/Admin:   admin / admin123
echo   Student:           rahul_dev / password123
echo   Client:            tech_solutions / password123
echo.
echo Press Ctrl+C in this window anytime to stop the server.
echo =====================================================================
echo.

python manage.py runserver

pause

