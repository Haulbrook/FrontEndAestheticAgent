"""Analyze overall styling patterns"""

import re
from typing import Dict, List
from collections import Counter


class StyleAnalyzer:
    """Analyzes overall styling patterns and modern techniques"""

    def __init__(self):
        pass

    def analyze(self, html: str, css: str = "") -> Dict:
        """Analyze styling patterns"""
        return {
            'animations': self._analyze_animations(css),
            'transitions': self._analyze_transitions(css),
            'shadows': self._analyze_shadows(css),
            'borders': self._analyze_borders(css),
            'gradients': self._analyze_gradients(css),
            'modern_features': self._detect_modern_features(css),
            'css_frameworks': self._detect_frameworks(html, css)
        }

    def _analyze_animations(self, css: str) -> Dict:
        """Analyze CSS animations"""
        keyframes = re.findall(r'@keyframes\s+(\w+)', css, re.I)
        animation_props = re.findall(r'animation(?:-name)?:\s*([^;{]+)', css, re.I)

        return {
            'has_animations': len(keyframes) > 0,
            'keyframe_count': len(keyframes),
            'animation_count': len(animation_props),
            'animation_names': list(set(keyframes))
        }

    def _analyze_transitions(self, css: str) -> Dict:
        """Analyze CSS transitions"""
        transitions = re.findall(r'transition:\s*([^;{]+)', css, re.I)

        properties = []
        for trans in transitions:
            # Extract property names
            props = re.findall(r'(\w+)\s+[\d.]+m?s', trans)
            properties.extend(props)

        return {
            'has_transitions': len(transitions) > 0,
            'transition_count': len(transitions),
            'transitioned_properties': dict(Counter(properties).most_common(10))
        }

    def _analyze_shadows(self, css: str) -> Dict:
        """Analyze shadow usage"""
        box_shadows = len(re.findall(r'box-shadow:', css, re.I))
        text_shadows = len(re.findall(r'text-shadow:', css, re.I))
        drop_shadows = len(re.findall(r'drop-shadow\(', css, re.I))

        return {
            'box_shadow_count': box_shadows,
            'text_shadow_count': text_shadows,
            'drop_shadow_count': drop_shadows,
            'uses_shadows': (box_shadows + text_shadows + drop_shadows) > 0,
            'shadow_intensity': 'high' if box_shadows > 20 else 'medium' if box_shadows > 5 else 'low'
        }

    def _analyze_borders(self, css: str) -> Dict:
        """Analyze border usage"""
        border_radius = len(re.findall(r'border-radius:', css, re.I))
        borders = len(re.findall(r'border(?:-top|-right|-bottom|-left)?:', css, re.I))

        # Extract border-radius values
        radius_values = re.findall(r'border-radius:\s*([\d.]+)(px|em|rem|%)', css, re.I)

        return {
            'uses_borders': borders > 0,
            'border_count': borders,
            'uses_border_radius': border_radius > 0,
            'border_radius_count': border_radius,
            'style': 'rounded' if border_radius > 10 else 'sharp'
        }

    def _analyze_gradients(self, css: str) -> Dict:
        """Analyze gradient usage"""
        linear_gradients = len(re.findall(r'linear-gradient\(', css, re.I))
        radial_gradients = len(re.findall(r'radial-gradient\(', css, re.I))
        conic_gradients = len(re.findall(r'conic-gradient\(', css, re.I))

        total = linear_gradients + radial_gradients + conic_gradients

        return {
            'uses_gradients': total > 0,
            'linear_gradient_count': linear_gradients,
            'radial_gradient_count': radial_gradients,
            'conic_gradient_count': conic_gradients,
            'gradient_intensity': 'high' if total > 10 else 'medium' if total > 3 else 'low'
        }

    def _detect_modern_features(self, css: str) -> Dict:
        """Detect usage of modern CSS features"""
        features = {
            'css_variables': len(re.findall(r'--[\w-]+:', css)) > 0,
            'css_grid': len(re.findall(r'display:\s*grid', css, re.I)) > 0,
            'flexbox': len(re.findall(r'display:\s*flex', css, re.I)) > 0,
            'backdrop_filter': len(re.findall(r'backdrop-filter:', css, re.I)) > 0,
            'clip_path': len(re.findall(r'clip-path:', css, re.I)) > 0,
            'transforms': len(re.findall(r'transform:', css, re.I)) > 0,
            'filters': len(re.findall(r'filter:', css, re.I)) > 0,
            'blend_modes': len(re.findall(r'mix-blend-mode|background-blend-mode', css, re.I)) > 0
        }

        modernity_score = sum(features.values()) * 12.5  # 8 features, 100 max

        return {
            **features,
            'modernity_score': round(modernity_score, 2)
        }

    def _detect_frameworks(self, html: str, css: str) -> Dict:
        """Detect CSS frameworks and libraries"""
        combined = html + css

        frameworks = {
            'bootstrap': bool(re.search(r'bootstrap', combined, re.I)),
            'tailwind': bool(re.search(r'tailwind', combined, re.I)),
            'bulma': bool(re.search(r'bulma', combined, re.I)),
            'foundation': bool(re.search(r'foundation', combined, re.I)),
            'materialize': bool(re.search(r'materialize', combined, re.I)),
            'semantic_ui': bool(re.search(r'semantic-ui|semantic\.', combined, re.I)),
            'pure_css': bool(re.search(r'pure-css|purecss', combined, re.I))
        }

        detected = [name for name, found in frameworks.items() if found]

        return {
            **frameworks,
            'detected_frameworks': detected,
            'uses_framework': len(detected) > 0
        }
