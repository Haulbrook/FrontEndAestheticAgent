"""Pattern learner that processes analyzed templates"""

import json
from pathlib import Path
from typing import Dict, List
from .knowledge_base import KnowledgeBase


class PatternLearner:
    """Learns patterns from analyzed templates and builds knowledge base"""

    def __init__(self, knowledge_base_path: str = "data/knowledge_base/design_patterns.json"):
        self.kb = KnowledgeBase(knowledge_base_path)

    def learn_from_analysis(self, analysis_file: Path) -> bool:
        """Learn from a single analyzed template file"""
        try:
            analysis = json.loads(analysis_file.read_text(encoding='utf-8'))
            self.kb.add_template_analysis(analysis)
            return True
        except Exception as e:
            print(f"! Error learning from {analysis_file.name}: {e}")
            return False

    def learn_from_directory(self, analysis_dir: str) -> Dict:
        """Learn from all analyzed templates in a directory"""
        analysis_path = Path(analysis_dir)

        if not analysis_path.exists():
            print(f"✗ Directory not found: {analysis_dir}")
            return {'success': False, 'learned': 0}

        analysis_files = list(analysis_path.glob("*.json"))

        # Filter out aggregate analysis
        analysis_files = [f for f in analysis_files if 'aggregate' not in f.name.lower()]

        print(f"\n🧠 Learning from {len(analysis_files)} analyzed templates...\n")

        learned_count = 0
        for analysis_file in analysis_files:
            print(f"  Learning: {analysis_file.stem}")
            if self.learn_from_analysis(analysis_file):
                learned_count += 1
                print(f"    ✓ Learned")

        print(f"\n✓ Learned from {learned_count} templates")
        print(f"  Knowledge base stats:")

        stats = self.kb.get_statistics()
        for key, value in stats.items():
            print(f"    - {key}: {value}")

        return {
            'success': True,
            'learned': learned_count,
            'total_in_kb': stats['total_templates'],
            'statistics': stats
        }

    def get_knowledge_base(self) -> KnowledgeBase:
        """Get the knowledge base instance"""
        return self.kb

    def get_recommendations(self, category: str = 'all') -> Dict:
        """Get design recommendations based on learned patterns"""
        return self.kb.get_recommendations(category)

    def export_patterns(self, output_file: str = "data/knowledge_base/patterns_export.json"):
        """Export learned patterns to a file"""
        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        export_data = {
            'statistics': self.kb.get_statistics(),
            'recommendations': self.get_recommendations(),
            'raw_patterns': self.kb.patterns
        }

        output_path.write_text(
            json.dumps(export_data, indent=2, ensure_ascii=False),
            encoding='utf-8'
        )

        print(f"✓ Patterns exported to: {output_file}")
        return export_data
