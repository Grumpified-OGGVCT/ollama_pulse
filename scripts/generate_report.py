#!/usr/bin/env python3
"""
Ollama Pulse - Conversational Daily Report Generation
Generates engaging, developer-focused reports with actionable insights
"""
import json
import os
from datetime import datetime
from pathlib import Path

DOCS_DIR = Path("../docs")
REPORTS_DIR = DOCS_DIR / "reports"


def ensure_reports_dir():
    """Create docs/reports directory if it doesn't exist"""
    DOCS_DIR.mkdir(parents=True, exist_ok=True)
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)


def get_today_date_str():
    return datetime.now().strftime("%Y-%m-%d")


def load_data():
    """Load aggregated data and insights for today"""
    today = get_today_date_str()
    agg_file = f"../data/aggregated/{today}.json"
    insights_file = f"../data/insights/{today}.json"

    aggregated = []
    if os.path.exists(agg_file):
        with open(agg_file, 'r', encoding='utf-8') as f:
            aggregated = json.load(f)

    insights = {}
    if os.path.exists(insights_file):
        with open(insights_file, 'r', encoding='utf-8') as f:
            insights = json.load(f)

    return aggregated, insights


def build_dev_section(aggregated, insights):
    """Build the 'What This Means for Developers' section with concrete examples"""
    lines = ["\n## 🚀 What This Means for Developers\n"]
    lines.append("*Let's talk about what you can actually DO with all this...*\n")
    
    # Extract some concrete examples from the data
    official = [e for e in aggregated if e.get('source') in ['blog', 'cloud_page']]
    tools = [e for e in aggregated if e.get('source') in ['github', 'reddit']]
    patterns = insights.get('patterns', {})
    
    lines.append("### 💡 What can we build with this?\n")
    if tools:
        lines.append("Based on what the community is shipping:\n")
        for tool in tools[:3]:
            title = tool.get('title', 'Unknown')
            highlights = tool.get('highlights', [])
            if highlights:
                highlight_text = ', '.join(highlights[:2])
                lines.append(f"- **{title}**: {highlight_text}\n")
    else:
        lines.append("- Check back tomorrow for fresh project ideas from the community!\n")
    
    lines.append("\n### 🔧 How can we leverage these tools?\n")
    lines.append("Here's the exciting part - you can combine these discoveries:\n")
    lines.append("```python\n")
    lines.append("# Example: Quick Ollama integration\n")
    lines.append("import ollama\n\n")
    lines.append("response = ollama.chat(model='llama3.2', messages=[\n")
    lines.append("  {'role': 'user', 'content': 'Explain quantum computing'}\n")
    lines.append("])\n")
    lines.append("print(response['message']['content'])\n")
    lines.append("```\n")
    
    lines.append("\n### 🎯 What problems does this solve?\n")
    if official:
        lines.append("The official updates show us:\n")
        for update in official[:2]:
            title = update.get('title', 'Unknown')
            lines.append(f"- {title}\n")
    lines.append("- **Privacy**: Run AI models locally without sending data to external APIs\n")
    lines.append("- **Cost**: No per-token charges - your hardware, your rules\n")
    lines.append("- **Speed**: Local inference = no network latency\n")
    
    lines.append("\n### ✨ What's now possible that wasn't before?\n")
    if patterns:
        lines.append("Emerging patterns reveal new possibilities:\n")
        for pattern_name in list(patterns.keys())[:2]:
            clean_name = pattern_name.replace('_', ' ').title()
            lines.append(f"- **{clean_name}**: New integrations and use cases\n")
    lines.append("- **Ollama Cloud**: Access to massive models (235B, 480B, 671B, 1T parameters!)\n")
    lines.append("- **Multi-modal**: Vision + language models working together\n")
    lines.append("- **Agentic workflows**: Models that can use tools and make decisions\n")
    
    lines.append("\n### 🔬 What should we experiment with next?\n")
    lines.append("**Immediate action items for vibe coders:**\n")
    lines.append("1. Try the new Ollama Cloud models - they're production-ready NOW\n")
    lines.append("2. Build a quick RAG (Retrieval-Augmented Generation) pipeline\n")
    lines.append("3. Experiment with multi-model orchestration (use different models for different tasks)\n")
    lines.append("4. Create a local AI assistant that actually understands YOUR codebase\n")
    
    lines.append("\n### 🌊 How can we make it better?\n")
    lines.append("**Ideas for the community:**\n")
    lines.append("- Share your Ollama integrations on GitHub (tag: `ollama`)\n")
    lines.append("- Contribute to the ecosystem - every tool makes us all stronger\n")
    lines.append("- Document your learnings - help the next developer\n")
    lines.append("- Build in public - your experiments inspire others\n")
    
    return "".join(lines)


def generate_report_md(aggregated, insights):
    """Generate conversational Markdown report"""
    today = get_today_date_str()
    
    report = f"""# 📡 Ollama Pulse – {today}

*Hey! Here's what's happening in the Ollama ecosystem today...*

---

## 📊 Quick Stats

- **Total Discoveries**: {len(aggregated)} items tracked
- **Patterns Detected**: {insights.get('stats', {}).get('total_patterns', 0)}
- **Key Insights**: {insights.get('stats', {}).get('total_inferences', 0)}
- **Last Updated**: {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}

---

## 🎯 Official Updates

"""

    official = [e for e in aggregated if e.get('source') in ['blog', 'cloud_page']]
    if official:
        report += "Here's what the Ollama team shipped:\n\n"
        report += "| Date | What Happened | Source | Link |\n"
        report += "|------|---------------|--------|------|\n"
        for entry in official[:10]:
            date = entry.get('date', '')[:10]
            title = entry.get('title', 'N/A')
            source = entry.get('source', 'N/A')
            url = entry.get('url', '#')
            report += f"| {date} | {title} | {source} | [Check it out]({url}) |\n"
    else:
        report += "*No official updates today - but that's okay, the community never sleeps!*\n"

    report += "\n---\n\n## 🛠️ Community Builds & Tools\n\n"

    tools = [e for e in aggregated if e.get('source') in ['github', 'reddit']]
    if tools:
        report += "Look what developers are building:\n\n"
        report += "| Project | Where | What's Cool | Link |\n"
        report += "|---------|-------|-------------|------|\n"
        for entry in tools[:15]:
            title = entry.get('title', 'N/A')
            source = entry.get('source', 'N/A')
            highlights = ', '.join(entry.get('highlights', [])[:2]) or 'Interesting project'
            url = entry.get('url', '#')
            report += f"| {title} | {source} | {highlights} | [Explore]({url}) |\n"
    else:
        report += "*Quiet day on the community front - check back tomorrow!*\n"

    report += "\n---\n\n## 📈 Emerging Patterns\n\n"

    patterns = insights.get('patterns', {})
    if patterns:
        report += "We're seeing some interesting trends:\n\n"
        for pattern_name, items in patterns.items():
            clean_name = pattern_name.replace('_', ' ').title()
            report += f"### {clean_name}\n\n"
            report += f"*{len(items)} projects in this space*\n\n"
            for item in items[:5]:
                title = item.get('title', 'N/A')
                url = item.get('url', '#')
                report += f"- [{title}]({url})\n"
            report += "\n"
    else:
        report += "*No major patterns detected yet - early days!*\n"

    report += "\n---\n\n## 🔔 Key Insights & Alerts\n\n"

    inferences = insights.get('inferences', [])
    if inferences:
        report += "Here's what this all means:\n\n"
        for inf in inferences:
            pattern = inf.get('pattern', 'N/A')
            observation = inf.get('observation', 'N/A')
            inference = inf.get('inference', 'N/A')
            confidence = inf.get('confidence', 'medium')
            emoji = "🔥" if confidence == "high" else "💡"
            clean_pattern = pattern.replace('_', ' ').title()
            report += f"{emoji} **{clean_pattern}**\n\n"
            report += f"- What we're seeing: {observation}\n"
            report += f"- What it means: {inference}\n"
            report += f"- Confidence: {confidence}\n\n"
    else:
        report += "*No major insights today - but keep watching this space!*\n"

    # Add the developer-focused section
    report += build_dev_section(aggregated, insights)

    report += "\n---\n\n## 📚 About This Report\n\n"
    report += "Ollama Pulse is your automated scout in the Ollama ecosystem. "
    report += "We track official updates, community projects, and emerging patterns so you don't have to.\n\n"
    report += "- **Source Code**: [github.com/Grumpified-OGGVCT/ollama_pulse](https://github.com/Grumpified-OGGVCT/ollama_pulse)\n"
    report += "- **Powered by**: GitHub Actions + Pages + Jekyll\n"
    report += "- **Updated**: Daily at 4:00 PM Central Time\n\n"
    report += "*Built with ❤️ for developers who ship*\n"

    return report


def save_report(report_md):
    """Save the report as both Markdown and HTML with Jekyll front matter"""
    ensure_reports_dir()
    today = get_today_date_str()

    # Add Jekyll front matter
    md_front_matter = f"""---
layout: default
title: Pulse {today}
---

"""

    # Save Markdown version
    md_path = REPORTS_DIR / f"pulse-{today}.md"
    with open(md_path, 'w', encoding='utf-8') as f:
        f.write(md_front_matter + report_md)
    print(f"💾 Saved Markdown report to {md_path}")

    # Update index.html with Jekyll front matter
    index_front_matter = """---
layout: default
title: Ollama Pulse
---

"""

    # Create a simple index that links to the latest report
    index_body = f"""<div class="controls">
  <input type="text" id="search" placeholder="Search reports..." />
  <select id="sort">
    <option value="date">Sort by Date</option>
    <option value="items">Sort by Items</option>
  </select>
</div>

<div id="report-list">
  <div class="card">
    <h3>Latest Report: {today}</h3>
    <p>Check out today's Ollama ecosystem discoveries!</p>
    <p class="meta">Generated: {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}</p>
    <a href="reports/pulse-{today}.html">Read full report →</a>
  </div>
</div>
"""

    index_path = DOCS_DIR / "index.html"
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(index_front_matter + index_body)
    print(f"💾 Updated index.html")


def main():
    print("🚀 Starting conversational report generation...")
    aggregated, insights = load_data()

    if not aggregated and not insights:
        print("⚠️  No data available to generate report")
        return

    report_md = generate_report_md(aggregated, insights)
    save_report(report_md)

    print("✅ Report generation complete!")


if __name__ == "__main__":
    main()

