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
from agent.extractor.component_extractor import ComponentExtractor
from agent.browser.template_browser import TemplateBrowser

console = Console()


@click.group()
@click.version_option(version='0.1.0')
def cli():
    """Front-End Aesthetic Agent - Learn from templates to create better designs"""
    pass


@cli.command()
@click.option('--source', type=click.Choice(['html5up', 'freecss', 'templatemo', 'colorlib', 'startbootstrap', 'website-templates', 'all']), default='all',
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
@click.option('--input', default='data/templates', help='Directory containing templates')
@click.option('--output', default='data/components', help='Output directory for extracted components')
@click.option('--limit', default=None, type=int, help='Limit number of templates to process')
def extract(input, output, limit):
    """Extract reusable components from templates"""
    console.print("\n[bold cyan]🧩 Front-End Aesthetic Agent - Component Extractor[/bold cyan]\n")

    extractor = ComponentExtractor(output)

    try:
        input_path = Path(input)

        if not input_path.exists():
            console.print(f"[bold red]✗ Directory not found: {input}[/bold red]")
            raise click.Abort()

        # Process each template source
        template_count = 0
        for source_dir in sorted(input_path.iterdir()):
            if not source_dir.is_dir():
                continue

            # Process templates in this source
            templates = sorted([d for d in source_dir.iterdir() if d.is_dir()])

            if limit and template_count >= limit:
                break

            for template_dir in templates:
                if limit and template_count >= limit:
                    break

                extractor.extract_from_directory(str(template_dir))
                template_count += 1

        # Save the component index
        extractor.save_index()

        console.print(f"\n[bold green]✓ Extracted components from {template_count} templates![/bold green]")
        console.print(f"[bold green]✓ Components saved to: {output}/[/bold green]\n")

    except Exception as e:
        console.print(f"[bold red]✗ Error: {e}[/bold red]")
        raise click.Abort()


@cli.command()
@click.option('--port', default=5000, help='Port to run the server on')
@click.option('--host', default='127.0.0.1', help='Host to bind to')
def browse(port, host):
    """Browse templates and components in your web browser"""
    console.print("\n[bold cyan]🌐 Front-End Aesthetic Agent - Template Browser[/bold cyan]\n")

    try:
        browser = TemplateBrowser()
        console.print(f"[green]✓ Starting browser on http://{host}:{port}[/green]")
        console.print(f"[yellow]  Press CTRL+C to stop[/yellow]\n")
        browser.run(host=host, port=port, debug=False)

    except KeyboardInterrupt:
        console.print("\n[yellow]Browser stopped[/yellow]")
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


@cli.command()
@click.argument('html_file', type=click.Path(exists=True))
@click.option('--output', help='Output file for transformed HTML (default: adds -transformed suffix)')
@click.option('--interactive', is_flag=True, help='Interactive mode with step-by-step guidance')
def transform(html_file, output, interactive):
    """Transform a basic website into a beautiful, professional design

    This command guides you through transforming a website using the
    component library and learned design patterns while preserving all
    backend functionality.
    """
    console.print("\n[bold cyan]✨ Frontend Aesthetic Transformation[/bold cyan]\n")

    try:
        # Set default output path
        if not output:
            input_path = Path(html_file)
            output = str(input_path.parent / f"{input_path.stem}-transformed{input_path.suffix}")

        # Read input file
        html_content = Path(html_file).read_text(encoding='utf-8')

        # Step 1: Analyze current site
        console.print("[bold]Step 1: Analyzing your website...[/bold]\n")
        engine = SuggestionEngine()
        result = engine.analyze_and_suggest(html_file)

        if 'error' in result:
            console.print(f"[bold red]✗ {result['error']}[/bold red]")
            raise click.Abort()

        quality_score = result['quality_score']
        suggestions = result['suggestions']

        score_color = "green" if quality_score >= 70 else "yellow" if quality_score >= 50 else "red"
        console.print(Panel.fit(
            f"Current Quality Score: [bold {score_color}]{quality_score}/100[/bold {score_color}]\n"
            f"Component Library: 228 professional components available",
            title="Analysis Complete",
            border_style="cyan"
        ))

        # Step 2: Show component library stats
        console.print("\n[bold]Step 2: Component Library Available[/bold]\n")

        component_summary_path = Path('data/components/summary.json')
        if component_summary_path.exists():
            summary = json.loads(component_summary_path.read_text())

            table = Table(title="Available Components")
            table.add_column("Category", style="cyan")
            table.add_column("Count", style="green")

            for category, count in summary.get('by_category', {}).items():
                if count > 0:
                    table.add_row(category.title(), str(count))

            console.print(table)

        # Step 3: Priority improvements
        console.print("\n[bold]Step 3: Priority Improvements Needed[/bold]\n")

        priority = suggestions.get('priority_improvements', [])
        if priority:
            for i, suggestion in enumerate(priority[:5], 1):
                console.print(f"{i}. [yellow]{suggestion['issue']}[/yellow]")
                console.print(f"   → {suggestion['suggestion']}\n")
        else:
            console.print("[green]✓ No critical issues found![/green]\n")

        # Step 4: Transformation guidance
        console.print("\n[bold]Step 4: Transformation Guidance[/bold]\n")

        console.print("📖 [cyan]To transform this website:[/cyan]")
        console.print("   1. Review SKILL.md for transformation patterns")
        console.print("   2. Browse components: python cli.py browse")
        console.print("   3. Match your components to library equivalents")
        console.print("   4. Preserve ALL functionality (onclick, IDs, data-attributes)")
        console.print("   5. Apply modern design system (colors, typography, spacing)")
        console.print("   6. Test all interactive elements\n")

        # Step 5: Design recommendations
        console.print("\n[bold]Step 5: Design Recommendations[/bold]\n")

        generator = DesignGenerator()
        guide = generator.generate_complete_design_guide()

        console.print(f"[cyan]Recommended Color Scheme:[/cyan] {guide['colors']['scheme']}")
        console.print(f"[cyan]Primary Color:[/cyan] {guide['colors']['primary']}")
        console.print(f"[cyan]Typography:[/cyan] {guide['typography']['recommended_fonts'].get('heading', 'Inter')} + {guide['typography']['recommended_fonts'].get('body', 'Inter')}")
        console.print(f"[cyan]Layout System:[/cyan] {', '.join(guide['layout']['recommended_systems'])}\n")

        # Interactive mode
        if interactive:
            console.print("\n[bold yellow]🤖 Interactive Transformation Mode[/bold yellow]\n")
            console.print("I will now guide you through transforming your website.")
            console.print("This feature requires Claude Code to assist with the actual transformation.\n")

            console.print("[cyan]Use this prompt with Claude Code:[/cyan]")
            console.print("─" * 60)
            console.print(f"""
Please transform {html_file} using the Frontend Aesthetic Agent skill:

1. Analyze the current HTML structure
2. Browse the component library (228 components available)
3. Create a modern design system with:
   - Color scheme: {guide['colors']['scheme']}
   - Typography: {guide['typography']['recommended_fonts'].get('heading')} + {guide['typography']['recommended_fonts'].get('body')}
   - Layout: {', '.join(guide['layout']['recommended_systems'])}
4. Transform each component while preserving:
   - All onclick/event handlers
   - All IDs and data-attributes
   - All backend functionality
5. Save the result to: {output}

Quality target: 80+/100 (current: {quality_score}/100)
""")
            console.print("─" * 60)

        # Save analysis report
        report_path = Path(output).parent / f"{Path(html_file).stem}-analysis-report.json"
        report = {
            'input_file': html_file,
            'output_file': output,
            'current_quality': quality_score,
            'target_quality': 80,
            'suggestions': suggestions,
            'recommended_design': {
                'colors': guide['colors'],
                'typography': guide['typography']['recommended_fonts'],
                'layout_systems': guide['layout']['recommended_systems']
            },
            'component_library': {
                'total_components': 228,
                'categories': summary.get('by_category', {}) if component_summary_path.exists() else {}
            }
        }

        report_path.write_text(json.dumps(report, indent=2), encoding='utf-8')

        console.print(f"\n[green]✓ Analysis report saved to: {report_path}[/green]")
        console.print(f"[green]✓ Ready to transform! Use Claude Code with SKILL.md guidance[/green]\n")

    except Exception as e:
        console.print(f"[bold red]✗ Error: {e}[/bold red]")
        import traceback
        traceback.print_exc()
        raise click.Abort()


if __name__ == '__main__':
    cli()
