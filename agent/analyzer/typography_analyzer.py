"""Analyze typography patterns"""

import re
from typing import Dict, List, Set
from collections import Counter
from bs4 import BeautifulSoup


class TypographyAnalyzer:
    """Analyzes typography and font usage"""

    def __init__(self):
        self.font_weight_map = {
            '100': 'thin',
            '200': 'extra-light',
            '300': 'light',
            '400': 'normal',
            '500': 'medium',
            '600': 'semi-bold',
            '700': 'bold',
            '800': 'extra-bold',
            '900': 'black'
        }

    def analyze(self, html: str, css: str = "") -> Dict:
        """Analyze typography patterns"""
        return {
            'fonts': self._extract_fonts(css, html),
            'sizes': self._analyze_font_sizes(css),
            'weights': self._analyze_font_weights(css),
            'spacing': self._analyze_spacing(css),
            'headings': self._analyze_headings(html),
            'web_fonts': self._detect_web_fonts(html, css)
        }

    def _extract_fonts(self, css: str, html: str) -> Dict:
        """Extract font families used"""
        font_family_pattern = re.compile(r'font-family:\s*([^;{}]+)', re.I)
        matches = font_family_pattern.findall(css + html)

        fonts = []
        for match in matches:
            # Clean up and split by comma
            font_list = [f.strip(' "\',') for f in match.split(',')]
            fonts.extend(font_list)

        # Count frequency
        font_counter = Counter(fonts)

        # Filter out generic families
        generic_families = {'serif', 'sans-serif', 'monospace', 'cursive', 'fantasy', 'system-ui'}
        custom_fonts = {f: c for f, c in font_counter.items() if f.lower() not in generic_families}

        return {
            'total_unique': len(set(fonts)),
            'most_used': font_counter.most_common(5),
            'custom_fonts': list(custom_fonts.keys()),
            'font_stack_count': len(matches)
        }

    def _analyze_font_sizes(self, css: str) -> Dict:
        """Analyze font size usage"""
        size_pattern = re.compile(r'font-size:\s*(\d+(?:\.\d+)?)(px|em|rem|pt|%)', re.I)
        matches = size_pattern.findall(css)

        sizes = {}
        for value, unit in matches:
            size_key = f"{value}{unit}"
            sizes[size_key] = sizes.get(size_key, 0) + 1

        # Convert to standardized scale
        size_scale = []
        for value, unit in matches:
            num = float(value)
            if unit == 'px':
                size_scale.append(num)
            elif unit in ['em', 'rem']:
                size_scale.append(num * 16)  # Assuming base 16px

        return {
            'unique_sizes': len(sizes),
            'size_distribution': dict(Counter(sizes).most_common(10)),
            'size_range': {
                'min': min(size_scale) if size_scale else 0,
                'max': max(size_scale) if size_scale else 0,
                'avg': round(sum(size_scale) / len(size_scale), 2) if size_scale else 0
            },
            'uses_relative_units': any(unit in ['em', 'rem', '%'] for _, unit in matches)
        }

    def _analyze_font_weights(self, css: str) -> Dict:
        """Analyze font weight usage"""
        weight_pattern = re.compile(r'font-weight:\s*(\d{3}|bold|normal|lighter|bolder)', re.I)
        matches = weight_pattern.findall(css)

        weight_counter = Counter(matches)

        return {
            'weights_used': dict(weight_counter),
            'uses_variable_weights': len(set(matches)) > 2,
            'most_common_weight': weight_counter.most_common(1)[0] if matches else ('normal', 0)
        }

    def _analyze_spacing(self, css: str) -> Dict:
        """Analyze text spacing (line-height, letter-spacing)"""
        line_height_pattern = re.compile(r'line-height:\s*(\d+(?:\.\d+)?)', re.I)
        letter_spacing_pattern = re.compile(r'letter-spacing:\s*([-\d.]+)(px|em|rem)', re.I)

        line_heights = [float(m) for m in line_height_pattern.findall(css)]
        letter_spacings = letter_spacing_pattern.findall(css)

        return {
            'line_height': {
                'used': len(line_heights) > 0,
                'avg': round(sum(line_heights) / len(line_heights), 2) if line_heights else 1.5,
                'range': (min(line_heights), max(line_heights)) if line_heights else (0, 0)
            },
            'letter_spacing': {
                'used': len(letter_spacings) > 0,
                'count': len(letter_spacings)
            }
        }

    def _analyze_headings(self, html: str) -> Dict:
        """Analyze heading usage"""
        soup = BeautifulSoup(html, 'html.parser')

        headings = {}
        for i in range(1, 7):
            h_tags = soup.find_all(f'h{i}')
            headings[f'h{i}'] = len(h_tags)

        return {
            'heading_count': headings,
            'uses_semantic_headings': sum(headings.values()) > 0,
            'heading_hierarchy_score': self._calculate_hierarchy_score(headings)
        }

    def _calculate_hierarchy_score(self, headings: Dict) -> int:
        """Calculate how well heading hierarchy is used (0-100)"""
        score = 100

        # Check if h1 exists
        if headings.get('h1', 0) == 0:
            score -= 30

        # Check if hierarchy is maintained
        for i in range(1, 6):
            current = headings.get(f'h{i}', 0)
            next_level = headings.get(f'h{i+1}', 0)

            # Penalize if skipping levels
            if current == 0 and next_level > 0:
                score -= 15

        return max(0, score)

    def _detect_web_fonts(self, html: str, css: str) -> Dict:
        """Detect usage of web fonts"""
        google_fonts = bool(re.search(r'fonts\.googleapis\.com', html + css))
        adobe_fonts = bool(re.search(r'use\.typekit\.net|typekit\.com', html + css))
        font_awesome = bool(re.search(r'fontawesome|font-awesome', html + css, re.I))

        font_face = len(re.findall(r'@font-face', css, re.I))

        return {
            'google_fonts': google_fonts,
            'adobe_fonts': adobe_fonts,
            'font_awesome': font_awesome,
            'custom_font_face': font_face > 0,
            'font_face_count': font_face
        }
