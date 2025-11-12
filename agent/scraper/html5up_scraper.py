"""HTML5 UP template scraper"""

import re
import zipfile
import io
from typing import List, Dict
from .base_scraper import BaseScraper
from pathlib import Path


class HTML5UPScraper(BaseScraper):
    """Scraper for HTML5 UP free templates"""

    def __init__(self, output_dir: str = "data/templates/html5up"):
        super().__init__(output_dir)
        self.base_url = "https://html5up.net"

    def get_template_list_url(self) -> str:
        return self.base_url

    def scrape(self, limit: int = 10) -> List[Dict]:
        """Scrape HTML5 UP templates"""
        print(f"🎨 Scraping HTML5 UP templates (limit: {limit})...")

        soup = self.fetch_page(self.base_url)
        if not soup:
            return []

        templates = []
        articles = soup.find_all('article', limit=limit)

        for article in articles:
            try:
                template_data = self._parse_template_article(article)
                if template_data:
                    print(f"  ✓ Found: {template_data['title']}")

                    # Download and save template
                    template_id = self.generate_template_id(template_data['url'])
                    template_data['id'] = template_id
                    template_data['source'] = 'html5up'

                    # Download template zip
                    if self._download_template(template_data, template_id):
                        templates.append(template_data)
                        print(f"    Downloaded to: {template_id}/")

            except Exception as e:
                print(f"  ✗ Error processing template: {e}")
                continue

        print(f"✓ Scraped {len(templates)} templates from HTML5 UP")
        return templates

    def _parse_template_article(self, article) -> Dict:
        """Parse template information from article element"""
        title_elem = article.find('h2')
        title = title_elem.text.strip() if title_elem else 'Unknown'

        # Get template page URL
        link = article.find('a')
        if not link:
            return None

        template_url = self.base_url + link.get('href', '')

        # Get description
        desc_elem = article.find('p')
        description = desc_elem.text.strip() if desc_elem else ''

        # Get preview image
        img = article.find('img')
        preview_image = img.get('src', '') if img else ''
        if preview_image:
            preview_image = self.base_url + preview_image

        return {
            'title': title,
            'url': template_url,
            'description': description,
            'preview_image': preview_image
        }

    def _download_template(self, template_data: Dict, template_id: str) -> bool:
        """Download and extract template zip file"""
        try:
            # HTML5 UP uses direct download links from the template page
            # First, get the template page to find the actual download link
            template_page = self.fetch_page(template_data['url'])
            if not template_page:
                print(f"    ! Could not fetch template page")
                return False

            # Find the download link on the page
            download_link = template_page.find('a', href=lambda x: x and 'download' in x.lower())
            if not download_link:
                # Try alternative: look for .zip link
                download_link = template_page.find('a', href=lambda x: x and '.zip' in str(x).lower())

            if not download_link:
                print(f"    ! Could not find download link")
                return False

            download_url = self.base_url + download_link.get('href')

            # Download zip file
            response = self.session.get(download_url, timeout=60)
            if response.status_code == 200 and len(response.content) > 1000:
                # Extract zip
                template_dir = self.output_dir / template_id
                template_dir.mkdir(parents=True, exist_ok=True)

                with zipfile.ZipFile(io.BytesIO(response.content)) as zf:
                    zf.extractall(template_dir)

                # Save metadata
                self.save_template(template_data, template_id)
                return True
            else:
                print(f"    ! Could not download zip (status: {response.status_code})")
                return False

        except Exception as e:
            print(f"    ! Download error: {e}")
            return False
