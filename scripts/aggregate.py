#!/usr/bin/env python3
"""
Ollama Pulse - Data Aggregation
Merges daily JSONs from all sources into unified view
"""
import json
import os
from datetime import datetime
from pathlib import Path


def ensure_data_dir():
    """Create data/aggregated directory if it doesn't exist"""
    Path("data/aggregated").mkdir(parents=True, exist_ok=True)


def get_today_filename():
    """Get filename for today's aggregated data"""
    today = datetime.now().strftime("%Y-%m-%d")
    return f"data/aggregated/{today}.json"


def load_source_data(source_dir):
    """Load today's data from a source directory"""
    today = datetime.now().strftime("%Y-%m-%d")
    filename = f"data/{source_dir}/{today}.json"
    
    if not os.path.exists(filename):
        return []
    
    with open(filename, 'r') as f:
        return json.load(f)


def score_turbo_relevance(entry):
    """
    Score entry relevance to Ollama Turbo Cloud (0-1)
    Higher scores = more relevant to Turbo/Cloud focus
    """
    text = (entry.get('title', '') + ' ' + 
            entry.get('summary', '') + ' ' + 
            ' '.join(entry.get('highlights', []))).lower()
    
    score = 0.0
    
    # Core Turbo/Cloud keywords (high weight)
    if 'turbo' in text:
        score += 0.3
    if 'cloud' in text:
        score += 0.3
    if '-cloud' in text:  # Model suffix
        score += 0.2
    
    # Related features
    if any(word in text for word in ['voice', 'stt', 'tts', 'speech']):
        score += 0.15
    if any(word in text for word in ['multimodal', 'vision', 'image']):
        score += 0.15
    if any(word in text for word in ['api', 'integration', 'service']):
        score += 0.1
    
    # Model mentions
    if any(model in text for model in ['gpt-oss', 'qwen3', 'glm', 'mixtral']):
        score += 0.1
    
    return min(score, 1.0)


def filter_by_relevance(entries, threshold=0.3):
    """Filter entries by Turbo relevance score"""
    scored_entries = []
    for entry in entries:
        score = score_turbo_relevance(entry)
        if score >= threshold:
            entry['turbo_score'] = round(score, 2)
            scored_entries.append(entry)
    
    return scored_entries


def aggregate_data():
    """Aggregate data from all sources with Turbo-centric filtering"""
    print("🔄 Aggregating data from all sources...")
    
    # Load from all sources
    official = load_source_data("official")
    community = load_source_data("community")
    tools = load_source_data("tools")`n    bounties = load_source_data("bounties")
    
    print(f"  📊 Official: {len(official)} entries")
    print(f"  📊 Community: {len(community)} entries")
    print(f"  📊 Tools: {len(tools)} entries")`n    print(f"  💰 Bounties: {len(bounties)} entries")
    
    # Combine all
    all_entries = official + community + tools + bounties + nostr
    
    # Deduplicate by URL
    unique_entries = list({e['url']: e for e in all_entries}.values())
    
    # Apply Turbo-centric filtering
    print("🎯 Applying Turbo-centric relevance filtering...")
    filtered_entries = filter_by_relevance(unique_entries, threshold=0.3)
    
    # Sort by relevance score, then date
    sorted_entries = sorted(
        filtered_entries,
        key=lambda x: (x.get('turbo_score', 0), x.get('date', '')),
        reverse=True
    )
    
    print(f"✅ Aggregated {len(sorted_entries)} high-relevance entries (from {len(unique_entries)} total)")
    return sorted_entries, len(unique_entries)


def save_aggregated(entries):
    """Save aggregated data"""
    if not entries:
        print("⚠️  No data to save")
        return
    
    filename = get_today_filename()
    
    with open(filename, 'w') as f:
        json.dump(entries, f, indent=2)
    
    print(f"💾 Saved aggregated data to {filename}")


def save_yield_metrics(filtered_count, total_count):
    """Save daily yield metrics for monitoring"""
    today = datetime.now().strftime("%Y-%m-%d")
    yield_filename = f"data/insights/{today}_yield.json"
    
    # Ensure directory exists
    Path("data/insights").mkdir(parents=True, exist_ok=True)
    
    yield_data = {
        "date": datetime.now().isoformat(),
        "total_items": total_count,
        "high_relevance_items": filtered_count,
        "turbo_sources": filtered_count,
        "filter_threshold": 0.3,
        "quality_ratio": round(filtered_count / max(total_count, 1), 2)
    }
    
    with open(yield_filename, 'w') as f:
        json.dump(yield_data, f, indent=2)
    
    print(f"📊 Saved yield metrics to {yield_filename}")


def main():
    """Main aggregation function"""
    print("🚀 Starting data aggregation...")
    ensure_data_dir()
    
    entries, total_count = aggregate_data()
    save_aggregated(entries)
    save_yield_metrics(len(entries), total_count)
    
    print("✅ Data aggregation complete!")


if __name__ == "__main__":
    main()


