"""Template Browser - Browse all templates and components in a web UI"""

import json
from pathlib import Path
from flask import Flask, render_template, send_from_directory, jsonify
import os


class TemplateBrowser:
    """Web-based browser for templates and components"""

    def __init__(self, templates_dir: str = "data/templates", components_dir: str = "data/components"):
        self.templates_dir = Path(templates_dir)
        self.components_dir = Path(components_dir)
        self.app = Flask(__name__,
                        template_folder=str(Path(__file__).parent / 'templates'),
                        static_folder=str(Path(__file__).parent / 'static'))

        self._setup_routes()

    def _setup_routes(self):
        """Setup Flask routes"""

        @self.app.route('/')
        def index():
            """Main page showing all templates"""
            templates = self._get_all_templates()
            stats = self._get_statistics()
            return render_template('index.html', templates=templates, stats=stats)

        @self.app.route('/templates')
        def templates_list():
            """API endpoint for templates list"""
            templates = self._get_all_templates()
            return jsonify(templates)

        @self.app.route('/components')
        def components_page():
            """Components browsing page"""
            components = self._get_component_summary()
            return render_template('components.html', components=components)

        @self.app.route('/components/<category>')
        def components_by_category(category):
            """View components in a specific category"""
            components = self._get_components_by_category(category)
            return render_template('component_category.html', category=category, components=components)

        @self.app.route('/template/<source>/<template_name>')
        def view_template(source, template_name):
            """View a specific template"""
            template_path = self.templates_dir / source / template_name

            # Find index.html or first HTML file
            html_files = list(template_path.rglob('*.html'))

            if not html_files:
                return "No HTML files found", 404

            # Prefer index.html
            index_file = None
            for f in html_files:
                if f.name.lower() == 'index.html':
                    index_file = f
                    break

            if not index_file:
                index_file = html_files[0]

            # Serve the HTML file
            return send_from_directory(index_file.parent, index_file.name)

        @self.app.route('/static/templates/<path:filepath>')
        def serve_template_assets(filepath):
            """Serve template static assets"""
            return send_from_directory(self.templates_dir, filepath)

        @self.app.route('/api/component/<category>/<filename>')
        def get_component(category, filename):
            """Get component details"""
            component_file = self.components_dir / category / filename
            if component_file.exists():
                with open(component_file, 'r') as f:
                    return jsonify(json.load(f))
            return jsonify({'error': 'Component not found'}), 404

    def _get_all_templates(self):
        """Get list of all templates"""
        templates = []

        if not self.templates_dir.exists():
            return templates

        for source_dir in sorted(self.templates_dir.iterdir()):
            if not source_dir.is_dir():
                continue

            source_name = source_dir.name

            for template_dir in sorted(source_dir.iterdir()):
                if not template_dir.is_dir():
                    continue

                # Get metadata if exists
                metadata_file = template_dir / 'metadata.json'
                metadata = {}
                if metadata_file.exists():
                    try:
                        with open(metadata_file, 'r') as f:
                            metadata = json.load(f)
                    except:
                        pass

                # Find HTML files
                html_files = list(template_dir.rglob('*.html'))

                templates.append({
                    'name': template_dir.name,
                    'source': source_name,
                    'title': metadata.get('title', template_dir.name),
                    'url': metadata.get('url', ''),
                    'description': metadata.get('description', ''),
                    'has_html': len(html_files) > 0,
                    'html_count': len(html_files),
                    'view_url': f'/template/{source_name}/{template_dir.name}'
                })

        return templates

    def _get_statistics(self):
        """Get browser statistics"""
        templates = self._get_all_templates()
        components_summary = self._get_component_summary()

        return {
            'total_templates': len(templates),
            'total_components': sum(cat['count'] for cat in components_summary),
            'sources': len(set(t['source'] for t in templates)),
            'templates_with_html': sum(1 for t in templates if t['has_html'])
        }

    def _get_component_summary(self):
        """Get summary of all components"""
        summary = []

        if not self.components_dir.exists():
            return summary

        categories = ['navigation', 'buttons', 'cards', 'heroes', 'forms', 'footers', 'headers', 'sections']

        for category in categories:
            category_dir = self.components_dir / category
            if category_dir.exists():
                components = list(category_dir.glob('*.json'))
                summary.append({
                    'category': category,
                    'count': len(components),
                    'view_url': f'/components/{category}'
                })

        return summary

    def _get_components_by_category(self, category):
        """Get all components in a category"""
        components = []
        category_dir = self.components_dir / category

        if not category_dir.exists():
            return components

        for component_file in sorted(category_dir.glob('*.json')):
            try:
                with open(component_file, 'r') as f:
                    component_data = json.load(f)
                    component_data['filename'] = component_file.name
                    components.append(component_data)
            except:
                pass

        return components

    def run(self, host='127.0.0.1', port=5000, debug=True):
        """Start the browser server"""
        print(f"\n🌐 Template Browser starting...")
        print(f"   Open your browser to: http://{host}:{port}")
        print(f"   Press CTRL+C to stop\n")

        self.app.run(host=host, port=port, debug=debug)


if __name__ == '__main__':
    browser = TemplateBrowser()
    browser.run()
