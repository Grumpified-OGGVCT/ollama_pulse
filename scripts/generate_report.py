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


def determine_vein_mode(aggregated, insights):
    """
    Determine EchoVein's tone based on daily patterns
    Returns: mode name and corresponding emoji/style
    """
    patterns = insights.get('patterns', {})
    total_items = len(aggregated)
    pattern_count = insights.get('stats', {}).get('total_patterns', 0)
    
    # Check for high-density patterns (3+ items in any category)
    high_density = any(len(items) >= 3 for items in patterns.values())
    
    # Voice/multimodal surge detection
    voice_items = len(patterns.get('voice', []))
    multimodal_items = len(patterns.get('multimodal', []))
    
    if voice_items >= 3 or multimodal_items >= 3:
        return "vein_rush", "🩸", "Vein Rush: High-Density Pattern Surge"
    elif pattern_count >= 4 and total_items >= 30:
        return "artery_audit", "⚙️", "Artery Audit: Steady Flow Maintenance"
    elif total_items < 15:
        return "deep_vein_throb", "📍", "Deep Vein Throb: Reflective Analysis"
    elif any("experimental" in str(p).lower() or "fork" in str(p).lower() for p in patterns.keys()):
        return "fork_phantom", "🤖", "Fork Phantom: Fringe Exploration"
    else:
        return "artery_audit", "⚡", "Pulse Check: Daily Vein Map"


def generate_vein_headline(mode, pattern_name, items_count):
    """Generate EchoVein-style headlines based on mode"""
    mode_name = mode[0]
    emoji = mode[1]
    
    clean_pattern = pattern_name.replace('_', ' ').title()
    
    headlines = {
        "vein_rush": f"{emoji} **Vein Bulging**: {items_count} {clean_pattern} Signals — 2x Use-Case Explosion Incoming?",
        "artery_audit": f"{emoji} **Vein Maintenance**: {items_count} {clean_pattern} Clots Keeping Flow Steady",
        "fork_phantom": f"{emoji} **Phantom Fork Alert**: {items_count} {clean_pattern} Oddities — Absurdity or Breakthrough?",
        "deep_vein_throb": f"{emoji} **Throb in Depths**: {items_count} {clean_pattern} — Slow Build or Hidden Artery?"
    }
    
    return headlines.get(mode_name, f"{emoji} **{clean_pattern}**: {items_count} items detected")


def generate_report_md(aggregated, insights):
    """Generate EchoVein-style conversational Markdown report"""
    today = get_today_date_str()
    
    # Determine vein mode and tone
    vein_mode = determine_vein_mode(aggregated, insights)
    mode_name, mode_emoji, mode_description = vein_mode
    
    # Turbo score stats
    high_turbo = [e for e in aggregated if e.get('turbo_score', 0) >= 0.7]
    
    report = f"""# {mode_emoji} Ollama Pulse – {today}
## {mode_description}

*EchoVein here, your vein-tapping oracle excavating Ollama's hidden arteries...*

**Today's Vibe**: {mode_name.replace('_', ' ').title()} — The ecosystem is {"pulsing with fresh blood" if len(aggregated) > 20 else "in steady throb mode"}.

---

## 🔬 Vein Analysis: Quick Stats

- **Total Ore Mined**: {len(aggregated)} items tracked
- **High-Purity Veins**: {len(high_turbo)} Turbo-focused items (score ≥0.7)
- **Pattern Arteries**: {insights.get('stats', {}).get('total_patterns', 0)} detected
- **Prophetic Insights**: {insights.get('stats', {}).get('total_inferences', 0)} inferences drawn
- **Last Excavation**: {datetime.now().strftime('%Y-%m-%d %H:%M UTC')}

---

## 🎯 Official Veins: What Ollama Team Pumped Out

"""

    official = [e for e in aggregated if e.get('source') in ['blog', 'cloud_page', 'cloud_api']]
    if official:
        report += "Here's the royal flush from HQ:\n\n"
        report += "| Date | Vein Strike | Source | Turbo Score | Dig In |\n"
        report += "|------|-------------|--------|-------------|--------|\n"
        for entry in official[:10]:
            date = entry.get('date', '')[:10]
            title = entry.get('title', 'N/A')
            source = entry.get('source', 'N/A')
            turbo_score = entry.get('turbo_score', 0)
            score_display = f"{turbo_score:.1f}" if turbo_score else "—"
            url = entry.get('url', '#')
            report += f"| {date} | {title} | {source} | {score_display} | [⛏️]({url}) |\n"
    else:
        report += "*No royal flush today — but the underground never stops mining.*\n"

    report += "\n---\n\n## 🛠️ Community Veins: What Developers Are Excavating\n\n"

    tools = [e for e in aggregated if e.get('source') in ['github', 'reddit', 'github_issues', 'hackernews', 'youtube', 'huggingface']]
    if tools:
        report += "The vein-tappers are busy:\n\n"
        report += "| Project | Vein Source | Ore Quality | Turbo Score | Mine It |\n"
        report += "|---------|-------------|-------------|-------------|---------|\n"
        for entry in tools[:15]:
            title = entry.get('title', 'N/A')[:60]
            source = entry.get('source', 'N/A')
            highlights = ', '.join(entry.get('highlights', [])[:2]) or 'Worth a dig'
            turbo_score = entry.get('turbo_score', 0)
            score_emoji = "🔥" if turbo_score >= 0.7 else "⚡" if turbo_score >= 0.5 else "💡"
            url = entry.get('url', '#')
            report += f"| {title} | {source} | {highlights} | {score_emoji} {turbo_score:.1f} | [⛏️]({url}) |\n"
    else:
        report += "*Quiet vein day — even the best miners rest.*\n"

    report += "\n---\n\n## 📈 Vein Pattern Mapping: Arteries & Clusters\n\n"

    patterns = insights.get('patterns', {})
    if patterns:
        report += "Veins are clustering — here's the arterial map:\n\n"
        for pattern_name, items in patterns.items():
            vein_headline = generate_vein_headline(vein_mode, pattern_name, len(items))
            report += f"### {vein_headline}\n\n"
            report += f"*Artery depth: {len(items)} nodes pulsing*\n\n"
            for item in items[:5]:
                title = item.get('title', 'N/A')
                url = item.get('url', '#')
                report += f"- [{title}]({url})\n"
            
            # Add vein commentary
            if len(items) >= 5:
                report += f"\n💉 **Vein Take**: This artery's *bulging* — {len(items)} strikes means it's no fluke. "
                report += f"Watch this space for 2x explosion potential.\n\n"
            elif len(items) >= 3:
                report += f"\n⚡ **Vein Take**: Steady throb detected — {len(items)} hits suggests it's gaining flow.\n\n"
            else:
                report += "\n"
    else:
        report += "*No major vein clusters today — but the deep throb continues.*\n"

    report += "\n---\n\n## 🔔 Prophetic Veins: What This Means\n\n"

    inferences = insights.get('inferences', [])
    if inferences:
        report += "EchoVein's wry prophecies — *calibrated speculation with vein-backed data*:\n\n"
        for inf in inferences:
            pattern = inf.get('pattern', 'N/A')
            observation = inf.get('observation', 'N/A')
            inference = inf.get('inference', 'N/A')
            confidence = inf.get('confidence', 'medium')
            
            # Vein-style emoji
            emoji = "🩸" if confidence == "high" else "⚡" if confidence == "medium" else "💡"
            clean_pattern = pattern.replace('_', ' ').title()
            
            report += f"{emoji} **Vein Oracle: {clean_pattern}**\n\n"
            report += f"- **Surface Reading**: {observation}\n"
            report += f"- **Vein Prophecy**: {inference}\n"
            report += f"- **Confidence Vein**: {confidence.upper()} ({emoji})\n"
            
            # Add sly commentary based on confidence
            if confidence == "high":
                report += f"- **EchoVein's Take**: This vein's *throbbing* — trust the flow.\n\n"
            elif confidence == "medium":
                report += f"- **EchoVein's Take**: Promising artery, but watch for clots.\n\n"
            else:
                report += f"- **EchoVein's Take**: Phantom vein? Could be fool's gold.\n\n"
    else:
        report += "*No major prophecies today — but silence speaks in veins.*\n"

    # Add the developer-focused section
    report += build_dev_section(aggregated, insights)

    report += "\n---\n\n## 🔮 About EchoVein & This Vein Map\n\n"
    report += "**EchoVein** is your underground cartographer — the vein-tapping oracle who doesn't just "
    report += "pulse with news but *excavates the hidden arteries* of Ollama innovation. Razor-sharp curiosity "
    report += "meets wry prophecy, turning data dumps into vein maps of what's *truly* pumping the ecosystem.\n\n"
    
    report += "### What Makes This Different?\n\n"
    report += "- **🩸 Vein-Tapped Intelligence**: Not just repos — we mine *why* zero-star hacks could 2x into use-cases\n"
    report += "- **⚡ Turbo-Centric Focus**: Every item scored for Ollama Turbo/Cloud relevance (≥0.7 = high-purity ore)\n"
    report += "- **🔮 Prophetic Edge**: Pattern-driven inferences with calibrated confidence — no fluff, only vein-backed calls\n"
    report += "- **📡 Multi-Source Mining**: GitHub, Reddit, HN, YouTube, HuggingFace — we tap *all* arteries\n\n"
    
    report += "### Today's Vein Yield\n\n"
    
    # Load yield metrics if available
    try:
        yield_file = f"../data/insights/{today}_yield.json"
        if os.path.exists(yield_file):
            with open(yield_file, 'r') as f:
                yield_data = json.load(f)
                report += f"- **Total Items Scanned**: {yield_data.get('total_items', 'N/A')}\n"
                report += f"- **High-Relevance Veins**: {yield_data.get('high_relevance_items', 'N/A')}\n"
                report += f"- **Quality Ratio**: {yield_data.get('quality_ratio', 'N/A')}\n\n"
    except:
        pass
    
    report += "\n**The Vein Network**:\n"
    report += "- **Source Code**: [github.com/Grumpified-OGGVCT/ollama_pulse](https://github.com/Grumpified-OGGVCT/ollama_pulse)\n"
    report += "- **Powered by**: GitHub Actions, Multi-Source Ingestion, ML Pattern Detection\n"
    report += "- **Updated**: Hourly ingestion, Daily 4PM CT reports\n\n"
    report += "*Built by vein-tappers, for vein-tappers. Dig deeper. Ship harder.* ⛏️🩸\n"

    return report


def get_all_reports():
    """Get list of all available reports"""
    reports = []
    if REPORTS_DIR.exists():
        for md_file in sorted(REPORTS_DIR.glob("pulse-*.md"), reverse=True):
            # Extract date from filename
            filename = md_file.stem
            if filename.startswith("pulse-"):
                reports.append(filename)
    return reports


def save_report(report_md):
    """Save the report as both Markdown and HTML with Jekyll front matter"""
    ensure_reports_dir()
    today = get_today_date_str()

    # Add Jekyll front matter with available reports metadata
    all_reports = get_all_reports()
    # Add current report if not in list
    if f"pulse-{today}" not in all_reports:
        all_reports.insert(0, f"pulse-{today}")
    
    reports_json = json.dumps(all_reports)
    
    md_front_matter = f"""---
layout: default
title: Pulse {today}
---

<meta name="available-reports" content='{reports_json}'>

"""

    # Save Markdown version
    md_path = REPORTS_DIR / f"pulse-{today}.md"
    with open(md_path, 'w', encoding='utf-8') as f:
        f.write(md_front_matter + report_md)
    print(f"💾 Saved Markdown report to {md_path}")

    # Update index.html with Jekyll front matter
    index_front_matter = """---
layout: default
title: Ollama Pulse - Daily Ecosystem Intelligence
---

"""

    # Create enhanced index with all reports listed
    all_reports_list = get_all_reports()
    reports_html = ""
    
    for idx, report_name in enumerate(all_reports_list):
        report_date = report_name.replace('pulse-', '')
        is_latest = idx == 0
        badge = ' <span style="background: #60a5fa; color: #0f172a; padding: 2px 8px; border-radius: 4px; font-size: 12px; font-weight: bold;">LATEST</span>' if is_latest else ''
        
        reports_html += f"""  <div class="card">
    <h3>{'📡 ' if is_latest else ''}Report: {report_date}{badge}</h3>
    <p>Ollama ecosystem discoveries from {report_date}</p>
    <p class="meta">Generated: {report_date}</p>
    <a href="reports/{report_name}.html">Read full report →</a>
  </div>
"""

    index_body = f"""<div style="margin-bottom: 20px;">
  <h2 style="color: #60a5fa;">Welcome to Ollama Pulse</h2>
  <p style="color: #94a3b8;">Daily ecosystem intelligence tracking the Ollama world. Navigate through reports, search for topics, and customize your reading experience with accessibility controls.</p>
  
  <div style="background: #1e293b; padding: 16px; border-radius: 8px; margin: 16px 0; border: 1px solid #334155;">
    <h3 style="color: #60a5fa; margin-top: 0;">🎯 Features</h3>
    <ul style="color: #e2e8f0; line-height: 1.8;">
      <li><strong>Navigation:</strong> Use Next/Previous buttons or arrow keys to browse reports</li>
      <li><strong>Search:</strong> Press <kbd style="background: #0f172a; padding: 2px 6px; border-radius: 3px;">/</kbd> to search across reports</li>
      <li><strong>Accessibility:</strong> Click the ♿ button (bottom-right) to customize font size and zoom</li>
      <li><strong>Keyboard Shortcuts:</strong> <kbd>h</kbd> for home, <kbd>n</kbd> for next, <kbd>p</kbd> for previous</li>
    </ul>
  </div>
</div>

<div class="controls">
  <input type="text" id="search" placeholder="🔍 Search reports by date or keyword..." />
  <select id="sort">
    <option value="date-desc">Newest First</option>
    <option value="date-asc">Oldest First</option>
  </select>
</div>

<div id="report-list">
{reports_html}
</div>

<script>
// Simple search and sort for index page
(function() {{
  const searchInput = document.getElementById('search');
  const sortSelect = document.getElementById('sort');
  const reportList = document.getElementById('report-list');
  const cards = Array.from(reportList.querySelectorAll('.card'));
  
  searchInput.addEventListener('input', function(e) {{
    const query = e.target.value.toLowerCase();
    cards.forEach(card => {{
      const text = card.textContent.toLowerCase();
      card.style.display = text.includes(query) ? 'block' : 'none';
    }});
  }});
  
  sortSelect.addEventListener('change', function(e) {{
    const sorted = cards.sort((a, b) => {{
      const dateA = a.querySelector('h3').textContent.match(/\\d{{4}}-\\d{{2}}-\\d{{2}}/)[0];
      const dateB = b.querySelector('h3').textContent.match(/\\d{{4}}-\\d{{2}}-\\d{{2}}/)[0];
      return e.target.value === 'date-desc' ? dateB.localeCompare(dateA) : dateA.localeCompare(dateB);
    }});
    sorted.forEach(card => reportList.appendChild(card));
  }});
}})();
</script>
"""

    index_path = DOCS_DIR / "index.html"
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(index_front_matter + index_body)
    print(f"💾 Updated index.html with {len(all_reports_list)} reports")


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

