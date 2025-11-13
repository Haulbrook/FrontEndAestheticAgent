"""Base scraper class for template collection"""

import os
import requests
from bs4 import BeautifulSoup
from typing import List, Dict, Optional
from pathlib import Path
import time
from urllib.parse import urljoin, urlparse
import hashlib


class BaseScraper:
    """Base class for all template scrapers"""

    def __init__(self, output_dir: str = "data/templates"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })

    def fetch_page(self, url: str) -> Optional[BeautifulSoup]:
        """Fetch and parse a web page"""
        try:
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            return BeautifulSoup(response.content, 'lxml')
        except Exception as e:
            print(f"Error fetching {url}: {e}")
            return None

    def download_file(self, url: str, output_path: Path) -> bool:
        """Download a file from URL"""
        try:
            response = self.session.get(url, timeout=30, stream=True)
            response.raise_for_status()

            output_path.parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            return True
        except Exception as e:
            print(f"Error downloading {url}: {e}")
            return False

    def extract_template_info(self, soup: BeautifulSoup, url: str) -> Dict:
        """Extract basic template information"""
        return {
            'url': url,
            'title': soup.title.string if soup.title else 'Unknown',
            'description': self._get_meta_description(soup),
            'styles': self._extract_css_links(soup, url),
            'scripts': self._extract_js_links(soup, url),
            'images': self._extract_images(soup, url)
        }

    def _get_meta_description(self, soup: BeautifulSoup) -> str:
        """Extract meta description"""
        meta = soup.find('meta', attrs={'name': 'description'})
        return meta.get('content', '') if meta else ''

    def _extract_css_links(self, soup: BeautifulSoup, base_url: str) -> List[str]:
        """Extract all CSS links"""
        links = []
        for link in soup.find_all('link', rel='stylesheet'):
            href = link.get('href')
            if href:
                links.append(urljoin(base_url, href))
        return links

    def _extract_js_links(self, soup: BeautifulSoup, base_url: str) -> List[str]:
        """Extract all JavaScript links"""
        links = []
        for script in soup.find_all('script', src=True):
            src = script.get('src')
            if src:
                links.append(urljoin(base_url, src))
        return links

    def _extract_images(self, soup: BeautifulSoup, base_url: str) -> List[str]:
        """Extract all image links"""
        images = []
        for img in soup.find_all('img', src=True):
            src = img.get('src')
            if src:
                images.append(urljoin(base_url, src))
        return images

    def template_exists(self, template_id: str) -> bool:
        """Check if template already exists"""
        template_dir = self.output_dir / template_id
        metadata_path = template_dir / 'metadata.json'
        return metadata_path.exists()

    def save_template(self, template_data: Dict, template_id: str) -> Path:
        """Save template data to disk"""
        template_dir = self.output_dir / template_id
        template_dir.mkdir(parents=True, exist_ok=True)

        # Save HTML
        if 'html' in template_data:
            html_path = template_dir / 'index.html'
            html_path.write_text(template_data['html'], encoding='utf-8')

        # Save metadata
        import json
        metadata_path = template_dir / 'metadata.json'
        metadata = {
            'url': template_data.get('url'),
            'title': template_data.get('title'),
            'description': template_data.get('description'),
            'source': template_data.get('source'),
            'scraped_at': time.strftime('%Y-%m-%d %H:%M:%S')
        }
        metadata_path.write_text(json.dumps(metadata, indent=2), encoding='utf-8')

        return template_dir

    def generate_template_id(self, url: str) -> str:
        """Generate unique template ID from URL"""
        return hashlib.md5(url.encode()).hexdigest()[:12]

    def scrape(self, limit: int = 10) -> List[Dict]:
        """Main scraping method - to be implemented by subclasses"""
        raise NotImplementedError("Subclasses must implement scrape()")

    def get_template_list_url(self) -> str:
        """Get the main URL for template listings"""
        raise NotImplementedError("Subclasses must implement get_template_list_url()")
