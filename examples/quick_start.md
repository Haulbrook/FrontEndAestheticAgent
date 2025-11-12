# Quick Start Guide

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd FrontEndAestheticAgent
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Basic Usage

### 1. Scrape Templates

Scrape 5 templates from HTML5 UP:
```bash
python cli.py scrape --source html5up --limit 5
```

Scrape from all sources:
```bash
python cli.py scrape --source all --limit 10
```

### 2. Analyze Templates

Analyze all scraped templates:
```bash
python cli.py analyze
```

Analyze specific directory:
```bash
python cli.py analyze --input data/templates/html5up --output data/analyzed/html5up
```

### 3. Train the Agent

Learn patterns from analyzed templates:
```bash
python cli.py train
```

Train from specific directory:
```bash
python cli.py train --data data/analyzed/html5up
```

### 4. Generate Design Guide

Generate a complete design guide:
```bash
python cli.py generate
```

Generate with specific color scheme:
```bash
python cli.py generate --scheme dark_mode --output my_design_guide.json
```

### 5. Get Suggestions for Your Design

Analyze your HTML file and get improvement suggestions:
```bash
python cli.py suggest path/to/your/index.html
```

### 6. View Statistics

View knowledge base statistics:
```bash
python cli.py stats
```

## Complete Workflow Example

```bash
# Step 1: Scrape templates from all sources
python cli.py scrape --source all --limit 10

# Step 2: Analyze the scraped templates
python cli.py analyze

# Step 3: Train the agent on analyzed patterns
python cli.py train

# Step 4: View what the agent has learned
python cli.py stats

# Step 5: Generate a design guide
python cli.py generate --output my_design_guide.json

# Step 6: Analyze your existing design
python cli.py suggest examples/sample_website.html
```

## Understanding the Output

### Design Guide Structure

The generated design guide includes:

- **Colors**: Recommended color palette with primary, secondary, and accent colors
- **Layout**: Suggested layout systems (Grid, Flexbox) and component structure
- **Typography**: Font recommendations and size scale
- **Style**: Modern CSS techniques and animation suggestions

### Suggestion Types

When analyzing your design, you'll see:

- 🔴 **Critical**: Must fix (e.g., no responsive design)
- ⚠️ **Warning**: Should fix (e.g., too many colors)
- ℹ️ **Info**: Nice to have (e.g., add animations)

## Tips

1. **Start with quality templates**: Scrape from multiple sources to learn diverse patterns
2. **Analyze first**: Always analyze templates before training
3. **Iterative improvement**: Re-train as you add more templates
4. **Use suggestions**: Apply the priority suggestions to your designs
5. **Check stats**: Monitor your knowledge base growth

## Common Issues

### No templates found
- Make sure you ran `scrape` before `analyze`
- Check `data/templates/` directory exists

### Analysis fails
- Ensure templates have HTML files
- Check file permissions

### Empty knowledge base
- Run `train` after analyzing templates
- Verify `data/analyzed/` contains JSON files

## Next Steps

- Explore the generated design guide
- Apply recommendations to your projects
- Contribute more template sources
- Customize the configuration in `config/config.yaml`
