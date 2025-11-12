"""Automatic scraping scheduler"""

import time
import schedule
from datetime import datetime
from pathlib import Path
import json

from agent.scraper.scraper_manager import ScraperManager
from agent.analyzer.template_analyzer import TemplateAnalyzer
from agent.learner.pattern_learner import PatternLearner


class AutoScraper:
    """Automatically scrape, analyze, and learn from templates"""

    def __init__(self, config: dict = None):
        self.config = config or self._default_config()
        self.scraper_manager = ScraperManager(self.config['output_dir'])
        self.analyzer = TemplateAnalyzer()
        self.learner = PatternLearner()
        self.log_file = Path("data/scraper_log.json")
        self.log_file.parent.mkdir(parents=True, exist_ok=True)

    def _default_config(self):
        """Default configuration"""
        return {
            'output_dir': 'data/templates',
            'analyzed_dir': 'data/analyzed',
            'templates_per_run': 5,
            'sources': ['html5up', 'freecss'],
            'schedule_interval': 'daily',  # 'hourly', 'daily', 'weekly'
            'auto_analyze': True,
            'auto_train': True
        }

    def run_scraping_cycle(self):
        """Run a complete scraping, analysis, and training cycle"""
        print(f"\n{'='*60}")
        print(f"🤖 Auto-Scraper Cycle Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*60}\n")

        results = {
            'timestamp': datetime.now().isoformat(),
            'scraped': 0,
            'analyzed': 0,
            'learned': 0,
            'errors': []
        }

        try:
            # Step 1: Scrape templates
            print("📥 Step 1: Scraping templates...")
            scraped_templates = {}

            for source in self.config['sources']:
                try:
                    templates = self.scraper_manager.scrape_source(
                        source,
                        self.config['templates_per_run']
                    )
                    scraped_templates[source] = templates
                    results['scraped'] += len(templates)
                    print(f"  ✓ Scraped {len(templates)} from {source}")
                except Exception as e:
                    error_msg = f"Error scraping {source}: {e}"
                    print(f"  ✗ {error_msg}")
                    results['errors'].append(error_msg)

            # Step 2: Analyze templates (if enabled)
            if self.config['auto_analyze'] and results['scraped'] > 0:
                print("\n🔍 Step 2: Analyzing templates...")

                for source, templates in scraped_templates.items():
                    try:
                        source_dir = Path(self.config['output_dir']) / source
                        output_dir = Path(self.config['analyzed_dir']) / source

                        if source_dir.exists():
                            analyzed = self.analyzer.analyze_directory(
                                str(source_dir),
                                str(output_dir)
                            )
                            results['analyzed'] += len(analyzed)
                            print(f"  ✓ Analyzed {len(analyzed)} from {source}")
                    except Exception as e:
                        error_msg = f"Error analyzing {source}: {e}"
                        print(f"  ✗ {error_msg}")
                        results['errors'].append(error_msg)

            # Step 3: Train on new data (if enabled)
            if self.config['auto_train'] and results['analyzed'] > 0:
                print("\n🧠 Step 3: Training on new patterns...")

                try:
                    analyzed_dir = Path(self.config['analyzed_dir'])

                    if analyzed_dir.exists():
                        for source_dir in analyzed_dir.iterdir():
                            if source_dir.is_dir():
                                result = self.learner.learn_from_directory(str(source_dir))
                                if result.get('success'):
                                    results['learned'] += result.get('learned', 0)

                        print(f"  ✓ Learned from {results['learned']} templates")

                        # Show updated stats
                        stats = self.learner.kb.get_statistics()
                        print(f"\n📊 Knowledge Base Stats:")
                        print(f"  Total templates: {stats['total_templates']}")
                        print(f"  Average quality: {stats['avg_quality']:.1f}/100")

                except Exception as e:
                    error_msg = f"Error training: {e}"
                    print(f"  ✗ {error_msg}")
                    results['errors'].append(error_msg)

            # Log results
            self._log_results(results)

            print(f"\n{'='*60}")
            print(f"✅ Cycle Complete!")
            print(f"  Scraped: {results['scraped']} | Analyzed: {results['analyzed']} | Learned: {results['learned']}")
            print(f"{'='*60}\n")

        except Exception as e:
            print(f"\n❌ Cycle failed: {e}")
            results['errors'].append(str(e))
            self._log_results(results)

        return results

    def _log_results(self, results: dict):
        """Log scraping results to file"""
        try:
            # Load existing logs
            if self.log_file.exists():
                logs = json.loads(self.log_file.read_text())
            else:
                logs = []

            # Append new results
            logs.append(results)

            # Keep only last 100 entries
            logs = logs[-100:]

            # Save
            self.log_file.write_text(json.dumps(logs, indent=2))

        except Exception as e:
            print(f"Warning: Could not log results: {e}")

    def start_scheduled(self):
        """Start scheduled scraping"""
        interval = self.config['schedule_interval']

        print(f"\n🚀 Starting Auto-Scraper with {interval} schedule")
        print(f"   Sources: {', '.join(self.config['sources'])}")
        print(f"   Templates per run: {self.config['templates_per_run']}")
        print(f"   Auto-analyze: {self.config['auto_analyze']}")
        print(f"   Auto-train: {self.config['auto_train']}\n")

        # Schedule based on interval
        if interval == 'hourly':
            schedule.every().hour.do(self.run_scraping_cycle)
            print("⏰ Scheduled to run every hour")
        elif interval == 'daily':
            schedule.every().day.at("02:00").do(self.run_scraping_cycle)
            print("⏰ Scheduled to run daily at 2:00 AM")
        elif interval == 'weekly':
            schedule.every().monday.at("02:00").do(self.run_scraping_cycle)
            print("⏰ Scheduled to run weekly on Mondays at 2:00 AM")
        else:
            # Custom interval in minutes
            try:
                minutes = int(interval)
                schedule.every(minutes).minutes.do(self.run_scraping_cycle)
                print(f"⏰ Scheduled to run every {minutes} minutes")
            except:
                print(f"⚠️  Unknown interval: {interval}, defaulting to daily")
                schedule.every().day.at("02:00").do(self.run_scraping_cycle)

        # Run immediately on start
        print("\n▶️  Running initial cycle...\n")
        self.run_scraping_cycle()

        # Keep running
        print("\n⏳ Waiting for next scheduled run... (Press Ctrl+C to stop)\n")

        try:
            while True:
                schedule.run_pending()
                time.sleep(60)  # Check every minute
        except KeyboardInterrupt:
            print("\n\n⏹️  Auto-Scraper stopped by user")

    def run_continuous(self, delay_minutes: int = 60):
        """Run continuously with a delay between cycles"""
        print(f"\n🔄 Starting Continuous Mode (delay: {delay_minutes} minutes)")
        print(f"   Press Ctrl+C to stop\n")

        try:
            while True:
                self.run_scraping_cycle()

                print(f"\n💤 Sleeping for {delay_minutes} minutes...")
                print(f"   Next run at: {datetime.now().replace(microsecond=0).isoformat()}\n")

                time.sleep(delay_minutes * 60)

        except KeyboardInterrupt:
            print("\n\n⏹️  Continuous mode stopped by user")

    def get_logs(self, limit: int = 10):
        """Get recent scraping logs"""
        if not self.log_file.exists():
            return []

        try:
            logs = json.loads(self.log_file.read_text())
            return logs[-limit:]
        except:
            return []
