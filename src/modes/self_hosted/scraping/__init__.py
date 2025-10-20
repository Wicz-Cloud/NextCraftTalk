"""
Web Scraping Module
"""

from .wiki_scraper import (
    ContentProcessor,
    WikiScraper,
    get_content_processor,
    get_wiki_scraper,
)

__all__ = [
    "WikiScraper",
    "ContentProcessor",
    "get_wiki_scraper",
    "get_content_processor",
]
