#!/usr/bin/env python3
"""
Integration Script: Load GitHub Training Data into Knowledge Base

This script processes all GitHub repository analyses and integrates
framework-specific patterns into the knowledge base.
"""

import json
import sys
from pathlib import Path
from typing import Dict, List
from collections import defaultdict

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from agent.learner.knowledge_base import KnowledgeBase


class GitHubLearningIntegrator:
    """Integrates GitHub repository learnings into the knowledge base"""

    def __init__(self, analysis_dir: str = "data/github_training/analysis"):
        self.analysis_dir = Path(analysis_dir)
        self.knowledge_base_path = Path("data/knowledge_base/design_patterns.json")

    def integrate_all(self):
        """Integrate all GitHub learnings into knowledge base"""
        print("=" * 70)
        print("  GitHub Learnings Integration")
        print("=" * 70)
        print()

        # Load existing knowledge base
        kb_data = self._load_knowledge_base()

        # Add framework learnings section if it doesn't exist
        if 'framework_patterns' not in kb_data:
            kb_data['framework_patterns'] = self._initialize_framework_patterns()
            print("✓ Initialized framework_patterns section in knowledge base")

        # Load all analysis files
        analysis_files = list(self.analysis_dir.glob("*.json"))
        print(f"Found {len(analysis_files)} analysis files to process\n")

        # Process each analysis file
        processed = 0
        for analysis_file in analysis_files:
            if analysis_file.name == "analysis_summary.json":
                continue

            analysis = json.loads(analysis_file.read_text())
            self._integrate_analysis(kb_data, analysis)
            processed += 1
            print(f"  [{processed}/{len(analysis_files)-1}] Integrated {analysis['name']}")

        # Save updated knowledge base
        self._save_knowledge_base(kb_data)

        print()
        print("=" * 70)
        print("  Integration Complete!")
        print("=" * 70)
        print()
        print(f"✓ Processed {processed} framework analyses")
        print(f"✓ Knowledge base updated: {self.knowledge_base_path}")
        print()

        # Display summary
        self._display_summary(kb_data)

    def _initialize_framework_patterns(self) -> Dict:
        """Initialize framework patterns structure"""
        return {
            'css_frameworks': {},
            'vue_frameworks': {},
            'react_frameworks': {},
            'html_frameworks': {},
            'component_library': {
                'buttons': defaultdict(list),
                'cards': defaultdict(list),
                'navbars': defaultdict(list),
                'forms': defaultdict(list),
                'modals': defaultdict(list),
                'inputs': defaultdict(list),
                'tables': defaultdict(list),
                'alerts': defaultdict(list)
            },
            'animation_library': {
                'keyframes': [],
                'animation_classes': [],
                'transitions': []
            },
            'utility_patterns': {
                'spacing': defaultdict(list),
                'colors': defaultdict(list),
                'display': defaultdict(list),
                'text': defaultdict(list)
            },
            'grid_systems': {},
            'design_tokens': {
                'colors': [],
                'spacing': [],
                'breakpoints': []
            }
        }

    def _integrate_analysis(self, kb_data: Dict, analysis: Dict):
        """Integrate a single analysis into knowledge base"""
        name = analysis['name']
        category = analysis['category']
        learnings = analysis.get('learnings', {})

        # Store framework-specific data
        category_key = f"{category}_frameworks"
        if category_key in kb_data['framework_patterns']:
            kb_data['framework_patterns'][category_key][name] = {
                'focus_areas': analysis.get('focus_areas', []),
                'learnings': learnings,
                'file_count': analysis.get('file_count', 0),
                'component_count': analysis.get('component_count', 0)
            }

        # Integrate specific patterns
        if category == 'css':
            self._integrate_css_framework(kb_data, name, learnings)
        elif category == 'react':
            self._integrate_react_framework(kb_data, name, learnings)
        elif category == 'vue':
            self._integrate_vue_framework(kb_data, name, learnings)
        elif category == 'html':
            self._integrate_html_framework(kb_data, name, learnings)

    def _integrate_css_framework(self, kb_data: Dict, name: str, learnings: Dict):
        """Integrate CSS framework patterns"""
        fp = kb_data['framework_patterns']

        # Components
        components = learnings.get('components', {})
        for comp_type, items in components.items():
            if comp_type in fp['component_library']:
                for item in items:
                    if item and item not in fp['component_library'][comp_type][name]:
                        fp['component_library'][comp_type][name].append(item)

        # Animations (Animate.css)
        animations = learnings.get('animations', {})
        if animations:
            keyframes = animations.get('keyframes', [])
            fp['animation_library']['keyframes'].extend([
                {'name': kf, 'source': name} for kf in keyframes
                if kf not in [k['name'] for k in fp['animation_library']['keyframes']]
            ])

            anim_classes = animations.get('animation_classes', [])
            fp['animation_library']['animation_classes'].extend([
                {'name': ac, 'source': name} for ac in anim_classes
                if ac not in [a['name'] for a in fp['animation_library']['animation_classes']]
            ])

        # Grid patterns (Bootstrap, Bulma, etc.)
        grid = learnings.get('grid_patterns', {})
        if grid:
            kb_data['framework_patterns']['grid_systems'][name] = grid

        # Utility classes (Tailwind, Bootstrap)
        utilities = learnings.get('utility_classes', {})
        for util_type, items in utilities.items():
            if util_type in fp['utility_patterns'] and items:
                fp['utility_patterns'][util_type][name].extend(items)

        # Colors (Tailwind)
        colors = learnings.get('colors', {})
        if colors:
            css_vars = colors.get('css_variables', [])
            if css_vars:
                fp['design_tokens']['colors'].extend([
                    {'value': cv, 'source': name} for cv in css_vars
                    if cv not in [c['value'] for c in fp['design_tokens']['colors']]
                ])

        # Spacing (Tailwind)
        spacing = learnings.get('spacing', {})
        if spacing:
            for space_type, values in spacing.items():
                if values:
                    fp['design_tokens']['spacing'].extend([
                        {'type': space_type, 'values': values, 'source': name}
                    ])

    def _integrate_react_framework(self, kb_data: Dict, name: str, learnings: Dict):
        """Integrate React framework patterns"""
        fp = kb_data['framework_patterns']

        # Component types (Material-UI, Ant Design, etc.)
        component_types = learnings.get('component_types', {})
        for comp_type, items in component_types.items():
            if comp_type in fp['component_library']:
                for item in items:
                    if item and item not in fp['component_library'][comp_type][name]:
                        fp['component_library'][comp_type][name].append(item)

    def _integrate_vue_framework(self, kb_data: Dict, name: str, learnings: Dict):
        """Integrate Vue framework patterns"""
        # Similar to React integration
        self._integrate_react_framework(kb_data, name, learnings)

    def _integrate_html_framework(self, kb_data: Dict, name: str, learnings: Dict):
        """Integrate HTML framework patterns"""
        # Process HTML-specific patterns
        pass

    def _load_knowledge_base(self) -> Dict:
        """Load existing knowledge base"""
        if self.knowledge_base_path.exists():
            return json.loads(self.knowledge_base_path.read_text())
        else:
            print("! Knowledge base not found, creating new one")
            return {
                'metadata': {
                    'total_templates_learned': 0,
                    'version': '1.0'
                }
            }

    def _save_knowledge_base(self, kb_data: Dict):
        """Save updated knowledge base"""
        # Convert defaultdicts to regular dicts
        kb_data_clean = self._convert_to_serializable(kb_data)

        self.knowledge_base_path.parent.mkdir(parents=True, exist_ok=True)
        self.knowledge_base_path.write_text(
            json.dumps(kb_data_clean, indent=2, ensure_ascii=False),
            encoding='utf-8'
        )

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

    def _display_summary(self, kb_data: Dict):
        """Display integration summary"""
        fp = kb_data.get('framework_patterns', {})

        print("Framework Patterns Summary:")
        print(f"  • CSS Frameworks: {len(fp.get('css_frameworks', {}))}")
        print(f"  • React Frameworks: {len(fp.get('react_frameworks', {}))}")
        print(f"  • Vue Frameworks: {len(fp.get('vue_frameworks', {}))}")
        print(f"  • HTML Frameworks: {len(fp.get('html_frameworks', {}))}")
        print()

        # Component library stats
        comp_lib = fp.get('component_library', {})
        total_components = sum(
            sum(len(items) for items in comp_type.values())
            for comp_type in comp_lib.values()
            if isinstance(comp_type, dict)
        )
        print(f"  • Total Component Patterns: {total_components}")

        # Animation library stats
        anim_lib = fp.get('animation_library', {})
        print(f"  • Animation Keyframes: {len(anim_lib.get('keyframes', []))}")
        print(f"  • Animation Classes: {len(anim_lib.get('animation_classes', []))}")
        print()


def main():
    """Main integration function"""
    integrator = GitHubLearningIntegrator()
    integrator.integrate_all()

    print("Next steps:")
    print("  1. Review the updated knowledge base")
    print("  2. Enhance component analyzers to use framework patterns")
    print("  3. Test framework detection on templates")
    print()


if __name__ == "__main__":
    main()
