# Front-End Aesthetic Agent

An AI-powered agent that learns from free website templates to create more creative, attractive, and sophisticated front-end designs.

## Overview

This agent scrapes and analyzes free website templates from various sources to build a comprehensive knowledge base of modern web design patterns, color schemes, layouts, and aesthetic choices. It then uses this knowledge to generate suggestions and improvements for front-end projects.

## Features

- **Template Scraping**: Automatically collects free website templates from popular sources
- **Design Resource Scraping**: Scrapes design resource websites (UI frameworks, icons, colors, fonts) for aesthetic patterns
- **Frontend2 Integration**: Includes curated design resources and training data from 40+ examples
- **Design Analysis**: Extracts color palettes, typography, layouts, spacing patterns, and component styles
- **Pattern Learning**: Builds a knowledge base of design patterns and aesthetic trends
- **Creative Generation**: Suggests design improvements and generates new design concepts
- **Component Extraction**: Extracts reusable UI components from templates
- **Template Browser**: Web interface to browse and preview templates
- **Extensible Architecture**: Easy to add new template sources and analysis methods

## Architecture

```
frontend-aesthetic-agent/
├── agent/
│   ├── scraper/          # Template scraping modules
│   ├── analyzer/         # Design analysis and extraction
│   ├── learner/          # Pattern learning and knowledge base
│   └── generator/        # Creative design generation
├── data/                 # Stored templates and knowledge base
├── config/               # Configuration files
└── cli.py               # Command-line interface
```

## Installation

```bash
pip install -r requirements.txt
```

## Usage

### 🤖 Automatic Mode (Recommended!)

The agent can automatically scrape, analyze, and train on a schedule:

#### Run a single automatic cycle
```bash
python cli.py auto --mode once
```

#### Schedule daily scraping (runs at 2:00 AM)
```bash
python cli.py auto --mode scheduled --interval daily
```

#### Continuous learning (every hour)
```bash
python cli.py auto --mode continuous --delay 60
```

#### View automation logs
```bash
python cli.py logs
```

See [docs/AUTOMATION.md](docs/AUTOMATION.md) for complete automation guide.

### Manual Commands

#### Scrape Templates
```bash
# Scrape website templates
python cli.py scrape --source html5up --limit 10

# Scrape design resources (NEW!)
python cli.py scrape-resources --categories ui_frameworks,icons,colors --limit 5
```

#### Import Frontend2 Data (NEW!)
```bash
# Import pre-collected training data from Frontend2 repo
python cli.py import-frontend2
```

#### Analyze Templates
```bash
python cli.py analyze --input data/templates/
```

#### Train Knowledge Base
```bash
python cli.py train --data data/analyzed/
```

#### Generate Design Guide
```bash
python cli.py generate --scheme vibrant --output design_guide.json
```

#### Analyze & Get Suggestions
```bash
python cli.py suggest your-website.html
```

#### Extract Components
```bash
python cli.py extract --input data/templates/ --output data/components/
```

#### Browse Templates
```bash
python cli.py browse --port 5000
```

#### View Statistics
```bash
python cli.py stats
```

## Template Sources

### Website Templates
- HTML5 UP (https://html5up.net) - ✅ Active
- Colorlib (https://colorlib.com/wp/templates/) - ✅ Active
- Start Bootstrap (https://startbootstrap.com) - ✅ Active
- Website Templates (https://www.websitetemplates.org) - ✅ Active
- TemplateMo (https://templatemo.com) - ⚠️ Detection issues
- Free-CSS.com (https://www.free-css.com) - ⚠️ SSL issues

### Design Resources (NEW!)
Integrated from Frontend2 repository with 40+ pre-analyzed examples:
- UI Frameworks (Bootstrap, Tailwind, Material-UI, etc.)
- Icon Libraries (Bootstrap Icons, React Icons, Font Awesome, etc.)
- Color Resources (Coolors, Adobe Color, Color Hunt, etc.)
- Design Systems (IBM Carbon, Shopify Polaris, etc.)
- CSS Frameworks (Bulma, Foundation, Semantic UI, etc.)

More sources can be easily added!

## License

MIT License
