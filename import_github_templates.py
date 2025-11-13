#!/usr/bin/env python
"""Import HTML5UP templates from GitHub mirror"""

import os
import json
import shutil
from pathlib import Path

# Paths
github_mirror = Path("/tmp/html5up_mirror")
output_dir = Path("data/templates/html5up")

# Create output directory
output_dir.mkdir(parents=True, exist_ok=True)

# Get all template directories (exclude README.md)
template_dirs = [d for d in github_mirror.iterdir() if d.is_dir() and d.name != '.git']

imported_count = 0
skipped_count = 0

print(f"🎨 Importing HTML5UP templates from GitHub mirror...")
print(f"   Found {len(template_dirs)} templates to import\n")

for template_dir in sorted(template_dirs):
    template_name = template_dir.name

    # Generate template ID (simple version - just use the name)
    template_id = f"html5up_{template_name}"

    dest_dir = output_dir / template_id
    metadata_file = dest_dir / "metadata.json"

    # Check if already exists
    if metadata_file.exists():
        print(f"⏭  {template_name}: Already exists, skipping...")
        skipped_count += 1
        continue

    # Copy template directory
    try:
        if dest_dir.exists():
            shutil.rmtree(dest_dir)

        shutil.copytree(template_dir, dest_dir)

        # Create metadata
        metadata = {
            "title": template_name.replace('-', ' ').title(),
            "url": f"https://html5up.net/{template_name}",
            "description": f"HTML5UP {template_name} template",
            "preview_image": "",
            "source": "html5up",
            "id": template_id,
            "imported_from": "github_mirror"
        }

        with open(metadata_file, 'w') as f:
            json.dump(metadata, f, indent=2)

        print(f"✓  {template_name}: Imported successfully")
        imported_count += 1

    except Exception as e:
        print(f"✗  {template_name}: Error - {e}")

print(f"\n{'='*60}")
print(f"✓ Import complete!")
print(f"  Imported: {imported_count} templates")
print(f"  Skipped:  {skipped_count} templates")
print(f"  Total:    {imported_count + skipped_count} templates")
print(f"{'='*60}")
