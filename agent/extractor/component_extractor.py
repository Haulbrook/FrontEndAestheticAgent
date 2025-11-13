"""Component Extractor - Extract reusable UI components from templates"""

import json
import re
from pathlib import Path
from typing import List, Dict, Set
from bs4 import BeautifulSoup, Tag
import hashlib


class ComponentExtractor:
    """Extract and catalog reusable UI components from HTML templates"""

    def __init__(self, output_dir: str = "data/components"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Component categories
        self.categories = {
            'navigation': self.output_dir / 'navigation',
            'buttons': self.output_dir / 'buttons',
            'cards': self.output_dir / 'cards',
            'heroes': self.output_dir / 'heroes',
            'forms': self.output_dir / 'forms',
            'footers': self.output_dir / 'footers',
            'headers': self.output_dir / 'headers',
            'sections': self.output_dir / 'sections'
        }

        # Create category directories
        for category_dir in self.categories.values():
            category_dir.mkdir(parents=True, exist_ok=True)

        self.components_index = []
        self.seen_hashes = set()

    def extract_from_directory(self, template_dir: str) -> Dict:
        """Extract components from all templates in a directory"""
        template_path = Path(template_dir)
        results = {
            'navigation': [],
            'buttons': [],
            'cards': [],
            'heroes': [],
            'forms': [],
            'footers': [],
            'headers': [],
            'sections': []
        }

        print(f"\n🔍 Extracting components from: {template_path.name}")

        # Find all HTML files recursively
        html_files = list(template_path.rglob("*.html"))

        if not html_files:
            print(f"  ! No HTML files found")
            return results

        print(f"  Found {len(html_files)} HTML files")

        for html_file in html_files:
            try:
                with open(html_file, 'r', encoding='utf-8', errors='ignore') as f:
                    html_content = f.read()

                soup = BeautifulSoup(html_content, 'html.parser')
                source_info = {
                    'template': template_path.name,
                    'file': html_file.name
                }

                # Extract different component types
                results['navigation'].extend(self._extract_navigation(soup, source_info))
                results['buttons'].extend(self._extract_buttons(soup, source_info))
                results['cards'].extend(self._extract_cards(soup, source_info))
                results['heroes'].extend(self._extract_heroes(soup, source_info))
                results['forms'].extend(self._extract_forms(soup, source_info))
                results['footers'].extend(self._extract_footers(soup, source_info))
                results['headers'].extend(self._extract_headers(soup, source_info))

            except Exception as e:
                print(f"  ! Error processing {html_file.name}: {e}")
                continue

        # Save extracted components
        total = sum(len(comps) for comps in results.values())
        if total > 0:
            self._save_components(results, template_path.name)
            print(f"  ✓ Extracted {total} components")
        else:
            print(f"  ! No components extracted")

        return results

    def _extract_navigation(self, soup: BeautifulSoup, source: Dict) -> List[Dict]:
        """Extract navigation bars"""
        navs = []

        # Find nav elements
        for nav in soup.find_all(['nav', 'header']):
            # Skip if it's too small or doesn't have links
            links = nav.find_all('a')
            if len(links) < 2:
                continue

            component = self._create_component(nav, 'navigation', source)
            if component and self._is_unique(component['html']):
                navs.append(component)

        # Also check for common nav classes
        for elem in soup.find_all(class_=re.compile(r'(navbar|navigation|menu|header-nav)', re.I)):
            if elem.name in ['nav', 'header', 'div', 'ul']:
                component = self._create_component(elem, 'navigation', source)
                if component and self._is_unique(component['html']):
                    navs.append(component)

        return navs[:5]  # Limit to 5 per template

    def _extract_buttons(self, soup: BeautifulSoup, source: Dict) -> List[Dict]:
        """Extract buttons with unique styles"""
        buttons = []
        seen_styles = set()

        # Find button elements
        for btn in soup.find_all(['button', 'a', 'input']):
            # Check if it looks like a button
            classes = ' '.join(btn.get('class', []))
            if not any(keyword in classes.lower() for keyword in ['btn', 'button', 'cta', 'action']):
                if btn.name != 'button':
                    continue

            # Skip if no visible text
            text = btn.get_text(strip=True)
            if not text and btn.name not in ['button', 'input']:
                continue

            # Create style signature to avoid duplicates
            style_sig = f"{classes}_{btn.name}"
            if style_sig in seen_styles:
                continue
            seen_styles.add(style_sig)

            component = self._create_component(btn, 'button', source, compact=True)
            if component:
                buttons.append(component)

        return buttons[:10]  # Limit to 10 per template

    def _extract_cards(self, soup: BeautifulSoup, source: Dict) -> List[Dict]:
        """Extract card components"""
        cards = []

        # Common card selectors
        card_patterns = [
            re.compile(r'card', re.I),
            re.compile(r'item', re.I),
            re.compile(r'box', re.I),
            re.compile(r'panel', re.I)
        ]

        for pattern in card_patterns:
            for elem in soup.find_all(class_=pattern):
                # Cards should have some content
                if len(elem.get_text(strip=True)) < 20:
                    continue

                # Cards often have images or headings
                has_image = elem.find('img') is not None
                has_heading = elem.find(['h1', 'h2', 'h3', 'h4', 'h5', 'h6']) is not None

                if has_image or has_heading:
                    component = self._create_component(elem, 'card', source)
                    if component and self._is_unique(component['html']):
                        cards.append(component)

        return cards[:8]  # Limit to 8 per template

    def _extract_heroes(self, soup: BeautifulSoup, source: Dict) -> List[Dict]:
        """Extract hero sections"""
        heroes = []

        # Look for hero sections
        hero_patterns = [
            re.compile(r'hero', re.I),
            re.compile(r'banner', re.I),
            re.compile(r'jumbotron', re.I),
            re.compile(r'intro', re.I)
        ]

        for pattern in hero_patterns:
            for elem in soup.find_all(class_=pattern):
                # Heroes should be substantial
                if len(elem.get_text(strip=True)) < 30:
                    continue

                component = self._create_component(elem, 'hero', source)
                if component and self._is_unique(component['html']):
                    heroes.append(component)

        # Also check for large first sections
        main = soup.find('main') or soup.find('body')
        if main:
            first_sections = main.find_all(['section', 'div'], limit=3)
            for section in first_sections:
                # Check if it's large and prominent
                if len(section.get_text(strip=True)) > 100:
                    h1 = section.find('h1')
                    if h1:  # Has main heading
                        component = self._create_component(section, 'hero', source)
                        if component and self._is_unique(component['html']):
                            heroes.append(component)
                            break  # Only take the first one

        return heroes[:3]  # Limit to 3 per template

    def _extract_forms(self, soup: BeautifulSoup, source: Dict) -> List[Dict]:
        """Extract forms"""
        forms = []

        for form in soup.find_all('form'):
            # Forms should have at least 2 inputs
            inputs = form.find_all(['input', 'textarea', 'select'])
            if len(inputs) < 2:
                continue

            component = self._create_component(form, 'form', source)
            if component and self._is_unique(component['html']):
                forms.append(component)

        return forms[:5]  # Limit to 5 per template

    def _extract_footers(self, soup: BeautifulSoup, source: Dict) -> List[Dict]:
        """Extract footers"""
        footers = []

        for footer in soup.find_all('footer'):
            component = self._create_component(footer, 'footer', source)
            if component and self._is_unique(component['html']):
                footers.append(component)

        return footers[:2]  # Limit to 2 per template

    def _extract_headers(self, soup: BeautifulSoup, source: Dict) -> List[Dict]:
        """Extract header sections"""
        headers = []

        for header in soup.find_all('header'):
            # Skip if it's a nav (already extracted)
            if header.find('nav'):
                continue

            component = self._create_component(header, 'header', source)
            if component and self._is_unique(component['html']):
                headers.append(component)

        return headers[:3]  # Limit to 3 per template

    def _create_component(self, element: Tag, category: str, source: Dict, compact: bool = False) -> Dict:
        """Create a component dictionary from an HTML element"""
        # Get HTML
        html = str(element)

        # For compact components (like buttons), limit size
        if compact and len(html) > 500:
            return None

        # Extract classes for categorization
        classes = element.get('class', [])
        if isinstance(classes, list):
            classes = ' '.join(classes)

        # Get text content for search
        text_content = element.get_text(strip=True)[:200]

        # Extract inline styles
        inline_style = element.get('style', '')

        return {
            'html': html,
            'category': category,
            'classes': classes,
            'text': text_content,
            'inline_style': inline_style,
            'source': source,
            'tag': element.name
        }

    def _is_unique(self, html: str) -> bool:
        """Check if component is unique (not already extracted)"""
        # Create hash of HTML (ignoring whitespace variations)
        normalized = re.sub(r'\s+', ' ', html).strip()
        component_hash = hashlib.md5(normalized.encode()).hexdigest()

        if component_hash in self.seen_hashes:
            return False

        self.seen_hashes.add(component_hash)
        return True

    def _save_components(self, components: Dict, template_name: str):
        """Save extracted components to files"""
        for category, items in components.items():
            if not items:
                continue

            category_dir = self.categories[category]

            for i, component in enumerate(items):
                # Generate unique filename
                filename = f"{template_name}_{category}_{i}.json"
                filepath = category_dir / filename

                # Save component
                with open(filepath, 'w', encoding='utf-8') as f:
                    json.dump(component, f, indent=2)

                # Add to index
                self.components_index.append({
                    'id': f"{category}_{template_name}_{i}",
                    'category': category,
                    'template': template_name,
                    'file': filename,
                    'classes': component.get('classes', ''),
                    'text': component.get('text', '')[:100]
                })

    def save_index(self):
        """Save the component index"""
        index_file = self.output_dir / 'index.json'
        with open(index_file, 'w', encoding='utf-8') as f:
            json.dump(self.components_index, f, indent=2)

        # Also create a summary
        summary = {
            'total_components': len(self.components_index),
            'by_category': {}
        }

        for category in self.categories.keys():
            count = sum(1 for c in self.components_index if c['category'] == category)
            summary['by_category'][category] = count

        summary_file = self.output_dir / 'summary.json'
        with open(summary_file, 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2)

        print(f"\n📊 Component Extraction Summary:")
        print(f"  Total components: {summary['total_components']}")
        for category, count in summary['by_category'].items():
            if count > 0:
                print(f"  {category.capitalize()}: {count}")
