@echo off
echo ========================================
echo Sex Education System - Quick Start
echo ========================================
echo.

echo Installing required packages...
pip install django Pillow

echo.
echo Running setup...
python setup.py

echo.
echo Starting development server...
python manage.py runserver

pause
