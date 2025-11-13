"""TemplateMo template scraper"""

import re
import zipfile
import io
import time
from typing import List, Dict
from .base_scraper import BaseScraper
from pathlib import Path
from urllib.parse import urljoin


class TemplateMoScraper(BaseScraper):
    """Scraper for TemplateMo free templates"""

    def __init__(self, output_dir: str = "data/templates/templatemo"):
        super().__init__(output_dir)
        self.base_url = "https://templatemo.com"

    def get_template_list_url(self) -> str:
        return self.base_url

    def scrape(self, limit: int = 10) -> List[Dict]:
        """Scrape TemplateMo templates"""
        print(f"🎨 Scraping TemplateMo templates (limit: {limit})...")

        soup = self.fetch_page(self.base_url)
        if not soup:
            return []

        templates = []

        # TemplateMo has templates in various container types
        # Try multiple selectors to find template items
        template_items = []

        # Try common patterns
        selectors = [
            ('div', {'class': re.compile(r'col.*')}),
            ('div', {'class': re.compile(r'template.*', re.I)}),
            ('article', {}),
            ('div', {'class': re.compile(r'item.*', re.I)}),
        ]

        for tag, attrs in selectors:
            template_items = soup.find_all(tag, attrs, limit=limit * 2)
            if template_items:
                print(f"  Found {len(template_items)} potential templates using {tag} selector")
                break

        if not template_items:
            # Last resort: find all links with 'tm-' in the href
            links = soup.find_all('a', href=re.compile(r'/tm-'))
            for link in links[:limit]:
                parent = link.find_parent(['div', 'article'])
                if parent and parent not in template_items:
                    template_items.append(parent)

        for i, item in enumerate(template_items):
            if len(templates) >= limit:
                break

            try:
                template_data = self._parse_template_item(item)
                if template_data:
                    print(f"  ✓ Found: {template_data['title']}")

                    # Add delay between requests to avoid rate limiting
                    if i > 0:
                        delay = 3
                        print(f"    ⏳ Waiting {delay}s to avoid rate limiting...")
                        time.sleep(delay)

                    # Download and save template
                    template_id = self.generate_template_id(template_data['url'])
                    template_data['id'] = template_id
                    template_data['source'] = 'templatemo'

                    # Download template
                    if self._download_template(template_data, template_id):
                        templates.append(template_data)
                        print(f"    Downloaded to: {template_id}/")

            except Exception as e:
                print(f"  ✗ Error processing template: {e}")
                continue

        print(f"✓ Scraped {len(templates)} templates from TemplateMo")
        return templates

    def _parse_template_item(self, item) -> Dict:
        """Parse template information from item element"""
        # Find title
        title_elem = item.find('h3')
        if not title_elem:
            title_elem = item.find('h2')

        title = title_elem.text.strip() if title_elem else 'Unknown'

        # Find template link
        link = item.find('a', href=True)
        if not link:
            return None

        template_url = urljoin(self.base_url, link.get('href', ''))

        # Find preview image
        img = item.find('img')
        preview_image = ''
        if img:
            preview_image = urljoin(self.base_url, img.get('src', ''))

        # Get description if available
        desc_elem = item.find('p')
        description = desc_elem.text.strip() if desc_elem else ''

        return {
            'title': title,
            'url': template_url,
            'description': description,
            'preview_image': preview_image
        }

    def _download_template(self, template_data: Dict, template_id: str) -> bool:
        """Download and extract template zip file"""
        try:
            # Visit the template page to find the download link
            template_page = self.fetch_page(template_data['url'])
            if not template_page:
                print(f"    ! Could not fetch template page")
                return False

            # Find download link - TemplateMo typically has a "Download" button/link
            download_link = template_page.find('a', href=lambda x: x and ('.zip' in str(x).lower() or 'download' in str(x).lower()))

            if not download_link:
                # Try alternative patterns
                download_link = template_page.find('a', class_=re.compile(r'download', re.I))

            if not download_link:
                # Try looking for direct zip links in buttons
                download_link = template_page.find('a', string=re.compile(r'download', re.I))

            if not download_link:
                print(f"    ! Could not find download link")
                return False

            # Construct download URL
            href = download_link.get('href', '')
            if href.startswith('http'):
                download_url = href
            elif href.startswith('/'):
                download_url = self.base_url + href
            else:
                download_url = urljoin(template_data['url'], href)

            # Download zip file with retry logic
            max_retries = 3
            for retry in range(max_retries):
                response = self.session.get(download_url, timeout=60, stream=True)

                if response.status_code == 200 and len(response.content) > 1000:
                    break
                elif response.status_code == 429:
                    if retry < max_retries - 1:
                        wait_time = (retry + 1) * 5
                        print(f"    ⚠ Rate limited (429), waiting {wait_time}s before retry...")
                        time.sleep(wait_time)
                        continue
                    else:
                        print(f"    ! Could not download zip (status: 429 - rate limited)")
                        return False
                else:
                    print(f"    ! Could not download zip (status: {response.status_code})")
                    return False

            if response.status_code == 200 and len(response.content) > 1000:
                # Extract zip
                template_dir = self.output_dir / template_id
                template_dir.mkdir(parents=True, exist_ok=True)

                try:
                    with zipfile.ZipFile(io.BytesIO(response.content)) as zf:
                        zf.extractall(template_dir)
                except zipfile.BadZipFile:
                    print(f"    ! Invalid zip file")
                    return False

                # Save metadata
                self.save_template(template_data, template_id)
                return True
            else:
                print(f"    ! Download failed")
                return False

        except Exception as e:
            print(f"    ! Download error: {e}")
            return False
