# Contributing to Front-End Aesthetic Agent

Thank you for your interest in contributing! This document provides guidelines for contributing to the project.

## How to Contribute

### Adding New Template Sources

To add a new template source scraper:

1. Create a new scraper class in `agent/scraper/` that inherits from `BaseScraper`
2. Implement the required methods:
   - `get_template_list_url()`
   - `scrape(limit)`
3. Add the scraper to `ScraperManager` in `scraper_manager.py`
4. Update the README with the new source

Example:
```python
from .base_scraper import BaseScraper

class MyTemplateScraper(BaseScraper):
    def __init__(self, output_dir="data/templates/mysite"):
        super().__init__(output_dir)
        self.base_url = "https://example.com"

    def get_template_list_url(self):
        return f"{self.base_url}/templates"

    def scrape(self, limit=10):
        # Implementation here
        pass
```

### Adding New Analyzers

To add new analysis capabilities:

1. Create a new analyzer in `agent/analyzer/`
2. Add analysis method that returns a dictionary
3. Integrate it into `TemplateAnalyzer`
4. Update the knowledge base to learn from new patterns

### Improving the Generator

To improve design generation:

1. Add new generation methods to `DesignGenerator`
2. Update recommendations based on research
3. Add new color schemes, font pairings, etc.

### Adding Tests

We welcome test contributions! Place tests in the `tests/` directory:

```python
import pytest
from agent.analyzer.color_analyzer import ColorAnalyzer

def test_color_extraction():
    analyzer = ColorAnalyzer()
    result = analyzer.analyze("<div style='color: #FF0000'>Test</div>")
    assert result['total_colors'] > 0
```

## Development Setup

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run tests:
   ```bash
   pytest tests/
   ```

## Code Style

- Follow PEP 8 guidelines
- Use meaningful variable names
- Add docstrings to functions and classes
- Keep functions focused and concise

## Pull Request Process

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Add tests if applicable
5. Update documentation
6. Commit your changes (`git commit -m 'Add amazing feature'`)
7. Push to your branch (`git push origin feature/amazing-feature`)
8. Open a Pull Request

## Ideas for Contributions

- Add more template sources
- Improve color analysis (detect complementary colors, etc.)
- Add screenshot capture for visual analysis
- Implement AI-powered suggestions using OpenAI API
- Add export to CSS/SCSS functionality
- Create a web interface
- Add accessibility analysis
- Implement performance analysis
- Add support for React/Vue component analysis

## Questions?

Feel free to open an issue for discussion!
