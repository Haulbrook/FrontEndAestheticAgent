"""Main template analyzer that coordinates all analysis modules"""

import json
from pathlib import Path
from typing import Dict, Optional
from .color_analyzer import ColorAnalyzer
from .layout_analyzer import LayoutAnalyzer
from .typography_analyzer import TypographyAnalyzer
from .style_analyzer import StyleAnalyzer
from .framework_detector import FrameworkDetector


class TemplateAnalyzer:
    """Main analyzer that coordinates all analysis modules"""

    def __init__(self):
        self.color_analyzer = ColorAnalyzer()
        self.layout_analyzer = LayoutAnalyzer()
        self.typography_analyzer = TypographyAnalyzer()
        self.style_analyzer = StyleAnalyzer()
        self.framework_detector = FrameworkDetector()

    def analyze_template(self, template_dir: Path) -> Optional[Dict]:
        """Analyze a template directory"""
        print(f"  Analyzing: {template_dir.name}")

        # Read HTML
        html_files = list(template_dir.glob('**/*.html'))
        if not html_files:
            print(f"    ! No HTML files found")
            return None

        html_content = ""
        for html_file in html_files[:5]:  # Analyze up to 5 HTML files
            try:
                html_content += html_file.read_text(encoding='utf-8', errors='ignore')
            except Exception as e:
                print(f"    ! Error reading {html_file.name}: {e}")

        # Read CSS
        css_content = ""
        css_files = list(template_dir.glob('**/*.css'))
        for css_file in css_files[:10]:  # Analyze up to 10 CSS files
            try:
                css_content += css_file.read_text(encoding='utf-8', errors='ignore')
            except Exception as e:
                print(f"    ! Error reading {css_file.name}: {e}")

        if not html_content and not css_content:
            print(f"    ! No content to analyze")
            return None

        # Perform analysis
        try:
            analysis = {
                'template_id': template_dir.name,
                'colors': self.color_analyzer.analyze(html_content, css_content),
                'layout': self.layout_analyzer.analyze(html_content, css_content),
                'typography': self.typography_analyzer.analyze(html_content, css_content),
                'style': self.style_analyzer.analyze(html_content, css_content),
                'frameworks': self.framework_detector.detect_frameworks(html_content, css_content),
                'files_analyzed': {
                    'html_count': len(html_files),
                    'css_count': len(css_files)
                }
            }

            # Add overall quality score
            analysis['quality_score'] = self._calculate_quality_score(analysis)

            # Display detected frameworks
            detected_frameworks = analysis['frameworks']['css_frameworks'] + \
                                  analysis['frameworks']['component_libraries'] + \
                                  analysis['frameworks']['animation_libraries']
            if detected_frameworks:
                print(f"    📦 Frameworks: {', '.join(detected_frameworks)}")

            print(f"    ✓ Analysis complete (Quality: {analysis['quality_score']}/100)")
            return analysis

        except Exception as e:
            print(f"    ! Analysis error: {e}")
            return None

    def analyze_directory(self, templates_dir: str, output_dir: str = "data/analyzed") -> Dict:
        """Analyze all templates in a directory"""
        templates_path = Path(templates_dir)
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        if not templates_path.exists():
            print(f"✗ Directory not found: {templates_dir}")
            return {}

        # Find all template directories
        template_dirs = [d for d in templates_path.iterdir() if d.is_dir()]

        print(f"\n🔍 Analyzing {len(template_dirs)} templates from {templates_dir}\n")

        results = {}
        for template_dir in template_dirs:
            analysis = self.analyze_template(template_dir)
            if analysis:
                results[template_dir.name] = analysis

                # Save individual analysis
                output_file = output_path / f"{template_dir.name}.json"
                output_file.write_text(json.dumps(analysis, indent=2), encoding='utf-8')

        # Save aggregate analysis
        if results:
            aggregate_file = output_path / "aggregate_analysis.json"
            aggregate_file.write_text(json.dumps(results, indent=2), encoding='utf-8')

            print(f"\n✓ Analyzed {len(results)} templates")
            print(f"  Results saved to: {output_dir}/")

        return results

    def _calculate_quality_score(self, analysis: Dict) -> int:
        """Calculate overall quality score based on analysis"""
        score = 0

        # Color analysis (20 points)
        if analysis['colors'].get('total_colors', 0) > 3:
            score += 10
        if analysis['colors'].get('color_scheme') in ['vibrant', 'balanced']:
            score += 10

        # Layout analysis (20 points)
        layout_systems = analysis['layout'].get('layout_systems', {})
        if layout_systems.get('flexbox', {}).get('detected'):
            score += 10
        if layout_systems.get('grid', {}).get('detected'):
            score += 10

        # Typography analysis (20 points)
        if analysis['typography'].get('fonts', {}).get('total_unique', 0) >= 2:
            score += 10
        if analysis['typography'].get('headings', {}).get('uses_semantic_headings'):
            score += 10

        # Style analysis (20 points)
        modernity_score = analysis['style'].get('modern_features', {}).get('modernity_score', 0)
        score += int(modernity_score * 0.2)

        # Responsive design (20 points)
        responsive_score = analysis['layout'].get('responsive', {}).get('responsive_score', 0)
        score += int(responsive_score * 0.2)

        return min(100, score)
