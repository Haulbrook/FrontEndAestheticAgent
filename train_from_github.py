#!/usr/bin/env python3
"""
GitHub Repository Training Script for FrontEndAestheticAgent

This script systematically analyzes top GitHub repositories to extract
design patterns and train the aesthetic bot.
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from agent.learner.github_repo_analyzer import GitHubRepoAnalyzer


def print_header(text: str):
    """Print a formatted header."""
    print("\n" + "=" * 70)
    print(f"  {text}")
    print("=" * 70 + "\n")


def main():
    """Main training function."""
    print_header("🚀 FrontEndAestheticAgent - GitHub Repository Training")

    analyzer = GitHubRepoAnalyzer(workspace_dir="data/github_training")

    print("This training program will analyze 20 top GitHub repositories:")
    print("  • 5 CSS frameworks (Bootstrap, Tailwind, Animate.css, etc.)")
    print("  • 5 Vue.js projects (Vue core, Nuxt, Vuetify, etc.)")
    print("  • 5 React libraries (React, Next.js, Material-UI, etc.)")
    print("  • 5 HTML frameworks (Reveal.js, HTML5 Boilerplate, etc.)\n")

    response = input("Ready to start? This will clone repositories and analyze them. (y/n): ")
    if response.lower() != 'y':
        print("Training cancelled.")
        return

    # Analyze all repositories
    print_header("Starting Repository Analysis")

    summary = analyzer.analyze_all_repositories(categories=["css", "vue", "react", "html"])

    # Generate training report
    print_header("Generating Training Report")
    analyzer.generate_training_report()

    # Print summary
    print_header("Training Complete! 🎉")
    print(f"✓ Total repositories analyzed: {summary['total_repos']}")
    print(f"✓ Analysis files saved in: data/github_training/analysis/")
    print(f"✓ Training report: data/github_training/learnings/training_report.md")
    print("\nNext steps:")
    print("  1. Review the training report")
    print("  2. Integrate learnings into your bot's knowledge base")
    print("  3. Test enhanced capabilities with: python cli.py generate\n")


if __name__ == "__main__":
    main()
