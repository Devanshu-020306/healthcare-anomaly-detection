#!/bin/bash

# Healthcare Anomaly Detection System - Quick Deploy Script
# Author: Devanshu (@Devanshu-020306)

echo "🏥 Healthcare Anomaly Detection System - Deployment Script"
echo "============================================================"
echo ""

# Check if git is initialized
if [ ! -d ".git" ]; then
    echo "📦 Initializing Git repository..."
    git init
fi

# Add all files
echo "📝 Adding files to Git..."
git add .

# Commit
echo "💾 Committing changes..."
git commit -m "Healthcare Anomaly Detection System - Production Ready by Devanshu"

# Check if remote exists
if git remote | grep -q "origin"; then
    echo "🔄 Remote already exists, updating..."
    git remote set-url origin https://github.com/Devanshu-020306/healthcare-anomaly-detection.git
else
    echo "🔗 Adding remote repository..."
    git remote add origin https://github.com/Devanshu-020306/healthcare-anomaly-detection.git
fi

# Push to GitHub
echo "🚀 Pushing to GitHub..."
git branch -M main
git push -u origin main

echo ""
echo "✅ Successfully pushed to GitHub!"
echo ""
echo "📱 Next Steps:"
echo "1. Deploy Backend: https://railway.app"
echo "2. Deploy Frontend: https://vercel.com"
echo "3. Update API URLs in frontend files"
echo ""
echo "🎯 Repository: https://github.com/Devanshu-020306/healthcare-anomaly-detection"
echo ""
echo "Good luck! 🚀"
