# Contributing to Ollama Pulse

Welcome! This guide helps you contribute to our automated Ollama ecosystem monitoring system.

## Quick Start

```bash
git clone https://github.com/Grumpified-OGGVCT/ollama_pulse.git
cd ollama_pulse
pip install -r requirements.txt
```

## Adding a New Data Source

Create `scripts/ingest_YOURNAME.py` following the standard format, then update:
- `.github/workflows/ingest.yml` (add to matrix)
- `scripts/aggregate.py` (load your data)

## Ethical Scraping Guidelines

- Check robots.txt
- Add 1-5s delays between requests
- Use descriptive User-Agent
- Only scrape public data
- Respect rate limits

## Pull Request Process

1. Fork the repository
2. Create feature branch
3. Make changes and test
4. Commit with descriptive messages
5. Open PR with clear description

## Priority Areas

- New data sources (X/Twitter, HackerNews)
- ML improvements (scoring, clustering)
- Visualization (charts, dashboards)
- Performance optimizations

Thank you for contributing!
