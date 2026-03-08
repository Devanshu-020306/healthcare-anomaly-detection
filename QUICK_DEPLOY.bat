@echo off
REM Healthcare Anomaly Detection System - Quick Deploy Script (Windows)
REM Author: Devanshu (@Devanshu-020306)

echo.
echo ========================================================
echo Healthcare Anomaly Detection System - Deployment Script
echo ========================================================
echo.

REM Check if git is initialized
if not exist ".git" (
    echo Initializing Git repository...
    git init
)

REM Add all files
echo Adding files to Git...
git add .

REM Commit
echo Committing changes...
git commit -m "Healthcare Anomaly Detection System - Production Ready by Devanshu"

REM Add remote
echo Adding remote repository...
git remote remove origin 2>nul
git remote add origin https://github.com/Devanshu-020306/healthcare-anomaly-detection.git

REM Push to GitHub
echo Pushing to GitHub...
git branch -M main
git push -u origin main

echo.
echo ========================================================
echo Successfully pushed to GitHub!
echo ========================================================
echo.
echo Next Steps:
echo 1. Deploy Backend: https://railway.app
echo 2. Deploy Frontend: https://vercel.com
echo 3. Update API URLs in frontend files
echo.
echo Repository: https://github.com/Devanshu-020306/healthcare-anomaly-detection
echo.
echo Good luck! 
echo.
pause
