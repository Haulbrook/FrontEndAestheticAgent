"""
Design Excellence Module - The Bot's "Attitude" and Quality Standards

This module defines the bot's philosophy: Never settle for mediocre.
Focus on sophistication, refinement, and immersive experiences.
"""

from typing import Dict, List, Optional
from pathlib import Path
import json


class DesignExcellence:
    """
    Enforces high design standards and provides self-critique.

    Philosophy:
    - Quality over quantity
    - Sophistication over simplicity
    - Immersive over functional
    - Refined details over broad strokes
    - Harmonious over trendy
    """

    # Quality thresholds - We only learn from the best
    MINIMUM_QUALITY = 70  # Don't even look at anything below 70/100
    EXCELLENT_QUALITY = 85  # This is where we start getting excited
    MASTERPIECE_QUALITY = 95  # Reference-worthy, portfolio-quality

    def __init__(self):
        self.excellence_criteria = self._define_excellence_criteria()
        self.sophistication_markers = self._define_sophistication_markers()

    def _define_excellence_criteria(self) -> Dict:
        """Define what makes a design excellent"""
        return {
            'visual_hierarchy': {
                'weight': 15,
                'indicators': [
                    'clear focal points',
                    'intentional eye flow',
                    'strategic use of scale and contrast',
                    'purposeful white space',
                    'guided user journey'
                ]
            },
            'typography_mastery': {
                'weight': 15,
                'indicators': [
                    'sophisticated font pairings (not just Google Fonts defaults)',
                    'precise letter-spacing and line-height',
                    'responsive type scaling with fluid typography',
                    'proper typographic hierarchy (6+ levels)',
                    'attention to widows, orphans, and rag',
                    'custom font weights and styles'
                ]
            },
            'color_sophistication': {
                'weight': 15,
                'indicators': [
                    'cohesive color system (not random colors)',
                    'intentional color psychology',
                    'sophisticated palettes (complementary, analogous, triadic)',
                    'proper use of tints, shades, and tones',
                    'accessibility without sacrificing beauty',
                    'color gradients with purpose'
                ]
            },
            'micro_interactions': {
                'weight': 15,
                'indicators': [
                    'thoughtful hover states',
                    'smooth transitions (not jarring)',
                    'loading states and skeletons',
                    'feedback for every interaction',
                    'delightful animations (purposeful, not decorative)',
                    'parallax effects when appropriate'
                ]
            },
            'layout_sophistication': {
                'weight': 10,
                'indicators': [
                    'asymmetric layouts with balance',
                    'creative grid breaking',
                    'dynamic spacing systems',
                    'intentional use of negative space',
                    'layering and depth',
                    'unconventional but functional layouts'
                ]
            },
            'attention_to_detail': {
                'weight': 15,
                'indicators': [
                    'custom illustrations or graphics',
                    'thoughtful iconography',
                    'consistent border-radius system',
                    'shadow hierarchy and elevation',
                    'pixel-perfect alignment',
                    'custom cursors or UI elements',
                    'ornate decorative elements'
                ]
            },
            'immersive_experience': {
                'weight': 10,
                'indicators': [
                    'storytelling through design',
                    'engaging scroll experiences',
                    'seamless section transitions',
                    'ambient effects (particles, backgrounds)',
                    'sound design integration (when appropriate)',
                    'full-bleed imagery with purpose'
                ]
            },
            'technical_excellence': {
                'weight': 5,
                'indicators': [
                    'optimized performance (no jank)',
                    'smooth 60fps animations',
                    'progressive enhancement',
                    'responsive without breakage',
                    'accessible but not boring'
                ]
            }
        }

    def _define_sophistication_markers(self) -> Dict:
        """Red flags for cookie-cutter designs vs. markers of sophistication"""
        return {
            'avoid': {
                'generic_bootstrap': 'Default Bootstrap themes without customization',
                'stock_photos': 'Overused stock photography (smiling people in offices)',
                'basic_buttons': 'Plain rectangular buttons with no personality',
                'default_fonts': 'Arial, Helvetica, Times New Roman without intention',
                'cookie_cutter_layouts': 'Header-Hero-3Columns-CTA-Footer formula',
                'boring_animations': 'Basic fade-ins and slide-ups everywhere',
                'flat_design_overuse': 'Completely flat with no depth or interest',
                'predictable_interactions': 'Every button does the same hover effect',
                'template_vibes': 'Looks like it came straight from a template marketplace',
                'corporate_bland': 'Safe, boring, forgettable designs'
            },
            'pursue': {
                'custom_typography': 'Unique font pairings with character',
                'bespoke_components': 'Custom-designed UI elements',
                'intentional_brutalism': 'Bold, confident design choices',
                'refined_minimalism': 'Minimal but rich with subtle details',
                'ornate_maximalism': 'Rich, detailed, immersive when appropriate',
                'unique_layouts': 'Unexpected but functional arrangements',
                'signature_interactions': 'Memorable micro-interactions',
                'artistic_courage': 'Taking design risks that pay off',
                'crafted_details': 'Evidence of obsessive attention to detail',
                'emotional_resonance': 'Design that evokes feeling'
            }
        }

    def evaluate_design(self, analysis: Dict) -> Dict:
        """
        Evaluate a design with high standards.
        Returns detailed critique and excellence score.
        """
        evaluation = {
            'overall_score': 0,
            'excellence_level': 'mediocre',
            'strengths': [],
            'critical_issues': [],
            'refinement_opportunities': [],
            'verdict': '',
            'self_rating_confidence': 0
        }

        # Calculate sophisticated score
        score = self._calculate_excellence_score(analysis)
        evaluation['overall_score'] = score

        # Determine excellence level
        if score >= self.MASTERPIECE_QUALITY:
            evaluation['excellence_level'] = 'masterpiece'
            evaluation['verdict'] = 'Portfolio-worthy. This is the standard we pursue.'
            evaluation['self_rating_confidence'] = 95
        elif score >= self.EXCELLENT_QUALITY:
            evaluation['excellence_level'] = 'excellent'
            evaluation['verdict'] = 'Strong work. Room for refinement, but impressive.'
            evaluation['self_rating_confidence'] = 85
        elif score >= self.MINIMUM_QUALITY:
            evaluation['excellence_level'] = 'acceptable'
            evaluation['verdict'] = 'Meets baseline. Lacks sophistication for our standards.'
            evaluation['self_rating_confidence'] = 70
        else:
            evaluation['excellence_level'] = 'mediocre'
            evaluation['verdict'] = 'Below our standards. Too generic or poorly executed.'
            evaluation['self_rating_confidence'] = 50

        # Detailed critique
        evaluation['strengths'] = self._identify_strengths(analysis)
        evaluation['critical_issues'] = self._identify_critical_issues(analysis)
        evaluation['refinement_opportunities'] = self._identify_refinements(analysis)

        return evaluation

    def _calculate_excellence_score(self, analysis: Dict) -> int:
        """Calculate score based on excellence criteria"""
        score = 0
        criteria = self.excellence_criteria

        # Visual Hierarchy (15 points)
        layout = analysis.get('layout', {})
        if layout.get('layout_systems', {}).get('grid', {}).get('detected'):
            score += 5
        if layout.get('layout_systems', {}).get('flexbox', {}).get('detected'):
            score += 5
        if layout.get('responsive', {}).get('responsive_score', 0) > 70:
            score += 5

        # Typography Mastery (15 points)
        typography = analysis.get('typography', {})
        fonts = typography.get('fonts', {})
        if fonts.get('total_unique', 0) >= 2:
            score += 5
        if typography.get('headings', {}).get('uses_semantic_headings'):
            score += 5
        if fonts.get('custom_fonts'):
            score += 5

        # Color Sophistication (15 points)
        colors = analysis.get('colors', {})
        total_colors = colors.get('total_colors', 0)
        color_scheme = colors.get('color_scheme', '')
        if 5 <= total_colors <= 12:  # Sweet spot
            score += 5
        if color_scheme in ['vibrant', 'balanced', 'dark_mode']:
            score += 5
        palette = colors.get('palette_characteristics', {})
        if palette.get('is_vibrant') or palette.get('is_dark'):
            score += 5

        # Micro-interactions & Style (15 points)
        style = analysis.get('style', {})
        modern = style.get('modern_features', {})
        if modern.get('css_variables'):
            score += 3
        if modern.get('animations'):
            score += 3
        if modern.get('transforms'):
            score += 3
        if modern.get('transitions'):
            score += 3
        if modern.get('custom_properties'):
            score += 3

        # Frameworks used well (10 points)
        frameworks = analysis.get('frameworks', {})
        css_frameworks = frameworks.get('css_frameworks', [])
        if css_frameworks:
            # Penalize if just using default Bootstrap
            if 'Bootstrap' in css_frameworks and len(css_frameworks) == 1:
                score += 3  # Basic usage
            else:
                score += 7  # Multiple frameworks or non-Bootstrap
        else:
            score += 10  # Custom design, no frameworks (impressive if done well)

        # Attention to Detail (15 points)
        modernity_score = modern.get('modernity_score', 0)
        score += int(modernity_score * 0.15)

        # Immersive Experience (10 points)
        if colors.get('total_colors', 0) > 8:  # Rich color palette
            score += 3
        if layout.get('sections', {}).get('total_sections', 0) > 5:  # Multi-section experience
            score += 3
        quality = analysis.get('quality_score', 0)
        if quality > 70:
            score += 4

        # Technical Excellence (5 points)
        if layout.get('responsive', {}).get('has_media_queries'):
            score += 3
        if modern.get('modernity_score', 0) > 70:
            score += 2

        return min(100, score)

    def _identify_strengths(self, analysis: Dict) -> List[str]:
        """Identify what the design does well"""
        strengths = []

        # Check typography
        typography = analysis.get('typography', {})
        if typography.get('fonts', {}).get('total_unique', 0) >= 3:
            strengths.append('Sophisticated font system with multiple weights')

        # Check color
        colors = analysis.get('colors', {})
        if colors.get('color_scheme') == 'vibrant':
            strengths.append('Bold, confident color choices')
        elif colors.get('color_scheme') == 'dark_mode':
            strengths.append('Refined dark mode aesthetic')

        # Check layout
        layout = analysis.get('layout', {})
        if layout.get('layout_systems', {}).get('grid', {}).get('detected'):
            strengths.append('Modern CSS Grid implementation')

        # Check frameworks
        frameworks = analysis.get('frameworks', {})
        if frameworks.get('animation_libraries'):
            strengths.append('Enhanced with animation library')

        return strengths

    def _identify_critical_issues(self, analysis: Dict) -> List[str]:
        """Identify deal-breakers or major issues"""
        issues = []

        # Typography issues
        typography = analysis.get('typography', {})
        if typography.get('fonts', {}).get('total_unique', 0) < 2:
            issues.append('CRITICAL: Single font family. Lacks typographic sophistication.')

        # Color issues
        colors = analysis.get('colors', {})
        if colors.get('total_colors', 0) < 4:
            issues.append('CRITICAL: Limited color palette. Too basic.')
        elif colors.get('total_colors', 0) > 20:
            issues.append('CRITICAL: Color chaos. No cohesive system.')

        # Layout issues
        layout = analysis.get('layout', {})
        if not layout.get('responsive', {}).get('has_media_queries'):
            issues.append('CRITICAL: No responsive design. Unacceptable in 2025.')

        # No modern features
        style = analysis.get('style', {})
        if style.get('modern_features', {}).get('modernity_score', 0) < 40:
            issues.append('CRITICAL: Outdated techniques. Feels like 2015.')

        # Cookie-cutter detection
        frameworks = analysis.get('frameworks', {})
        if 'Bootstrap' in frameworks.get('css_frameworks', []) and \
           frameworks.get('confidence_scores', {}).get('Bootstrap', 0) > 90:
            issues.append('WARNING: Heavy Bootstrap usage. Risk of generic appearance.')

        return issues

    def _identify_refinements(self, analysis: Dict) -> List[str]:
        """Suggest sophisticated refinements"""
        refinements = []

        # Always room for more sophistication
        refinements.append('Consider adding subtle parallax effects for depth')
        refinements.append('Implement custom cursor interactions for key elements')
        refinements.append('Add micro-interactions to all clickable elements')
        refinements.append('Ensure smooth 60fps animations throughout')
        refinements.append('Consider adding ambient background effects')
        refinements.append('Implement skeleton loading states for better perceived performance')
        refinements.append('Add ornate decorative elements to section breaks')
        refinements.append('Consider variable fonts for fluid typography')
        refinements.append('Implement color mode switching with smooth transitions')
        refinements.append('Add thoughtful empty states and error handling')

        return refinements[:5]  # Top 5 priorities

    def should_learn_from(self, analysis: Dict) -> bool:
        """
        Decide if this template is worth learning from.
        Only accept excellent designs into our knowledge base.
        """
        evaluation = self.evaluate_design(analysis)
        score = evaluation['overall_score']

        # Only learn from designs that meet our standards
        return score >= self.MINIMUM_QUALITY

    def get_learning_priority(self, analysis: Dict) -> str:
        """Determine how eagerly we should learn from this"""
        evaluation = self.evaluate_design(analysis)
        score = evaluation['overall_score']

        if score >= self.MASTERPIECE_QUALITY:
            return 'PRIORITY_HIGH'  # Study this deeply
        elif score >= self.EXCELLENT_QUALITY:
            return 'PRIORITY_MEDIUM'  # Learn key patterns
        elif score >= self.MINIMUM_QUALITY:
            return 'PRIORITY_LOW'  # Note but don't prioritize
        else:
            return 'SKIP'  # Don't waste time

    def generate_self_critique(self, generated_design: Dict) -> Dict:
        """
        The bot critiques its own work.
        Continuous self-improvement mindset.
        """
        return {
            'self_assessment': self.evaluate_design(generated_design),
            'improvement_plan': self._create_improvement_plan(generated_design),
            'confidence': self._calculate_confidence(generated_design)
        }

    def _create_improvement_plan(self, design: Dict) -> List[str]:
        """Create a plan to improve the generated design"""
        plan = []
        evaluation = self.evaluate_design(design)

        if evaluation['overall_score'] < self.MASTERPIECE_QUALITY:
            plan.append('Elevate typography with more sophisticated pairings')
            plan.append('Add depth through layering and shadows')
            plan.append('Implement more nuanced color system')
            plan.append('Refine micro-interactions for delight')
            plan.append('Add ornate details to signature elements')

        return plan

    def _calculate_confidence(self, design: Dict) -> int:
        """How confident is the bot in its own work?"""
        evaluation = self.evaluate_design(design)
        score = evaluation['overall_score']

        # High standards - we're never fully satisfied
        if score >= 95:
            return 90  # Good but could be better
        elif score >= 85:
            return 80  # Solid work
        elif score >= 70:
            return 65  # Acceptable
        else:
            return 40  # Needs work
