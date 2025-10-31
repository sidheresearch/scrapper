#scraper.py
import logging, time, asyncio, os
from urllib.parse import urlparse
from typing import Dict, Any, List, Optional, Union
from .config import CACHE_ENABLED, CACHE_TTL, LLM_ENABLED, LLM_PROVIDER, LLM_MODEL, LLM_TEMPERATURE, LLM_MAX_TOKENS
from langchain_community.document_loaders.recursive_url_loader import RecursiveUrlLoader
from dataclasses import dataclass, field

#=======================================================================================
# Define caching
class SimpleCache:
    def __init__(self, ttl: int = 3600):
        self._cache: Dict[str, Any] = {}
        self._timestamps: Dict[str, float] = {}
        self._ttl = ttl

    def get(self, key: str) -> Optional[Any]:
        if key in self._cache and time.time() - self._timestamps.get(key, 0) < self._ttl:
            return self._cache[key]
        self._cache.pop(key, None)
        self._timestamps.pop(key, None)
        return None

    def set(self, key: str, value: Any):
        self._cache[key] = value
        self._timestamps[key] = time.time()


# Assuming CACHE_ENABLED and CACHE_TTL are globally available from setup.py or config.py
from .config import CACHE_ENABLED, CACHE_TTL # Example import

# Initialize cache
# Ensure CACHE_ENABLED and CACHE_TTL are defined before this in your environment/setup
try:
    # Define a default TTL if CACHE_TTL is not found
    default_ttl = 3600 # Default to 1 hour if CACHE_TTL is not defined

    # Check if CACHE_ENABLED is defined, default to False if not
    cache_enabled = globals().get('CACHE_ENABLED', True)
    cache_ttl = globals().get('CACHE_TTL', default_ttl)


    if cache_enabled:
        cache = SimpleCache(ttl=cache_ttl)
        logging.info(f"Cache initialized with TTL={cache_ttl}s")
    else:
        cache = None # Cache disabled
        logging.info("Caching is disabled.")

except NameError as e:
    logging.warning(f"Cache related variable not found: {e}. Caching will be disabled.")
    cache = None

#=======================================================================================
# Initialize LLM for content formatting
llm_formatter = None

try:
    if LLM_ENABLED:
        # --- Configuration ---
        # Together API calling
        together1 = "openai/gpt-oss-20b"  # check if this model is running properly
        TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY")
        GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
        TOGETHER_MODEL = together1

        # LLM calling with langchain chat client
        try:
            if TOGETHER_API_KEY:
                from langchain_together import ChatTogether
                llm_formatter = ChatTogether(
                    model=TOGETHER_MODEL, 
                    temperature=LLM_TEMPERATURE, 
                    max_tokens=LLM_MAX_TOKENS, 
                    timeout=None, 
                    max_retries=4, 
                    together_api_key=TOGETHER_API_KEY
                )
                logging.info(f"Initialized ChatTogether (llm_formatter) with {TOGETHER_MODEL}")
            elif GOOGLE_API_KEY:
                from langchain_google_genai import ChatGoogleGenerativeAI
                llm_formatter = ChatGoogleGenerativeAI(
                    model="gemini-2.0-flash-lite", 
                    temperature=0, 
                    google_api_key=GOOGLE_API_KEY
                )
                logging.info("Initialized ChatGoogleGenerativeAI (llm_formatter) with gemini-2.0-flash-lite")
            else:
                logging.error("No API key available for initializing llm_formatter (Together or Google).")

        except Exception as e:
            llm_formatter = None
            logging.error(f"Failed to initialize llm_formatter model: {e}")
    else:
        logging.info("LLM formatting is disabled in config")
        
except Exception as e:
    logging.warning(f"Failed to initialize LLM formatter: {e}")
    llm_formatter = None

#=======================================================================================
# Define dataclass
@dataclass
class ScrapedContent:
    url: str
    title: str = ""
    text: str = ""
    html: Optional[str] = None
    content_type: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    success: bool = False
    error: Optional[str] = None
    scrape_time: float = 0.0

    def is_successful(self) -> bool:
        return self.success

    def to_dict(self) -> Dict[str, Any]:
        return self.__dict__

#=======================================================================================
# main method
class Scraper:
    def __init__(self, cache_enabled: bool = CACHE_ENABLED, cache_ttl: int = CACHE_TTL, llm_enabled: bool = True):
        self.cache = SimpleCache(ttl=cache_ttl) if cache_enabled else None
        self._cache_enabled = cache_enabled
        self._llm_enabled = llm_enabled and LLM_ENABLED  # Both user choice and config must be True

    async def _scrape_with_aiohttp(self, url: str) -> ScrapedContent:
        import aiohttp
        from bs4 import BeautifulSoup
        start = time.time()
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, timeout=30) as response:
                    html = await response.text()
                    soup = BeautifulSoup(html, "html.parser")
                    title = soup.title.string if soup.title else url
                    raw_text = soup.get_text(separator="\n", strip=True)
                    
                    # Format content with LLM if available
                    formatted_text = await self.format_content_with_llm(raw_text, title)
                    
                    return ScrapedContent(
                        url=url,
                        title=title,
                        text=formatted_text,
                        html=html,
                        success=True,
                        scrape_time=time.time() - start
                    )
        except Exception as e:
            return ScrapedContent(url=url, success=False, error=str(e), scrape_time=time.time() - start)

    async def _scrape_with_requests_html(self, url: str) -> ScrapedContent:
        from requests_html import AsyncHTMLSession
        start = time.time()
        try:
            session = AsyncHTMLSession()
            r = await session.get(url, timeout=30)
            raw_text = r.html.full_text
            title = r.html.find("title", first=True).text if r.html.find("title", first=True) else url
            
            # Format content with LLM if available
            formatted_text = await self.format_content_with_llm(raw_text, title)
            
            return ScrapedContent(
                url=url,
                title=title,
                text=formatted_text,
                html=r.html.html,
                success=True,
                scrape_time=time.time() - start
            )
        except Exception as e:
            return ScrapedContent(url=url, success=False, error=str(e), scrape_time=time.time() - start)

    async def _scrape_with_playwright(self, url: str) -> ScrapedContent:
        from playwright.async_api import async_playwright
        start = time.time()
        try:
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=True)
                page = await browser.new_page()
                await page.goto(url, timeout=30000)
                html = await page.content()
                raw_text = await page.inner_text("body")
                title = await page.title()
                await browser.close()
                
                # Format content with LLM if available
                formatted_text = await self.format_content_with_llm(raw_text, title)
                
                return ScrapedContent(
                    url=url,
                    title=title,
                    text=formatted_text,
                    html=html,
                    success=True,
                    scrape_time=time.time() - start
                )
        except Exception as e:
            return ScrapedContent(url=url, success=False, error=str(e), scrape_time=time.time() - start)

    async def _scrape_with_selenium(self, url: str) -> ScrapedContent:
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options
        from bs4 import BeautifulSoup
        start = time.time()
        try:
            options = Options()
            options.add_argument("--headless")
            options.add_argument("--disable-gpu")
            options.add_argument("--no-sandbox")
            driver = webdriver.Chrome(options=options)
            driver.get(url)
            time.sleep(2)
            html = driver.page_source
            soup = BeautifulSoup(html, "html.parser")
            driver.quit()
            
            title = soup.title.string if soup.title else url
            raw_text = soup.get_text(separator="\n", strip=True)
            
            # Format content with LLM if available
            formatted_text = await self.format_content_with_llm(raw_text, title)
            
            return ScrapedContent(
                url=url,
                title=title,
                text=formatted_text,
                html=html,
                success=True,
                scrape_time=time.time() - start
            )
        except Exception as e:
            return ScrapedContent(url=url, success=False, error=str(e), scrape_time=time.time() - start)

    async def scrape_url(self, url: str, dynamic: bool = False) -> ScrapedContent:
        logging.info(f"Scraping: {url}")

        # Check cache
        if self._cache_enabled and self.cache:
            cached = self.cache.get(url)
            if cached:
                try:
                    return ScrapedContent(**cached)
                except Exception as e:
                    logging.warning(f"Cache load failed: {e}")

        # Strategy list
        strategies = [
            self._scrape_with_aiohttp,
            self._scrape_with_playwright,
            self._scrape_with_selenium
        ]

        # Execute strategies
        for strategy in strategies:
            result = await strategy(url)
            logging.debug(f"{strategy.__name__} took {result.scrape_time:.2f}s")
            if result.is_successful():
                if self._cache_enabled and self.cache:
                    self.cache.set(url, result.to_dict())
                return result
            else:
                logging.warning(f"{strategy.__name__} failed: {result.error}")

        return ScrapedContent(url=url, success=False, error="All strategies failed.")

    async def scrape_recursive(self, url: str, max_depth: int = 1) -> ScrapedContent:
        """
        Scrape a URL recursively up to the specified depth.
        
        Args:
            url (str): The starting URL to scrape
            max_depth (int): Maximum depth to follow links (0=single page, 1-2=follow links)
        
        Returns:
            ScrapedContent: Combined content from all scraped pages
        """
        start_time = time.time()
        
        try:
            if max_depth == 0:
                # Single page scraping
                return await self.scrape_url(url)
            
            # For now, use a simple approach: scrape the main page and fall back if recursive fails
            logging.info(f"Starting recursive scraping of {url} with depth {max_depth}")
            
            try:
                # Try using RecursiveUrlLoader with simplified settings
                loader = RecursiveUrlLoader(
                    url=url,
                    max_depth=max_depth,
                    use_async=False,
                    check_response_status=True,
                    continue_on_failure=True,
                    timeout=30,
                    prevent_outside=True
                )
                
                # Load documents - run in thread since it's blocking
                loop = asyncio.get_event_loop()
                docs = await loop.run_in_executor(None, loader.load)
                
                if docs and len(docs) > 0:
                    # Combine all content
                    combined_text = []
                    total_pages = len(docs)
                    
                    for i, doc in enumerate(docs, 1):
                        page_url = doc.metadata.get('source', 'Unknown URL') if hasattr(doc, 'metadata') else 'Unknown URL'
                        page_title = doc.metadata.get('title', f'Page {i}') if hasattr(doc, 'metadata') else f'Page {i}'
                        raw_page_content = doc.page_content if hasattr(doc, 'page_content') else str(doc)
                        
                        # Parse HTML to extract clean text if content looks like HTML
                        from bs4 import BeautifulSoup
                        if raw_page_content.strip().startswith('<!') or raw_page_content.strip().startswith('<html'):
                            soup = BeautifulSoup(raw_page_content, 'html.parser')
                            # Remove script and style elements
                            for script in soup(["script", "style", "meta", "link", "noscript"]):
                                script.decompose()
                            raw_page_content = soup.get_text(separator='\n', strip=True)
                        
                        # Format each page's content with LLM
                        formatted_page_content = await self.format_content_with_llm(raw_page_content, page_title)
                        
                        combined_text.append(f"\n{'='*80}")
                        combined_text.append(f"PAGE {i} OF {total_pages}: {page_title}")
                        combined_text.append(f"URL: {page_url}")
                        combined_text.append(f"{'='*80}\n")
                        combined_text.append(formatted_page_content)
                        combined_text.append(f"\n{'='*80}")
                        combined_text.append(f"END OF PAGE {i}")
                        combined_text.append(f"{'='*80}\n")
                    
                    scrape_time = time.time() - start_time
                    
                    # Create main title from first page
                    first_doc = docs[0]
                    main_title = first_doc.metadata.get('title', 'Recursive Scrape') if hasattr(first_doc, 'metadata') else 'Recursive Scrape'
                    
                    return ScrapedContent(
                        url=url,
                        title=f"{main_title} (Recursive - {total_pages} pages)",
                        text='\n'.join(combined_text),
                        html=None,  # HTML not preserved in recursive mode
                        content_type="text/recursive",
                        metadata={
                            'total_pages': total_pages,
                            'max_depth': max_depth,
                            'scraped_urls': [doc.metadata.get('source') if hasattr(doc, 'metadata') else 'Unknown' for doc in docs]
                        },
                        success=True,
                        scrape_time=scrape_time
                    )
                else:
                    # No documents found, fall back to single page
                    logging.warning("No documents found in recursive scraping, falling back to single page")
                    return await self.scrape_url(url)
                    
            except Exception as recursive_error:
                logging.warning(f"Recursive scraping failed: {recursive_error}, falling back to single page")
                # Fall back to single page scraping
                result = await self.scrape_url(url)
                # Update title to indicate attempted recursion
                if result.success:
                    result.title = f"{result.title} (Recursive attempt failed, single page only)"
                    result.metadata['attempted_depth'] = max_depth
                    result.metadata['fallback_reason'] = str(recursive_error)
                return result
            
        except Exception as e:
            scrape_time = time.time() - start_time
            logging.error(f"Complete scraping failed: {e}")
            return ScrapedContent(
                url=url,
                title="Scraping Failed",
                text="",
                success=False,
                error=f"Scraping failed: {str(e)}",
                scrape_time=scrape_time
            )

    async def format_content_with_llm(self, content: str, title: str = "") -> str:
        """
        Format scraped content using LLM to remove CSS, placeholders, and improve readability.
        
        Args:
            content (str): Raw scraped content
            title (str): Page title for context
            
        Returns:
            str: Formatted content
        """
        if not self._llm_enabled or not llm_formatter or not content.strip():
            return content
            
        try:
            # Create formatting prompt
            formatting_prompt = f"""
Please clean and format the following web content to make it readable and well-structured:

TITLE: {title}

CONTENT:
{content}

Please:
1. Remove all CSS styling, JavaScript code, and HTML artifacts
2. Remove navigation menus, headers, footers, and sidebars that are not main content
3. Remove placeholder text like "Lorem ipsum", "Click here", etc.
4. Format the text with proper headings, paragraphs, and bullet points
5. Preserve important information like dates, names, numbers, and links
6. Use markdown formatting for better readability
7. Remove repetitive or boilerplate content
8. Keep only the main content that a human reader would find valuable

Return only the cleaned, formatted content without any additional commentary.
"""

            # Get formatted content from LLM
            response = await asyncio.to_thread(llm_formatter.invoke, formatting_prompt)
            formatted_content = response.content if hasattr(response, 'content') else str(response)
            
            # Validate that we got meaningful content back
            if len(formatted_content.strip()) < 50:  # Too short, probably failed
                logging.warning("LLM formatting produced very short content, using original")
                return content
                
            logging.info("Content successfully formatted with LLM")
            return formatted_content.strip()
            
        except Exception as e:
            logging.warning(f"LLM formatting failed: {e}, using original content")
            return content
