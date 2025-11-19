"""Design Resource Scraper - Analyzes design resource websites for patterns"""

import json
import re
import time
from pathlib import Path
from typing import Dict, List, Optional
from urllib.parse import urlparse

from bs4 import BeautifulSoup
from .base_scraper import BaseScraper


class DesignResourceScraper(BaseScraper):
    """
    Scraper for design resource websites (icons, colors, fonts, UI frameworks, etc.)
    Unlike template scrapers, this extracts design patterns and aesthetic elements
    """

    def __init__(self, output_dir: str = "data/design_resources", delay: int = 3):
        super().__init__(output_dir)
        self.delay = delay
        self.resources_file = Path("data/frontend2_training/categorized_resources.json")
        self.training_output = Path("data/frontend2_training/extended_training_data.json")

        # Update user agent to be more identifiable
        self.session.headers.update({
            'User-Agent': 'FrontEndAestheticAgent/1.0 (Educational Design Analysis; github.com/Haulbrook/FrontEndAestheticAgent)'
        })

    def check_robots_txt(self, url: str) -> bool:
        """Check if scraping is allowed by robots.txt"""
        parsed = urlparse(url)
        robots_url = f"{parsed.scheme}://{parsed.netloc}/robots.txt"

        try:
            response = self.session.get(robots_url, timeout=5)
            if response.status_code == 200:
                # Simple check - more sophisticated parsing could be added
                if 'Disallow: /' in response.text and 'User-agent: *' in response.text:
                    return False
            return True
        except:
            # If robots.txt doesn't exist or fails, assume allowed
            return True

    def extract_colors(self, soup: BeautifulSoup) -> List[str]:
        """Extract color codes from page"""
        colors = []

        # From inline styles
        for tag in soup.find_all(style=True):
            style = tag.get('style', '')
            hex_colors = re.findall(r'#[0-9A-Fa-f]{6}', style)
            rgb_colors = re.findall(r'rgb\([^)]+\)', style)
            colors.extend(hex_colors)
            colors.extend(rgb_colors)

        # From style tags
        for style_tag in soup.find_all('style'):
            if style_tag.string:
                hex_colors = re.findall(r'#[0-9A-Fa-f]{6}', style_tag.string)
                colors.extend(hex_colors)

        # From CSS classes that might contain color names
        for tag in soup.find_all(class_=True):
            classes = tag.get('class', [])
            for cls in classes:
                if any(color in cls.lower() for color in ['red', 'blue', 'green', 'yellow', 'purple', 'orange', 'pink', 'gray', 'black', 'white']):
                    colors.append(f"class:{cls}")

        return list(set(colors))[:30]  # Limit to 30 unique colors

    def extract_layout_structure(self, soup: BeautifulSoup) -> Dict:
        """Extract layout and structural information"""
        return {
            'headers': len(soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])),
            'sections': len(soup.find_all('section')),
            'articles': len(soup.find_all('article')),
            'nav': len(soup.find_all('nav')),
            'divs': len(soup.find_all('div')),
            'buttons': len(soup.find_all('button')),
            'forms': len(soup.find_all('form')),
            'lists': len(soup.find_all(['ul', 'ol'])),
            'tables': len(soup.find_all('table')),
            'cards': len(soup.find_all(class_=re.compile(r'card', re.I)))
        }

    def extract_typography(self, soup: BeautifulSoup) -> Dict:
        """Extract typography information"""
        fonts = []

        # From link tags (Google Fonts, etc.)
        for link in soup.find_all('link', href=True):
            href = link.get('href', '')
            if 'font' in href.lower():
                fonts.append(href)

        # From style tags
        for style_tag in soup.find_all('style'):
            if style_tag.string:
                font_families = re.findall(r'font-family:\s*([^;]+)', style_tag.string)
                fonts.extend(font_families)

        return {
            'font_links': fonts[:10],
            'total_fonts_detected': len(set(fonts))
        }

    def scrape_design_elements(self, url: str, resource_name: str, category: str) -> Optional[Dict]:
        """
        Extract design elements from a resource website
        Returns structured data about colors, layout, typography, etc.
        """

        if not self.check_robots_txt(url):
            print(f"  ❌ Blocked by robots.txt: {resource_name}")
            return None

        try:
            # Respectful delay
            time.sleep(self.delay)

            soup = self.fetch_page(url)
            if not soup:
                return None

            # Extract various design elements
            colors = self.extract_colors(soup)
            layout = self.extract_layout_structure(soup)
            typography = self.extract_typography(soup)

            # Meta information
            meta_desc = soup.find('meta', attrs={'name': 'description'})
            description = meta_desc.get('content', '') if meta_desc else ''

            # Open Graph images (often showcase the design)
            og_image = soup.find('meta', property='og:image')
            preview_image = og_image.get('content', '') if og_image else ''

            title = soup.title.string if soup.title else ''

            print(f"  ✓ Scraped: {resource_name} ({category})")

            return {
                'url': url,
                'resource_name': resource_name,
                'category': category,
                'colors': colors,
                'layout': layout,
                'typography': typography,
                'title': title,
                'description': description,
                'preview_image': preview_image,
                'scraped_at': time.time()
            }

        except Exception as e:
            print(f"  ⚠ Error scraping {resource_name}: {str(e)[:100]}")
            return None

    def load_resources(self) -> Dict:
        """Load categorized resources from Frontend2 data"""
        if not self.resources_file.exists():
            print(f"❌ Resources file not found: {self.resources_file}")
            return {}

        with open(self.resources_file, 'r', encoding='utf-8') as f:
            return json.load(f)

    def scrape(self, limit: int = 10, categories: Optional[List[str]] = None) -> List[Dict]:
        """
        Scrape design resources

        Args:
            limit: Number of resources to scrape per category
            categories: List of categories to scrape (None = all)

        Returns:
            List of scraped resource data
        """
        resources = self.load_resources()

        if not resources:
            print("No resources to scrape!")
            return []

        # Default categories if none specified
        if categories is None:
            categories = ['ui_frameworks', 'icons', 'colors', 'design_systems', 'css_frameworks']

        training_data = []

        print(f"\n🎨 Starting design resource scraping...")
        print(f"   Categories: {', '.join(categories)}")
        print(f"   Limit per category: {limit}\n")

        for category in categories:
            category_resources = resources.get(category, [])

            if not category_resources:
                print(f"⚠ No resources found for category: {category}")
                continue

            print(f"\n📁 Processing {category} ({len(category_resources)} available)...")

            count = 0
            for resource in category_resources:
                if count >= limit:
                    break

                data = self.scrape_design_elements(
                    resource['url'],
                    resource['name'],
                    category
                )

                if data:
                    training_data.append(data)
                    count += 1

        # Save the training data
        if training_data:
            self.save_training_data(training_data)

        return training_data

    def save_training_data(self, data: List[Dict]) -> None:
        """Save scraped data to training file"""
        # Load existing data if it exists
        existing_data = []
        if self.training_output.exists():
            with open(self.training_output, 'r', encoding='utf-8') as f:
                existing_data = json.load(f)

        # Merge and deduplicate by URL
        all_data = existing_data + data
        seen_urls = set()
        unique_data = []

        for item in all_data:
            if item['url'] not in seen_urls:
                seen_urls.add(item['url'])
                unique_data.append(item)

        # Save merged data
        self.training_output.parent.mkdir(parents=True, exist_ok=True)
        with open(self.training_output, 'w', encoding='utf-8') as f:
            json.dump(unique_data, f, indent=2)

        print(f"\n✅ Saved {len(unique_data)} total training samples")
        print(f"   (Added {len(data)} new samples)")
        print(f"📄 Saved to: {self.training_output}")

    def get_template_list_url(self) -> str:
        """Not applicable for design resources"""
        return "https://github.com/Haulbrook/Frontend2"
