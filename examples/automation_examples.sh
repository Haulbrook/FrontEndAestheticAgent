#!/bin/bash
# Example automation scripts for Front-End Aesthetic Agent

echo "Front-End Aesthetic Agent - Automation Examples"
echo "================================================"
echo ""

# Example 1: Run a single complete cycle
echo "Example 1: Single cycle (scrape → analyze → train)"
echo "Command: python cli.py auto --mode once"
echo ""

# Example 2: Schedule daily scraping
echo "Example 2: Daily scheduled scraping at 2:00 AM"
echo "Command: python cli.py auto --mode scheduled --interval daily"
echo ""

# Example 3: Hourly scraping
echo "Example 3: Hourly scraping"
echo "Command: python cli.py auto --mode scheduled --interval hourly"
echo ""

# Example 4: Every 30 minutes
echo "Example 4: Scrape every 30 minutes"
echo "Command: python cli.py auto --mode scheduled --interval 30"
echo ""

# Example 5: Continuous mode
echo "Example 5: Continuous mode with 1-hour delay"
echo "Command: python cli.py auto --mode continuous --delay 60"
echo ""

# Example 6: Background execution
echo "Example 6: Run in background with nohup"
echo "Command: nohup python cli.py auto --mode scheduled --interval daily > scraper.log 2>&1 &"
echo ""

# Example 7: View logs
echo "Example 7: View recent logs"
echo "Command: python cli.py logs --limit 10"
echo ""

# Example 8: Check stats
echo "Example 8: Check knowledge base stats"
echo "Command: python cli.py stats"
echo ""

echo "To run any example, copy the command after 'Command:' and execute it"
