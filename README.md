# Front-End Aesthetic Agent

An AI-powered agent that learns from free website templates to create more creative, attractive, and sophisticated front-end designs.

## Overview

This agent scrapes and analyzes free website templates from various sources to build a comprehensive knowledge base of modern web design patterns, color schemes, layouts, and aesthetic choices. It then uses this knowledge to generate suggestions and improvements for front-end projects.

## Features

- **Template Scraping**: Automatically collects free website templates from popular sources
- **Design Analysis**: Extracts color palettes, typography, layouts, spacing patterns, and component styles
- **Pattern Learning**: Builds a knowledge base of design patterns and aesthetic trends
- **Creative Generation**: Suggests design improvements and generates new design concepts
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
python cli.py scrape --source html5up --limit 10
```

#### Analyze Templates
```bash
python cli.py analyze --input data/templates/
```

#### Train Knowledge Base
```bash
python cli.py train --data data/analyzed/
```

#### Generate Suggestions
```bash
python cli.py generate --input your-website.html
```

## Template Sources

- HTML5 UP (https://html5up.net)
- Free-CSS.com (https://www.free-css.com)
- Templated.co (https://templated.co)
- BootstrapMade (https://bootstrapmade.com/free-templates/)

## License

MIT License
