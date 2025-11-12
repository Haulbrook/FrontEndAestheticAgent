"""Analyze color schemes and palettes from templates"""

import re
from typing import List, Dict, Set
from collections import Counter
import colorsys


class ColorAnalyzer:
    """Analyzes colors used in templates"""

    def __init__(self):
        self.color_pattern = re.compile(
            r'#(?:[0-9a-fA-F]{3}){1,2}|'
            r'rgb\(\s*\d+\s*,\s*\d+\s*,\s*\d+\s*\)|'
            r'rgba\(\s*\d+\s*,\s*\d+\s*,\s*\d+\s*,\s*[\d.]+\s*\)|'
            r'hsl\(\s*\d+\s*,\s*\d+%\s*,\s*\d+%\s*\)|'
            r'hsla\(\s*\d+\s*,\s*\d+%\s*,\s*\d+%\s*,\s*[\d.]+\s*\)'
        )

    def analyze(self, html: str, css: str = "") -> Dict:
        """Analyze colors from HTML and CSS"""
        combined_text = html + "\n" + css

        # Extract all colors
        colors = self._extract_colors(combined_text)

        # Normalize colors to hex
        normalized_colors = [self._normalize_color(c) for c in colors]
        normalized_colors = [c for c in normalized_colors if c]

        # Count frequency
        color_frequency = Counter(normalized_colors)

        # Get dominant colors (top 10)
        dominant_colors = color_frequency.most_common(10)

        # Analyze color palette characteristics
        palette_analysis = self._analyze_palette([c for c, _ in dominant_colors])

        return {
            'total_colors': len(set(normalized_colors)),
            'dominant_colors': [
                {'color': color, 'count': count, 'percentage': round(count / len(normalized_colors) * 100, 2)}
                for color, count in dominant_colors
            ],
            'palette_characteristics': palette_analysis,
            'color_scheme': self._detect_color_scheme(palette_analysis)
        }

    def _extract_colors(self, text: str) -> List[str]:
        """Extract all color values from text"""
        return self.color_pattern.findall(text)

    def _normalize_color(self, color: str) -> str:
        """Normalize color to hex format"""
        color = color.strip().lower()

        # Already hex
        if color.startswith('#'):
            # Expand shorthand hex
            if len(color) == 4:
                color = '#' + ''.join([c * 2 for c in color[1:]])
            return color.upper()

        # RGB
        if color.startswith('rgb'):
            nums = re.findall(r'\d+', color)
            if len(nums) >= 3:
                r, g, b = int(nums[0]), int(nums[1]), int(nums[2])
                return f'#{r:02X}{g:02X}{b:02X}'

        # HSL
        if color.startswith('hsl'):
            nums = re.findall(r'\d+', color)
            if len(nums) >= 3:
                h, s, l = int(nums[0]) / 360, int(nums[1]) / 100, int(nums[2]) / 100
                r, g, b = colorsys.hls_to_rgb(h, l, s)
                return f'#{int(r*255):02X}{int(g*255):02X}{int(b*255):02X}'

        return None

    def _analyze_palette(self, colors: List[str]) -> Dict:
        """Analyze characteristics of color palette"""
        if not colors:
            return {}

        hues = []
        saturations = []
        lightnesses = []

        for color in colors:
            if not color.startswith('#'):
                continue

            # Convert hex to RGB
            r = int(color[1:3], 16) / 255
            g = int(color[3:5], 16) / 255
            b = int(color[5:7], 16) / 255

            # Convert to HSL
            h, l, s = colorsys.rgb_to_hls(r, g, b)

            hues.append(h * 360)
            saturations.append(s * 100)
            lightnesses.append(l * 100)

        return {
            'avg_hue': round(sum(hues) / len(hues), 2) if hues else 0,
            'avg_saturation': round(sum(saturations) / len(saturations), 2) if saturations else 0,
            'avg_lightness': round(sum(lightnesses) / len(lightnesses), 2) if lightnesses else 0,
            'is_vibrant': sum(saturations) / len(saturations) > 50 if saturations else False,
            'is_dark': sum(lightnesses) / len(lightnesses) < 40 if lightnesses else False,
            'is_light': sum(lightnesses) / len(lightnesses) > 60 if lightnesses else False
        }

    def _detect_color_scheme(self, palette_analysis: Dict) -> str:
        """Detect the overall color scheme type"""
        if not palette_analysis:
            return 'unknown'

        avg_sat = palette_analysis.get('avg_saturation', 0)
        avg_light = palette_analysis.get('avg_lightness', 50)

        if avg_sat < 20:
            if avg_light > 70:
                return 'minimal_light'
            elif avg_light < 30:
                return 'minimal_dark'
            else:
                return 'monochromatic'
        elif avg_sat > 60:
            return 'vibrant'
        elif avg_light < 30:
            return 'dark_mode'
        elif avg_light > 70:
            return 'light_airy'
        else:
            return 'balanced'
