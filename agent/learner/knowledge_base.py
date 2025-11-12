"""Knowledge base for storing and retrieving design patterns"""

import json
from pathlib import Path
from typing import Dict, List, Optional
from collections import defaultdict
from datetime import datetime


class KnowledgeBase:
    """Stores and manages learned design patterns"""

    def __init__(self, db_path: str = "data/knowledge_base/design_patterns.json"):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)

        self.patterns = self._load_or_initialize()

    def _load_or_initialize(self) -> Dict:
        """Load existing knowledge base or initialize new one"""
        if self.db_path.exists():
            try:
                return json.loads(self.db_path.read_text(encoding='utf-8'))
            except Exception as e:
                print(f"! Error loading knowledge base: {e}")

        return self._initialize_structure()

    def _initialize_structure(self) -> Dict:
        """Initialize knowledge base structure"""
        return {
            'metadata': {
                'created_at': datetime.now().isoformat(),
                'last_updated': datetime.now().isoformat(),
                'total_templates_learned': 0,
                'version': '1.0'
            },
            'color_patterns': {
                'schemes': defaultdict(int),
                'popular_palettes': [],
                'dominant_colors': []
            },
            'layout_patterns': {
                'structures': defaultdict(int),
                'component_usage': defaultdict(int),
                'section_types': defaultdict(int)
            },
            'typography_patterns': {
                'popular_fonts': defaultdict(int),
                'font_pairings': [],
                'size_scales': []
            },
            'style_patterns': {
                'animation_techniques': [],
                'shadow_styles': [],
                'border_styles': defaultdict(int)
            },
            'modern_features': {
                'feature_usage': defaultdict(int),
                'framework_popularity': defaultdict(int)
            },
            'quality_benchmarks': {
                'high_quality_templates': [],
                'avg_quality_score': 0
            }
        }

    def add_template_analysis(self, analysis: Dict):
        """Add analyzed template to knowledge base"""
        template_id = analysis.get('template_id', 'unknown')

        # Update metadata
        self.patterns['metadata']['total_templates_learned'] += 1
        self.patterns['metadata']['last_updated'] = datetime.now().isoformat()

        # Learn color patterns
        self._learn_color_patterns(analysis.get('colors', {}))

        # Learn layout patterns
        self._learn_layout_patterns(analysis.get('layout', {}))

        # Learn typography patterns
        self._learn_typography_patterns(analysis.get('typography', {}))

        # Learn style patterns
        self._learn_style_patterns(analysis.get('style', {}))

        # Track quality
        quality_score = analysis.get('quality_score', 0)
        if quality_score >= 70:
            self.patterns['quality_benchmarks']['high_quality_templates'].append({
                'template_id': template_id,
                'score': quality_score,
                'features': self._extract_quality_features(analysis)
            })

        # Update average quality
        self._update_average_quality(quality_score)

        # Save changes
        self.save()

    def _learn_color_patterns(self, colors: Dict):
        """Learn from color analysis"""
        scheme = colors.get('color_scheme', 'unknown')
        if scheme != 'unknown':
            self.patterns['color_patterns']['schemes'][scheme] = \
                self.patterns['color_patterns']['schemes'].get(scheme, 0) + 1

        # Track dominant colors
        dominant = colors.get('dominant_colors', [])
        if dominant:
            top_colors = [c['color'] for c in dominant[:3]]
            self.patterns['color_patterns']['popular_palettes'].append(top_colors)

    def _learn_layout_patterns(self, layout: Dict):
        """Learn from layout analysis"""
        # Track layout systems
        systems = layout.get('layout_systems', {})
        for system, data in systems.items():
            if data.get('detected'):
                self.patterns['layout_patterns']['structures'][system] = \
                    self.patterns['layout_patterns']['structures'].get(system, 0) + 1

        # Track component usage
        components = layout.get('components', {})
        for component, count in components.items():
            if count > 0:
                self.patterns['layout_patterns']['component_usage'][component] = \
                    self.patterns['layout_patterns']['component_usage'].get(component, 0) + count

        # Track section types
        section_types = layout.get('sections', {}).get('section_types', [])
        for section_type in section_types:
            self.patterns['layout_patterns']['section_types'][section_type] = \
                self.patterns['layout_patterns']['section_types'].get(section_type, 0) + 1

    def _learn_typography_patterns(self, typography: Dict):
        """Learn from typography analysis"""
        # Track popular fonts
        fonts = typography.get('fonts', {}).get('custom_fonts', [])
        for font in fonts:
            self.patterns['typography_patterns']['popular_fonts'][font] = \
                self.patterns['typography_patterns']['popular_fonts'].get(font, 0) + 1

    def _learn_style_patterns(self, style: Dict):
        """Learn from style analysis"""
        # Track modern features
        modern = style.get('modern_features', {})
        for feature, used in modern.items():
            if used and feature != 'modernity_score':
                self.patterns['modern_features']['feature_usage'][feature] = \
                    self.patterns['modern_features']['feature_usage'].get(feature, 0) + 1

        # Track frameworks
        frameworks = style.get('css_frameworks', {}).get('detected_frameworks', [])
        for framework in frameworks:
            self.patterns['modern_features']['framework_popularity'][framework] = \
                self.patterns['modern_features']['framework_popularity'].get(framework, 0) + 1

    def _extract_quality_features(self, analysis: Dict) -> Dict:
        """Extract key features from high-quality templates"""
        return {
            'color_scheme': analysis.get('colors', {}).get('color_scheme'),
            'uses_grid': analysis.get('layout', {}).get('layout_systems', {}).get('grid', {}).get('detected'),
            'uses_flexbox': analysis.get('layout', {}).get('layout_systems', {}).get('flexbox', {}).get('detected'),
            'modernity_score': analysis.get('style', {}).get('modern_features', {}).get('modernity_score'),
            'responsive': analysis.get('layout', {}).get('responsive', {}).get('has_media_queries')
        }

    def _update_average_quality(self, new_score: int):
        """Update running average quality score"""
        total = self.patterns['metadata']['total_templates_learned']
        current_avg = self.patterns['quality_benchmarks']['avg_quality_score']

        new_avg = ((current_avg * (total - 1)) + new_score) / total
        self.patterns['quality_benchmarks']['avg_quality_score'] = round(new_avg, 2)

    def get_recommendations(self, category: str = 'all') -> Dict:
        """Get recommendations based on learned patterns"""
        recommendations = {}

        if category in ['all', 'colors']:
            recommendations['colors'] = self._get_color_recommendations()

        if category in ['all', 'layout']:
            recommendations['layout'] = self._get_layout_recommendations()

        if category in ['all', 'typography']:
            recommendations['typography'] = self._get_typography_recommendations()

        if category in ['all', 'style']:
            recommendations['style'] = self._get_style_recommendations()

        return recommendations

    def _get_color_recommendations(self) -> Dict:
        """Get color recommendations"""
        schemes = dict(self.patterns['color_patterns']['schemes'])
        most_popular = max(schemes.items(), key=lambda x: x[1])[0] if schemes else 'balanced'

        return {
            'recommended_scheme': most_popular,
            'popular_schemes': sorted(schemes.items(), key=lambda x: x[1], reverse=True)[:3]
        }

    def _get_layout_recommendations(self) -> Dict:
        """Get layout recommendations"""
        structures = dict(self.patterns['layout_patterns']['structures'])

        return {
            'recommended_systems': ['flexbox', 'grid'] if structures.get('grid', 0) > 0 else ['flexbox'],
            'popular_components': sorted(
                self.patterns['layout_patterns']['component_usage'].items(),
                key=lambda x: x[1],
                reverse=True
            )[:5],
            'common_sections': sorted(
                self.patterns['layout_patterns']['section_types'].items(),
                key=lambda x: x[1],
                reverse=True
            )[:5]
        }

    def _get_typography_recommendations(self) -> Dict:
        """Get typography recommendations"""
        fonts = dict(self.patterns['typography_patterns']['popular_fonts'])
        top_fonts = sorted(fonts.items(), key=lambda x: x[1], reverse=True)[:5]

        return {
            'popular_fonts': top_fonts,
            'recommendation': 'Use a combination of sans-serif for headings and body text'
        }

    def _get_style_recommendations(self) -> Dict:
        """Get style recommendations"""
        features = dict(self.patterns['modern_features']['feature_usage'])
        top_features = sorted(features.items(), key=lambda x: x[1], reverse=True)[:5]

        return {
            'recommended_features': top_features,
            'modernity_tip': 'Use CSS Grid, Flexbox, and CSS variables for modern designs'
        }

    def get_statistics(self) -> Dict:
        """Get knowledge base statistics"""
        return {
            'total_templates': self.patterns['metadata']['total_templates_learned'],
            'avg_quality': self.patterns['quality_benchmarks']['avg_quality_score'],
            'high_quality_count': len(self.patterns['quality_benchmarks']['high_quality_templates']),
            'most_popular_color_scheme': max(
                self.patterns['color_patterns']['schemes'].items(),
                key=lambda x: x[1],
                default=('unknown', 0)
            )[0],
            'most_popular_layout': max(
                self.patterns['layout_patterns']['structures'].items(),
                key=lambda x: x[1],
                default=('unknown', 0)
            )[0]
        }

    def save(self):
        """Save knowledge base to disk"""
        try:
            # Convert defaultdicts to regular dicts for JSON serialization
            serializable = self._convert_to_serializable(self.patterns)

            self.db_path.write_text(
                json.dumps(serializable, indent=2, ensure_ascii=False),
                encoding='utf-8'
            )
        except Exception as e:
            print(f"! Error saving knowledge base: {e}")

    def _convert_to_serializable(self, obj):
        """Convert defaultdicts to regular dicts recursively"""
        if isinstance(obj, defaultdict):
            return {k: self._convert_to_serializable(v) for k, v in obj.items()}
        elif isinstance(obj, dict):
            return {k: self._convert_to_serializable(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [self._convert_to_serializable(item) for item in obj]
        else:
            return obj
