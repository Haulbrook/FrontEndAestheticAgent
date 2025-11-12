"""Analyze layout patterns and structure"""

import re
from typing import Dict, List
from bs4 import BeautifulSoup


class LayoutAnalyzer:
    """Analyzes layout patterns and structure"""

    def __init__(self):
        self.layout_keywords = {
            'flexbox': ['display: flex', 'display:flex', 'flex-direction', 'justify-content'],
            'grid': ['display: grid', 'display:grid', 'grid-template', 'grid-gap'],
            'float': ['float: left', 'float: right', 'float:left', 'float:right'],
            'position': ['position: absolute', 'position: fixed', 'position: relative']
        }

    def analyze(self, html: str, css: str = "") -> Dict:
        """Analyze layout patterns"""
        soup = BeautifulSoup(html, 'html.parser')

        return {
            'structure': self._analyze_structure(soup),
            'layout_systems': self._detect_layout_systems(css),
            'sections': self._analyze_sections(soup),
            'navigation': self._analyze_navigation(soup),
            'responsive': self._analyze_responsive(css),
            'components': self._identify_components(soup)
        }

    def _analyze_structure(self, soup: BeautifulSoup) -> Dict:
        """Analyze overall page structure"""
        return {
            'has_header': bool(soup.find(['header', 'div', 'nav'], class_=re.compile(r'header|navbar', re.I))),
            'has_footer': bool(soup.find(['footer', 'div'], class_=re.compile(r'footer', re.I))),
            'has_sidebar': bool(soup.find(['aside', 'div'], class_=re.compile(r'sidebar|aside', re.I))),
            'main_content_containers': len(soup.find_all(['main', 'div'], class_=re.compile(r'main|content|container', re.I))),
            'max_nesting_depth': self._get_max_depth(soup)
        }

    def _detect_layout_systems(self, css: str) -> Dict:
        """Detect which layout systems are used"""
        systems = {}

        for system, patterns in self.layout_keywords.items():
            count = sum(css.lower().count(pattern) for pattern in patterns)
            systems[system] = {
                'detected': count > 0,
                'usage_count': count
            }

        return systems

    def _analyze_sections(self, soup: BeautifulSoup) -> Dict:
        """Analyze page sections"""
        sections = soup.find_all(['section', 'div'], class_=re.compile(r'section|block', re.I))

        return {
            'total_sections': len(sections),
            'section_types': self._classify_sections(sections)
        }

    def _classify_sections(self, sections) -> List[str]:
        """Classify sections by common types"""
        types = []

        for section in sections:
            classes = ' '.join(section.get('class', [])).lower()

            if any(word in classes for word in ['hero', 'banner', 'splash']):
                types.append('hero')
            elif any(word in classes for word in ['feature', 'service']):
                types.append('features')
            elif any(word in classes for word in ['testimonial', 'review']):
                types.append('testimonials')
            elif any(word in classes for word in ['contact', 'form']):
                types.append('contact')
            elif any(word in classes for word in ['gallery', 'portfolio']):
                types.append('gallery')
            elif any(word in classes for word in ['about', 'team']):
                types.append('about')
            elif any(word in classes for word in ['cta', 'call-to-action']):
                types.append('call_to_action')
            else:
                types.append('content')

        return types

    def _analyze_navigation(self, soup: BeautifulSoup) -> Dict:
        """Analyze navigation patterns"""
        nav_elements = soup.find_all(['nav', 'div'], class_=re.compile(r'nav|menu', re.I))

        nav_links = []
        for nav in nav_elements:
            links = nav.find_all('a')
            nav_links.extend(links)

        return {
            'nav_count': len(nav_elements),
            'total_nav_links': len(nav_links),
            'has_dropdown': bool(soup.find(class_=re.compile(r'dropdown|submenu', re.I))),
            'has_hamburger': bool(soup.find(class_=re.compile(r'hamburger|menu-toggle|mobile-menu', re.I)))
        }

    def _analyze_responsive(self, css: str) -> Dict:
        """Analyze responsive design patterns"""
        media_queries = re.findall(r'@media[^{]+', css)

        breakpoints = []
        for query in media_queries:
            nums = re.findall(r'\d+px', query)
            breakpoints.extend(nums)

        return {
            'has_media_queries': len(media_queries) > 0,
            'media_query_count': len(media_queries),
            'breakpoints': list(set(breakpoints)),
            'responsive_score': min(len(media_queries) * 10, 100)
        }

    def _identify_components(self, soup: BeautifulSoup) -> Dict:
        """Identify common UI components"""
        return {
            'buttons': len(soup.find_all(['button', 'a'], class_=re.compile(r'btn|button', re.I))),
            'cards': len(soup.find_all(class_=re.compile(r'card', re.I))),
            'forms': len(soup.find_all('form')),
            'modals': len(soup.find_all(class_=re.compile(r'modal|popup|dialog', re.I))),
            'sliders': len(soup.find_all(class_=re.compile(r'slider|carousel|swiper', re.I))),
            'icons': len(soup.find_all(['i', 'svg', 'span'], class_=re.compile(r'icon|fa-|material-icons', re.I)))
        }

    def _get_max_depth(self, soup: BeautifulSoup, depth: int = 0) -> int:
        """Calculate maximum nesting depth of HTML"""
        if not soup.children:
            return depth

        max_child_depth = depth
        for child in soup.children:
            if hasattr(child, 'children'):
                child_depth = self._get_max_depth(child, depth + 1)
                max_child_depth = max(max_child_depth, child_depth)

        return max_child_depth
