"""Template scraping modules"""

from .base_scraper import BaseScraper
from .html5up_scraper import HTML5UPScraper
from .freecss_scraper import FreeCSScraper
from .templatemo_scraper import TemplateMoScraper
from .colorlib_scraper import ColorlibScraper
from .design_resources_scraper import DesignResourcesScraper
from .react_bits_scraper import ReactBitsScraper
from .scraper_manager import ScraperManager

__all__ = ['BaseScraper', 'HTML5UPScraper', 'FreeCSScraper', 'TemplateMoScraper', 'ColorlibScraper', 'DesignResourcesScraper', 'ReactBitsScraper', 'ScraperManager']
