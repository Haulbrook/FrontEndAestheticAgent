"""
GitHub Repository Analyzer for Frontend Aesthetic Agent

This module analyzes top GitHub repositories (CSS frameworks, Vue, React, HTML)
to extract design patterns, components, and best practices for training the bot.
"""

import os
import json
import subprocess
from pathlib import Path
from typing import Dict, List, Optional, Set
from datetime import datetime
import re


class GitHubRepoAnalyzer:
    """Analyzes GitHub repositories to extract frontend patterns and learnings."""

    # Repository catalog from the lesson plan
    REPO_CATALOG = {
        "css": [
            {
                "name": "Bootstrap",
                "repo": "https://github.com/twbs/bootstrap.git",
                "stars": 174000,
                "forks": 79100,
                "focus": ["component_patterns", "grid_system", "utilities", "responsive_design"]
            },
            {
                "name": "Animate.css",
                "repo": "https://github.com/animate-css/animate.css.git",
                "stars": 82500,
                "forks": 16100,
                "focus": ["animations", "transitions", "css_classes"]
            },
            {
                "name": "Tailwind CSS",
                "repo": "https://github.com/tailwindlabs/tailwindcss.git",
                "stars": 91200,
                "forks": 4800,
                "focus": ["utility_first", "design_tokens", "color_schemes", "spacing"]
            },
            {
                "name": "Normalize.css",
                "repo": "https://github.com/necolas/normalize.css.git",
                "stars": 53700,
                "forks": 10500,
                "focus": ["browser_normalization", "reset_patterns"]
            },
            {
                "name": "Bulma",
                "repo": "https://github.com/jgthms/bulma.git",
                "stars": 50000,
                "forks": 3900,
                "focus": ["flexbox", "components", "modular_css"]
            }
        ],
        "vue": [
            {
                "name": "Vue",
                "repo": "https://github.com/vuejs/vue.git",
                "stars": 210000,
                "forks": 33800,
                "focus": ["component_architecture", "reactive_patterns", "directives"]
            },
            {
                "name": "Awesome-Vue",
                "repo": "https://github.com/vuejs/awesome-vue.git",
                "stars": 73400,
                "forks": 9500,
                "focus": ["curated_components", "libraries", "resources"]
            },
            {
                "name": "Nuxt",
                "repo": "https://github.com/nuxt/nuxt.git",
                "stars": 58900,
                "forks": 5400,
                "focus": ["ssr_patterns", "layouts", "routing"]
            },
            {
                "name": "Vuetify",
                "repo": "https://github.com/vuetifyjs/vuetify.git",
                "stars": 40800,
                "forks": 7100,
                "focus": ["material_design", "components", "theming"]
            },
            {
                "name": "Element Plus",
                "repo": "https://github.com/element-plus/element-plus.git",
                "stars": 26800,
                "forks": 19600,
                "focus": ["ui_components", "design_system", "accessibility"]
            }
        ],
        "react": [
            {
                "name": "React",
                "repo": "https://github.com/facebook/react.git",
                "stars": 241000,
                "forks": 49900,
                "focus": ["component_patterns", "hooks", "composition"]
            },
            {
                "name": "Next.js",
                "repo": "https://github.com/vercel/next.js.git",
                "stars": 136000,
                "forks": 29900,
                "focus": ["ssr", "routing", "layouts", "optimization"]
            },
            {
                "name": "Create React App",
                "repo": "https://github.com/facebook/create-react-app.git",
                "stars": 104000,
                "forks": 27200,
                "focus": ["project_structure", "build_config", "best_practices"]
            },
            {
                "name": "Material-UI",
                "repo": "https://github.com/mui/material-ui.git",
                "stars": 97300,
                "forks": 32800,
                "focus": ["material_design", "components", "theming", "styling"]
            },
            {
                "name": "Ant Design",
                "repo": "https://github.com/ant-design/ant-design.git",
                "stars": 96600,
                "forks": 54100,
                "focus": ["enterprise_ui", "components", "design_language"]
            }
        ],
        "html": [
            {
                "name": "Reveal.js",
                "repo": "https://github.com/hakimel/reveal.js.git",
                "stars": 69900,
                "forks": 16800,
                "focus": ["presentation_layouts", "transitions", "animations"]
            },
            {
                "name": "HTML5 Boilerplate",
                "repo": "https://github.com/h5bp/html5-boilerplate.git",
                "stars": 57300,
                "forks": 12300,
                "focus": ["best_practices", "structure", "optimization"]
            },
            {
                "name": "html2canvas",
                "repo": "https://github.com/niklasvh/html2canvas.git",
                "stars": 31700,
                "forks": 4900,
                "focus": ["dom_manipulation", "rendering"]
            },
            {
                "name": "Foundation Sites",
                "repo": "https://github.com/foundation/foundation-sites.git",
                "stars": 29800,
                "forks": 5400,
                "focus": ["responsive_framework", "grid", "components"]
            }
        ]
    }

    def __init__(self, workspace_dir: str = "data/github_training"):
        """Initialize the GitHub repository analyzer.

        Args:
            workspace_dir: Directory to clone repositories and store analysis
        """
        self.workspace_dir = Path(workspace_dir)
        self.repos_dir = self.workspace_dir / "repos"
        self.analysis_dir = self.workspace_dir / "analysis"
        self.learnings_dir = self.workspace_dir / "learnings"

        # Create directories
        for dir_path in [self.repos_dir, self.analysis_dir, self.learnings_dir]:
            dir_path.mkdir(parents=True, exist_ok=True)

    def clone_repository(self, repo_url: str, name: str, shallow: bool = True) -> Optional[Path]:
        """Clone a GitHub repository.

        Args:
            repo_url: GitHub repository URL
            name: Repository name for the local directory
            shallow: If True, perform a shallow clone (faster, less disk space)

        Returns:
            Path to the cloned repository, or None if clone failed
        """
        repo_path = self.repos_dir / name.lower().replace(" ", "_")

        # Skip if already cloned
        if repo_path.exists() and (repo_path / ".git").exists():
            print(f"✓ Repository '{name}' already cloned at {repo_path}")
            return repo_path

        try:
            print(f"Cloning {name} from {repo_url}...")
            cmd = ["git", "clone"]
            if shallow:
                cmd.extend(["--depth", "1"])
            cmd.extend([repo_url, str(repo_path)])

            subprocess.run(cmd, check=True, capture_output=True)
            print(f"✓ Successfully cloned {name}")
            return repo_path
        except subprocess.CalledProcessError as e:
            print(f"✗ Failed to clone {name}: {e}")
            return None

    def analyze_css_framework(self, repo_path: Path, name: str, focus_areas: List[str]) -> Dict:
        """Analyze a CSS framework repository.

        Args:
            repo_path: Path to the cloned repository
            name: Framework name
            focus_areas: List of focus areas to analyze

        Returns:
            Dictionary with analysis results
        """
        analysis = {
            "name": name,
            "category": "css",
            "analyzed_at": datetime.now().isoformat(),
            "focus_areas": focus_areas,
            "learnings": {}
        }

        # Find CSS files
        css_files = list(repo_path.rglob("*.css")) + list(repo_path.rglob("*.scss"))
        analysis["file_count"] = len(css_files)

        # Extract patterns based on focus areas
        if "component_patterns" in focus_areas:
            analysis["learnings"]["components"] = self._extract_css_components(css_files[:50])

        if "grid_system" in focus_areas:
            analysis["learnings"]["grid_patterns"] = self._extract_grid_patterns(css_files[:20])

        if "utilities" in focus_areas:
            analysis["learnings"]["utility_classes"] = self._extract_utility_classes(css_files[:30])

        if "animations" in focus_areas or "transitions" in focus_areas:
            analysis["learnings"]["animations"] = self._extract_animation_patterns(css_files[:50])

        if "color_schemes" in focus_areas or "design_tokens" in focus_areas:
            analysis["learnings"]["colors"] = self._extract_color_variables(css_files[:30])

        if "spacing" in focus_areas:
            analysis["learnings"]["spacing"] = self._extract_spacing_patterns(css_files[:20])

        return analysis

    def _extract_css_components(self, css_files: List[Path]) -> Dict:
        """Extract component class patterns from CSS files."""
        components = {
            "buttons": [],
            "cards": [],
            "navbars": [],
            "forms": [],
            "modals": [],
            "alerts": []
        }

        component_patterns = {
            "buttons": r'\.(btn|button)[-_]?[\w-]*\s*\{',
            "cards": r'\.(card)[-_]?[\w-]*\s*\{',
            "navbars": r'\.(nav|navbar|navigation)[-_]?[\w-]*\s*\{',
            "forms": r'\.(form|input|select|textarea)[-_]?[\w-]*\s*\{',
            "modals": r'\.(modal|dialog)[-_]?[\w-]*\s*\{',
            "alerts": r'\.(alert|notification|toast)[-_]?[\w-]*\s*\{',
        }

        for css_file in css_files:
            try:
                content = css_file.read_text(encoding='utf-8', errors='ignore')
                for comp_type, pattern in component_patterns.items():
                    matches = re.findall(pattern, content, re.IGNORECASE)
                    components[comp_type].extend([m.strip() for m in matches])
            except Exception as e:
                continue

        # Deduplicate and limit
        for key in components:
            components[key] = list(set(components[key]))[:20]

        return components

    def _extract_grid_patterns(self, css_files: List[Path]) -> Dict:
        """Extract grid and layout patterns."""
        patterns = {
            "grid_classes": [],
            "flexbox_classes": [],
            "breakpoints": []
        }

        for css_file in css_files[:10]:
            try:
                content = css_file.read_text(encoding='utf-8', errors='ignore')

                # Grid classes
                grid_matches = re.findall(r'\.(col|grid|row)[-_]?[\w-]*\s*\{', content, re.IGNORECASE)
                patterns["grid_classes"].extend([m.strip() for m in grid_matches])

                # Flexbox
                if 'display: flex' in content or 'display:flex' in content:
                    flex_matches = re.findall(r'\.(flex|d-flex)[-_]?[\w-]*\s*\{', content, re.IGNORECASE)
                    patterns["flexbox_classes"].extend([m.strip() for m in flex_matches])

                # Media queries / breakpoints
                breakpoint_matches = re.findall(r'@media.*?\(.*?(min|max)-width:\s*(\d+px)', content)
                patterns["breakpoints"].extend([f"{m[0]}-{m[1]}" for m in breakpoint_matches])
            except Exception:
                continue

        # Deduplicate
        for key in patterns:
            patterns[key] = list(set(patterns[key]))[:15]

        return patterns

    def _extract_utility_classes(self, css_files: List[Path]) -> Dict:
        """Extract utility class patterns (spacing, display, text, etc.)."""
        utilities = {
            "spacing": [],
            "display": [],
            "text": [],
            "colors": []
        }

        utility_patterns = {
            "spacing": r'\.(m|p|mt|mb|ml|mr|mx|my|pt|pb|pl|pr|px|py)[-_]?[\w-]*\s*\{',
            "display": r'\.(d|display)[-_]?(block|inline|flex|grid|none)[-_]?[\w-]*\s*\{',
            "text": r'\.(text)[-_]?(center|left|right|bold|italic|uppercase)[-_]?[\w-]*\s*\{',
            "colors": r'\.(bg|text|border)[-_]?color[-_]?[\w-]*\s*\{'
        }

        for css_file in css_files:
            try:
                content = css_file.read_text(encoding='utf-8', errors='ignore')
                for util_type, pattern in utility_patterns.items():
                    matches = re.findall(pattern, content, re.IGNORECASE)
                    utilities[util_type].extend([m.strip() for m in matches])
            except Exception:
                continue

        # Deduplicate
        for key in utilities:
            utilities[key] = list(set(utilities[key]))[:20]

        return utilities

    def _extract_animation_patterns(self, css_files: List[Path]) -> Dict:
        """Extract animation and transition patterns."""
        animations = {
            "keyframes": [],
            "animation_classes": [],
            "transitions": []
        }

        for css_file in css_files:
            try:
                content = css_file.read_text(encoding='utf-8', errors='ignore')

                # @keyframes
                keyframe_matches = re.findall(r'@keyframes\s+([\w-]+)', content)
                animations["keyframes"].extend(keyframe_matches)

                # Animation classes
                anim_class_matches = re.findall(r'\.(animate|animation|anim)[-_]?[\w-]*\s*\{', content, re.IGNORECASE)
                animations["animation_classes"].extend([m.strip() for m in anim_class_matches])

                # Transition patterns
                if 'transition:' in content or 'transition-' in content:
                    trans_matches = re.findall(r'\.(transition|trans)[-_]?[\w-]*\s*\{', content, re.IGNORECASE)
                    animations["transitions"].extend([m.strip() for m in trans_matches])
            except Exception:
                continue

        # Deduplicate
        for key in animations:
            animations[key] = list(set(animations[key]))[:25]

        return animations

    def _extract_color_variables(self, css_files: List[Path]) -> Dict:
        """Extract color variables and palettes."""
        colors = {
            "css_variables": [],
            "scss_variables": [],
            "hex_colors": []
        }

        for css_file in css_files:
            try:
                content = css_file.read_text(encoding='utf-8', errors='ignore')

                # CSS custom properties
                css_var_matches = re.findall(r'--[\w-]+:\s*(#[0-9a-fA-F]{3,6}|rgb|hsl)', content)
                colors["css_variables"].extend([m.strip() for m in css_var_matches])

                # SCSS variables
                if css_file.suffix == '.scss':
                    scss_var_matches = re.findall(r'\$[\w-]+:\s*(#[0-9a-fA-F]{3,6})', content)
                    colors["scss_variables"].extend([m.strip() for m in scss_var_matches])

                # Hex colors
                hex_matches = re.findall(r'#[0-9a-fA-F]{6}', content)
                colors["hex_colors"].extend(hex_matches)
            except Exception:
                continue

        # Deduplicate and limit
        for key in colors:
            colors[key] = list(set(colors[key]))[:30]

        return colors

    def _extract_spacing_patterns(self, css_files: List[Path]) -> Dict:
        """Extract spacing scale patterns."""
        spacing = {
            "margin_values": [],
            "padding_values": [],
            "gap_values": []
        }

        for css_file in css_files[:10]:
            try:
                content = css_file.read_text(encoding='utf-8', errors='ignore')

                # Extract unique spacing values
                margin_matches = re.findall(r'margin(?:-\w+)?:\s*([\d.]+(?:px|rem|em))', content)
                spacing["margin_values"].extend(margin_matches)

                padding_matches = re.findall(r'padding(?:-\w+)?:\s*([\d.]+(?:px|rem|em))', content)
                spacing["padding_values"].extend(padding_matches)

                gap_matches = re.findall(r'gap:\s*([\d.]+(?:px|rem|em))', content)
                spacing["gap_values"].extend(gap_matches)
            except Exception:
                continue

        # Deduplicate and limit
        for key in spacing:
            spacing[key] = list(set(spacing[key]))[:20]

        return spacing

    def analyze_repository(self, category: str, repo_info: Dict) -> Dict:
        """Analyze a single repository.

        Args:
            category: Repository category (css, vue, react, html)
            repo_info: Repository information dictionary

        Returns:
            Analysis results dictionary
        """
        name = repo_info["name"]
        repo_url = repo_info["repo"]
        focus_areas = repo_info["focus"]

        print(f"\n{'='*60}")
        print(f"Analyzing {name} ({category.upper()})")
        print(f"Focus: {', '.join(focus_areas)}")
        print(f"{'='*60}")

        # Clone repository
        repo_path = self.clone_repository(repo_url, name, shallow=True)
        if not repo_path:
            return {"error": f"Failed to clone {name}"}

        # Analyze based on category
        if category == "css":
            analysis = self.analyze_css_framework(repo_path, name, focus_areas)
        elif category in ["vue", "react"]:
            analysis = self.analyze_component_library(repo_path, name, category, focus_areas)
        elif category == "html":
            analysis = self.analyze_html_framework(repo_path, name, focus_areas)
        else:
            analysis = {"error": f"Unknown category: {category}"}

        # Save analysis
        analysis_file = self.analysis_dir / f"{name.lower().replace(' ', '_')}.json"
        with open(analysis_file, 'w', encoding='utf-8') as f:
            json.dump(analysis, f, indent=2, ensure_ascii=False)

        print(f"✓ Analysis saved to {analysis_file}")
        return analysis

    def analyze_component_library(self, repo_path: Path, name: str,
                                   framework: str, focus_areas: List[str]) -> Dict:
        """Analyze Vue/React component libraries.

        Args:
            repo_path: Path to repository
            name: Library name
            framework: 'vue' or 'react'
            focus_areas: Areas to focus on

        Returns:
            Analysis dictionary
        """
        analysis = {
            "name": name,
            "category": framework,
            "analyzed_at": datetime.now().isoformat(),
            "focus_areas": focus_areas,
            "learnings": {}
        }

        # Find component files
        if framework == "vue":
            component_files = list(repo_path.rglob("*.vue"))
        else:  # react
            component_files = list(repo_path.rglob("*.jsx")) + list(repo_path.rglob("*.tsx"))

        analysis["component_count"] = len(component_files)

        # Extract component patterns
        if "components" in focus_areas or "ui_components" in focus_areas:
            analysis["learnings"]["component_types"] = self._extract_component_types(
                component_files[:100], framework
            )

        # Extract styling approaches
        css_files = list(repo_path.rglob("*.css")) + list(repo_path.rglob("*.scss"))
        if css_files:
            analysis["learnings"]["styling_patterns"] = self._extract_styling_approaches(
                css_files[:30]
            )

        return analysis

    def _extract_component_types(self, component_files: List[Path], framework: str) -> Dict:
        """Extract component type patterns from Vue/React files."""
        components = {
            "buttons": [],
            "inputs": [],
            "cards": [],
            "modals": [],
            "navbars": [],
            "tables": []
        }

        component_keywords = {
            "buttons": r'(button|btn)',
            "inputs": r'(input|field|text)',
            "cards": r'(card)',
            "modals": r'(modal|dialog)',
            "navbars": r'(nav|navbar|menu)',
            "tables": r'(table|grid|datagrid)'
        }

        for comp_file in component_files:
            filename = comp_file.name.lower()
            for comp_type, pattern in component_keywords.items():
                if re.search(pattern, filename, re.IGNORECASE):
                    components[comp_type].append(comp_file.stem)

        # Limit entries
        for key in components:
            components[key] = components[key][:15]

        return components

    def _extract_styling_approaches(self, css_files: List[Path]) -> Dict:
        """Extract styling methodologies from component libraries."""
        approaches = {
            "css_modules": 0,
            "styled_components": 0,
            "scoped_styles": 0,
            "utility_classes": 0
        }

        for css_file in css_files:
            filename = css_file.name.lower()
            if '.module.' in filename:
                approaches["css_modules"] += 1
            if 'scoped' in filename or css_file.suffix == '.vue':
                approaches["scoped_styles"] += 1

        return approaches

    def analyze_html_framework(self, repo_path: Path, name: str, focus_areas: List[str]) -> Dict:
        """Analyze HTML frameworks and tools.

        Args:
            repo_path: Path to repository
            name: Framework name
            focus_areas: Areas to focus on

        Returns:
            Analysis dictionary
        """
        analysis = {
            "name": name,
            "category": "html",
            "analyzed_at": datetime.now().isoformat(),
            "focus_areas": focus_areas,
            "learnings": {}
        }

        # Find HTML files
        html_files = list(repo_path.rglob("*.html"))
        analysis["file_count"] = len(html_files)

        # Extract structure patterns
        if "structure" in focus_areas or "best_practices" in focus_areas:
            analysis["learnings"]["html_patterns"] = self._extract_html_patterns(html_files[:20])

        # Extract layout patterns
        if "presentation_layouts" in focus_areas or "responsive_framework" in focus_areas:
            analysis["learnings"]["layout_patterns"] = self._extract_layout_patterns(html_files[:15])

        return analysis

    def _extract_html_patterns(self, html_files: List[Path]) -> Dict:
        """Extract HTML structure patterns."""
        patterns = {
            "semantic_tags": [],
            "meta_tags": [],
            "structural_patterns": []
        }

        semantic_tags = ['header', 'nav', 'main', 'article', 'section', 'aside', 'footer']

        for html_file in html_files:
            try:
                content = html_file.read_text(encoding='utf-8', errors='ignore')

                # Check for semantic tags
                for tag in semantic_tags:
                    if f'<{tag}' in content:
                        patterns["semantic_tags"].append(tag)

                # Extract meta tags
                meta_matches = re.findall(r'<meta\s+([^>]+)>', content)
                patterns["meta_tags"].extend(meta_matches[:10])
            except Exception:
                continue

        patterns["semantic_tags"] = list(set(patterns["semantic_tags"]))
        return patterns

    def _extract_layout_patterns(self, html_files: List[Path]) -> List[str]:
        """Extract common layout patterns."""
        patterns = []

        layout_indicators = [
            "grid-template",
            "flex-direction",
            "display: grid",
            "display: flex",
            "container",
            "wrapper"
        ]

        for html_file in html_files:
            try:
                content = html_file.read_text(encoding='utf-8', errors='ignore')
                for indicator in layout_indicators:
                    if indicator in content:
                        patterns.append(indicator)
            except Exception:
                continue

        return list(set(patterns))

    def analyze_all_repositories(self, categories: List[str] = None) -> Dict:
        """Analyze all repositories in specified categories.

        Args:
            categories: List of categories to analyze. If None, analyze all.

        Returns:
            Summary of all analyses
        """
        if categories is None:
            categories = ["css", "vue", "react", "html"]

        summary = {
            "analyzed_at": datetime.now().isoformat(),
            "categories": {},
            "total_repos": 0
        }

        for category in categories:
            if category not in self.REPO_CATALOG:
                continue

            summary["categories"][category] = []
            repos = self.REPO_CATALOG[category]

            for repo_info in repos:
                analysis = self.analyze_repository(category, repo_info)
                summary["categories"][category].append({
                    "name": repo_info["name"],
                    "status": "completed" if "error" not in analysis else "failed"
                })
                summary["total_repos"] += 1

        # Save summary
        summary_file = self.analysis_dir / "analysis_summary.json"
        with open(summary_file, 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2, ensure_ascii=False)

        print(f"\n{'='*60}")
        print(f"Analysis Complete!")
        print(f"Total repositories analyzed: {summary['total_repos']}")
        print(f"Summary saved to: {summary_file}")
        print(f"{'='*60}\n")

        return summary

    def generate_training_report(self) -> str:
        """Generate a comprehensive training report from all analyses.

        Returns:
            Markdown report as string
        """
        report_lines = [
            "# GitHub Repository Training Report",
            f"\nGenerated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            "\n## Overview",
            "\nThis report summarizes learnings extracted from top GitHub repositories",
            "across CSS frameworks, Vue, React, and HTML categories.",
            "\n---\n"
        ]

        # Load all analysis files
        analysis_files = list(self.analysis_dir.glob("*.json"))
        analysis_files = [f for f in analysis_files if f.name != "analysis_summary.json"]

        for category in ["css", "vue", "react", "html"]:
            category_analyses = []
            for analysis_file in analysis_files:
                try:
                    with open(analysis_file, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        if data.get("category") == category:
                            category_analyses.append(data)
                except Exception:
                    continue

            if not category_analyses:
                continue

            report_lines.append(f"## {category.upper()} Category\n")

            for analysis in category_analyses:
                report_lines.append(f"### {analysis['name']}\n")
                report_lines.append(f"**Focus Areas:** {', '.join(analysis['focus_areas'])}\n")

                if "learnings" in analysis:
                    report_lines.append("\n**Key Learnings:**\n")
                    for learning_type, data in analysis["learnings"].items():
                        if isinstance(data, dict):
                            report_lines.append(f"- **{learning_type.replace('_', ' ').title()}:**")
                            for key, values in data.items():
                                if values:
                                    report_lines.append(f"  - {key}: {len(values)} patterns")
                        elif isinstance(data, list):
                            report_lines.append(f"- **{learning_type.replace('_', ' ').title()}:** {len(data)} items")
                    report_lines.append("")

                report_lines.append("---\n")

        report = "\n".join(report_lines)

        # Save report
        report_file = self.learnings_dir / "training_report.md"
        report_file.write_text(report, encoding='utf-8')

        print(f"✓ Training report generated: {report_file}")
        return report
