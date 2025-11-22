"""Pattern learner that processes analyzed templates"""

import json
from pathlib import Path
from typing import Dict, List
from .knowledge_base import KnowledgeBase
from .design_excellence import DesignExcellence


class PatternLearner:
    """
    Learns patterns from analyzed templates and builds knowledge base.

    Philosophy: Quality over quantity. Only learn from exceptional designs.
    """

    def __init__(self, knowledge_base_path: str = "data/knowledge_base/design_patterns.json"):
        self.kb = KnowledgeBase(knowledge_base_path)
        self.excellence = DesignExcellence()
        self.rejected_count = 0
        self.excellence_stats = {
            'masterpiece': 0,
            'excellent': 0,
            'acceptable': 0,
            'rejected': 0
        }

    def learn_from_analysis(self, analysis_file: Path) -> bool:
        """
        Learn from a single analyzed template file.
        Only accepts designs that meet our excellence standards.
        """
        try:
            analysis = json.loads(analysis_file.read_text(encoding='utf-8'))

            # Evaluate design quality with high standards
            evaluation = self.excellence.evaluate_design(analysis)
            score = evaluation['overall_score']
            level = evaluation['excellence_level']

            # Only learn from designs that meet our minimum quality threshold
            if not self.excellence.should_learn_from(analysis):
                print(f"    ⊘ REJECTED - Score: {score}/100 ({level})")
                print(f"      Reason: {evaluation['verdict']}")
                self.rejected_count += 1
                self.excellence_stats['rejected'] += 1
                return False

            # Track excellence levels
            if level == 'masterpiece':
                self.excellence_stats['masterpiece'] += 1
                print(f"    ★ MASTERPIECE - Score: {score}/100")
            elif level == 'excellent':
                self.excellence_stats['excellent'] += 1
                print(f"    ✓ EXCELLENT - Score: {score}/100")
            else:  # acceptable
                self.excellence_stats['acceptable'] += 1
                print(f"    ✓ Acceptable - Score: {score}/100")

            # Learn from this quality design
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
        print(f"  ⊘ Rejected: {self.rejected_count} (below excellence threshold)")
        print(f"\n  Excellence Breakdown:")
        print(f"    ★ Masterpieces: {self.excellence_stats['masterpiece']}")
        print(f"    ✓ Excellent: {self.excellence_stats['excellent']}")
        print(f"    ✓ Acceptable: {self.excellence_stats['acceptable']}")
        print(f"    ⊘ Rejected: {self.excellence_stats['rejected']}")

        print(f"\n  Knowledge base stats:")
        stats = self.kb.get_statistics()
        for key, value in stats.items():
            print(f"    - {key}: {value}")

        return {
            'success': True,
            'learned': learned_count,
            'rejected': self.rejected_count,
            'excellence_stats': self.excellence_stats,
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
