"""Design Resources for Developers scraper

This scraper parses the design-resources-for-developers repository
and extracts template URLs from relevant sections.
"""

import re
import time
from typing import List, Dict, Optional
from .base_scraper import BaseScraper
from urllib.parse import urlparse
import zipfile
import io


class DesignResourcesScraper(BaseScraper):
    """Scraper that extracts templates from design-resources-for-developers repo"""

    def __init__(self, output_dir: str = "data/templates/design_resources"):
        super().__init__(output_dir)
        self.repo_url = "https://raw.githubusercontent.com/Haulbrook/design-resources-for-developers/master/readme.md"

        # Sections to extract template URLs from
        self.template_sections = [
            "HTML & CSS Templates",
            "UI Components & Kits",
            "React UI Libraries",
            "Vue UI Libraries",
            "Angular UI Libraries"
        ]

    def get_template_list_url(self) -> str:
        return self.repo_url

    def scrape(self, limit: int = 10) -> List[Dict]:
        """Scrape templates from design resources repo"""
        print(f"🎨 Scraping Design Resources for Developers (limit: {limit})...")

        # Fetch the readme
        readme_content = self._fetch_readme()
        if not readme_content:
            print("  ❌ Failed to fetch readme")
            return []

        # Extract template URLs
        template_urls = self._extract_template_urls(readme_content)
        print(f"  Found {len(template_urls)} potential template sources")

        templates = []
        downloaded_count = 0

        for url_info in template_urls:
            if downloaded_count >= limit:
                break

            try:
                # Check if already downloaded
                template_id = self.generate_template_id(url_info['url'])
                if self.template_exists(template_id):
                    print(f"  ⏭  {url_info['name']}: Already downloaded, skipping...")
                    continue

                print(f"  ✓ Processing: {url_info['name']}")

                # Add delay between requests
                if downloaded_count > 0:
                    delay = 3
                    print(f"    ⏳ Waiting {delay}s...")
                    time.sleep(delay)

                # Try to scrape the template
                template_data = self._scrape_template_site(url_info)
                if template_data:
                    template_data['id'] = template_id
                    template_data['source'] = 'design_resources'

                    # Save template
                    self.save_template(template_data, template_id)
                    templates.append(template_data)
                    downloaded_count += 1
                    print(f"    ✅ Downloaded successfully")
                else:
                    print(f"    ⚠️  Could not extract template content")

            except Exception as e:
                print(f"    ❌ Error processing {url_info.get('name', 'unknown')}: {e}")
                continue

        print(f"\n✅ Successfully downloaded {downloaded_count} new templates")
        return templates

    def _fetch_readme(self) -> Optional[str]:
        """Fetch the readme content from the repo"""
        try:
            response = self.session.get(self.repo_url, timeout=30)
            response.raise_for_status()
            return response.text
        except Exception as e:
            print(f"Error fetching readme: {e}")
            return None

    def _extract_template_urls(self, readme_content: str) -> List[Dict]:
        """Extract template URLs from readme sections"""
        urls = []

        # Split readme into lines
        lines = readme_content.split('\n')

        current_section = None
        for line in lines:
            # Check if we're entering a relevant section
            for section in self.template_sections:
                if section in line and line.startswith('#'):
                    current_section = section
                    break

            # Check if we're leaving the section (new section starts)
            if line.startswith('#') and current_section:
                # Check if this is a new section
                is_new_section = True
                for section in self.template_sections:
                    if section in line:
                        is_new_section = False
                        break
                if is_new_section and line.startswith('##'):
                    current_section = None

            # Extract URLs from lines in relevant sections
            if current_section:
                # Match markdown links: [Name](URL)
                matches = re.findall(r'\[([^\]]+)\]\(([^)]+)\)', line)
                for name, url in matches:
                    # Filter out internal links and GitHub links
                    if url.startswith('http') and 'github.com' not in url:
                        # Only add if it looks like a template site (not just a tool)
                        if self._is_template_site(url, name):
                            urls.append({
                                'name': name,
                                'url': url,
                                'section': current_section
                            })

        return urls

    def _is_template_site(self, url: str, name: str) -> bool:
        """Check if URL likely points to a template site"""
        # Keywords that indicate template sites
        template_keywords = [
            'template', 'theme', 'bootstrap', 'ui kit', 'components',
            'tailwind', 'html5', 'css', 'framework', 'starter'
        ]

        # Check URL and name for template-related keywords
        url_lower = url.lower()
        name_lower = name.lower()

        for keyword in template_keywords:
            if keyword in url_lower or keyword in name_lower:
                return True

        return False

    def _scrape_template_site(self, url_info: Dict) -> Optional[Dict]:
        """Attempt to scrape a template from the given site"""
        try:
            soup = self.fetch_page(url_info['url'])
            if not soup:
                return None

            # Look for downloadable templates or demos
            template_data = {
                'url': url_info['url'],
                'title': url_info['name'],
                'description': url_info['section'],
                'html': str(soup)
            }

            # Try to find a download link or demo
            download_link = self._find_download_link(soup, url_info['url'])
            if download_link:
                template_data['download_url'] = download_link

            # Try to find a live demo
            demo_link = self._find_demo_link(soup, url_info['url'])
            if demo_link:
                # Fetch the demo page as the template
                demo_soup = self.fetch_page(demo_link)
                if demo_soup:
                    template_data['html'] = str(demo_soup)
                    template_data['demo_url'] = demo_link

            return template_data

        except Exception as e:
            print(f"    Error scraping {url_info['url']}: {e}")
            return None

    def _find_download_link(self, soup, base_url: str) -> Optional[str]:
        """Find download links in the page"""
        # Look for common download link patterns
        for a in soup.find_all('a'):
            href = a.get('href', '')
            text = a.get_text().lower()

            if any(keyword in text for keyword in ['download', 'get started', 'free']):
                if href.endswith('.zip') or 'download' in href:
                    from urllib.parse import urljoin
                    return urljoin(base_url, href)

        return None

    def _find_demo_link(self, soup, base_url: str) -> Optional[str]:
        """Find demo/preview links in the page"""
        for a in soup.find_all('a'):
            href = a.get('href', '')
            text = a.get_text().lower()

            if any(keyword in text for keyword in ['demo', 'preview', 'example', 'live']):
                from urllib.parse import urljoin
                return urljoin(base_url, href)

        return None
