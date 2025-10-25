# Contributing to Ollama Pulse

Welcome to Ollama Pulse! We're excited to have you contribute to our automated Ollama ecosystem monitoring system.

## 🎯 What is Ollama Pulse?

Ollama Pulse is an automated daily reporting system that:
- Monitors the Ollama ecosystem across multiple sources
- Generates themed daily reports with prophetic insights
- Tracks bounties, hackathons, and community activity
- Uses ML-powered relevance scoring for "Turbo" content

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Git
- GitHub account

### Setup
```bash
git clone https://github.com/Grumpified-OGGVCT/ollama_pulse.git
cd ollama_pulse
pip install -r requirements.txt
```

### Test Your Setup
```bash
# Run ingestion scripts
python scripts/ingest_official.py
python scripts/ingest_bounties.py

# Generate a test report
python scripts/generate_report.py
```

## 📝 How to Contribute

### 1. Adding a New Data Source

Want to add a new ingestion source? Great! Here's how:

**Create `scripts/ingest_YOURNAME.py`:**
```python
#!/usr/bin/env python3
"""Ollama Pulse - YOUR SOURCE Ingestion"""
import json
from datetime import datetime
from pathlib import Path

def ensure_data_dir():
    Path("data/YOURNAME").mkdir(parents=True, exist_ok=True)

def get_today_filename():
    return f"data/YOURNAME/{datetime.now().strftime('%Y-%m-%d')}.json"

def fetch_data():
    """Fetch data from your source"""
    # Your implementation here
    return []

def main():
    print("🎯 Starting YOUR SOURCE ingestion...")
    ensure_data_dir()
    data = fetch_data()
    
    # Save in standard format
    with open(get_today_filename(), 'w') as f:
        json.dump(data, f, indent=2)
    
    print(f"✅ Saved {len(data)} entries")

if __name__ == "__main__":
    main()
```

**Standard Data Format:**
```json
[
  {
    "title": "Entry title",
    "source": "your_source_name",
    "summary": "Brief description",
    "url": "https://...",
    "date": "2025-10-25T12:00:00",
    "highlights": ["tag1", "tag2"]
  }
]
```

**Update `.github/workflows/ingest.yml`:**
```yaml
strategy:
  matrix:
    script:
      - ingest_official.py
      - ingest_YOURNAME.py  # Add your script
```

**Update `scripts/aggregate.py`:**
```python
yourname = load_source_data("YOURNAME")
all_entries = official + community + tools + bounties + yourname
```

### 2. Improving ML Scoring

Want to enhance Turbo relevance scoring? Edit `scripts/mine_insights.py`:

```python
def score_turbo_relevance(entry):
    """Score 0-1 how relevant entry is to Ollama Turbo/Cloud"""
    # Add your scoring logic
    score = 0.0
    
    # Your improvements here
    if 'your_keyword' in text:
        score += 0.2
    
    return min(score, 1.0)
```

### 3. Adding Report Sections

Create `scripts/YOURNAME_section.py`:
```python
def render_YOURNAME_section():
    """Render your custom section"""
    lines = []
    lines.append("\n## YOUR SECTION TITLE\n\n")
    # Your rendering logic
    return ''.join(lines)
```

Update `scripts/generate_report.py`:
```python
from YOURNAME_section import render_YOURNAME_section

# In main report generation:
report_md += render_YOURNAME_section()
```

### 4. Ethical Scraping Guidelines

All web scraping MUST follow these rules:

✅ **DO:**
- Check `robots.txt` before scraping
- Add delays between requests (1-5 seconds)
- Use descriptive User-Agent: `OllamaPulseBot/1.0 (+https://github.com/Grumpified-OGGVCT/ollama_pulse)`
- Only scrape public data
- Respect rate limits
- Handle errors gracefully

❌ **DON'T:**
- Scrape auth-walled content
- Ignore robots.txt
- Make rapid-fire requests
- Scrape personal data
- Violate ToS

**Example:**
```python
import time, random, requests

def ethical_delay():
    time.sleep(1 + random.random() * 4)

def fetch_with_respect(url):
    headers = {"User-Agent": "OllamaPulseBot/1.0"}
    ethical_delay()
    return requests.get(url, headers=headers, timeout=10)
```

## 🧪 Testing

### Run Tests Locally
```bash
# Test individual scripts
python scripts/ingest_YOURNAME.py

# Test aggregation
python scripts/aggregate.py

# Test report generation
python scripts/generate_report.py
```

### Workflow Testing
```bash
# Trigger workflows manually via GitHub Actions UI
# Or use GitHub CLI:
gh workflow run ingest.yml
gh workflow run daily_report.yml --input force_run=true
```

## 📋 Pull Request Process

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/your-feature`
3. **Make your changes**
4. **Test thoroughly**
5. **Commit with descriptive messages**:
   ```
   feat(source): add HackerNews ingestion
   fix(scoring): improve Turbo relevance for cloud keywords
   docs(contributing): add scraping guidelines
   ```
6. **Push to your fork**: `git push origin feature/your-feature`
7. **Open a Pull Request** with:
   - Clear description of changes
   - Why the change is needed
   - How you tested it
   - Screenshots/examples if applicable

### PR Labels
- `enhancement`: New features
- `bug`: Bug fixes
- `documentation`: Documentation improvements
- `good-first-issue`: Good for newcomers
- `help-wanted`: Extra attention needed

## 🎨 Code Style

- **Python**: Follow PEP 8
- **Line length**: 100 characters max
- **Imports**: Group stdlib, third-party, local
- **Docstrings**: Use for all public functions
- **Comments**: Explain *why*, not *what*

## 🔒 Security

Found a security issue? **DO NOT** open a public issue.

Email: [your-security-email@example.com]

## 📜 License

By contributing, you agree that your contributions will be licensed under the same license as the project.

## 🙏 Recognition

Contributors are recognized in:
- GitHub contributors page
- Monthly acknowledgment in reports
- Special mentions for major features

## 💬 Questions?

- Open a [Discussion](https://github.com/Grumpified-OGGVCT/ollama_pulse/discussions)
- Join our community chat
- Tag maintainers in issues

## 🎯 Priority Areas

We're especially interested in:
- 🌐 New data sources (X/Twitter, HackerNews, Discord)
- 🤖 ML improvements (better scoring, clustering)
- 📊 Visualization (charts, graphs, dashboards)
- 🔍 Search/discovery features
- 🌍 Internationalization
- ⚡ Performance optimizations

Thank you for contributing to Ollama Pulse! 🩸⛏️

