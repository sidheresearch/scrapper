#!/usr/bin/env python3
"""
Interactive Website Scraper with Recursive Capabilities
A script to scrape content from websites with optional recursive link following.

Usage:
1. Run without arguments for interactive mode: python website_scraper.py
2. Run with URL argument: python website_scraper.py <URL> [output_filename] [depth]

Features:
- Interactive user input for URL and recursion depth
- Recursive scraping with depth control (0, 1, or 2 levels)
- Custom filename option
- Saves output to root directory as text file
- Auto-generates filename from URL if not specified
- Detailed content formatting with metadata
- Combines multiple pages for recursive scrapes

Recursion Depths:
- 0: Single page only (fastest)
- 1: Include linked pages (1 level deep)
- 2: Include linked pages (2 levels deep)
"""

import asyncio
import sys
import os
import logging
from datetime import datetime
from pathlib import Path

# Add the src directory to the path so we can import our scraper
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from scraper import Scraper, ScrapedContent


def setup_logging():
    """Set up logging configuration."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(),
        ]
    )


def sanitize_filename(url: str) -> str:
    """Create a safe filename from a URL."""
    # Remove protocol and replace invalid characters
    filename = url.replace('https://', '').replace('http://', '')
    filename = filename.replace('/', '_').replace('\\', '_')
    filename = filename.replace(':', '_').replace('?', '_').replace('&', '_')
    filename = filename.replace('<', '_').replace('>', '_').replace('|', '_')
    filename = filename.replace('"', '_').replace('*', '_')
    
    # Limit length and add timestamp
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
        # Handle recursive metadata specially
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
    
    if content.success and content.text:
        output.append(content.text)
    else:
        output.append("No content extracted or scraping failed.")
    
    output.append("")
    output.append("=" * 80)
    output.append("END OF CONTENT")
    output.append("=" * 80)
    
    return "\n".join(output)


async def scrape_website_to_file(url: str, output_file: str = None, output_dir: str = ".", depth: int = 0, use_llm: bool = True) -> str:
    """
    Scrape a website and save the content to a text file.
    
    Args:
        url (str): The URL of the website to scrape
        output_file (str, optional): Custom output filename. If None, auto-generates from URL
        output_dir (str): Directory to save the output file (default: current directory)
        depth (int): Recursive scraping depth (0=single page, 1-2=include linked pages)
        use_llm (bool): Whether to use LLM for content formatting
    
    Returns:
        str: Path to the saved file
    """
    setup_logging()
    
    # Validate URL
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    
    if depth > 0:
        logging.info(f"Starting recursive scraping: {url} (depth: {depth}, LLM: {'enabled' if use_llm else 'disabled'})")
    else:
        logging.info(f"Starting single page scraping: {url} (LLM: {'enabled' if use_llm else 'disabled'})")
    
    # Initialize scraper
    scraper = Scraper(llm_enabled=use_llm)
    
    try:
        # Choose scraping method based on depth
        if depth > 0:
            content = await scraper.scrape_recursive(url, max_depth=depth)
        else:
            content = await scraper.scrape_url(url)
        
        # Create output directory if it doesn't exist
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)
        
        # Generate filename if not provided
        if output_file is None:
            output_file = sanitize_filename(url)
        
        # Ensure the file has .txt extension
        if not output_file.endswith('.txt'):
            output_file += '.txt'
        
        # Full path to output file
        file_path = output_path / output_file
        
        # Format and save content
        formatted_content = format_scraped_content(content)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(formatted_content)
        
        if content.success:
            logging.info(f"Successfully scraped and saved to: {file_path}")
            logging.info(f"Content length: {len(content.text)} characters")
        else:
            logging.error(f"Scraping failed: {content.error}")
            logging.info(f"Error details saved to: {file_path}")
        
        return str(file_path)
        
    except Exception as e:
        error_msg = f"Error during scraping: {str(e)}"
        logging.error(error_msg)
        
        # Save error to file anyway
        if output_file is None:
            output_file = sanitize_filename(url)
        
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)
        file_path = output_path / output_file
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(f"SCRAPING ERROR\n")
            f.write(f"URL: {url}\n")
            f.write(f"Error: {error_msg}\n")
            f.write(f"Timestamp: {datetime.now()}\n")
        
        return str(file_path)


def get_user_input():
    """
    Get URL input from the user interactively.
    
    Returns:
        tuple: (url, custom_filename, depth, use_llm) where custom_filename can be None
    """
    print("=" * 60)
    print("CRYSTAL SCRAPER - Website Content Extractor")
    print("=" * 60)
    print()
    
    # Get URL from user
    while True:
        url = input("Enter the URL to scrape: ").strip()
        if not url:
            print("Please enter a valid URL.")
            continue
        
        # Add https:// if no protocol specified
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        
        break
    
    # Ask about recursive scraping depth
    print()
    print("Scraping Depth Options:")
    print("  0 - Single page only (fastest)")
    print("  1 - Include linked pages (1 level deep)")
    print("  2 - Include linked pages (2 levels deep)")
    print()
    
    while True:
        depth_input = input("Enter scraping depth (0, 1, or 2) [default: 0]: ").strip()
        if not depth_input:
            depth = 0
            break
        
        try:
            depth = int(depth_input)
            if depth in [0, 1, 2]:
                break
            else:
                print("Please enter 0, 1, or 2.")
        except ValueError:
            print("Please enter a valid number (0, 1, or 2).")
    
    # Ask about LLM formatting
    print()
    print("Content Formatting Options:")
    print("  y - Use AI to clean and format content (recommended)")
    print("  n - Keep raw scraped content")
    print()
    
    use_llm_input = input("Use AI formatting? (Y/n) [default: Y]: ").strip().lower()
    use_llm = use_llm_input not in ['n', 'no']
    
    # Ask if user wants custom filename
    print()
    custom_filename = input("Enter custom filename (or press Enter for auto-generated): ").strip()
    if not custom_filename:
        custom_filename = None
    elif not custom_filename.endswith('.txt'):
        custom_filename += '.txt'
    
    # Show summary
    print()
    print("-" * 40)
    print("SCRAPING SUMMARY:")
    print(f"URL: {url}")
    print(f"Depth: {depth} ({'Single page' if depth == 0 else f'{depth} level(s) deep'})")
    print(f"AI Formatting: {'Enabled' if use_llm else 'Disabled'}")
    if custom_filename:
        print(f"Output file: {custom_filename}")
    else:
        print("Output file: Auto-generated based on URL")
    print(f"Save location: {os.path.abspath('.')}")
    print("-" * 40)
    print()
    
    # Confirm before proceeding
    confirm = input("Proceed with scraping? (y/N): ").strip().lower()
    if confirm not in ['y', 'yes']:
        print("Operation cancelled.")
        sys.exit(0)
    
    return url, custom_filename, depth, use_llm


async def main():
    """
    Main function for both command-line and interactive usage.
    """
    # Check if URL was provided as command line argument
    if len(sys.argv) >= 2:
        # Command line mode
        url = sys.argv[1]
        
        # Parse optional arguments
        output_file = None
        depth = 0
        use_llm = True  # Default to enabled for command line
        
        if len(sys.argv) >= 3:
            # Check if second argument is a depth (number) or filename
            try:
                # If it's a number, it's depth, no filename
                depth = int(sys.argv[2])
                output_file = None
            except ValueError:
                # If not a number, it's a filename
                output_file = sys.argv[2]
                # Check for depth as third argument
                if len(sys.argv) >= 4:
                    try:
                        depth = int(sys.argv[3])
                    except ValueError:
                        depth = 0
                # Check for LLM flag as fourth argument
                if len(sys.argv) >= 5:
                    use_llm = sys.argv[4].lower() not in ['false', 'no', '0']
        
        output_dir = "."  # Save to root directory
    else:
        # Interactive mode
        try:
            url, output_file, depth, use_llm = get_user_input()
            output_dir = "."  # Save to root directory
        except KeyboardInterrupt:
            print("\nOperation cancelled by user.")
            sys.exit(0)
    
    try:
        file_path = await scrape_website_to_file(url, output_file, output_dir, depth, use_llm)
        print(f"\nScraping completed! Content saved to: {file_path}")
        print(f"File location: {os.path.abspath(file_path)}")
    except KeyboardInterrupt:
        print("\nScraping interrupted by user.")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
