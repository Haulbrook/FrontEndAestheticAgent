"""Start Bootstrap template scraper"""

import subprocess
import shutil
import json
from typing import List, Dict
from pathlib import Path
from .base_scraper import BaseScraper


class StartBootstrapScraper(BaseScraper):
    """Scraper for Start Bootstrap free templates from GitHub"""

    def __init__(self, output_dir: str = "data/templates/startbootstrap"):
        super().__init__(output_dir)
        self.base_url = "https://startbootstrap.com"
        self.github_org = "StartBootstrap"

        # List of all Start Bootstrap template repositories
        self.templates = [
            'startbootstrap-creative',
            'startbootstrap-agency',
            'startbootstrap-landing-page',
            'startbootstrap-sb-admin-2',
            'startbootstrap-bare',
            'startbootstrap-personal',
            'startbootstrap-stylish-portfolio',
            'startbootstrap-coming-soon',
            'startbootstrap-freelancer',
            'startbootstrap-clean-blog',
            'startbootstrap-modern-business',
            'startbootstrap-shop-homepage',
            'startbootstrap-heroic-features',
            'startbootstrap-simple-sidebar',
            'startbootstrap-the-big-picture',
            'startbootstrap-shop-item',
            'startbootstrap-scrolling-nav',
            'startbootstrap-one-page-wonder',
            'startbootstrap-full-width-pics',
            'startbootstrap-new-age',
            'startbootstrap-small-business',
            'startbootstrap-business-casual',
            'startbootstrap-blog-post',
            'startbootstrap-blog-home',
            'startbootstrap-sb-admin',
            'startbootstrap-grayscale',
            'startbootstrap-resume',
            'startbootstrap-business-frontpage',
            'startbootstrap-4-col-portfolio',
            'startbootstrap-3-col-portfolio',
            'startbootstrap-2-col-portfolio',
            'startbootstrap-1-col-portfolio',
            'startbootstrap-thumbnail-gallery',
            'startbootstrap-portfolio-item'
        ]

    def get_template_list_url(self) -> str:
        return f"https://github.com/{self.github_org}"

    def scrape(self, limit: int = 10) -> List[Dict]:
        """Clone Start Bootstrap templates from GitHub"""
        print(f"🎨 Scraping Start Bootstrap templates (limit: {limit})...")
        print(f"  Total available templates: {len(self.templates)}")

        templates = []
        downloaded_count = 0

        for template_name in self.templates:
            # Stop if we've downloaded enough
            if downloaded_count >= limit:
                break

            try:
                template_id = f"startbootstrap_{template_name.replace('startbootstrap-', '')}"

                # Check if already downloaded
                if self.template_exists(template_id):
                    print(f"  ⏭  {template_name}: Already downloaded, skipping...")
                    continue

                print(f"  🔍 Cloning: {template_name}")

                # Clone from GitHub
                github_url = f"https://github.com/{self.github_org}/{template_name}.git"
                temp_dir = Path(f"/tmp/{template_name}")

                # Remove temp dir if exists
                if temp_dir.exists():
                    shutil.rmtree(temp_dir)

                # Clone repository (shallow clone for speed)
                result = subprocess.run(
                    ['git', 'clone', '--depth', '1', github_url, str(temp_dir)],
                    capture_output=True,
                    text=True,
                    timeout=60
                )

                if result.returncode != 0:
                    print(f"    ! Clone failed: {result.stderr}")
                    continue

                # Copy to output directory
                dest_dir = self.output_dir / template_id
                if dest_dir.exists():
                    shutil.rmtree(dest_dir)

                shutil.copytree(temp_dir, dest_dir)

                # Remove .git directory to save space
                git_dir = dest_dir / '.git'
                if git_dir.exists():
                    shutil.rmtree(git_dir)

                # Create metadata
                template_data = {
                    'title': template_name.replace('startbootstrap-', '').replace('-', ' ').title(),
                    'url': f"https://startbootstrap.com/theme/{template_name.replace('startbootstrap-', '')}",
                    'description': f"Start Bootstrap {template_name} template",
                    'preview_image': '',
                    'source': 'startbootstrap',
                    'id': template_id,
                    'github_url': github_url
                }

                # Save metadata
                self.save_template(template_data, template_id)

                # Clean up temp directory
                shutil.rmtree(temp_dir)

                templates.append(template_data)
                downloaded_count += 1
                print(f"    ✓ Downloaded to: {template_id}/")

            except subprocess.TimeoutExpired:
                print(f"    ! Timeout cloning {template_name}")
                continue
            except Exception as e:
                print(f"    ! Error: {e}")
                continue

        print(f"✓ Scraped {len(templates)} templates from Start Bootstrap")
        return templates
