"""React Bits scraper for extracting React components

This scraper clones/fetches the react-bits repository and extracts
React component files for analysis and learning.
"""

import os
import json
import time
import shutil
import subprocess
from typing import List, Dict, Optional
from pathlib import Path
from .base_scraper import BaseScraper


class ReactBitsScraper(BaseScraper):
    """Scraper that extracts React components from react-bits repo"""

    def __init__(self, output_dir: str = "data/templates/react-bits"):
        super().__init__(output_dir)
        self.repo_url = "https://github.com/Haulbrook/react-bits.git"
        self.repo_name = "react-bits"
        self.temp_clone_dir = Path(output_dir) / "_temp_clone"

        # Component file extensions to look for
        self.component_extensions = ['.jsx', '.tsx', '.js', '.ts']

        # Directories to search for components
        self.component_dirs = ['src']

    def get_template_list_url(self) -> str:
        return self.repo_url

    def scrape(self, limit: int = 10) -> List[Dict]:
        """Scrape React components from react-bits repository"""
        print(f"🎨 Scraping React Bits components (limit: {limit})...")

        components = []

        try:
            # Clone or update the repository
            if not self._clone_or_update_repo():
                print("  ❌ Failed to clone/update repository")
                return []

            # Find all component files
            component_files = self._find_component_files()
            print(f"  Found {len(component_files)} component files in repository")

            # Process components
            processed_count = 0
            for component_file in component_files:
                if processed_count >= limit:
                    break

                try:
                    # Generate unique ID for this component
                    relative_path = component_file.relative_to(self.temp_clone_dir)
                    component_id = self.generate_template_id(str(relative_path))

                    # Check if already processed
                    if self.template_exists(component_id):
                        print(f"  ⏭  {relative_path}: Already processed, skipping...")
                        continue

                    print(f"  ✓ Processing: {relative_path}")

                    # Extract component data
                    component_data = self._extract_component_data(component_file, relative_path)

                    if component_data:
                        component_data['id'] = component_id
                        component_data['source'] = 'react-bits'

                        # Save component
                        self.save_template(component_data, component_id)
                        components.append(component_data)
                        processed_count += 1
                        print(f"    ✅ Extracted successfully")
                    else:
                        print(f"    ⚠️  Could not extract component data")

                except Exception as e:
                    print(f"    ❌ Error processing {component_file.name}: {e}")
                    continue

            print(f"\n✅ Successfully extracted {processed_count} new components")

        finally:
            # Clean up temp clone directory
            self._cleanup_temp_clone()

        return components

    def _clone_or_update_repo(self) -> bool:
        """Clone the repository or update if it exists"""
        try:
            # Remove old temp directory if it exists
            if self.temp_clone_dir.exists():
                shutil.rmtree(self.temp_clone_dir)

            # Create temp directory
            self.temp_clone_dir.mkdir(parents=True, exist_ok=True)

            print(f"  📥 Cloning repository from {self.repo_url}...")

            # Clone the repository
            result = subprocess.run(
                ['git', 'clone', '--depth', '1', self.repo_url, str(self.temp_clone_dir)],
                capture_output=True,
                text=True,
                timeout=300
            )

            if result.returncode == 0:
                print(f"  ✅ Repository cloned successfully")
                return True
            else:
                print(f"  ❌ Git clone failed: {result.stderr}")
                return False

        except subprocess.TimeoutExpired:
            print(f"  ❌ Clone operation timed out")
            return False
        except Exception as e:
            print(f"  ❌ Error cloning repository: {e}")
            return False

    def _find_component_files(self) -> List[Path]:
        """Find all component files in the repository"""
        component_files = []

        for component_dir in self.component_dirs:
            search_dir = self.temp_clone_dir / component_dir

            if not search_dir.exists():
                print(f"  ⚠️  Directory not found: {component_dir}")
                continue

            # Recursively find all component files
            for ext in self.component_extensions:
                component_files.extend(search_dir.rglob(f'*{ext}'))

        # Filter out test files, config files, etc.
        component_files = [
            f for f in component_files
            if not any(exclude in str(f).lower() for exclude in [
                'test', 'spec', '.test.', '.spec.', 'config', 'setup',
                'node_modules', '.git', 'dist', 'build'
            ])
        ]

        return component_files

    def _extract_component_data(self, component_file: Path, relative_path: Path) -> Optional[Dict]:
        """Extract data from a component file"""
        try:
            # Read the component code
            code = component_file.read_text(encoding='utf-8')

            # Extract component name from filename
            component_name = component_file.stem

            # Determine component type and variant
            file_ext = component_file.suffix
            is_typescript = file_ext in ['.tsx', '.ts']

            # Try to detect styling approach
            styling_approach = 'unknown'
            if 'tailwind' in code.lower() or 'className=' in code:
                styling_approach = 'tailwind'
            elif 'styled-components' in code or 'styled.' in code:
                styling_approach = 'styled-components'
            elif '.css' in code or 'import.*css' in code.lower():
                styling_approach = 'css'

            # Look for associated CSS files
            css_files = self._find_associated_files(component_file, ['.css', '.scss', '.sass'])

            # Build component data
            component_data = {
                'url': f"{self.repo_url}/tree/main/{relative_path}",
                'title': component_name,
                'description': f"React component from react-bits: {component_name}",
                'code': code,
                'file_path': str(relative_path),
                'file_type': file_ext,
                'is_typescript': is_typescript,
                'styling_approach': styling_approach,
                'component_type': self._detect_component_type(relative_path, code),
                'css_files': css_files
            }

            # Create HTML representation for analysis
            html_content = self._create_html_wrapper(component_data)
            component_data['html'] = html_content

            return component_data

        except Exception as e:
            print(f"    Error extracting component data: {e}")
            return None

    def _find_associated_files(self, component_file: Path, extensions: List[str]) -> List[str]:
        """Find associated files (like CSS) for a component"""
        associated_files = []
        component_dir = component_file.parent
        component_name = component_file.stem

        for ext in extensions:
            # Check for files with same name
            potential_file = component_dir / f"{component_name}{ext}"
            if potential_file.exists():
                try:
                    content = potential_file.read_text(encoding='utf-8')
                    associated_files.append({
                        'path': str(potential_file.relative_to(self.temp_clone_dir)),
                        'content': content,
                        'type': ext
                    })
                except Exception:
                    pass

        return associated_files

    def _detect_component_type(self, relative_path: Path, code: str) -> str:
        """Detect the type/category of component"""
        path_str = str(relative_path).lower()
        code_lower = code.lower()

        # Check path for category hints
        if 'animation' in path_str or 'text-animation' in path_str:
            return 'animation'
        elif 'background' in path_str:
            return 'background'
        elif 'button' in path_str or 'button' in code_lower:
            return 'button'
        elif 'card' in path_str or 'card' in code_lower:
            return 'card'
        elif 'nav' in path_str or 'navigation' in code_lower:
            return 'navigation'
        elif 'form' in path_str or 'input' in code_lower:
            return 'form'
        elif 'modal' in path_str or 'dialog' in code_lower:
            return 'modal'
        else:
            return 'component'

    def _create_html_wrapper(self, component_data: Dict) -> str:
        """Create an HTML wrapper for the component (for analysis purposes)"""
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{component_data['title']} - React Bits Component</title>
    <meta name="description" content="{component_data['description']}">
    <meta name="component-type" content="{component_data['component_type']}">
    <meta name="styling" content="{component_data['styling_approach']}">
    <meta name="typescript" content="{component_data['is_typescript']}">
</head>
<body>
    <!-- React Component: {component_data['title']} -->
    <!-- File: {component_data['file_path']} -->
    <!-- Type: {component_data['component_type']} -->
    <!-- Styling: {component_data['styling_approach']} -->

    <pre><code class="language-{'tsx' if component_data['is_typescript'] else 'jsx'}">
{component_data['code']}
    </code></pre>

    <!-- Associated CSS Files -->
"""

        # Add CSS content if available
        for css_file in component_data.get('css_files', []):
            html += f"""
    <style data-source="{css_file['path']}">
{css_file['content']}
    </style>
"""

        html += """
</body>
</html>
"""
        return html

    def _cleanup_temp_clone(self):
        """Clean up temporary clone directory"""
        try:
            if self.temp_clone_dir.exists():
                shutil.rmtree(self.temp_clone_dir)
                print(f"  🧹 Cleaned up temporary files")
        except Exception as e:
            print(f"  ⚠️  Could not clean up temp directory: {e}")

    def template_exists(self, template_id: str) -> bool:
        """Check if component already exists"""
        template_dir = self.output_dir / template_id
        metadata_path = template_dir / 'metadata.json'
        return metadata_path.exists()

    def save_template(self, template_data: Dict, template_id: str) -> Path:
        """Save component data to disk"""
        template_dir = self.output_dir / template_id
        template_dir.mkdir(parents=True, exist_ok=True)

        # Save HTML wrapper
        if 'html' in template_data:
            html_path = template_dir / 'index.html'
            html_path.write_text(template_data['html'], encoding='utf-8')

        # Save original component code
        if 'code' in template_data:
            ext = template_data.get('file_type', '.jsx')
            code_path = template_dir / f'component{ext}'
            code_path.write_text(template_data['code'], encoding='utf-8')

        # Save associated CSS files
        if 'css_files' in template_data:
            for i, css_file in enumerate(template_data['css_files']):
                css_path = template_dir / f'style_{i}{css_file["type"]}'
                css_path.write_text(css_file['content'], encoding='utf-8')

        # Save metadata
        metadata_path = template_dir / 'metadata.json'
        metadata = {
            'url': template_data.get('url'),
            'title': template_data.get('title'),
            'description': template_data.get('description'),
            'source': template_data.get('source'),
            'file_path': template_data.get('file_path'),
            'component_type': template_data.get('component_type'),
            'styling_approach': template_data.get('styling_approach'),
            'is_typescript': template_data.get('is_typescript'),
            'scraped_at': time.strftime('%Y-%m-%d %H:%M:%S')
        }
        metadata_path.write_text(json.dumps(metadata, indent=2), encoding='utf-8')

        return template_dir
