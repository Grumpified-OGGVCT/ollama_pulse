#!/usr/bin/env python3
"""
Ollama Pulse - Conversational Daily Report Generation
Generates engaging, developer-focused reports with actionable insights
"""
import json
import os
from datetime import datetime
from pathlib import Path

# Import review database integration
try:
    from review_integration import ReviewIntegration
    from bounty_section import render_bounty_section
    REVIEW_DB_AVAILABLE = True
except ImportError:
    REVIEW_DB_AVAILABLE = False
    print('⚠️  Review database not available - running without historical context')

# Import enhanced model-powered report generation
try:
    from enhanced_report_generator import enhance_report_with_models
    ENHANCED_GENERATION_AVAILABLE = True
except ImportError:
    ENHANCED_GENERATION_AVAILABLE = False
    print('⚠️  Enhanced generation not available - using template mode')

# Import navigation menu system
try:
    from navigation_menu import generate_navigation_menu, generate_section_header, generate_back_to_top, get_navigation_css
    NAVIGATION_AVAILABLE = True
except ImportError:
    NAVIGATION_AVAILABLE = False


DOCS_DIR = Path("../docs")
REPORTS_DIR = DOCS_DIR / "reports"
ROOT_REPORTS_DIR = Path("../reports")  # Root level reports directory


def ensure_reports_dir():
    """Create docs/reports and root/reports directories if they don't exist"""
    DOCS_DIR.mkdir(parents=True, exist_ok=True)
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    ROOT_REPORTS_DIR.mkdir(parents=True, exist_ok=True)


def get_today_date_str():
    """Get today's date in UTC to match GitHub Actions timezone"""
    from datetime import datetime
    import pytz
    # Use UTC for consistency with GitHub Actions
    utc = pytz.UTC
    return datetime.now(utc).strftime("%Y-%m-%d")


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


def build_breakthrough_section(aggregated, model_enhancements=None):
    """Build detailed breakthrough discoveries section with LLM analysis"""
    lines = ["\n## ⚡ Breakthrough Discoveries\n"]
    
    # Check if we have LLM-analyzed breakthroughs
    if model_enhancements and model_enhancements.get('breakthrough_analyses'):
        lines.append("*Deep analysis from DeepSeek-V3.1 (81.0% GPQA) - structured intelligence at work!*\n\n")
        
        for i, item in enumerate(model_enhancements['breakthrough_analyses'], 1):
            title = item.get('title', 'Unknown')[:80]
            source = item.get('source', 'unknown')
            score = item.get('turbo_score', 0)
            url = item.get('url', '#')
            
            lines.append(f"### {i}. {title}\n\n")
            lines.append(f"**Source**: {source} | **Relevance Score**: {score:.2f} | **Analyzed by**: {item.get('analyzed_by', 'AI')}\n\n")
            
            # Use LLM analysis if available
            if 'llm_analysis' in item:
                analysis = item['llm_analysis']
                lines.append(f"**Category**: {analysis.get('category', 'Unknown')}\n\n")
                lines.append(f"**Use Case**: {analysis.get('use_case', 'N/A')}\n\n")
                lines.append(f"**Maturity**: {analysis.get('maturity', 'Unknown').title()}\n\n")
                
                if analysis.get('features'):
                    lines.append("**Key Features**:\n")
                    for feature in analysis.get('features', [])[:3]:
                        lines.append(f"- {feature}\n")
                    lines.append("\n")
                
                if analysis.get('audience'):
                    lines.append(f"**Target Audience**: {', '.join(analysis.get('audience', []))}\n\n")
            
            lines.append(f"[Explore Further →]({url})\n\n")
        
        return ''.join(lines)
    
    # Fallback to template mode
    lines.append("*The most significant ecosystem signals detected today*\n\n")

    # Get high-impact items
    high_turbo = sorted(
        [e for e in aggregated if e.get('turbo_score', 0) >= 0.7],
        key=lambda x: x.get('turbo_score', 0),
        reverse=True
    )[:5]

    if not high_turbo:
        lines.append("No breakthrough discoveries today - check back tomorrow!\n")
        return ''.join(lines)

    for i, item in enumerate(high_turbo, 1):
        title = item.get('title', 'Unknown')[:80]
        source = item.get('source', 'unknown')
        score = item.get('turbo_score', 0)
        url = item.get('url', '#')
        highlights = item.get('highlights', [])

        lines.append(f"### {i}. {title}\n\n")
        lines.append(f"**Source**: {source} | **Relevance Score**: {score:.2f}\n\n")

        # Core contribution
        if highlights:
            lines.append(f"**Core Contribution**: {highlights[0]}\n\n")

        # Why this matters (template)
        lines.append(f"**Why This Matters**: This discovery advances the Ollama ecosystem by ")
        lines.append(f"providing new capabilities and patterns that developers can build upon.\n\n")

        # Ecosystem context
        lines.append(f"**Ecosystem Context**: Builds on recent developments in the community ")
        lines.append(f"and represents convergence around important use cases.\n\n")

        # For builders
        lines.append(f"**For Builders**: You can leverage this to build more sophisticated ")
        lines.append(f"applications. [Explore Further →]({url})\n\n")

    return ''.join(lines)


def build_dev_section(aggregated, insights, model_enhancements=None):
    """Build the 'What This Means for Developers' section with LLM-generated insights or templates"""
    
    # If we have LLM-generated insights, use them!
    if model_enhancements and model_enhancements.get('developer_insights'):
        lines = ["\n## 🚀 What This Means for Developers\n"]
        lines.append("*Fresh analysis from GPT-OSS 120B - every report is unique!*\n\n")
        lines.append(model_enhancements['developer_insights'])
        lines.append("\n")
        return ''.join(lines)
    
    # Fallback to template mode
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


def generate_report_md(aggregated, insights, historical_context=None):
    """Generate EchoVein-style conversational Markdown report with navigation"""
    today = get_today_date_str()

    # Get current time in both UTC and CST
    from datetime import datetime
    import pytz
    utc = pytz.UTC
    cst = pytz.timezone('America/Chicago')
    current_time_utc = datetime.now(utc).strftime('%I:%M %p UTC')
    current_time_cst = datetime.now(cst).strftime('%I:%M %p CST')

    # Determine vein mode and tone
    vein_mode = determine_vein_mode(aggregated, insights)
    mode_name, mode_emoji, mode_description = vein_mode

    # Turbo score stats
    high_turbo = [e for e in aggregated if e.get('turbo_score', 0) >= 0.7]

    # Navigation menu
    nav_menu = """
<nav id="report-navigation" style="position: sticky; top: 0; z-index: 1000; background: linear-gradient(135deg, #8B0000 0%, #DC143C 100%); padding: 1rem; margin-bottom: 2rem; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.3);">
  <div style="font-size: 1.2rem; font-weight: bold; color: #fff; margin-bottom: 1rem;">📋 Report Navigation</div>
  <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 0.75rem;">
    <a href="#summary" style="display: block; padding: 0.75rem 1rem; background: rgba(255, 255, 255, 0.1); color: #fff; text-decoration: none; border-radius: 4px; border: 1px solid rgba(255,255,255,0.2); transition: all 0.3s;">📊 Summary</a>
    <a href="#breakthroughs" style="display: block; padding: 0.75rem 1rem; background: rgba(255, 255, 255, 0.1); color: #fff; text-decoration: none; border-radius: 4px; border: 1px solid rgba(255,255,255,0.2); transition: all 0.3s;">⚡ Breakthroughs</a>
    <a href="#official" style="display: block; padding: 0.75rem 1rem; background: rgba(255, 255, 255, 0.1); color: #fff; text-decoration: none; border-radius: 4px; border: 1px solid rgba(255,255,255,0.2); transition: all 0.3s;">🎯 Official</a>
    <a href="#community" style="display: block; padding: 0.75rem 1rem; background: rgba(255, 255, 255, 0.1); color: #fff; text-decoration: none; border-radius: 4px; border: 1px solid rgba(255,255,255,0.2); transition: all 0.3s;">🛠️ Community</a>
    <a href="#patterns" style="display: block; padding: 0.75rem 1rem; background: rgba(255, 255, 255, 0.1); color: #fff; text-decoration: none; border-radius: 4px; border: 1px solid rgba(255,255,255,0.2); transition: all 0.3s;">📈 Patterns</a>
    <a href="#prophecies" style="display: block; padding: 0.75rem 1rem; background: rgba(255, 255, 255, 0.1); color: #fff; text-decoration: none; border-radius: 4px; border: 1px solid rgba(255,255,255,0.2); transition: all 0.3s;">🔔 Prophecies</a>
    <a href="#developers" style="display: block; padding: 0.75rem 1rem; background: rgba(255, 255, 255, 0.1); color: #fff; text-decoration: none; border-radius: 4px; border: 1px solid rgba(255,255,255,0.2); transition: all 0.3s;">🚀 Developers</a>
    <a href="#bounties" style="display: block; padding: 0.75rem 1rem; background: rgba(255, 255, 255, 0.1); color: #fff; text-decoration: none; border-radius: 4px; border: 1px solid rgba(255,255,255,0.2); transition: all 0.3s;">💰 Bounties</a>
  </div>
</nav>

<script>
document.addEventListener('DOMContentLoaded', function() {
  const links = document.querySelectorAll('a[href^="#"]');
  links.forEach(link => {
    link.addEventListener('click', function(e) {
      e.preventDefault();
      const target = document.querySelector(this.getAttribute('href'));
      if (target) target.scrollIntoView({ behavior: 'smooth' });
    });
  });
});
</script>
"""

    report = f"""{nav_menu}

# {mode_emoji} Ollama Pulse – {today}
## {mode_description}

**Generated**: {current_time_utc} ({current_time_cst}) on {today}

*EchoVein here, your vein-tapping oracle excavating Ollama's hidden arteries...*

**Today's Vibe**: {mode_name.replace('_', ' ').title()} — The ecosystem is {"pulsing with fresh blood" if len(aggregated) > 20 else "in steady throb mode"}.

---

<div id="summary"></div>

## 🔬 Ecosystem Intelligence Summary

**Today's Snapshot**: Comprehensive analysis of the Ollama ecosystem across 10 data sources.

### Key Metrics

- **Total Items Analyzed**: {len(aggregated)} discoveries tracked across all sources
- **High-Impact Discoveries**: {len(high_turbo)} items with significant ecosystem relevance (score ≥0.7)
- **Emerging Patterns**: {insights.get('stats', {}).get('total_patterns', 0)} distinct trend clusters identified
- **Ecosystem Implications**: {insights.get('stats', {}).get('total_inferences', 0)} actionable insights drawn
- **Analysis Timestamp**: {datetime.now().strftime('%Y-%m-%d %H:%M UTC')}

### What This Means

The ecosystem shows {"strong convergence around key areas" if len(high_turbo) >= 3 else "steady development across multiple fronts"}. {len(high_turbo)} high-impact items suggest {"accelerating development velocity" if len(high_turbo) >= 3 else "consistent innovation"} in these areas.

**Key Insight**: When multiple independent developers converge on similar problems, it signals important directions. Today's patterns suggest the ecosystem is moving toward {"production-ready solutions" if len(high_turbo) >= 3 else "new capabilities"}.

---

## ⚡ Breakthrough Discoveries

*The most significant ecosystem signals detected today*

"""

    # Add breakthrough section with LLM analysis
    model_enhancements = historical_context.get('model_enhancements', {})
    
    report += """
<div id="breakthroughs"></div>

"""
    report += build_breakthrough_section(aggregated, model_enhancements)

    report += """
<div style="text-align: right; margin: 2rem 0;">
  <a href="#report-navigation" style="padding: 0.5rem 1.5rem; background: linear-gradient(135deg, #8B0000 0%, #DC143C 100%); color: #fff; text-decoration: none; border-radius: 4px; font-weight: bold;">⬆️ Back to Top</a>
</div>

---

<div id="official"></div>

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

    report += """
<div style="text-align: right; margin: 2rem 0;">
  <a href="#report-navigation" style="padding: 0.5rem 1.5rem; background: linear-gradient(135deg, #8B0000 0%, #DC143C 100%); color: #fff; text-decoration: none; border-radius: 4px; font-weight: bold;">⬆️ Back to Top</a>
</div>

---

<div id="community"></div>

## 🛠️ Community Veins: What Developers Are Excavating

"""

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

    report += """
<div style="text-align: right; margin: 2rem 0;">
  <a href="#report-navigation" style="padding: 0.5rem 1.5rem; background: linear-gradient(135deg, #8B0000 0%, #DC143C 100%); color: #fff; text-decoration: none; border-radius: 4px; font-weight: bold;">⬆️ Back to Top</a>
</div>

---

<div id="patterns"></div>

## 📈 Vein Pattern Mapping: Arteries & Clusters

"""

    patterns = insights.get('patterns', {})
    if patterns:
        report += "Veins are clustering — here's the arterial map:\n\n"
        for pattern_name, items in patterns.items():
            vein_headline = generate_vein_headline(vein_mode, pattern_name, len(items))
            items_count = len(items)

            # Determine signal strength
            if items_count >= 5:
                signal_level = "HIGH"
                signal_emoji = "🔥"
            elif items_count >= 3:
                signal_level = "MEDIUM"
                signal_emoji = "⚡"
            else:
                signal_level = "LOW"
                signal_emoji = "💫"

            report += f"### {signal_emoji} {vein_headline}\n\n"
            report += f"**Signal Strength**: {items_count} items detected\n\n"

            # Analysis with convergence
            report += f"**Analysis**: When {items_count} independent developers converge on "
            report += f"similar patterns, it signals an important direction. This clustering "
            report += f"suggests this area has reached a maturity level where meaningful advances are possible.\n\n"

            # Items list
            report += "**Items in this cluster**:\n"
            for item in items[:5]:
                title = item.get('title', 'N/A')
                url = item.get('url', '#')
                report += f"- [{title}]({url})\n"

            if items_count > 5:
                report += f"- ... and {items_count - 5} more\n"

            # Add convergence level and confidence
            report += f"\n**Convergence Level**: {signal_level}\n"
            report += f"**Confidence**: {'HIGH' if items_count >= 5 else 'MEDIUM' if items_count >= 3 else 'MEDIUM-LOW'}\n\n"

            # Add vein commentary
            if items_count >= 5:
                report += f"💉 **EchoVein's Take**: This artery's *bulging* — {items_count} strikes means it's no fluke. "
                report += f"Watch this space for 2x explosion potential.\n\n"
            elif items_count >= 3:
                report += f"⚡ **EchoVein's Take**: Steady throb detected — {items_count} hits suggests it's gaining flow.\n\n"
            else:
                report += "\n"
    else:
        report += "*No major vein clusters today — but the deep throb continues.*\n"

    report += """
<div style="text-align: right; margin: 2rem 0;">
  <a href="#report-navigation" style="padding: 0.5rem 1.5rem; background: linear-gradient(135deg, #8B0000 0%, #DC143C 100%); color: #fff; text-decoration: none; border-radius: 4px; font-weight: bold;">⬆️ Back to Top</a>
</div>

---

<div id="prophecies"></div>

## 🔔 Prophetic Veins: What This Means

"""

    # Use LLM-generated prophecies if available (RAG-powered by Kimi-K2!)
    llm_prophecies = model_enhancements.get('prophecies', []) if model_enhancements else []
    
    if llm_prophecies:
        report += "EchoVein's RAG-powered prophecies — *historical patterns + fresh intelligence*:\n\n"
        report += "*Powered by Kimi-K2:1T (66.1% Tau-Bench) + ChromaDB vector memory*\n\n"
        
        for inf in llm_prophecies:
            pattern = inf.get('pattern', 'N/A')
            observation = inf.get('observation', 'N/A')
            inference = inf.get('inference', 'N/A')
            confidence = inf.get('confidence', 'medium')
            rag_enabled = inf.get('rag_enabled', False)
            
            # Vein-style emoji
            emoji = "🩸" if confidence == "high" else "⚡" if confidence == "medium" else "💡"
            clean_pattern = pattern.replace('_', ' ').title()
            
            report += f"{emoji} **Vein Oracle: {clean_pattern}**\n\n"
            report += f"- **Surface Reading**: {observation}\n"
            report += f"- **Vein Prophecy**: {inference}\n"
            report += f"- **Confidence Vein**: {confidence.upper()} ({emoji})\n"
            if rag_enabled:
                report += f"- **RAG Context**: ✅ Historical patterns analyzed\n"
            
            # Add sly commentary based on confidence
            if confidence == "high":
                report += f"- **EchoVein's Take**: This vein's *throbbing* — trust the flow.\n\n"
            elif confidence == "medium":
                report += f"- **EchoVein's Take**: Promising artery, but watch for clots.\n\n"
            else:
                report += f"- **EchoVein's Take**: Phantom vein? Could be fool's gold.\n\n"
    else:
        # Fallback to template-based inferences
        inferences = insights.get('inferences', [])
        if inferences:
            report += "EchoVein's prophecies — *calibrated speculation with vein-backed data*:\n\n"
            for inf in inferences:
                pattern = inf.get('pattern', 'N/A')
                observation = inf.get('observation', 'N/A')
                inference = inf.get('inference', 'N/A')
                confidence = inf.get('confidence', 'medium')
                
                emoji = "🩸" if confidence == "high" else "⚡" if confidence == "medium" else "💡"
                clean_pattern = pattern.replace('_', ' ').title()
                
                report += f"{emoji} **Vein Oracle: {clean_pattern}**\n\n"
                report += f"- **Surface Reading**: {observation}\n"
                report += f"- **Vein Prophecy**: {inference}\n"
                report += f"- **Confidence Vein**: {confidence.upper()} ({emoji})\n"
                
                if confidence == "high":
                    report += f"- **EchoVein's Take**: This vein's *throbbing* — trust the flow.\n\n"
                elif confidence == "medium":
                    report += f"- **EchoVein's Take**: Promising artery, but watch for clots.\n\n"
                else:
                    report += f"- **EchoVein's Take**: Phantom vein? Could be fool's gold.\n\n"
        else:
            report += "*No major prophecies today — but silence speaks in veins.*\n"

    # Add the developer-focused section with LLM-generated insights
    report += """
<div style="text-align: right; margin: 2rem 0;">
  <a href="#report-navigation" style="padding: 0.5rem 1.5rem; background: linear-gradient(135deg, #8B0000 0%, #DC143C 100%); color: #fff; text-decoration: none; border-radius: 4px; font-weight: bold;">⬆️ Back to Top</a>
</div>

---

<div id="developers"></div>

"""
    report += build_dev_section(aggregated, insights, model_enhancements)

    # Add bounty section if available
    report += """
<div style="text-align: right; margin: 2rem 0;">
  <a href="#report-navigation" style="padding: 0.5rem 1.5rem; background: linear-gradient(135deg, #8B0000 0%, #DC143C 100%); color: #fff; text-decoration: none; border-radius: 4px; font-weight: bold;">⬆️ Back to Top</a>
</div>

---

<div id="bounties"></div>

"""
    try:
        bounty_content = render_bounty_section()
        if bounty_content and "No bounty pulses" not in bounty_content:
            report += bounty_content
    except Exception as e:
        print(f"⚠️  Bounty section error: {e}")

    # Add "What to Watch" section
    report += "\n---\n\n## 👀 What to Watch\n\n"
    report += "**Projects to Track for Impact**:\n"

    # Get high-scoring items to watch
    watch_items = sorted(
        [e for e in aggregated if e.get('turbo_score', 0) >= 0.5],
        key=lambda x: x.get('turbo_score', 0),
        reverse=True
    )[:3]

    for item in watch_items:
        title = item.get('title', 'Unknown')[:60]
        report += f"- {title} (watch for adoption metrics)\n"

    report += "\n**Emerging Trends to Monitor**:\n"

    # Extract top patterns as trends
    patterns = insights.get('patterns', {})
    for pattern_name in list(patterns.keys())[:3]:
        clean_name = pattern_name.replace('_', ' ').title()
        report += f"- **{clean_name}**: Watch for convergence and standardization\n"

    report += "\n**Confidence Levels**:\n"
    report += f"- High-Impact Items: HIGH - Strong convergence signal\n"
    report += f"- Emerging Patterns: MEDIUM-HIGH - Patterns forming\n"
    report += f"- Speculative Trends: MEDIUM - Monitor for confirmation\n\n"

    # Add "Returning Projects" section if RAG context available
    if historical_context and 'returning_projects' in historical_context:
        returning = historical_context['returning_projects']
        if returning:
            report += "\n---\n\n## 🔄 Returning to the Veins: Projects We've Tracked Before\n\n"
            report += "*EchoVein remembers... these projects pulsed through our veins before, and they're back.*\n\n"

            for project in returning[:5]:  # Show top 5
                name = project.get('project_name', 'Unknown')
                last_seen = project.get('last_seen', 'Unknown')
                total_mentions = project.get('total_mentions', 0)
                avg_score = project.get('avg_turbo_score', 0)
                trend = project.get('trend_direction', 'STABLE')
                highlights = project.get('last_highlights', 'No highlights available')

                trend_emoji = "📈" if trend == "UP" else "📉" if trend == "DOWN" else "➡️"
                score_emoji = "🔥" if avg_score >= 0.7 else "⚡" if avg_score >= 0.5 else "💡"

                report += f"### {trend_emoji} {name}\n\n"
                report += f"**Last Seen**: {last_seen} | **Total Mentions**: {total_mentions} | **Avg Score**: {score_emoji} {avg_score:.2f}\n\n"
                report += f"**Previous Highlights**: {highlights}\n\n"
                report += f"**What's New**: This project is back in the ecosystem pulse. Check the tools/discoveries sections above for latest updates.\n\n"

            report += "*The veins remember. These projects have proven staying power.* 🩸\n\n"

    # Add Nostr section
    report += "\n---\n\n## 🌐 Nostr Veins: Decentralized Pulse\n\n"
    today = get_today_date_str()
    nostr_file = f"../data/nostr/{today}.json"
    if os.path.exists(nostr_file):
        with open(nostr_file, 'r', encoding='utf-8') as f:
            nostr_data = json.load(f)
            posts = nostr_data.get('posts', []) if isinstance(nostr_data, dict) else nostr_data
            if posts:
                report += f"**{len(posts)} Nostr articles** detected on the decentralized network:\n\n"
                report += "| Article | Author | Turbo Score | Read |\n"
                report += "|---------|--------|-------------|------|\n"
                for item in posts[:5]:
                    title = item.get('title', 'Untitled')[:50]
                    author_npub = item.get('author_npub', 'Unknown')[:20]
                    score = item.get('turbo_score', 0)
                    score_emoji = "🔥" if score >= 0.7 else "⚡" if score >= 0.5 else "💡"
                    url = item.get('url', '#')
                    report += f"| {title} | {author_npub} | {score_emoji} {score:.1f} | [📖]({url}) |\n"
                report += f"\n*This report auto-published to Nostr via NIP-23 at 4 PM CT*\n"
            else:
                report += "*No Nostr veins detected today — but the network never sleeps.*\n"
    else:
        report += "*No Nostr veins detected today — but the network never sleeps.*\n"

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

    # Add Lingo Legend
    report += "\n---\n\n## 🩸 EchoVein Lingo Legend\n\n"
    report += "Decode the vein-tapping oracle's unique terminology:\n\n"
    report += "| Term | Meaning |\n"
    report += "|------|----------|\n"
    report += "| **Vein** | A signal, trend, or data point |\n"
    report += "| **Ore** | Raw data items collected |\n"
    report += "| **High-Purity Vein** | Turbo-relevant item (score ≥0.7) |\n"
    report += "| **Vein Rush** | High-density pattern surge |\n"
    report += "| **Artery Audit** | Steady maintenance updates |\n"
    report += "| **Fork Phantom** | Niche experimental projects |\n"
    report += "| **Deep Vein Throb** | Slow-day aggregated trends |\n"
    report += "| **Vein Bulging** | Emerging pattern (≥5 items) |\n"
    report += "| **Vein Oracle** | Prophetic inference |\n"
    report += "| **Vein Prophecy** | Predicted trend direction |\n"
    report += "| **Confidence Vein** | HIGH (🩸), MEDIUM (⚡), LOW (🤖) |\n"
    report += "| **Vein Yield** | Quality ratio metric |\n"
    report += "| **Vein-Tapping** | Mining/extracting insights |\n"
    report += "| **Artery** | Major trend pathway |\n"
    report += "| **Vein Strike** | Significant discovery |\n"
    report += "| **Throbbing Vein** | High-confidence signal |\n"
    report += "| **Vein Map** | Daily report structure |\n"
    report += "| **Dig In** | Link to source/details |\n\n"

    # Add enhanced donation section with interactive elements
    report += "\n---\n\n## 💰 Support the Vein Network\n\n"
    report += "If Ollama Pulse helps you stay ahead of the ecosystem, consider supporting development:\n\n"

    # Ko-fi section with properly sized QR code
    report += "### ☕ Ko-fi (Fiat/Card)\n\n"
    report += "**[💝 Tip on Ko-fi](https://ko-fi.com/grumpified)** | Scan QR Code Below\n\n"
    report += '<a href="https://ko-fi.com/grumpified"><img src="../assets/KofiTipQR_Code_GrumpiFied.png" alt="Ko-fi QR Code" width="200" height="200" /></a>\n\n'
    report += "*Click the QR code or button above to support via Ko-fi*\n\n"

    # Lightning Network section with both wallets and QR codes
    report += "### ⚡ Lightning Network (Bitcoin)\n\n"
    report += "**Send Sats via Lightning:**\n\n"
    report += "- [🔗 gossamerfalling850577@getalby.com](lightning:gossamerfalling850577@getalby.com)\n"
    report += "- [🔗 havenhelpful360120@getalby.com](lightning:havenhelpful360120@getalby.com)\n\n"
    report += "**Scan QR Codes:**\n\n"
    report += '<a href="lightning:gossamerfalling850577@getalby.com"><img src="../assets/lightning_wallet_QR_Code.png" alt="Lightning Wallet 1 QR Code" width="200" height="200" /></a> '
    report += '<a href="lightning:havenhelpful360120@getalby.com"><img src="../assets/lightning_wallet_QR_Code_2.png" alt="Lightning Wallet 2 QR Code" width="200" height="200" /></a>\n\n'

    # Why support section
    report += "### 🎯 Why Support?\n\n"
    report += "- **Keeps the project maintained and updated** — Daily ingestion, hourly pattern detection\n"
    report += "- **Funds new data source integrations** — Expanding from 10 to 15+ sources\n"
    report += "- **Supports open-source AI tooling** — All donations go to ecosystem projects\n"
    report += "- **Enables Nostr decentralization** — Publishing to 8+ relays, NIP-23 long-form content\n\n"

    report += "*All donations support open-source AI tooling and ecosystem monitoring.*\n\n"

    # Ko-fi widget script
    report += "<!-- Ko-fi Floating Widget -->\n"
    report += "<script src='https://storage.ko-fi.com/cdn/scripts/overlay-widget.js'></script>\n"
    report += "<script>\n"
    report += "  kofiWidgetOverlay.draw('grumpified', {\n"
    report += "    'type': 'floating-chat',\n"
    report += "    'floating-chat.donateButton.text': 'Tip EchoVein',\n"
    report += "    'floating-chat.donateButton.background-color': '#8B0000',\n"
    report += "    'floating-chat.donateButton.text-color': '#fff'\n"
    report += "  });\n"
    report += "</script>\n\n"

    # Add viral hashtags for social sharing
    report += "\n---\n\n## 🔖 Share This Report\n\n"
    viral_hashtags = [
        "#AI", "#Ollama", "#LocalLLM", "#OpenSource", "#MachineLearning",
        "#DevTools", "#Innovation", "#TechNews", "#AIResearch", "#Developers"
    ]
    report += f"**Hashtags**: {' '.join(viral_hashtags)}\n\n"
    report += f"**Share on**: [Twitter](https://twitter.com/intent/tweet?text=Check%20out%20Ollama%20Pulse%20{today}%20Report&url=https://grumpified-oggvct.github.io/ollama_pulse/reports/pulse-{today}&hashtags={','.join([h.replace('#', '') for h in viral_hashtags[:5]])}) | "
    report += f"[LinkedIn](https://www.linkedin.com/sharing/share-offsite/?url=https://grumpified-oggvct.github.io/ollama_pulse/reports/pulse-{today}) | "
    report += f"[Reddit](https://reddit.com/submit?url=https://grumpified-oggvct.github.io/ollama_pulse/reports/pulse-{today}&title=Ollama%20Pulse%20{today}%20Report)\n\n"

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
    """Save the report to docs/reports with Jekyll front matter and comprehensive SEO"""
    ensure_reports_dir()
    today = get_today_date_str()

    # Add Jekyll front matter with available reports metadata
    all_reports = get_all_reports()
    # Add current report if not in list
    if f"pulse-{today}" not in all_reports:
        all_reports.insert(0, f"pulse-{today}")

    reports_json = json.dumps(all_reports)

    # SEO Keywords and Hashtags
    seo_keywords = [
        "Ollama ecosystem",
        "AI development",
        "local LLM",
        "machine learning tools",
        "open source AI",
        "Ollama Turbo",
        "Ollama Cloud",
        "AI innovation",
        "developer tools",
        "AI trends"
    ]

    viral_hashtags = [
        "AI", "Ollama", "LocalLLM", "OpenSource", "MachineLearning",
        "DevTools", "Innovation", "TechNews", "AIResearch", "Developers"
    ]

    # Generate description from report content (first 200 chars)
    description_text = report_md.split('\n')[0:5]
    description = ' '.join([line.strip() for line in description_text if line.strip() and not line.startswith('#')])[:200]
    if len(description) > 197:
        description = description[:197] + "..."

    # Comprehensive SEO meta tags
    seo_meta_tags = f"""
<!-- Primary Meta Tags -->
<meta name="title" content="Ollama Pulse - {today} Ecosystem Report">
<meta name="description" content="{description}">
<meta name="keywords" content="{', '.join(seo_keywords)}">
<meta name="author" content="EchoVein Oracle">
<meta name="robots" content="index, follow">
<meta name="language" content="English">
<meta name="revisit-after" content="1 days">

<!-- Open Graph / Facebook -->
<meta property="og:type" content="article">
<meta property="og:url" content="https://grumpified-oggvct.github.io/ollama_pulse/reports/pulse-{today}">
<meta property="og:title" content="Ollama Pulse - {today} Ecosystem Intelligence">
<meta property="og:description" content="{description}">
<meta property="og:image" content="https://grumpified-oggvct.github.io/ollama_pulse/assets/banner.png">
<meta property="og:site_name" content="Ollama Pulse">
<meta property="article:published_time" content="{today}T00:00:00Z">
<meta property="article:author" content="EchoVein Oracle">
<meta property="article:section" content="Technology">
<meta property="article:tag" content="{', '.join(viral_hashtags[:5])}">

<!-- Twitter Card -->
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:url" content="https://grumpified-oggvct.github.io/ollama_pulse/reports/pulse-{today}">
<meta name="twitter:title" content="Ollama Pulse - {today} Ecosystem Intelligence">
<meta name="twitter:description" content="{description}">
<meta name="twitter:image" content="https://grumpified-oggvct.github.io/ollama_pulse/assets/banner.png">
<meta name="twitter:creator" content="@GrumpifiedOGGVCT">

<!-- Canonical URL -->
<link rel="canonical" href="https://grumpified-oggvct.github.io/ollama_pulse/reports/pulse-{today}">

<!-- JSON-LD Structured Data -->
<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "Ollama Pulse - {today} Ecosystem Intelligence",
  "description": "{description}",
  "image": "https://grumpified-oggvct.github.io/ollama_pulse/assets/banner.png",
  "author": {{
    "@type": "Person",
    "name": "EchoVein Oracle"
  }},
  "publisher": {{
    "@type": "Organization",
    "name": "Ollama Pulse",
    "logo": {{
      "@type": "ImageObject",
      "url": "https://grumpified-oggvct.github.io/ollama_pulse/assets/banner.png"
    }}
  }},
  "datePublished": "{today}T00:00:00Z",
  "dateModified": "{today}T00:00:00Z",
  "mainEntityOfPage": {{
    "@type": "WebPage",
    "@id": "https://grumpified-oggvct.github.io/ollama_pulse/reports/pulse-{today}"
  }},
  "keywords": "{', '.join(seo_keywords)}"
}}
</script>
"""

    md_front_matter = f"""---
layout: default
title: Pulse {today}
---

<meta name="available-reports" content='{reports_json}'>
{seo_meta_tags}

"""

    # Save Markdown version to docs/reports (PRIMARY location for GitHub Pages)
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
    
    # Get current time in CST for latest report
    from datetime import datetime
    import pytz
    cst = pytz.timezone('America/Chicago')
    current_time_cst = datetime.now(cst).strftime('%I:%M %p CST')

    for idx, report_name in enumerate(all_reports_list):
        report_date = report_name.replace('pulse-', '')
        is_latest = idx == 0
        badge = ' <span style="background: #60a5fa; color: #0f172a; padding: 2px 8px; border-radius: 4px; font-size: 12px; font-weight: bold;">LATEST</span>' if is_latest else ''

        # Show time for latest report, just date for others
        generated_text = f"{current_time_cst} on {report_date}" if is_latest else report_date

        reports_html += f"""  <div class="card">
    <h3>{'📡 ' if is_latest else ''}Report: {report_date}{badge}</h3>
    <p>Ollama ecosystem discoveries from {report_date}</p>
    <p class="meta">Generated: {generated_text}</p>
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
    print("🚀 Starting ENHANCED conversational report generation...")
    print("🤖 Multi-model pipeline: DeepSeek → GPT-OSS → Kimi-K2 → GLM-4.6")

    # Initialize review integration if available
    integration = None
    if REVIEW_DB_AVAILABLE:
        try:
            integration = ReviewIntegration()
            print("✅ Review database integration enabled")
        except Exception as e:
            print(f"⚠️  Review database error: {e}")

    # Initialize RAG engine if available (NOW CLOUD-COMPATIBLE!)
    rag_engine = None
    try:
        from langchain_adaptive import AdaptiveProphecyEngine
        rag_engine = AdaptiveProphecyEngine()  # Uses cloud by default now
        if rag_engine.initialize():
            print("✅ RAG engine initialized with Ollama Cloud + ChromaDB vectors")
        else:
            rag_engine = None
    except Exception as e:
        print(f"⚠️  RAG engine unavailable: {e}")

    aggregated, insights = load_data()

    if not aggregated and not insights:
        print("⚠️  No data available to generate report")
        return

    # Get historical context
    historical_context = {}
    if integration:
        try:
            historical_context = integration.get_historical_context_for_items(aggregated)
            print(f"📊 Retrieved historical context for {len(historical_context)} items")
        except Exception as e:
            print(f"⚠️  Error getting historical context: {e}")

    # Get returning projects using RAG
    if rag_engine:
        try:
            # Extract project names from aggregated data
            current_projects = [item.get('title', '') for item in aggregated if item.get('title')]
            returning_projects = rag_engine.get_returning_projects(current_projects, days_back=7)

            if returning_projects:
                historical_context['returning_projects'] = returning_projects
                print(f"🔄 Found {len(returning_projects)} returning projects")
        except Exception as e:
            print(f"⚠️  Error finding returning projects: {e}")

    # NEW: Run multi-model enhancement pipeline
    model_enhancements = {}
    if ENHANCED_GENERATION_AVAILABLE and os.getenv("OLLAMA_API_KEY"):
        try:
            import asyncio
            print("\n🤖 Activating multi-model intelligence pipeline...")
            model_enhancements = asyncio.run(
                enhance_report_with_models(aggregated, insights, rag_engine)
            )
            print("✅ Model enhancements complete!")
            historical_context['model_enhancements'] = model_enhancements
        except Exception as e:
            print(f"⚠️  Model enhancement error: {e}")
            print("   Falling back to template mode...")

    # Cleanup RAG engine before writing to database
    if rag_engine:
        try:
            rag_engine.cleanup()
            import time
            time.sleep(0.2)  # Brief delay to ensure cleanup completes
        except Exception as e:
            print(f"⚠️  RAG cleanup warning: {e}")

    report_md = generate_report_md(aggregated, insights, historical_context)
    save_report(report_md)
    
    # Store new reviews
    if integration:
        try:
            today = get_today_date_str()
            stored_count = 0
            for item in aggregated:
                review = integration.process_ollama_pulse_item(
                    item=item,
                    review_date=today,
                    persona="EchoVein"
                )
                integration.db.add_review(review)
                stored_count += 1
            print(f"💾 Stored {stored_count} reviews in database")
        except Exception as e:
            print(f"⚠️  Error storing reviews: {e}")
    
    print("✅ Report generation complete!")


if __name__ == "__main__":
    main()


