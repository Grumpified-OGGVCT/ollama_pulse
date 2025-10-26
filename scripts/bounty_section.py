#!/usr/bin/env python3
import json, os, sys
from datetime import datetime

def load_bounties():
    today = datetime.now().strftime("%Y-%m-%d")
    bounty_file = f"data/bounties/{today}.json"
    if not os.path.exists(bounty_file):
        return []
    with open(bounty_file, 'r', encoding='utf-8') as f:
        return json.load(f)

def score_bounty_turbo_relevance(bounty):
    text = (bounty.get('title', '') + ' ' + bounty.get('summary', '')).lower()
    score = 0.0
    if 'ollama' in text:
        score += 0.4
    if 'turbo' in text or 'cloud' in text:
        score += 0.3
    if 'llm' in text or 'ai' in text:
        score += 0.2
    return min(score, 1.0)

def format_turbo_score(score):
    if score >= 0.8:
        return "FIRE 0.8+"
    elif score >= 0.6:
        return "BOLT 0.6+"
    elif score >= 0.4:
        return "STAR 0.4+"
    return "SPARK <0.4"

def render_bounty_section():
    bounties = load_bounties()
    
    lines = []
    lines.append("\n## BOUNTY VEINS: Reward-Pumping Opportunities\n\n")
    
    if not bounties:
        lines.append("No bounty pulses detected today. Check back tomorrow!\n")
        return ''.join(lines)
    
    for b in bounties:
        b['turbo_score'] = score_bounty_turbo_relevance(b)
    bounties.sort(key=lambda b: b['turbo_score'], reverse=True)
    
    lines.append("| Bounty | Source | Reward | Summary | Turbo Score |\n")
    lines.append("|--------|--------|--------|---------|-------------|\n")
    
    for b in bounties[:10]:
        title = b.get('title', 'Unknown')[:50]
        source = b.get('source', 'unknown').replace('_', ' ').title()
        reward = b.get('reward', 'TBD')
        summary = b.get('summary', '')[:60]
        score = format_turbo_score(b['turbo_score'])
        url = b.get('url', '#')
        lines.append(f"| [{title}]({url}) | {source} | {reward} | {summary} | {score} |\n")
    
    lines.append(f"\nBOUNTY PULSE: {len(bounties)} opportunities detected.\n")
    if len(bounties) >= 5:
        lines.append("**Prophecy**: Strong flow—expect 2x contributor surge. **Confidence: HIGH**\n")
    
    return ''.join(lines)

if __name__ == "__main__":
    sys.stdout.reconfigure(encoding='utf-8')
    print(render_bounty_section())
