@echo off
echo =====================================================================
echo Starting Student Freelance Marketplace Web Application
echo =====================================================================
echo.

cd /d "%~dp0"

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

python manage.py runserver

pause

