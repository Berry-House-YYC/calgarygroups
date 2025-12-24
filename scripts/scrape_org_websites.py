#!/usr/bin/env python3
"""
Web scraper for Calgary Groups organization websites.
Extracts text content from organization websites for description generation.
"""

import argparse
import csv
import json
import os
import time
import logging
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@dataclass
class ScrapedContent:
    """Represents scraped content from an organization website."""
    name: str
    url: str
    success: bool
    title: str = ""
    main_text: str = ""
    meta_description: str = ""
    error: Optional[str] = None
    status_code: Optional[int] = None


class WebScraper:
    """Scrapes content from organization websites."""
    
    def __init__(self, timeout: int = 10, delay: float = 1.0):
        """
        Initialize the scraper.
        
        Args:
            timeout: Request timeout in seconds
            delay: Delay between requests in seconds
        """
        self.timeout = timeout
        self.delay = delay
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
        })
    
    def extract_text_from_html(self, soup: BeautifulSoup) -> str:
        """
        Extract main content text from BeautifulSoup object.
        
        Args:
            soup: BeautifulSoup object
            
        Returns:
            Extracted text content
        """
        # Remove script and style elements
        for element in soup(['script', 'style', 'nav', 'header', 'footer', 'aside']):
            element.decompose()
        
        # Try to find main content areas
        main_content = None
        for selector in ['main', 'article', '[role="main"]', '.content', '#content']:
            main_content = soup.select_one(selector)
            if main_content:
                break
        
        # If no main content found, use body
        if not main_content:
            main_content = soup.find('body')
        
        if not main_content:
            return ""
        
        # Extract text
        text = main_content.get_text(separator=' ', strip=True)
        
        # Clean up whitespace
        text = ' '.join(text.split())
        
        # Limit length (keep first ~2000 characters for LLM processing)
        if len(text) > 2000:
            text = text[:2000] + "..."
        
        return text
    
    def scrape_url(self, url: str, name: str) -> ScrapedContent:
        """
        Scrape content from a single URL.
        
        Args:
            url: URL to scrape
            name: Organization name
            
        Returns:
            ScrapedContent object
        """
        try:
            logger.info(f"Scraping {name}: {url}")
            
            response = self.session.get(url, timeout=self.timeout, allow_redirects=True)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'lxml')
            
            # Extract title
            title = soup.title.string if soup.title else ""
            title = title.strip() if title else ""
            
            # Extract meta description
            meta_desc = soup.find('meta', attrs={'name': 'description'})
            if not meta_desc:
                meta_desc = soup.find('meta', property='og:description')
            meta_description = meta_desc.get('content', '').strip() if meta_desc else ""
            
            # Extract main text
            main_text = self.extract_text_from_html(soup)
            
            return ScrapedContent(
                name=name,
                url=url,
                success=True,
                title=title,
                main_text=main_text,
                meta_description=meta_description,
                status_code=response.status_code
            )
            
        except requests.Timeout:
            logger.warning(f"Timeout scraping {name}: {url}")
            return ScrapedContent(
                name=name,
                url=url,
                success=False,
                error="Timeout"
            )
        except requests.RequestException as e:
            logger.warning(f"Error scraping {name}: {url} - {str(e)}")
            return ScrapedContent(
                name=name,
                url=url,
                success=False,
                error=str(e),
                status_code=getattr(e.response, 'status_code', None) if hasattr(e, 'response') else None
            )
        except Exception as e:
            logger.error(f"Unexpected error scraping {name}: {url} - {str(e)}")
            return ScrapedContent(
                name=name,
                url=url,
                success=False,
                error=f"Unexpected error: {str(e)}"
            )
    
    def scrape_organizations(self, organizations: List[Dict[str, str]]) -> List[ScrapedContent]:
        """
        Scrape content from multiple organization websites.
        
        Args:
            organizations: List of dicts with 'name' and 'url' keys
            
        Returns:
            List of ScrapedContent objects
        """
        results = []
        total = len(organizations)
        
        for i, org in enumerate(organizations, 1):
            name = org.get('name', 'Unknown')
            url = org.get('url', '')
            
            if not url:
                logger.warning(f"Skipping {name}: No URL provided")
                results.append(ScrapedContent(
                    name=name,
                    url="",
                    success=False,
                    error="No URL provided"
                ))
                continue
            
            result = self.scrape_url(url, name)
            results.append(result)
            
            logger.info(f"Progress: {i}/{total} ({i*100//total}%)")
            
            # Rate limiting
            if i < total:
                time.sleep(self.delay)
        
        return results


def read_organizations_from_csv(csv_path: str, website_column: str = 'Website') -> List[Dict[str, str]]:
    """
    Read organization names and URLs from CSV.
    
    Args:
        csv_path: Path to CSV file
        website_column: Name of column containing URLs
        
    Returns:
        List of dicts with 'name' and 'url' keys
    """
    organizations = []
    
    with open(csv_path, 'r', encoding='utf-8', newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row.get('Organization Name', '').strip()
            url = row.get(website_column, '').strip()
            
            # Only include if marked for Calgary Groups Site
            site_flag = row.get('Calgary Groups Site', '').strip().upper()
            if site_flag == 'Y' and name:
                organizations.append({
                    'name': name,
                    'url': url
                })
    
    return organizations


def save_results(results: List[ScrapedContent], output_path: str):
    """
    Save scraping results to JSON file.
    
    Args:
        results: List of ScrapedContent objects
        output_path: Path to output JSON file
    """
    os.makedirs(os.path.dirname(output_path) or '.', exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump([asdict(r) for r in results], f, indent=2, ensure_ascii=False)
    
    logger.info(f"Results saved to {output_path}")


def print_summary(results: List[ScrapedContent]):
    """Print summary of scraping results."""
    total = len(results)
    successful = sum(1 for r in results if r.success)
    failed = total - successful
    
    print("\n" + "="*60)
    print("SCRAPING SUMMARY")
    print("="*60)
    print(f"Total organizations: {total}")
    print(f"Successfully scraped: {successful} ({successful*100//total if total > 0 else 0}%)")
    print(f"Failed: {failed}")
    
    if failed > 0:
        print("\nFailed organizations:")
        for r in results:
            if not r.success:
                print(f"  - {r.name}: {r.error}")
    
    print("="*60 + "\n")


def main():
    parser = argparse.ArgumentParser(
        description='Scrape content from Calgary Groups organization websites'
    )
    parser.add_argument(
        '--csv',
        dest='csv_path',
        default=os.path.join('docs', 'UPDATED', 'Calgary Groups - Organizations.with_urls.csv'),
        help='Path to CSV file with organization data'
    )
    parser.add_argument(
        '--output',
        dest='output_path',
        default=os.path.join('scripts', 'scraped_content', 'scraped_data.json'),
        help='Path to output JSON file'
    )
    parser.add_argument(
        '--timeout',
        type=int,
        default=10,
        help='Request timeout in seconds (default: 10)'
    )
    parser.add_argument(
        '--delay',
        type=float,
        default=1.0,
        help='Delay between requests in seconds (default: 1.0)'
    )
    parser.add_argument(
        '--limit',
        type=int,
        default=None,
        help='Limit number of organizations to scrape (for testing)'
    )
    
    args = parser.parse_args()
    
    # Read organizations from CSV
    logger.info(f"Reading organizations from {args.csv_path}")
    organizations = read_organizations_from_csv(args.csv_path)
    
    if args.limit:
        organizations = organizations[:args.limit]
        logger.info(f"Limited to {args.limit} organizations for testing")
    
    logger.info(f"Found {len(organizations)} organizations to scrape")
    
    # Scrape content
    scraper = WebScraper(timeout=args.timeout, delay=args.delay)
    results = scraper.scrape_organizations(organizations)
    
    # Save results
    save_results(results, args.output_path)
    
    # Print summary
    print_summary(results)
    
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
