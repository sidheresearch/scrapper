#!/usr/bin/env python3
"""
Flask REST API for Crystal Scraper
Provides endpoints for web scraping functionality
"""

from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import asyncio
import os
import logging
from datetime import datetime
from pathlib import Path
import sys

# Add the scraper to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'scraper'))

from scraper import Scraper, ScrapedContent

# Initialize Flask app
app = Flask(__name__)

# Enable CORS with specific configuration
CORS(app, resources={
    r"/api/*": {
        "origins": ["http://localhost:3000", "http://localhost:3001", "http://127.0.0.1:3000", "http://127.0.0.1:3001"],
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type"]
    }
})

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Store scraping results temporarily
scraping_results = {}

def sanitize_filename(url: str) -> str:
    """Create a safe filename from a URL."""
    filename = url.replace('https://', '').replace('http://', '')
    filename = filename.replace('/', '_').replace('\\', '_')
    filename = filename.replace(':', '_').replace('?', '_').replace('&', '_')
    filename = filename.replace('<', '_').replace('>', '_').replace('|', '_')
    filename = filename.replace('"', '_').replace('*', '_')
    
    if len(filename) > 100:
        filename = filename[:100]
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{filename}_{timestamp}.txt"


def format_scraped_content(content: ScrapedContent) -> str:
    """Format the scraped content for saving to file."""
    output = []
    output.append("=" * 80)
    output.append("SCRAPED WEBSITE CONTENT")
    output.append("=" * 80)
    output.append(f"URL: {content.url}")
    output.append(f"Title: {content.title}")
    output.append(f"Scraped on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    output.append(f"Success: {content.success}")
    
    if content.error:
        output.append(f"Error: {content.error}")
    
    output.append(f"Scrape time: {content.scrape_time:.2f} seconds")
    
    if content.content_type:
        output.append(f"Content type: {content.content_type}")
    
    if content.metadata:
        if 'total_pages' in content.metadata:
            output.append(f"Total pages scraped: {content.metadata['total_pages']}")
            output.append(f"Max depth used: {content.metadata['max_depth']}")
            if 'scraped_urls' in content.metadata:
                output.append("Scraped URLs:")
                for i, scraped_url in enumerate(content.metadata['scraped_urls'], 1):
                    output.append(f"  {i}. {scraped_url}")
        else:
            output.append(f"Metadata: {content.metadata}")
    
    output.append("=" * 80)
    output.append("CONTENT:")
    output.append("=" * 80)
    output.append("")
    output.append(content.text)
    output.append("")
    output.append("=" * 80)
    output.append("END OF SCRAPED CONTENT")
    output.append("=" * 80)
    
    return '\n'.join(output)


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'Crystal Scraper API',
        'version': '1.0.0'
    })


@app.route('/api/scrape', methods=['POST'])
def scrape_website():
    """
    Scrape a website
    
    Request body:
    {
        "url": "https://example.com",
        "depth": 0-2 (optional, default: 0),
        "llm_enabled": true/false (optional, default: true),
        "filename": "custom_name" (optional)
    }
    """
    try:
        data = request.get_json()
        
        if not data or 'url' not in data:
            return jsonify({'error': 'URL is required'}), 400
        
        url = data['url']
        depth = data.get('depth', 0)
        llm_enabled = data.get('llm_enabled', True)
        custom_filename = data.get('filename', '')
        
        # Validate depth
        if depth not in [0, 1, 2]:
            return jsonify({'error': 'Depth must be 0, 1, or 2'}), 400
        
        # Validate URL
        if not url.startswith('http://') and not url.startswith('https://'):
            return jsonify({'error': 'URL must start with http:// or https://'}), 400
        
        logging.info(f"API: Scraping {url} with depth {depth}, LLM: {llm_enabled}")
        
        # Create scraper instance
        scraper = Scraper(llm_enabled=llm_enabled)
        
        # Run scraping
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        if depth > 0:
            result = loop.run_until_complete(scraper.scrape_recursive(url, max_depth=depth))
        else:
            result = loop.run_until_complete(scraper.scrape_url(url))
        
        loop.close()
        
        if not result.success:
            return jsonify({
                'success': False,
                'error': result.error or 'Scraping failed'
            }), 500
        
        # Generate filename
        if custom_filename:
            filename = f"{custom_filename}.txt"
        else:
            filename = sanitize_filename(url)
        
        # Format and save content
        formatted_content = format_scraped_content(result)
        output_path = os.path.join(os.path.dirname(__file__), filename)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(formatted_content)
        
        # Store result for potential download
        result_id = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        scraping_results[result_id] = {
            'filename': filename,
            'path': output_path,
            'url': url,
            'timestamp': datetime.now().isoformat()
        }
        
        # Prepare response
        response_data = {
            'success': True,
            'result_id': result_id,
            'url': url,
            'title': result.title,
            'scrape_time': result.scrape_time,
            'filename': filename,
            'content_preview': result.text[:500] + '...' if len(result.text) > 500 else result.text,
            'total_length': len(result.text),
            'metadata': result.metadata
        }
        
        logging.info(f"API: Successfully scraped {url}")
        return jsonify(response_data)
        
    except Exception as e:
        logging.error(f"API Error: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/download/<result_id>', methods=['GET'])
def download_result(result_id):
    """Download scraped content as a text file"""
    try:
        if result_id not in scraping_results:
            return jsonify({'error': 'Result not found'}), 404
        
        result_info = scraping_results[result_id]
        file_path = result_info['path']
        
        if not os.path.exists(file_path):
            return jsonify({'error': 'File not found'}), 404
        
        return send_file(
            file_path,
            as_attachment=True,
            download_name=result_info['filename'],
            mimetype='text/plain'
        )
        
    except Exception as e:
        logging.error(f"Download Error: {str(e)}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/results/<result_id>', methods=['GET'])
def get_result_details(result_id):
    """Get details of a scraping result"""
    try:
        if result_id not in scraping_results:
            return jsonify({'error': 'Result not found'}), 404
        
        result_info = scraping_results[result_id]
        file_path = result_info['path']
        
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            return jsonify({
                'result_id': result_id,
                'filename': result_info['filename'],
                'url': result_info['url'],
                'timestamp': result_info['timestamp'],
                'content': content,
                'file_size': os.path.getsize(file_path)
            })
        else:
            return jsonify({'error': 'File not found'}), 404
            
    except Exception as e:
        logging.error(f"Get Result Error: {str(e)}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/results', methods=['GET'])
def list_results():
    """List all available scraping results"""
    try:
        results_list = []
        for result_id, info in scraping_results.items():
            if os.path.exists(info['path']):
                results_list.append({
                    'result_id': result_id,
                    'filename': info['filename'],
                    'url': info['url'],
                    'timestamp': info['timestamp'],
                    'file_size': os.path.getsize(info['path'])
                })
        
        return jsonify({
            'results': results_list,
            'count': len(results_list)
        })
        
    except Exception as e:
        logging.error(f"List Results Error: {str(e)}")
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    print("=" * 60)
    print("Crystal Scraper API Server")
    print("=" * 60)
    print("API Documentation:")
    print("  POST   /api/scrape          - Scrape a website")
    print("  GET    /api/results         - List all results")
    print("  GET    /api/results/<id>    - Get result details")
    print("  GET    /api/download/<id>   - Download result file")
    print("  GET    /api/health          - Health check")
    print("=" * 60)
    
    # Use PORT from environment variable (for Render) or default to 5000
    port = int(os.environ.get('PORT', 5000))
    print(f"\nStarting server on http://0.0.0.0:{port}")
    print("Press CTRL+C to stop the server\n")
    
    app.run(debug=False, host='0.0.0.0', port=port)
