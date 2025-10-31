# 🚀 Quick Setup Guide

Follow these steps to get Crystal Scraper running:

## Step 1: Backend Setup ✅ DONE
The Python dependencies are already installed!

## Step 2: Frontend Setup

Open a NEW terminal and run:
```bash
cd frontend
npm install
```

This will install all React dependencies (only needed once).

## Step 3: Start the Application

### Option A: Automatic (Easiest)
Double-click `start_app.bat`

### Option B: Manual
1. Start Backend:
   - Run `start_backend.bat` OR
   - Run `python api.py`

2. Start Frontend (in a new terminal):
   - Run `start_frontend.bat` OR
   - Run `cd frontend && npm start`

## Step 4: Open Your Browser

Navigate to: **http://localhost:3000**

That's it! 🎉

## What You'll See

- A beautiful gradient interface
- Form to enter URLs
- Options for scraping depth
- AI formatting toggle
- Real-time results
- Download buttons
- Scraping history

## First Test

Try scraping: `https://example.com`
- Depth: 0 (single page)
- AI Formatting: Yes
- Click "Start Scraping"

## Troubleshooting

**Backend won't start?**
- Make sure port 5000 is free
- Check if Python dependencies are installed: `pip list | findstr flask`

**Frontend won't start?**
- Make sure Node.js is installed: `node --version`
- Install dependencies: `cd frontend && npm install`
- Make sure port 3000 is free

**Need help?**
Check README_FULLSTACK.md for detailed documentation.

---
Happy Scraping! 🔮✨
