"""Free-CSS.com template scraper"""

import re
from typing import List, Dict
from .base_scraper import BaseScraper
from urllib.parse import urljoin


class FreeCSScraper(BaseScraper):
    """Scraper for Free-CSS.com templates"""

    def __init__(self, output_dir: str = "data/templates/freecss"):
        super().__init__(output_dir)
        self.base_url = "https://www.free-css.com"
        self.templates_url = f"{self.base_url}/free-css-templates"

    def get_template_list_url(self) -> str:
        return self.templates_url

    def scrape(self, limit: int = 10) -> List[Dict]:
        """Scrape Free-CSS templates"""
        print(f"🎨 Scraping Free-CSS templates (limit: {limit})...")

        soup = self.fetch_page(self.templates_url)
        if not soup:
            return []

        templates = []
        template_items = soup.find_all('div', class_='template-item', limit=limit * 2)

        for item in template_items:
            if len(templates) >= limit:
                break

            try:
                template_data = self._parse_template_item(item)
                if template_data:
                    print(f"  ✓ Found: {template_data['title']}")

                    template_id = self.generate_template_id(template_data['url'])
                    template_data['id'] = template_id
                    template_data['source'] = 'freecss'

                    # Download template page for analysis
                    if self._download_template_page(template_data, template_id):
                        templates.append(template_data)
                        print(f"    Saved to: {template_id}/")

            except Exception as e:
                print(f"  ✗ Error processing template: {e}")
                continue

        print(f"✓ Scraped {len(templates)} templates from Free-CSS")
        return templates

    def _parse_template_item(self, item) -> Dict:
        """Parse template information from item element"""
        # Find title and link
        title_elem = item.find('a')
        if not title_elem:
            return None

        title = title_elem.get('title', 'Unknown')
        url = urljoin(self.base_url, title_elem.get('href', ''))

        # Find preview image
        img = item.find('img')
        preview_image = ''
        if img:
            preview_image = urljoin(self.base_url, img.get('src', ''))

        return {
            'title': title,
            'url': url,
            'preview_image': preview_image,
            'description': ''
        }

    def _download_template_page(self, template_data: Dict, template_id: str) -> bool:
        """Download template page for analysis"""
        try:
            soup = self.fetch_page(template_data['url'])
            if not soup:
                return False

            template_dir = self.output_dir / template_id
            template_dir.mkdir(parents=True, exist_ok=True)

            # Try to find and download demo link
            demo_link = soup.find('a', string=re.compile(r'demo', re.I))
            if demo_link:
                demo_url = urljoin(self.base_url, demo_link.get('href', ''))
                demo_soup = self.fetch_page(demo_url)

                if demo_soup:
                    # Save demo HTML
                    html_path = template_dir / 'index.html'
                    html_path.write_text(str(demo_soup), encoding='utf-8')

                    # Extract and save template info
                    template_data['html'] = str(demo_soup)
                    template_data['demo_url'] = demo_url

            # Save metadata
            self.save_template(template_data, template_id)
            return True

        except Exception as e:
            print(f"    ! Download error: {e}")
            return False
