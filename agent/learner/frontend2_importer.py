"""Importer for Frontend2 training data into knowledge base"""

import json
from pathlib import Path
from typing import Dict, List
from collections import Counter
from .knowledge_base import KnowledgeBase


class Frontend2Importer:
    """Imports training data from Frontend2 repo into knowledge base"""

    def __init__(self, knowledge_base_path: str = "data/knowledge_base/design_patterns.json"):
        self.kb = KnowledgeBase(knowledge_base_path)
        self.frontend2_data_dir = Path("data/frontend2_training")

    def import_training_data(self) -> Dict:
        """Import all Frontend2 training data"""
        results = {
            'bot_training': self._import_bot_training(),
            'aesthetic_training': self._import_aesthetic_training(),
            'patterns_integrated': True
        }

        # Save the updated knowledge base
        self.kb.save()

        print("\n✅ Frontend2 data successfully integrated into knowledge base!")
        return results

    def _import_bot_training(self) -> Dict:
        """Import bot_training_dataset.json"""
        bot_training_file = self.frontend2_data_dir / "bot_training_dataset.json"

        if not bot_training_file.exists():
            print("⚠ bot_training_dataset.json not found")
            return {'success': False}

        print("\n📊 Importing bot training dataset...")

        with open(bot_training_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Extract and integrate learned patterns
        learned_patterns = data.get('learned_patterns', {})

        # Import popular colors
        popular_colors = learned_patterns.get('popular_colors', [])
        for color_data in popular_colors:
            color = color_data.get('color', '')
            frequency = color_data.get('frequency', 0)

            # Add to color patterns
            if color and color.startswith('#'):
                # Store in dominant_colors
                existing = self.kb.patterns['color_patterns']['dominant_colors']
                color_entry = {'color': color, 'frequency': frequency, 'source': 'frontend2'}

                # Check if color already exists
                found = False
                for i, existing_color in enumerate(existing):
                    if existing_color.get('color') == color:
                        existing[i]['frequency'] = existing_color.get('frequency', 0) + frequency
                        found = True
                        break

                if not found:
                    existing.append(color_entry)

        print(f"  ✓ Imported {len(popular_colors)} popular colors")

        # Import training examples to extract more patterns
        examples = data.get('training_examples', [])
        categories_learned = set()

        for example in examples:
            output = example.get('output', {})
            input_data = example.get('input', {})

            category = input_data.get('category', 'unknown')
            categories_learned.add(category)

            # Extract color palettes
            color_palette = output.get('color_palette', [])
            if color_palette:
                self.kb.patterns['color_patterns']['popular_palettes'].append(color_palette)

            # Extract layout structure
            layout_structure = output.get('layout_structure', {})
            for component, count in layout_structure.items():
                if count > 0:
                    current = self.kb.patterns['layout_patterns']['component_usage'].get(component, 0)
                    self.kb.patterns['layout_patterns']['component_usage'][component] = current + count

            # Extract design principles
            design_principles = output.get('design_principles', {})
            if design_principles.get('has_semantic_html'):
                current = self.kb.patterns['modern_features']['feature_usage'].get('semantic_html', 0)
                self.kb.patterns['modern_features']['feature_usage']['semantic_html'] = current + 1

        print(f"  ✓ Processed {len(examples)} training examples")
        print(f"  ✓ Categories: {', '.join(categories_learned)}")

        # Update metadata
        self.kb.patterns['metadata']['frontend2_integrated'] = True
        self.kb.patterns['metadata']['frontend2_examples'] = len(examples)

        return {
            'success': True,
            'colors_imported': len(popular_colors),
            'examples_processed': len(examples),
            'categories': list(categories_learned)
        }

    def _import_aesthetic_training(self) -> Dict:
        """Import aesthetic_training_data.json"""
        aesthetic_file = self.frontend2_data_dir / "aesthetic_training_data.json"

        if not aesthetic_file.exists():
            print("⚠ aesthetic_training_data.json not found")
            return {'success': False}

        print("\n🎨 Importing aesthetic training data...")

        with open(aesthetic_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        resources_by_category = {}

        for item in data:
            category = item.get('category', 'unknown')
            resources_by_category[category] = resources_by_category.get(category, 0) + 1

            # Import colors
            colors = item.get('colors', [])
            hex_colors = [c for c in colors if c.startswith('#')]

            for color in hex_colors[:5]:  # Top 5 colors per resource
                existing = self.kb.patterns['color_patterns']['dominant_colors']

                # Add or update color frequency
                found = False
                for i, existing_color in enumerate(existing):
                    if existing_color.get('color') == color:
                        existing[i]['frequency'] = existing_color.get('frequency', 0) + 1
                        found = True
                        break

                if not found:
                    existing.append({'color': color, 'frequency': 1, 'source': 'frontend2_aesthetic'})

            # Import layout data
            layout = item.get('layout', {})
            for component, count in layout.items():
                if count > 0:
                    current = self.kb.patterns['layout_patterns']['component_usage'].get(component, 0)
                    self.kb.patterns['layout_patterns']['component_usage'][component] = current + count

            # Import typography
            typography = item.get('typography', {})
            font_links = typography.get('font_links', [])

            for font_link in font_links:
                # Extract font family names from links
                if 'family=' in font_link:
                    font_name = font_link.split('family=')[1].split('&')[0]
                    current = self.kb.patterns['typography_patterns']['popular_fonts'].get(font_name, 0)
                    self.kb.patterns['typography_patterns']['popular_fonts'][font_name] = current + 1

        print(f"  ✓ Imported {len(data)} aesthetic training samples")
        print(f"  ✓ Resources by category:")
        for category, count in resources_by_category.items():
            print(f"      - {category}: {count}")

        return {
            'success': True,
            'samples_imported': len(data),
            'categories': resources_by_category
        }

    def get_integrated_statistics(self) -> Dict:
        """Get statistics after integration"""
        return self.kb.get_statistics()

    def create_integration_report(self, output_file: str = "data/frontend2_training/integration_report.json"):
        """Create a report of the integration"""
        output_path = Path(output_file)

        # Sort dominant colors by frequency
        dominant_colors = self.kb.patterns['color_patterns']['dominant_colors']
        sorted_colors = sorted(dominant_colors, key=lambda x: x.get('frequency', 0), reverse=True)[:20]

        # Get top components
        component_usage = self.kb.patterns['layout_patterns']['component_usage']
        top_components = sorted(component_usage.items(), key=lambda x: x[1], reverse=True)[:10]

        # Get top fonts
        popular_fonts = self.kb.patterns['typography_patterns']['popular_fonts']
        top_fonts = sorted(popular_fonts.items(), key=lambda x: x[1], reverse=True)[:10]

        report = {
            'integration_summary': {
                'frontend2_integrated': self.kb.patterns['metadata'].get('frontend2_integrated', False),
                'total_examples': self.kb.patterns['metadata'].get('frontend2_examples', 0),
                'total_templates_in_kb': self.kb.patterns['metadata']['total_templates_learned']
            },
            'top_colors': [
                {'color': c['color'], 'frequency': c['frequency'], 'source': c.get('source', 'unknown')}
                for c in sorted_colors
            ],
            'top_components': [
                {'component': comp, 'usage_count': count}
                for comp, count in top_components
            ],
            'top_fonts': [
                {'font': font, 'usage_count': count}
                for font, count in top_fonts
            ],
            'knowledge_base_stats': self.get_integrated_statistics()
        }

        output_path.write_text(
            json.dumps(report, indent=2, ensure_ascii=False),
            encoding='utf-8'
        )

        print(f"\n📄 Integration report saved to: {output_file}")

        # Print summary
        print("\n" + "="*60)
        print("INTEGRATION SUMMARY")
        print("="*60)
        print(f"\nTop 10 Colors (by frequency):")
        for i, color in enumerate(sorted_colors[:10], 1):
            print(f"  {i}. {color['color']} (used {color['frequency']} times)")

        print(f"\nTop 10 Components:")
        for i, (comp, count) in enumerate(top_components[:10], 1):
            print(f"  {i}. {comp}: {count} instances")

        print(f"\nTop 10 Fonts:")
        for i, (font, count) in enumerate(top_fonts[:10], 1):
            print(f"  {i}. {font}: {count} instances")

        return report


def import_frontend2_data():
    """Convenience function to import Frontend2 data"""
    importer = Frontend2Importer()
    results = importer.import_training_data()
    report = importer.create_integration_report()
    return results, report


if __name__ == "__main__":
    import_frontend2_data()
