# Frontend2 Integration Guide

This document describes the integration of the [Frontend2 repository](https://github.com/Haulbrook/Frontend2) design resources and training data into the FrontEndAestheticAgent.

## What is Frontend2?

Frontend2 is a curated collection of free design resources for web development, including:
- UI frameworks and component libraries
- Icon sets and icon libraries
- Color palette tools
- Typography resources
- Design systems
- CSS frameworks
- And much more!

## Integration Overview

The integration adds three major capabilities to FrontEndAestheticAgent:

### 1. Pre-Collected Training Data

The Frontend2 repository includes pre-scraped and analyzed design data from 40+ popular design resource websites. This data has been ethically collected with respect to robots.txt and terms of service.

**Location**: `data/frontend2_training/`

**Files**:
- `aesthetic_training_data.json` - Raw scraped data (colors, layouts, typography)
- `bot_training_dataset.json` - Structured training examples with learned patterns
- `bot_prompt_templates.txt` - Example prompts based on learned aesthetics
- `categorized_resources.json` - Organized list of design resource URLs
- `design_resources.json` - Complete design resource database

### 2. Design Resource Scraper

A new scraper module specifically designed for design resource websites (as opposed to complete templates).

**Module**: `agent/scraper/design_resource_scraper.py`

**Features**:
- Ethical scraping with robots.txt checking
- Extracts colors, layout structures, typography
- Respects rate limits with configurable delays
- Categorizes resources (UI frameworks, icons, colors, etc.)

**Usage**:
```bash
# Scrape specific categories
python cli.py scrape-resources --categories ui_frameworks,icons,colors --limit 10

# Scrape all default categories
python cli.py scrape-resources --limit 5
```

### 3. Knowledge Base Importer

Imports the Frontend2 training data directly into your knowledge base without needing to scrape.

**Module**: `agent/learner/frontend2_importer.py`

**Features**:
- Imports pre-analyzed color patterns
- Integrates layout structures
- Adds typography patterns
- Merges with existing knowledge base
- Generates integration reports

**Usage**:
```bash
# Import all Frontend2 data
python cli.py import-frontend2

# Import without generating report
python cli.py import-frontend2 --no-report
```

## Quick Start

### Option 1: Import Existing Data (Fastest)

```bash
# Import pre-collected training data
python cli.py import-frontend2

# View updated statistics
python cli.py stats
```

This immediately gives you knowledge from 40+ design resources without any scraping.

### Option 2: Scrape Fresh Data

```bash
# Scrape design resources
python cli.py scrape-resources --limit 10

# This creates: data/frontend2_training/extended_training_data.json
```

### Option 3: Combined Approach

```bash
# Import existing data first
python cli.py import-frontend2

# Then scrape for additional data
python cli.py scrape-resources --limit 5

# Train on everything
python cli.py train
```

## Available Resource Categories

When using `scrape-resources`, you can target these categories:

- `ui_frameworks` - React, Vue, Angular libraries
- `icons` - Icon sets and libraries
- `colors` - Color palette generators
- `fonts` - Font resources
- `illustrations` - Illustration libraries
- `design_systems` - Complete design systems
- `css_frameworks` - CSS frameworks like Bootstrap, Tailwind
- `animations` - Animation libraries
- `charts` - Chart and data visualization libraries

## Data Structure

### Aesthetic Training Data
```json
{
  "url": "https://example.com",
  "resource_name": "Bootstrap Icons",
  "category": "icons",
  "colors": ["#563d7c", "#212529"],
  "layout": {
    "headers": 5,
    "sections": 3,
    "buttons": 10
  },
  "typography": {
    "font_links": ["https://fonts.google.com/..."]
  }
}
```

### Bot Training Dataset
```json
{
  "version": "1.0",
  "total_examples": 43,
  "learned_patterns": {
    "popular_colors": [
      {"color": "#ffffff", "frequency": 3}
    ],
    "categories_analyzed": ["ui_frameworks", "icons"]
  },
  "training_examples": [...]
}
```

## Integration Reports

After importing, an integration report is generated at:
`data/frontend2_training/integration_report.json`

This includes:
- Top 20 most popular colors
- Top 10 most used components
- Top 10 most popular fonts
- Knowledge base statistics

## Ethical Considerations

The Frontend2 integration follows these ethical guidelines:

1. **robots.txt Compliance**: Checks and respects robots.txt before scraping
2. **Rate Limiting**: Configurable delays between requests (default: 3 seconds)
3. **User Agent**: Identifiable user agent with contact information
4. **Attribution**: All scraped data includes source URLs
5. **Public Resources**: Only scrapes publicly available design resources
6. **No Content Theft**: Extracts only metadata and design patterns, not content

## Architecture Changes

### New Modules
```
agent/
├── scraper/
│   └── design_resource_scraper.py    (NEW)
└── learner/
    └── frontend2_importer.py         (NEW)

data/
└── frontend2_training/               (NEW)
    ├── aesthetic_training_data.json
    ├── bot_training_dataset.json
    ├── categorized_resources.json
    ├── design_resources.json
    └── integration_report.json
```

### Updated Modules
- `agent/scraper/__init__.py` - Added DesignResourceScraper
- `agent/scraper/scraper_manager.py` - Added design-resources source
- `agent/learner/__init__.py` - Added Frontend2Importer
- `cli.py` - Added scrape-resources and import-frontend2 commands

## CLI Commands Reference

### scrape-resources
```bash
python cli.py scrape-resources [OPTIONS]

Options:
  --categories TEXT  Comma-separated categories (default: ui_frameworks,icons,colors,design_systems,css_frameworks)
  --limit INTEGER    Resources per category (default: 10)
```

### import-frontend2
```bash
python cli.py import-frontend2 [OPTIONS]

Options:
  --report / --no-report  Generate integration report (default: True)
```

## Troubleshooting

### "Resources file not found"
Make sure the Frontend2 training data is in `data/frontend2_training/`. Run `git pull` to ensure you have the latest files.

### "Blocked by robots.txt"
Some sites may block scraping. The importer will skip these and report which ones were blocked.

### "SSL Certificate Error"
Some older sites may have SSL issues. The scraper will catch these errors and continue with other resources.

## Credits

- Frontend2 Repository: https://github.com/Haulbrook/Frontend2
- Original design resources: See `data/frontend2_training/design_resources.json` for complete attribution

## License

The integration code is MIT licensed. Individual design resources maintain their own licenses - please check each resource's terms before use.
