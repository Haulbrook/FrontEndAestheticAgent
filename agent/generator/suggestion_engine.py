"""Analyze existing designs and suggest improvements"""

from pathlib import Path
from typing import Dict, List
from ..analyzer.template_analyzer import TemplateAnalyzer
from ..learner.knowledge_base import KnowledgeBase


class SuggestionEngine:
    """Analyzes existing designs and suggests improvements"""

    def __init__(self, knowledge_base_path: str = "data/knowledge_base/design_patterns.json"):
        self.analyzer = TemplateAnalyzer()
        self.kb = KnowledgeBase(knowledge_base_path)

    def analyze_and_suggest(self, html_file: str) -> Dict:
        """Analyze an HTML file and suggest improvements"""
        html_path = Path(html_file)

        if not html_path.exists():
            return {'error': f'File not found: {html_file}'}

        print(f"\n🔍 Analyzing: {html_path.name}\n")

        # Create temporary directory for analysis
        temp_dir = Path("temp_analysis") / html_path.stem
        temp_dir.mkdir(parents=True, exist_ok=True)

        # Copy HTML to temp directory
        import shutil
        shutil.copy(html_file, temp_dir / "index.html")

        # Analyze
        analysis = self.analyzer.analyze_template(temp_dir)

        if not analysis:
            return {'error': 'Failed to analyze file'}

        # Clean up
        shutil.rmtree("temp_analysis", ignore_errors=True)

        # Generate suggestions
        suggestions = self._generate_suggestions(analysis)

        return {
            'analysis': analysis,
            'suggestions': suggestions,
            'quality_score': analysis.get('quality_score', 0)
        }

    def _generate_suggestions(self, analysis: Dict) -> Dict:
        """Generate improvement suggestions based on analysis"""
        suggestions = {
            'colors': self._suggest_color_improvements(analysis.get('colors', {})),
            'layout': self._suggest_layout_improvements(analysis.get('layout', {})),
            'typography': self._suggest_typography_improvements(analysis.get('typography', {})),
            'style': self._suggest_style_improvements(analysis.get('style', {})),
            'priority_improvements': []
        }

        # Determine priority improvements
        suggestions['priority_improvements'] = self._prioritize_suggestions(analysis, suggestions)

        return suggestions

    def _suggest_color_improvements(self, colors: Dict) -> List[Dict]:
        """Suggest color improvements"""
        suggestions = []

        total_colors = colors.get('total_colors', 0)

        if total_colors < 3:
            suggestions.append({
                'type': 'warning',
                'issue': 'Limited color palette',
                'suggestion': 'Consider adding more colors to create visual interest',
                'recommendation': 'Add accent colors for CTAs and interactive elements'
            })

        if total_colors > 15:
            suggestions.append({
                'type': 'warning',
                'issue': 'Too many colors',
                'suggestion': 'Simplify your color palette for better consistency',
                'recommendation': 'Stick to 5-7 main colors plus shades'
            })

        color_scheme = colors.get('color_scheme', '')

        if color_scheme == 'unknown':
            suggestions.append({
                'type': 'info',
                'issue': 'No clear color scheme',
                'suggestion': 'Establish a cohesive color scheme',
                'recommendation': self.kb.get_recommendations('colors')
            })

        # Check palette characteristics
        palette = colors.get('palette_characteristics', {})

        if not palette.get('is_vibrant') and not palette.get('is_dark') and not palette.get('is_light'):
            suggestions.append({
                'type': 'info',
                'issue': 'Neutral color palette',
                'suggestion': 'Consider adding vibrant accent colors',
                'recommendation': 'Use bright colors for buttons and important CTAs'
            })

        return suggestions

    def _suggest_layout_improvements(self, layout: Dict) -> List[Dict]:
        """Suggest layout improvements"""
        suggestions = []

        # Check layout systems
        systems = layout.get('layout_systems', {})

        if not systems.get('flexbox', {}).get('detected'):
            suggestions.append({
                'type': 'recommendation',
                'issue': 'Not using Flexbox',
                'suggestion': 'Consider using Flexbox for component layouts',
                'recommendation': 'Flexbox is essential for modern, responsive designs'
            })

        if not systems.get('grid', {}).get('detected'):
            suggestions.append({
                'type': 'recommendation',
                'issue': 'Not using CSS Grid',
                'suggestion': 'Consider using CSS Grid for page layouts',
                'recommendation': 'CSS Grid excels at creating complex, responsive layouts'
            })

        # Check responsive design
        responsive = layout.get('responsive', {})

        if not responsive.get('has_media_queries'):
            suggestions.append({
                'type': 'critical',
                'issue': 'No media queries detected',
                'suggestion': 'Add responsive design with media queries',
                'recommendation': 'Essential for mobile-friendly design'
            })

        responsive_score = responsive.get('responsive_score', 0)

        if responsive_score < 50:
            suggestions.append({
                'type': 'warning',
                'issue': 'Limited responsive design',
                'suggestion': 'Improve responsive design coverage',
                'recommendation': 'Add more breakpoints for different screen sizes'
            })

        # Check structure
        structure = layout.get('structure', {})

        if not structure.get('has_header'):
            suggestions.append({
                'type': 'info',
                'issue': 'No header detected',
                'suggestion': 'Consider adding a header/navigation',
                'recommendation': 'Headers help users navigate your site'
            })

        return suggestions

    def _suggest_typography_improvements(self, typography: Dict) -> List[Dict]:
        """Suggest typography improvements"""
        suggestions = []

        fonts = typography.get('fonts', {})
        total_fonts = fonts.get('total_unique', 0)

        if total_fonts == 0:
            suggestions.append({
                'type': 'warning',
                'issue': 'No custom fonts detected',
                'suggestion': 'Consider using web fonts for better typography',
                'recommendation': 'Use Google Fonts or system font stacks'
            })

        if total_fonts > 4:
            suggestions.append({
                'type': 'warning',
                'issue': 'Too many fonts',
                'suggestion': 'Limit to 2-3 font families',
                'recommendation': 'Too many fonts can look inconsistent and hurt performance'
            })

        # Check headings
        headings = typography.get('headings', {})

        if not headings.get('uses_semantic_headings'):
            suggestions.append({
                'type': 'recommendation',
                'issue': 'No semantic headings',
                'suggestion': 'Use proper heading hierarchy (h1-h6)',
                'recommendation': 'Important for SEO and accessibility'
            })

        hierarchy_score = headings.get('heading_hierarchy_score', 100)

        if hierarchy_score < 70:
            suggestions.append({
                'type': 'warning',
                'issue': 'Poor heading hierarchy',
                'suggestion': 'Improve heading structure',
                'recommendation': 'Ensure proper nesting and use of h1-h6'
            })

        # Check spacing
        spacing = typography.get('spacing', {})

        if not spacing.get('line_height', {}).get('used'):
            suggestions.append({
                'type': 'info',
                'issue': 'No custom line-height',
                'suggestion': 'Set appropriate line-height for readability',
                'recommendation': 'Use 1.5-1.6 for body text, 1.2-1.4 for headings'
            })

        return suggestions

    def _suggest_style_improvements(self, style: Dict) -> List[Dict]:
        """Suggest style improvements"""
        suggestions = []

        # Check modern features
        modern = style.get('modern_features', {})
        modernity_score = modern.get('modernity_score', 0)

        if modernity_score < 50:
            suggestions.append({
                'type': 'recommendation',
                'issue': 'Limited modern CSS features',
                'suggestion': 'Adopt modern CSS techniques',
                'recommendation': self.kb.get_recommendations('style')
            })

        if not modern.get('css_variables'):
            suggestions.append({
                'type': 'recommendation',
                'issue': 'Not using CSS variables',
                'suggestion': 'Use CSS custom properties for theming',
                'recommendation': 'Makes it easier to maintain consistent styles'
            })

        if not modern.get('transforms'):
            suggestions.append({
                'type': 'info',
                'issue': 'No CSS transforms',
                'suggestion': 'Consider adding subtle transform animations',
                'recommendation': 'Enhances user interaction feedback'
            })

        # Check animations
        animations = style.get('animations', {})

        if not animations.get('has_animations'):
            suggestions.append({
                'type': 'info',
                'issue': 'No animations',
                'suggestion': 'Add subtle animations for better UX',
                'recommendation': 'Animations guide user attention and improve perceived performance'
            })

        # Check transitions
        transitions = style.get('transitions', {})

        if not transitions.get('has_transitions'):
            suggestions.append({
                'type': 'recommendation',
                'issue': 'No transitions',
                'suggestion': 'Add transitions to interactive elements',
                'recommendation': 'Smooth transitions improve user experience'
            })

        return suggestions

    def _prioritize_suggestions(self, analysis: Dict, suggestions: Dict) -> List[Dict]:
        """Prioritize suggestions based on impact"""
        priority = []

        quality_score = analysis.get('quality_score', 0)

        # Critical: Responsive design
        layout_suggestions = suggestions.get('layout', [])
        for suggestion in layout_suggestions:
            if suggestion.get('type') == 'critical':
                priority.append(suggestion)

        # High priority: Typography and colors
        if quality_score < 50:
            priority.extend([
                {
                    'type': 'high_priority',
                    'issue': 'Low overall quality score',
                    'suggestion': 'Focus on improving layout, colors, and typography',
                    'recommendation': 'Review the specific suggestions in each category'
                }
            ])

        # Add top 3 warnings from each category
        for category in ['colors', 'layout', 'typography', 'style']:
            warnings = [s for s in suggestions.get(category, []) if s.get('type') == 'warning']
            priority.extend(warnings[:2])

        return priority[:10]  # Return top 10 priority suggestions
