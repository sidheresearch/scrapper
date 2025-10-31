# 🔮 Crystal Scraper - Full Stack Web Scraping Platform

A powerful full-stack web scraping application with a React frontend and Flask backend that extracts clean, readable content from websites with AI-powered formatting.

![Crystal Scraper](https://img.shields.io/badge/version-1.0.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.8+-green.svg)
![React](https://img.shields.io/badge/react-18.2.0-blue.svg)
![Flask](https://img.shields.io/badge/flask-3.0.0-lightgrey.svg)

## 🌟 Features

### Web Interface
- **Modern React UI**: Beautiful, responsive interface with gradient design
- **Real-time Status**: Live API connection status indicator
- **Scraping History**: View and download previously scraped content
- **Result Preview**: Instant preview of scraped content
- **Download Manager**: Easy file download system

### Scraping Engine
- **Recursive Scraping**: Follow links to specified depth (0, 1, or 2 levels)
- **AI Content Formatting**: Uses LLM to clean and format scraped content
- **HTML Parsing**: Automatically removes HTML, CSS, and JavaScript
- **Multiple Strategies**: Falls back through multiple scraping methods
- **Custom Filenames**: Option to specify custom output filename
- **Multi-Page Support**: Combines content from multiple pages

### API Features
- **RESTful API**: Full REST API with Flask
- **CORS Enabled**: Works with frontend on different ports
- **Health Checks**: Monitor API availability
- **Result Management**: Store and retrieve scraping results
- **File Downloads**: Stream files directly to users

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- Node.js 14 or higher
- npm or yarn

### Installation

1. **Install Python dependencies**
```bash
pip install -r requirements.txt
```

2. **Install Node.js dependencies**
```bash
cd frontend
npm install
cd ..
```

### Running the Application

#### Option 1: Full Stack (Easiest)
Double-click **`start_app.bat`** 

This automatically starts both backend and frontend!

#### Option 2: Manual Start

**Terminal 1 - Backend:**
```bash
python api.py
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm start
```

### Accessing the Application
- **Frontend UI**: http://localhost:3000
- **Backend API**: http://localhost:5000

## 📖 Usage Guide

### Using the Web Interface

1. Open http://localhost:3000 in your browser
2. Enter the URL you want to scrape
3. Select scraping depth (0, 1, or 2)
4. Toggle AI formatting if desired
5. Optionally enter a custom filename
6. Click "Start Scraping"
7. View results and download the file

### Scraping Depths
- **Depth 0**: Single page only (fastest)
- **Depth 1**: Main page + directly linked pages
- **Depth 2**: Main page + linked pages + their linked pages

## 🔌 API Documentation

### Endpoints

#### Health Check
```http
GET /api/health
```

#### Scrape Website
```http
POST /api/scrape
Content-Type: application/json

{
  "url": "https://example.com",
  "depth": 0,
  "llm_enabled": true,
  "filename": "custom_name"
}
```

#### List Results
```http
GET /api/results
```

#### Get Result Details
```http
GET /api/results/<result_id>
```

#### Download Result
```http
GET /api/download/<result_id>
```

## 🎨 Project Structure

```
Crystal_Scraper/
├── api.py                 # Flask REST API server
├── website_scraper.py     # CLI scraper (legacy)
├── requirements.txt       # Python dependencies
├── start_app.bat         # Launch full stack
├── start_backend.bat     # Launch backend only
├── start_frontend.bat    # Launch frontend only
├── scraper/              # Scraper module
│   ├── __init__.py
│   ├── config.py         # Configuration
│   └── scraper.py        # Core scraping logic
└── frontend/             # React application
    ├── package.json      # Node dependencies
    ├── public/
    │   └── index.html
    └── src/
        ├── App.js        # Main component
        ├── App.css       # Styling
        ├── index.js      # Entry point
        └── services/
            └── api.js    # API client
```

## ⚙️ Configuration

### Optional: AI Formatting

Create a `.env` file in the root directory:

```env
# Optional - for AI-powered content formatting
TOGETHER_API_KEY=your_together_api_key
GOOGLE_API_KEY=your_google_api_key
```

**Note**: The scraper works perfectly without API keys by using HTML parsing!

### Customize Settings

Edit `scraper/config.py`:
```python
CACHE_ENABLED = True
CACHE_TTL = 3600
LLM_ENABLED = True
```

## 🐛 Troubleshooting

### Backend Issues

**Module not found**
```bash
pip install -r requirements.txt
```

**Port 5000 in use**
- Change port in `api.py`
- Or close the application using port 5000

### Frontend Issues

**npm not found**
- Install Node.js from https://nodejs.org

**Dependencies missing**
```bash
cd frontend
npm install
```

**Port 3000 in use**
- React will offer an alternative port
- Or close the application using port 3000

## 📝 Features Deep Dive

### AI Content Formatting

**With AI** (API keys provided):
- Removes HTML, CSS, JavaScript
- Cleans navigation and boilerplate
- Formats as readable markdown
- Preserves important information

**Without AI** (no API keys needed):
- Parses HTML with BeautifulSoup
- Extracts clean text
- Removes scripts and styles
- Returns readable output

### Multiple Scraping Strategies

The scraper tries multiple methods:
1. aiohttp + BeautifulSoup (fastest)
2. Playwright (JavaScript-heavy sites)
3. Selenium (complex sites)

### Recursive Scraping

Follows links intelligently:
- Respects domain boundaries
- Avoids external links
- Combines all content
- Tracks scraped URLs

## 🚀 Deployment

### Backend (Production)

Using Gunicorn:
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 api:app
```

Using Waitress (Windows):
```bash
pip install waitress
waitress-serve --host=0.0.0.0 --port=5000 api:app
```

### Frontend (Production)

Build:
```bash
cd frontend
npm run build
```

Deploy the `build` folder to:
- Vercel
- Netlify
- GitHub Pages
- AWS S3 + CloudFront

## 🧪 Testing

### Test Backend
```bash
# Health check
curl http://localhost:5000/api/health

# Scrape
curl -X POST http://localhost:5000/api/scrape \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com"}'
```

### Test Frontend
Open http://localhost:3000 and try scraping a website

## 📄 License

Open source - free for personal and commercial use.

## 🤝 Contributing

Contributions welcome! 
- Report bugs
- Suggest features
- Submit pull requests

## 🎯 Roadmap

- [ ] User authentication
- [ ] Scheduled scraping
- [ ] Export to multiple formats (PDF, JSON)
- [ ] Advanced filtering options
- [ ] Chrome extension
- [ ] Mobile app

## 📧 Support

For issues or questions, open an issue on GitHub.

---

**Made with ❤️ using Python, Flask, React, and AI**

**Star ⭐ this repo if you find it useful!**
