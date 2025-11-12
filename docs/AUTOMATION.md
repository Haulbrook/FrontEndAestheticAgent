# Automation Guide

## Overview

The Front-End Aesthetic Agent includes powerful automation features to continuously scrape, analyze, and learn from templates without manual intervention.

## Quick Start

### Run a Single Automatic Cycle

Scrape → Analyze → Train in one command:

```bash
python cli.py auto --mode once
```

### Run on a Schedule

Run daily at 2:00 AM:

```bash
python cli.py auto --mode scheduled --interval daily
```

Run every hour:

```bash
python cli.py auto --mode scheduled --interval hourly
```

Run every 30 minutes:

```bash
python cli.py auto --mode scheduled --interval 30
```

### Run Continuously

Run with 60-minute delay between cycles:

```bash
python cli.py auto --mode continuous --delay 60
```

## Modes Explained

### 1. Once Mode (--mode once)

Runs a single complete cycle:
1. Scrapes templates from all configured sources
2. Analyzes the scraped templates
3. Trains the knowledge base
4. Exits

**Use when:** You want to manually trigger a one-time update

```bash
python cli.py auto --mode once
```

### 2. Scheduled Mode (--mode scheduled)

Runs on a schedule using cron-like intervals:
- `hourly`: Every hour
- `daily`: Daily at 2:00 AM
- `weekly`: Weekly on Mondays at 2:00 AM
- `<number>`: Every N minutes (e.g., `30` = every 30 minutes)

**Use when:** You want to run the agent automatically at specific times

```bash
# Daily scraping
python cli.py auto --mode scheduled --interval daily

# Every 2 hours
python cli.py auto --mode scheduled --interval 120
```

### 3. Continuous Mode (--mode continuous)

Runs indefinitely with a delay between cycles:

**Use when:** You want continuous learning with controlled intervals

```bash
# Run every hour
python cli.py auto --mode continuous --delay 60

# Run every 4 hours
python cli.py auto --mode continuous --delay 240
```

## Configuration

Edit `config/auto_scraper_config.yaml`:

```yaml
# Directory settings
output_dir: "data/templates"
analyzed_dir: "data/analyzed"

# Scraping settings
templates_per_run: 5  # Templates per source per run
sources:
  - html5up
  - freecss

# Schedule settings
schedule_interval: "daily"  # or 'hourly', 'weekly', or minutes

# Automation settings
auto_analyze: true   # Auto-analyze scraped templates
auto_train: true     # Auto-train on analyzed templates
```

## Viewing Logs

Check recent automation runs:

```bash
# Show last 10 runs
python cli.py logs

# Show last 20 runs
python cli.py logs --limit 20
```

Log output includes:
- Timestamp of each run
- Number of templates scraped, analyzed, and learned
- Any errors encountered

## Running in Background

### Using nohup (Linux/Mac)

```bash
nohup python cli.py auto --mode scheduled --interval daily > scraper.log 2>&1 &
```

### Using screen (Linux/Mac)

```bash
# Start a screen session
screen -S aesthetic-agent

# Run the auto-scraper
python cli.py auto --mode scheduled --interval daily

# Detach with Ctrl+A, then D
# Reattach with: screen -r aesthetic-agent
```

### Using systemd (Linux)

Create `/etc/systemd/system/aesthetic-agent.service`:

```ini
[Unit]
Description=Front-End Aesthetic Agent Auto-Scraper
After=network.target

[Service]
Type=simple
User=youruser
WorkingDirectory=/path/to/FrontEndAestheticAgent
ExecStart=/usr/bin/python3 /path/to/FrontEndAestheticAgent/cli.py auto --mode scheduled --interval daily
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

Enable and start:

```bash
sudo systemctl enable aesthetic-agent
sudo systemctl start aesthetic-agent
sudo systemctl status aesthetic-agent
```

### Using Docker

Create `Dockerfile`:

```dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "cli.py", "auto", "--mode", "scheduled", "--interval", "daily"]
```

Run:

```bash
docker build -t aesthetic-agent .
docker run -d --name aesthetic-agent -v $(pwd)/data:/app/data aesthetic-agent
```

## Best Practices

### 1. Start Small

Begin with fewer templates and shorter intervals:

```bash
# Test with 3 templates every hour
python cli.py auto --mode scheduled --interval hourly
```

Update config:
```yaml
templates_per_run: 3
```

### 2. Monitor Initially

Keep logs visible for the first few runs:

```bash
# Run in foreground first
python cli.py auto --mode continuous --delay 60
```

Watch for:
- Successful scraping
- Analysis errors
- Memory usage

### 3. Scale Gradually

Once stable, increase frequency and volume:

```yaml
templates_per_run: 10  # Increase from 5
schedule_interval: "30"  # Every 30 minutes
```

### 4. Review Logs Regularly

```bash
python cli.py logs --limit 20
```

Check for:
- Consistent scraping success
- Error patterns
- Knowledge base growth

### 5. Check Knowledge Base

```bash
python cli.py stats
```

Monitor:
- Total templates learned
- Quality score trends
- Popular patterns

## Troubleshooting

### Issue: No templates being scraped

**Solution:** Check internet connection and template sources
```bash
# Test manual scraping
python cli.py scrape --source html5up --limit 1
```

### Issue: Analysis failing

**Solution:** Check disk space and file permissions
```bash
ls -la data/templates/
df -h
```

### Issue: High memory usage

**Solution:** Reduce templates per run
```yaml
templates_per_run: 3  # Reduce from 5 or 10
```

### Issue: Process stops unexpectedly

**Solution:** Check logs and use proper background execution
```bash
python cli.py logs --limit 5

# Run with nohup
nohup python cli.py auto --mode scheduled --interval daily > scraper.log 2>&1 &
```

## Automation Workflows

### Workflow 1: Daily Learning

Perfect for steady, consistent growth:

```bash
python cli.py auto --mode scheduled --interval daily
```

- Scrapes new templates daily
- Analyzes and learns automatically
- Low resource usage
- Ideal for production

### Workflow 2: Aggressive Learning

For rapid knowledge base building:

```bash
python cli.py auto --mode continuous --delay 30
```

With config:
```yaml
templates_per_run: 10
```

- Scrapes every 30 minutes
- Builds knowledge base quickly
- Higher resource usage
- Good for initial training

### Workflow 3: Weekly Updates

Minimal but consistent:

```bash
python cli.py auto --mode scheduled --interval weekly
```

- Low resource usage
- Good for established knowledge bases
- Catch new trends weekly

## Example: Complete Setup

1. **Configure:**

```bash
# Edit config
nano config/auto_scraper_config.yaml
```

Set:
```yaml
templates_per_run: 5
schedule_interval: "daily"
auto_analyze: true
auto_train: true
```

2. **Initial Run:**

```bash
# Test with one cycle
python cli.py auto --mode once
```

3. **Check Results:**

```bash
python cli.py stats
python cli.py logs
```

4. **Start Automation:**

```bash
# Run in background
nohup python cli.py auto --mode scheduled --interval daily > scraper.log 2>&1 &
```

5. **Monitor:**

```bash
# Check logs
tail -f scraper.log

# Check agent logs
python cli.py logs --limit 5
```

## Advanced: Webhook Integration

Coming soon: Trigger scraping via webhook for CI/CD integration.

## Support

For issues or questions about automation, check the logs first:

```bash
python cli.py logs --limit 20
```

Then review the main application logs if needed.
