"""
Web Scraping Module for Self-Hosted Mode

Scrapes wiki pages and other web content to build knowledge base.
"""

import json
import logging
import time
from pathlib import Path
from typing import Any, Dict, List, Optional
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)


class WikiScraper:
    """Scraper for wiki and documentation sites"""

    def __init__(self, base_url: str, delay: float = 1.0):
        self.base_url = base_url.rstrip("/")
        self.delay = delay
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": "NextCraftTalk/1.0 (Knowledge Base Builder)"})

    def scrape_page(self, url: str) -> Optional[Dict[str, Any]]:
        """Scrape a single page and extract content"""
        try:
            time.sleep(self.delay)  # Be respectful to servers

            response = self.session.get(url, timeout=30, allow_redirects=False)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, "html.parser")

            # Extract title
            title = soup.find("title")
            title_text = title.get_text().strip() if title else url

            # Extract main content (customize selectors based on wiki structure)
            content_selectors = [".mw-parser-output", "main", ".content", "#content"]
            content = None

            for selector in content_selectors:
                content_elem = soup.select_one(selector)
                if content_elem:
                    content = content_elem.get_text(separator="\n", strip=True)
                    break

            if not content:
                # Fallback to body text
                content = soup.body.get_text(separator="\n", strip=True) if soup.body else ""

            return {
                "url": url,
                "title": title_text,
                "content": content,
                "scraped_at": time.time(),
            }

        except Exception as e:
            logger.error(f"Error scraping {url}: {e}")
            return None

    def scrape_wiki_pages(self, start_url: str, max_pages: int = 50) -> List[Dict[str, Any]]:
        """Scrape multiple wiki pages starting from a given URL"""
        scraped_pages: List[Dict[str, Any]] = []
        visited_urls = set()
        urls_to_visit = [start_url]

        while urls_to_visit and len(scraped_pages) < max_pages:
            current_url = urls_to_visit.pop(0)

            if current_url in visited_urls:
                continue

            visited_urls.add(current_url)
            logger.info(f"Scraping: {current_url}")

            page_data = self.scrape_page(current_url)
            if page_data:
                scraped_pages.append(page_data)

                # Find links to other wiki pages (customize based on wiki structure)
                try:
                    response = self.session.get(current_url, timeout=30)
                    soup = BeautifulSoup(response.content, "html.parser")

                    for link in soup.find_all("a", href=True):
                        href = link["href"]
                        if href.startswith("/"):  # Relative link
                            full_url = urljoin(self.base_url, href)
                        elif href.startswith(self.base_url):  # Absolute link on same domain
                            full_url = href
                        else:
                            continue

                        # Only follow links within the wiki
                        if full_url.startswith(self.base_url) and full_url not in visited_urls:
                            urls_to_visit.append(full_url)

                except Exception as e:
                    logger.error(f"Error finding links on {current_url}: {e}")

        return scraped_pages

    def save_to_json(self, pages: List[Dict[str, Any]], output_path: str) -> None:
        """Save scraped pages to JSON file"""
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)

        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(pages, f, indent=2, ensure_ascii=False)

        logger.info(f"Saved {len(pages)} pages to {output_path}")


class ContentProcessor:
    """Process scraped content for vector database ingestion"""

    def __init__(self) -> None:
        pass

    def chunk_text(self, text: str, chunk_size: int = 1000, overlap: int = 200) -> List[str]:
        """Split text into overlapping chunks for better retrieval"""
        chunks = []
        start = 0

        while start < len(text):
            end = start + chunk_size
            chunk = text[start:end]

            # Don't cut in the middle of a word
            if end < len(text):
                last_space = chunk.rfind(" ")
                if last_space > chunk_size // 2:
                    end = start + last_space
                    chunk = text[start:end]

            chunks.append(chunk.strip())
            start = end - overlap

        return chunks

    def process_scraped_pages(self, pages: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Process scraped pages into chunks with metadata"""
        processed_chunks = []

        for page in pages:
            content = page.get("content", "")
            if not content:
                continue

            chunks = self.chunk_text(content)

            for i, chunk in enumerate(chunks):
                processed_chunks.append(
                    {
                        "content": chunk,
                        "metadata": {
                            "source": page.get("url", ""),
                            "title": page.get("title", ""),
                            "chunk_id": i,
                            "total_chunks": len(chunks),
                            "scraped_at": page.get("scraped_at", time.time()),
                        },
                    }
                )

        return processed_chunks


# Global instances
_scraper: Optional[WikiScraper] = None
_processor: Optional[ContentProcessor] = None


def get_wiki_scraper(base_url: str) -> WikiScraper:
    """Get or create wiki scraper instance"""
    global _scraper
    if _scraper is None:
        _scraper = WikiScraper(base_url)
    return _scraper


def get_content_processor() -> ContentProcessor:
    """Get or create content processor instance"""
    global _processor
    if _processor is None:
        _processor = ContentProcessor()
    return _processor
