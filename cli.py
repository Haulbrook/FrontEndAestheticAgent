#!/usr/bin/env python3
"""Command-line interface for the Front-End Aesthetic Agent"""

import click
import json
from pathlib import Path
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import print as rprint

from agent.scraper.scraper_manager import ScraperManager
from agent.analyzer.template_analyzer import TemplateAnalyzer
from agent.learner.pattern_learner import PatternLearner
from agent.generator.design_generator import DesignGenerator
from agent.generator.suggestion_engine import SuggestionEngine
from agent.scheduler import AutoScraper

console = Console()


@click.group()
@click.version_option(version='0.1.0')
def cli():
    """Front-End Aesthetic Agent - Learn from templates to create better designs"""
    pass


@cli.command()
@click.option('--source', type=click.Choice(['html5up', 'freecss', 'templatemo', 'colorlib', 'startbootstrap', 'all']), default='all',
              help='Template source to scrape from')
@click.option('--limit', default=10, help='Number of templates to scrape per source')
@click.option('--output', default='data/templates', help='Output directory for scraped templates')
def scrape(source, limit, output):
    """Scrape free website templates"""
    console.print("\n[bold cyan]🎨 Front-End Aesthetic Agent - Template Scraper[/bold cyan]\n")

    manager = ScraperManager(output)

    try:
        if source == 'all':
            results = manager.scrape_all(limit_per_source=limit)

            # Display results
            table = Table(title="Scraping Results")
            table.add_column("Source", style="cyan")
            table.add_column("Templates", style="green")

            total = 0
            for src, templates in results.items():
                count = len(templates)
                total += count
                table.add_row(src.upper(), str(count))

            console.print(table)
            console.print(f"\n[bold green]✓ Total templates scraped: {total}[/bold green]\n")

        else:
            templates = manager.scrape_source(source, limit)
            console.print(f"\n[bold green]✓ Scraped {len(templates)} templates from {source}[/bold green]\n")

    except Exception as e:
        console.print(f"[bold red]✗ Error: {e}[/bold red]")
        raise click.Abort()


@cli.command()
@click.option('--input', default='data/templates', help='Directory containing templates to analyze')
@click.option('--output', default='data/analyzed', help='Output directory for analysis results')
def analyze(input, output):
    """Analyze scraped templates"""
    console.print("\n[bold cyan]🔍 Front-End Aesthetic Agent - Template Analyzer[/bold cyan]\n")

    analyzer = TemplateAnalyzer()

    try:
        # Find all template directories
        input_path = Path(input)

        if not input_path.exists():
            console.print(f"[bold red]✗ Directory not found: {input}[/bold red]")
            raise click.Abort()

        # Analyze templates from all sources
        all_results = {}

        for source_dir in input_path.iterdir():
            if source_dir.is_dir():
                console.print(f"\n[bold]Analyzing templates from: {source_dir.name}[/bold]\n")
                results = analyzer.analyze_directory(str(source_dir), f"{output}/{source_dir.name}")
                all_results.update(results)

        # Display summary
        if all_results:
            table = Table(title="Analysis Summary")
            table.add_column("Metric", style="cyan")
            table.add_column("Value", style="green")

            avg_quality = sum(t['quality_score'] for t in all_results.values()) / len(all_results)

            table.add_row("Templates Analyzed", str(len(all_results)))
            table.add_row("Average Quality Score", f"{avg_quality:.1f}/100")

            console.print(table)
            console.print(f"\n[bold green]✓ Analysis complete! Results saved to: {output}/[/bold green]\n")
        else:
            console.print("[yellow]! No templates found to analyze[/yellow]")

    except Exception as e:
        console.print(f"[bold red]✗ Error: {e}[/bold red]")
        raise click.Abort()


@cli.command()
@click.option('--data', default='data/analyzed', help='Directory containing analyzed templates')
@click.option('--output', default='data/knowledge_base/design_patterns.json',
              help='Output file for knowledge base')
def train(data, output):
    """Train the agent on analyzed templates"""
    console.print("\n[bold cyan]🧠 Front-End Aesthetic Agent - Pattern Learner[/bold cyan]\n")

    learner = PatternLearner(output)

    try:
        # Find all analyzed template directories
        data_path = Path(data)

        if not data_path.exists():
            console.print(f"[bold red]✗ Directory not found: {data}[/bold red]")
            raise click.Abort()

        # Learn from all sources
        total_learned = 0

        for source_dir in data_path.iterdir():
            if source_dir.is_dir():
                console.print(f"\n[bold]Learning from: {source_dir.name}[/bold]")
                result = learner.learn_from_directory(str(source_dir))

                if result.get('success'):
                    total_learned += result.get('learned', 0)

        # Display statistics
        stats = learner.kb.get_statistics()

        table = Table(title="Knowledge Base Statistics")
        table.add_column("Metric", style="cyan")
        table.add_column("Value", style="green")

        table.add_row("Total Templates Learned", str(stats['total_templates']))
        table.add_row("Average Quality Score", f"{stats['avg_quality']:.1f}/100")
        table.add_row("High Quality Templates", str(stats['high_quality_count']))
        table.add_row("Most Popular Color Scheme", stats['most_popular_color_scheme'])
        table.add_row("Most Popular Layout System", stats['most_popular_layout'])

        console.print(table)
        console.print(f"\n[bold green]✓ Training complete! Knowledge base saved to: {output}[/bold green]\n")

    except Exception as e:
        console.print(f"[bold red]✗ Error: {e}[/bold red]")
        raise click.Abort()


@cli.command()
@click.option('--scheme', type=click.Choice([
    'vibrant', 'minimal_dark', 'minimal_light', 'dark_mode', 'light_airy', 'balanced'
]), help='Specific color scheme (optional)')
@click.option('--output', default='design_guide.json', help='Output file for design guide')
def generate(scheme, output):
    """Generate design guide based on learned patterns"""
    console.print("\n[bold cyan]✨ Front-End Aesthetic Agent - Design Generator[/bold cyan]\n")

    generator = DesignGenerator()

    try:
        # Generate complete design guide
        guide = generator.generate_complete_design_guide()

        # Override color scheme if specified
        if scheme:
            guide['colors'] = generator.generate_color_palette(scheme)

        # Display color palette
        console.print(Panel.fit(
            f"[bold]Color Scheme:[/bold] {guide['colors']['scheme']}\n"
            f"[bold]Primary:[/bold] {guide['colors']['primary']}\n"
            f"[bold]Secondary:[/bold] {guide['colors']['secondary']}\n"
            f"[bold]Accent:[/bold] {guide['colors']['accent']}",
            title="Generated Color Palette",
            border_style="cyan"
        ))

        # Display typography
        typo = guide['typography']['recommended_fonts']
        console.print(Panel.fit(
            f"[bold]Heading Font:[/bold] {typo.get('heading', 'Inter')}\n"
            f"[bold]Body Font:[/bold] {typo.get('body', 'Inter')}\n"
            f"[bold]Style:[/bold] {typo.get('type', 'modern')}",
            title="Typography",
            border_style="green"
        ))

        # Save to file
        output_path = Path(output)
        output_path.write_text(json.dumps(guide, indent=2), encoding='utf-8')

        console.print(f"\n[bold green]✓ Design guide generated and saved to: {output}[/bold green]\n")

    except Exception as e:
        console.print(f"[bold red]✗ Error: {e}[/bold red]")
        raise click.Abort()


@cli.command()
@click.argument('html_file', type=click.Path(exists=True))
def suggest(html_file):
    """Analyze an HTML file and suggest improvements"""
    console.print("\n[bold cyan]💡 Front-End Aesthetic Agent - Suggestion Engine[/bold cyan]\n")

    engine = SuggestionEngine()

    try:
        result = engine.analyze_and_suggest(html_file)

        if 'error' in result:
            console.print(f"[bold red]✗ {result['error']}[/bold red]")
            raise click.Abort()

        analysis = result['analysis']
        suggestions = result['suggestions']
        quality_score = result['quality_score']

        # Display quality score
        score_color = "green" if quality_score >= 70 else "yellow" if quality_score >= 50 else "red"
        console.print(Panel.fit(
            f"[bold {score_color}]{quality_score}/100[/bold {score_color}]",
            title="Quality Score",
            border_style=score_color
        ))

        # Display priority improvements
        priority = suggestions['priority_improvements']

        if priority:
            console.print("\n[bold yellow]⚠ Priority Improvements:[/bold yellow]\n")

            for i, suggestion in enumerate(priority[:5], 1):
                console.print(f"{i}. [bold]{suggestion['issue']}[/bold]")
                console.print(f"   → {suggestion['suggestion']}\n")

        # Display category summaries
        for category in ['colors', 'layout', 'typography', 'style']:
            cat_suggestions = suggestions.get(category, [])

            if cat_suggestions:
                console.print(f"\n[bold cyan]{category.upper()} Suggestions:[/bold cyan]")

                for suggestion in cat_suggestions[:3]:
                    icon = "🔴" if suggestion['type'] == 'critical' else "⚠️" if suggestion['type'] == 'warning' else "ℹ️"
                    console.print(f"  {icon} {suggestion['issue']}")
                    console.print(f"     → {suggestion['suggestion']}\n")

        console.print("[bold green]✓ Analysis complete![/bold green]\n")

    except Exception as e:
        console.print(f"[bold red]✗ Error: {e}[/bold red]")
        raise click.Abort()


@cli.command()
@click.option('--config', default='config/auto_scraper_config.yaml', help='Config file for auto-scraper')
@click.option('--interval', help='Schedule interval (hourly/daily/weekly or minutes)')
@click.option('--mode', type=click.Choice(['scheduled', 'continuous', 'once']), default='once',
              help='Running mode')
@click.option('--delay', default=60, help='Delay in minutes for continuous mode')
def auto(config, interval, mode, delay):
    """Automatically scrape, analyze, and train on a schedule"""
    console.print("\n[bold cyan]🤖 Front-End Aesthetic Agent - Auto-Scraper[/bold cyan]\n")

    try:
        # Load config
        import yaml
        config_data = {}

        if Path(config).exists():
            with open(config, 'r') as f:
                config_data = yaml.safe_load(f) or {}
            console.print(f"[green]✓ Loaded config from: {config}[/green]\n")
        else:
            console.print(f"[yellow]! Config not found, using defaults[/yellow]\n")

        # Override with CLI options
        if interval:
            config_data['schedule_interval'] = interval

        # Create auto-scraper
        auto_scraper = AutoScraper(config_data)

        # Run based on mode
        if mode == 'once':
            console.print("[bold]Running single cycle...[/bold]\n")
            results = auto_scraper.run_scraping_cycle()

            # Display summary
            table = Table(title="Cycle Results")
            table.add_column("Metric", style="cyan")
            table.add_column("Count", style="green")

            table.add_row("Scraped", str(results['scraped']))
            table.add_row("Analyzed", str(results['analyzed']))
            table.add_row("Learned", str(results['learned']))
            table.add_row("Errors", str(len(results['errors'])))

            console.print(table)

        elif mode == 'scheduled':
            auto_scraper.start_scheduled()

        elif mode == 'continuous':
            auto_scraper.run_continuous(delay_minutes=delay)

    except Exception as e:
        console.print(f"[bold red]✗ Error: {e}[/bold red]")
        raise click.Abort()


@cli.command()
@click.option('--limit', default=10, help='Number of recent logs to show')
def logs(limit):
    """Show auto-scraper logs"""
    console.print("\n[bold cyan]📋 Auto-Scraper Logs[/bold cyan]\n")

    try:
        auto_scraper = AutoScraper()
        logs = auto_scraper.get_logs(limit)

        if not logs:
            console.print("[yellow]No logs found. Run 'auto' command first.[/yellow]")
            return

        for i, log in enumerate(reversed(logs), 1):
            timestamp = log.get('timestamp', 'Unknown')
            scraped = log.get('scraped', 0)
            analyzed = log.get('analyzed', 0)
            learned = log.get('learned', 0)
            errors = len(log.get('errors', []))

            status = "✓" if errors == 0 else "⚠"
            color = "green" if errors == 0 else "yellow"

            console.print(f"{i}. [{color}]{status}[/{color}] {timestamp}")
            console.print(f"   Scraped: {scraped} | Analyzed: {analyzed} | Learned: {learned} | Errors: {errors}")

            if errors > 0:
                for error in log['errors'][:2]:
                    console.print(f"   [red]• {error}[/red]")
            console.print()

    except Exception as e:
        console.print(f"[bold red]✗ Error: {e}[/bold red]")


@cli.command()
def stats():
    """Show knowledge base statistics"""
    console.print("\n[bold cyan]📊 Front-End Aesthetic Agent - Statistics[/bold cyan]\n")

    try:
        learner = PatternLearner()
        stats = learner.kb.get_statistics()
        recommendations = learner.get_recommendations()

        # Main stats table
        table = Table(title="Knowledge Base Statistics")
        table.add_column("Metric", style="cyan")
        table.add_column("Value", style="green")

        table.add_row("Total Templates", str(stats['total_templates']))
        table.add_row("Average Quality", f"{stats['avg_quality']:.1f}/100")
        table.add_row("High Quality Count", str(stats['high_quality_count']))
        table.add_row("Popular Color Scheme", stats['most_popular_color_scheme'])
        table.add_row("Popular Layout", stats['most_popular_layout'])

        console.print(table)

        # Recommendations
        console.print("\n[bold]Top Recommendations:[/bold]\n")

        if 'colors' in recommendations:
            console.print(f"  [cyan]Colors:[/cyan] {recommendations['colors']['recommended_scheme']}")

        if 'layout' in recommendations:
            systems = recommendations['layout']['recommended_systems']
            console.print(f"  [cyan]Layout:[/cyan] {', '.join(systems)}")

        console.print()

    except Exception as e:
        console.print(f"[bold red]✗ Error: {e}[/bold red]")
        console.print("[yellow]Tip: Run 'train' command first to build the knowledge base[/yellow]")


if __name__ == '__main__':
    cli()
