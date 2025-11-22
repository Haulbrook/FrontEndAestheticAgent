"""Generate design improvements and suggestions"""

import random
from typing import Dict, List, Optional
from pathlib import Path
from ..learner.knowledge_base import KnowledgeBase


class DesignGenerator:
    """Generates design improvements based on learned patterns"""

    def __init__(self, knowledge_base_path: str = "data/knowledge_base/design_patterns.json"):
        self.kb = KnowledgeBase(knowledge_base_path)
        self.framework_patterns = self._load_framework_patterns()

    def _load_framework_patterns(self) -> Dict:
        """Load framework patterns from knowledge base"""
        return self.kb.patterns.get('framework_patterns', {})

    def generate_color_palette(self, scheme: Optional[str] = None) -> Dict:
        """Generate a color palette based on learned patterns"""
        if not scheme:
            # Use most popular scheme
            recommendations = self.kb.get_recommendations('colors')
            scheme = recommendations.get('recommended_scheme', 'balanced')

        # Get popular palettes
        popular_palettes = self.kb.patterns['color_patterns']['popular_palettes']

        if popular_palettes:
            # Pick a random palette from learned ones
            base_palette = random.choice(popular_palettes[-20:])  # From recent learnings
        else:
            # Default palettes
            base_palette = self._get_default_palette(scheme)

        return {
            'scheme': scheme,
            'colors': base_palette,
            'primary': base_palette[0] if base_palette else '#007bff',
            'secondary': base_palette[1] if len(base_palette) > 1 else '#6c757d',
            'accent': base_palette[2] if len(base_palette) > 2 else '#28a745',
            'usage_tips': self._get_color_usage_tips(scheme)
        }

    def _get_default_palette(self, scheme: str) -> List[str]:
        """Get default palette for a given scheme"""
        defaults = {
            'vibrant': ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', '#98D8C8'],
            'minimal_dark': ['#1A1A1A', '#2D2D2D', '#404040', '#FFFFFF', '#E0E0E0'],
            'minimal_light': ['#FFFFFF', '#F8F9FA', '#E9ECEF', '#212529', '#6C757D'],
            'dark_mode': ['#0D1117', '#161B22', '#21262D', '#58A6FF', '#F0F6FC'],
            'light_airy': ['#FFFFFF', '#F0F4F8', '#D9E2EC', '#627D98', '#102A43'],
            'balanced': ['#2C3E50', '#3498DB', '#E74C3C', '#ECF0F1', '#95A5A6']
        }

        return defaults.get(scheme, defaults['balanced'])

    def _get_color_usage_tips(self, scheme: str) -> List[str]:
        """Get usage tips for color scheme"""
        tips = {
            'vibrant': [
                'Use vibrant colors sparingly as accents',
                'Balance with neutral backgrounds',
                'Consider accessibility - ensure good contrast'
            ],
            'minimal_dark': [
                'Use subtle shadows for depth',
                'Add accent colors for CTAs',
                'Ensure text has sufficient contrast'
            ],
            'minimal_light': [
                'Use soft shadows for elevation',
                'Add colorful accents for important elements',
                'Maintain clean, spacious layouts'
            ],
            'dark_mode': [
                'Use blue tints for links and interactive elements',
                'Avoid pure black - use dark grays',
                'Reduce white text brightness to reduce eye strain'
            ]
        }

        return tips.get(scheme, ['Use colors consistently', 'Maintain good contrast', 'Test accessibility'])

    def generate_layout_suggestions(self) -> Dict:
        """Generate layout suggestions based on learned patterns"""
        recommendations = self.kb.get_recommendations('layout')

        return {
            'recommended_systems': recommendations.get('recommended_systems', ['flexbox']),
            'popular_components': recommendations.get('popular_components', [])[:5],
            'section_structure': self._generate_section_structure(recommendations),
            'layout_tips': [
                'Use CSS Grid for page-level layouts',
                'Use Flexbox for component-level layouts',
                'Implement mobile-first responsive design',
                'Use consistent spacing (8px or 4px grid)',
                'Limit content width for readability (max 1200-1400px)'
            ]
        }

    def _generate_section_structure(self, recommendations: Dict) -> List[str]:
        """Generate recommended section structure"""
        common_sections = recommendations.get('common_sections', [])

        # Extract section names
        section_names = [s[0] for s in common_sections] if common_sections else []

        # Build recommended structure
        structure = ['hero']  # Always start with hero

        if 'features' in section_names:
            structure.append('features')

        structure.append('content')

        if 'testimonials' in section_names:
            structure.append('testimonials')

        if 'gallery' in section_names or 'about' in section_names:
            structure.append('gallery_or_about')

        if 'call_to_action' in section_names:
            structure.append('call_to_action')

        structure.append('contact')

        return structure

    def generate_typography_suggestions(self) -> Dict:
        """Generate typography suggestions"""
        recommendations = self.kb.get_recommendations('typography')
        popular_fonts = recommendations.get('popular_fonts', [])

        # Extract font names
        font_list = [f[0] for f in popular_fonts] if popular_fonts else []

        return {
            'recommended_fonts': self._get_font_recommendations(font_list),
            'size_scale': self._generate_type_scale(),
            'typography_tips': [
                'Use a maximum of 2-3 font families',
                'Establish a clear hierarchy with size and weight',
                'Maintain consistent line-height (1.5-1.6 for body text)',
                'Use system fonts for better performance',
                'Ensure sufficient contrast for readability'
            ]
        }

    def _get_font_recommendations(self, learned_fonts: List[str]) -> Dict:
        """Get font pairing recommendations"""
        # Popular font pairings
        pairings = [
            {'heading': 'Inter', 'body': 'Inter', 'type': 'monofont'},
            {'heading': 'Playfair Display', 'body': 'Source Sans Pro', 'type': 'classic'},
            {'heading': 'Montserrat', 'body': 'Open Sans', 'type': 'modern'},
            {'heading': 'Raleway', 'body': 'Lato', 'type': 'clean'},
            {'heading': 'Poppins', 'body': 'Roboto', 'type': 'friendly'}
        ]

        # If we have learned fonts, try to use them
        if learned_fonts:
            heading_font = learned_fonts[0] if learned_fonts else 'Inter'
            body_font = learned_fonts[1] if len(learned_fonts) > 1 else heading_font

            return {
                'heading': heading_font,
                'body': body_font,
                'type': 'learned',
                'alternatives': pairings
            }

        # Otherwise, suggest popular pairings
        return random.choice(pairings)

    def _generate_type_scale(self) -> Dict:
        """Generate a typographic scale"""
        # Using a 1.25 ratio (Major Third)
        base = 16  # Base font size in pixels

        return {
            'base': f'{base}px',
            'small': f'{base * 0.875}px',  # 14px
            'h6': f'{base * 1}px',  # 16px
            'h5': f'{base * 1.25}px',  # 20px
            'h4': f'{base * 1.563}px',  # 25px
            'h3': f'{base * 1.953}px',  # 31px
            'h2': f'{base * 2.441}px',  # 39px
            'h1': f'{base * 3.052}px',  # 49px
            'display': f'{base * 3.815}px'  # 61px
        }

    def generate_style_suggestions(self) -> Dict:
        """Generate modern style suggestions"""
        recommendations = self.kb.get_recommendations('style')

        return {
            'recommended_features': recommendations.get('recommended_features', [])[:5],
            'animation_suggestions': [
                'Use subtle transitions (200-300ms) for interactive elements',
                'Add fade-in animations for content on scroll',
                'Implement smooth hover effects on buttons and cards',
                'Use transform instead of position for animations (better performance)'
            ],
            'modern_techniques': [
                'Use CSS custom properties (variables) for theming',
                'Implement smooth scrolling behavior',
                'Add subtle shadows for depth',
                'Use backdrop-filter for glass morphism effects',
                'Implement dark mode support'
            ],
            'accessibility_tips': [
                'Respect prefers-reduced-motion for animations',
                'Ensure sufficient color contrast (WCAG AA: 4.5:1)',
                'Use semantic HTML elements',
                'Add focus indicators for keyboard navigation',
                'Test with screen readers'
            ]
        }

    def generate_framework_guide(self, framework: str) -> Dict:
        """Generate framework-specific design guide"""
        guide = {
            'framework': framework,
            'available': False,
            'components': [],
            'utilities': [],
            'animations': [],
            'grid_system': {},
            'code_examples': []
        }

        # Get framework-specific patterns
        css_frameworks = self.framework_patterns.get('css_frameworks', {})
        component_lib = self.framework_patterns.get('component_library', {})
        anim_lib = self.framework_patterns.get('animation_library', {})
        grid_systems = self.framework_patterns.get('grid_systems', {})

        # Bootstrap guide
        if framework.lower() == 'bootstrap':
            if 'Bootstrap' in css_frameworks:
                guide['available'] = True
                guide['components'] = self._extract_framework_components('Bootstrap', component_lib)
                guide['grid_system'] = grid_systems.get('Bootstrap', {})
                guide['code_examples'] = [
                    {
                        'name': 'Grid Layout',
                        'code': '<div class="container">\n  <div class="row">\n    <div class="col-md-6">Column 1</div>\n    <div class="col-md-6">Column 2</div>\n  </div>\n</div>'
                    },
                    {
                        'name': 'Card Component',
                        'code': '<div class="card">\n  <div class="card-body">\n    <h5 class="card-title">Card title</h5>\n    <p class="card-text">Card content</p>\n  </div>\n</div>'
                    }
                ]

        # Tailwind guide
        elif framework.lower() == 'tailwind':
            if 'Tailwind CSS' in css_frameworks:
                guide['available'] = True
                guide['utilities'] = self._extract_framework_utilities('Tailwind CSS')
                guide['code_examples'] = [
                    {
                        'name': 'Flexbox Layout',
                        'code': '<div class="flex flex-col md:flex-row gap-4">\n  <div class="flex-1 p-4 bg-blue-500">Item 1</div>\n  <div class="flex-1 p-4 bg-green-500">Item 2</div>\n</div>'
                    },
                    {
                        'name': 'Card with Hover',
                        'code': '<div class="bg-white rounded-lg shadow-md p-6 hover:shadow-xl transition-shadow duration-300">\n  <h3 class="text-xl font-bold mb-2">Card Title</h3>\n  <p class="text-gray-600">Card content</p>\n</div>'
                    }
                ]

        # Animation guide
        elif framework.lower() == 'animate.css':
            guide['available'] = True
            guide['animations'] = [kf['name'] for kf in anim_lib.get('keyframes', [])[:20]]
            guide['code_examples'] = [
                {
                    'name': 'Fade In Animation',
                    'code': '<div class="animate__animated animate__fadeIn">\n  Animated content\n</div>'
                },
                {
                    'name': 'Bounce In Animation',
                    'code': '<div class="animate__animated animate__bounceIn animate__delay-1s">\n  Delayed bounce\n</div>'
                }
            ]

        return guide

    def _extract_framework_components(self, framework: str, component_lib: Dict) -> List[str]:
        """Extract components for a specific framework"""
        components = []
        for comp_type, frameworks in component_lib.items():
            if framework in frameworks:
                components.extend(frameworks[framework])
        return list(set(components))[:15]  # Limit to 15 unique components

    def _extract_framework_utilities(self, framework: str) -> Dict:
        """Extract utility classes for a framework"""
        util_patterns = self.framework_patterns.get('utility_patterns', {})
        utilities = {}
        for util_type, frameworks in util_patterns.items():
            if framework in frameworks:
                utilities[util_type] = frameworks[framework]
        return utilities

    def generate_complete_design_guide(self, framework: Optional[str] = None) -> Dict:
        """Generate a complete design guide based on all learned patterns"""
        guide = {
            'colors': self.generate_color_palette(),
            'layout': self.generate_layout_suggestions(),
            'typography': self.generate_typography_suggestions(),
            'style': self.generate_style_suggestions(),
            'overall_tips': [
                'Start with mobile-first design',
                'Maintain consistent spacing throughout',
                'Use a design system or style guide',
                'Test across different browsers and devices',
                'Optimize for performance (lazy loading, code splitting)',
                'Focus on user experience and accessibility'
            ]
        }

        # Add framework-specific guide if requested
        if framework:
            guide['framework_guide'] = self.generate_framework_guide(framework)

        return guide

    def export_design_guide(self, output_file: str = "design_guide.json"):
        """Export design guide to a file"""
        guide = self.generate_complete_design_guide()

        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        import json
        output_path.write_text(
            json.dumps(guide, indent=2, ensure_ascii=False),
            encoding='utf-8'
        )

        print(f"✓ Design guide exported to: {output_file}")
        return guide
