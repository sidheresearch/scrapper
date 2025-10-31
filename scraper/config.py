# config.py

USE_PERSISTENCE = False        # Toggle ChromaDB disk usage
MAX_RESULTS = 15               # Search results per query
CACHE_TTL = 86400              # Time-to-live for cached results (24 hours)
CACHE_ENABLED = True

REPORT_FORMAT = "both"          # Options: "pdf", "txt", or "both"
REPORT_FILENAME_PDF = "Crystal_Scraper.pdf"
REPORT_FILENAME_TEXT = "Crystal_Scraper.txt"

# LLM Configuration
LLM_ENABLED = True             # Enable/disable LLM content formatting
LLM_PROVIDER = "together"      # Options: "together", "gemini", "openai", "claude"
LLM_MODEL = "openai/gpt-oss-20b"  # Together model for content formatting
LLM_TEMPERATURE = 0.2          # Temperature for content formatting
LLM_MAX_TOKENS = 20000         # Maximum tokens for LLM response

# Performance tuning
MAX_SEARCH_QUERIES = 15
MAX_CONCURRENT_SCRAPES = 5     # Parallel scraping limit
MAX_SEARCH_RETRIES = 3        # Retry attempts per engine
MAX_AI_ITERATIONS = 6             # Max refinement loops during extraction
MAX_USER_QUERY_LOOPS = 3

# Scraping behavior
DEFAULT_USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
)

DEFAULT_REFERER = "https://www.google.com/"
URL_TIMEOUT = 60
SKIP_EXTENSIONS = []

RED = '\033[91m'
GREEN = '\033[92m'
BLUE = '\033[94m'
YELLOW = '\033[93m'
ENDC = '\033[0m'

CHUNK_SIZE = 1000
CHUNK_OVERLAP = 100

