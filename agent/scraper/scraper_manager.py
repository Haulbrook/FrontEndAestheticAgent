"""Manager for coordinating multiple scrapers"""

from typing import List, Dict, Optional
from .html5up_scraper import HTML5UPScraper
from .freecss_scraper import FreeCSScraper
from .templatemo_scraper import TemplateMoScraper


class ScraperManager:
    """Manages multiple template scrapers"""

    def __init__(self, output_dir: str = "data/templates"):
        self.scrapers = {
            'html5up': HTML5UPScraper(f"{output_dir}/html5up"),
            'freecss': FreeCSScraper(f"{output_dir}/freecss"),
            'templatemo': TemplateMoScraper(f"{output_dir}/templatemo"),
        }

    def scrape_source(self, source: str, limit: int = 10) -> List[Dict]:
        """Scrape templates from a specific source"""
        if source not in self.scrapers:
            raise ValueError(f"Unknown source: {source}. Available: {list(self.scrapers.keys())}")

        scraper = self.scrapers[source]
        return scraper.scrape(limit)

    def scrape_all(self, limit_per_source: int = 10) -> Dict[str, List[Dict]]:
        """Scrape templates from all available sources"""
        results = {}

        for source, scraper in self.scrapers.items():
            print(f"\n{'='*60}")
            print(f"Scraping from: {source.upper()}")
            print(f"{'='*60}\n")

            try:
                templates = scraper.scrape(limit_per_source)
                results[source] = templates
            except Exception as e:
                print(f"✗ Error scraping {source}: {e}")
                results[source] = []

        return results

    def list_sources(self) -> List[str]:
        """List all available scraper sources"""
        return list(self.scrapers.keys())
