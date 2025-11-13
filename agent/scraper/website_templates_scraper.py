"""Website Templates scraper - learning-zone/website-templates"""

import subprocess
import shutil
import json
from typing import List, Dict
from pathlib import Path
from .base_scraper import BaseScraper


class WebsiteTemplatesScraper(BaseScraper):
    """Scraper for website-templates from learning-zone GitHub repository"""

    def __init__(self, output_dir: str = "data/templates/website-templates"):
        super().__init__(output_dir)
        self.base_url = "https://learning-zone.github.io/website-templates"
        self.github_repo = "https://github.com/learning-zone/website-templates.git"
        self.temp_clone_dir = Path("/tmp/website-templates-clone")

    def get_template_list_url(self) -> str:
        return self.base_url

    def scrape(self, limit: int = 10) -> List[Dict]:
        """Clone and extract templates from website-templates repository"""
        print(f"🎨 Scraping Website Templates (learning-zone)...")
        print(f"  Repository has 170+ HTML5 templates available")

        templates = []
        downloaded_count = 0

        try:
            # Clone the repository if not already cloned
            if not self.temp_clone_dir.exists():
                print(f"  📦 Cloning repository (one-time operation, may take a minute)...")
                result = subprocess.run(
                    ['git', 'clone', '--depth', '1', self.github_repo, str(self.temp_clone_dir)],
                    capture_output=True,
                    text=True,
                    timeout=180
                )

                if result.returncode != 0:
                    print(f"    ! Clone failed: {result.stderr}")
                    return []

                print(f"    ✓ Repository cloned successfully")
            else:
                print(f"  ✓ Using existing repository clone")

            # Get all template directories (exclude special directories)
            exclude_dirs = {'.git', 'assets', '.github', 'docs'}
            template_dirs = [
                d for d in self.temp_clone_dir.iterdir()
                if d.is_dir() and d.name not in exclude_dirs and not d.name.startswith('.')
            ]

            print(f"  Found {len(template_dirs)} templates in repository")

            # Process templates up to limit
            for template_dir in sorted(template_dirs):
                if downloaded_count >= limit:
                    break

                template_name = template_dir.name
                template_id = f"website-templates_{template_name}"

                # Check if already downloaded
                if self.template_exists(template_id):
                    print(f"  ⏭  {template_name}: Already downloaded, skipping...")
                    continue

                print(f"  📋 Processing: {template_name}")

                try:
                    # Copy template to output directory
                    dest_dir = self.output_dir / template_id
                    if dest_dir.exists():
                        shutil.rmtree(dest_dir)

                    shutil.copytree(template_dir, dest_dir)

                    # Create metadata
                    template_data = {
                        'title': template_name.replace('-', ' ').replace('_', ' ').title(),
                        'url': f"{self.base_url}/{template_name}",
                        'description': f"HTML5 template from website-templates collection: {template_name}",
                        'preview_image': '',
                        'source': 'website-templates',
                        'id': template_id,
                        'github_url': self.github_repo
                    }

                    # Save metadata
                    self.save_template(template_data, template_id)

                    templates.append(template_data)
                    downloaded_count += 1
                    print(f"    ✓ Downloaded to: {template_id}/")

                except Exception as e:
                    print(f"    ! Error: {e}")
                    continue

            print(f"✓ Scraped {len(templates)} templates from Website Templates")
            return templates

        except subprocess.TimeoutExpired:
            print(f"    ! Timeout cloning repository")
            return []
        except Exception as e:
            print(f"    ! Error: {e}")
            return []
