# 🔮 Crystal Scraper - Full Stack Web Scraping Platform

A powerful full-stack web scraping application with a React frontend and Flask backend that extracts clean, readable content from websites with AI-powered formatting.

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
- Node.js 14 or higher (for frontend)
- npm or yarn

### Installation

1. **Clone or download the repository**

2. **Install Python dependencies**
```bash
pip install -r requirements.txt
```

3. **Install Node.js dependencies (for frontend)**
```bash
cd frontend
npm install
cd ..
```

### Running the Application

#### Option 1: Full Stack (Recommended)
Double-click `start_app.bat` or run:
```bash
start_app.bat
```
This starts both backend and frontend automatically!

#### Option 2: Manual Start

**Backend (Terminal 1):**
```bash
python api.py
# or
start_backend.bat
```

**Frontend (Terminal 2):**
```bash
cd frontend
npm start
# or
start_frontend.bat
```

### Accessing the Application
- **Frontend UI**: http://localhost:3000
- **Backend API**: http://localhost:5000
- **API Docs**: http://localhost:5000/api/health

## 📖 Usage

### Web Interface

1. **Open your browser** to http://localhost:3000
2. **Enter a URL** you want to scrape
3. **Select scraping depth**:
   - Depth 0: Single page only (fastest)
   - Depth 1: Include linked pages (1 level deep)
   - Depth 2: Include linked pages (2 levels deep)
4. **Choose AI formatting** (recommended for clean output)
5. **Optional**: Enter custom filename
6. **Click "Start Scraping"**
7. **View results** and download the file

### Command Line Mode (Legacy)
```bash
python website_scraper.py
python website_scraper.py https://example.com

# With custom filename
python website_scraper.py https://example.com my_content.txt

# With recursive depth
python website_scraper.py https://example.com my_content.txt 1

# Recursive with auto-generated filename
python website_scraper.py https://example.com "" 2

# Disable AI formatting (command line)
python website_scraper.py https://example.com my_content.txt 0 false
```

## Output

All scraped content is saved as `.txt` files in the `C:\Crystal_Scraper` directory.

### Single Page Format:
```
================================================================================
SCRAPED WEBSITE CONTENT
================================================================================
URL: https://example.com
Title: Example Domain
Scraped on: 2025-10-30 12:52:43
Success: True
Scrape time: 0.97 seconds
================================================================================
CONTENT:
================================================================================

[Website content here]

================================================================================
END OF CONTENT
================================================================================
```

### Recursive Format:
```
================================================================================
SCRAPED WEBSITE CONTENT
================================================================================
URL: https://example.com
Title: Example Domain (Recursive - 5 pages)
Scraped on: 2025-10-30 12:52:43
Success: True
Scrape time: 15.43 seconds
Content type: text/recursive
Total pages scraped: 5
Max depth used: 2
Scraped URLs:
  1. https://example.com
  2. https://example.com/about
  3. https://example.com/contact
  4. https://example.com/services
  5. https://example.com/blog
================================================================================
CONTENT:
================================================================================

================================================================================
PAGE 1 OF 5: Example Domain
URL: https://example.com
================================================================================

[Page 1 content here]

================================================================================
END OF PAGE 1
================================================================================

================================================================================
PAGE 2 OF 5: About Us
URL: https://example.com/about
================================================================================

[Page 2 content here]

================================================================================
END OF PAGE 2
================================================================================

[... additional pages ...]

================================================================================
END OF CONTENT
================================================================================
```

## File Naming

- **Auto-generated**: `domain.com_YYYYMMDD_HHMMSS.txt`
- **Custom**: Whatever you specify (`.txt` extension added automatically)

## Examples

1. **Interactive scraping with recursion**:
   ```
   Enter the URL to scrape: reddit.com
   Enter scraping depth (0, 1, or 2) [default: 0]: 1
   Enter custom filename (or press Enter for auto-generated): reddit_content
   ```
   → Saves as `reddit_content.txt` with linked pages included

2. **Quick single page**:
   ```bash
   python website_scraper.py news.ycombinator.com
   ```
   → Saves as `news.ycombinator.com_20251030_125243.txt`

3. **Recursive command line**:
   ```bash
   python website_scraper.py https://blog.example.com blog_archive.txt 2
   ```
   → Saves as `blog_archive.txt` with 2 levels of linked pages

## Requirements

- Python 3.7+
- Required packages are managed by the scraper module
- Internet connection for web scraping

## Error Handling

- Invalid URLs are automatically prefixed with `https://`
- Failed scrapes still create output files with error details
- All errors are logged and saved to the output file
- Recursive scraping falls back to single page if needed

## Performance Notes

- **Single page (depth 0)**: Fastest, typically 1-3 seconds
- **Depth 1**: Moderate, depends on number of linked pages
- **Depth 2**: Slowest, can take several minutes for large sites

⚠️ **Recursive scraping warning**: Higher depths can generate large files and take significant time. Start with depth 1 to test.

## Recent Updates

✅ **NEW: AI-Powered Content Formatting**
- Added Together AI and Google Gemini integration
- Automatic removal of CSS, JavaScript, and HTML artifacts
- Clean markdown formatting with proper structure
- Removal of navigation, ads, and boilerplate content
- Enhanced readability and professional presentation

✅ **NEW: Recursive Scraping Support**
- Added depth control (0, 1, 2 levels)
- Interactive prompts for recursion depth
- Combined multi-page output format
- Fallback to single page if recursive fails
- Improved command line argument parsing

Enjoy scraping with Crystal Scraper! 🔍✨