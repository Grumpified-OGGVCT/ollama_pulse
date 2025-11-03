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
        data = json.load(f)

        # Ensure we always return a list
        if isinstance(data, dict):
            # If it's a dict, check if it has an 'entries' key
            if 'entries' in data:
                return data['entries']
            # Otherwise, wrap it in a list
            return [data]
        elif isinstance(data, list):
            return data
        else:
            # Unknown type, return empty list
            return []


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
    print("🔄 Aggregating data from all 16 sources...")

    # Load from all sources (original 10)
    official = load_source_data("official")
    cloud = load_source_data("cloud")  # Changed from models - cloud models data
    community = load_source_data("community")
    tools = load_source_data("tools")
    bounties = load_source_data("bounties")
    nostr = load_source_data("nostr")

    # Load from new sources (6 new)
    issues = load_source_data("issues")  # Fixed - was saving to community/
    stackoverflow = load_source_data("stackoverflow")
    model_registry = load_source_data("model_registry")  # Fixed - was models/
    releases = load_source_data("releases")
    devblogs = load_source_data("devblogs")
    discord = load_source_data("discord")
    manual = load_source_data("manual")

    print(f"  📊 Official: {len(official)} entries")
    print(f"  ☁️  Cloud Models: {len(cloud)} entries")
    print(f"  📊 Community: {len(community)} entries")
    print(f"  🔧 Tools: {len(tools)} entries")
    print(f"  💰 Bounties: {len(bounties)} entries")
    print(f"  🌐 Nostr: {len(nostr)} entries")
    print(f"  ❓ Issues/PRs: {len(issues)} entries")
    print(f"  💬 Stack Overflow: {len(stackoverflow)} entries")
    print(f"  🤖 Model Registry: {len(model_registry)} entries")
    print(f"  📦 Releases: {len(releases)} entries")
    print(f"  📝 Dev Blogs: {len(devblogs)} entries")
    print(f"  🎮 Discord: {len(discord)} entries")
    print(f"  ⭐ Manual Tracking: {len(manual)} entries")

    # Combine all
    all_entries = (official + cloud + community + tools + bounties + nostr +
                   issues + stackoverflow + model_registry + releases + devblogs + discord + manual)
    
    # Deduplicate by URL (handle entries without URL gracefully)
    unique_dict = {}
    entries_without_url = []
    
    for e in all_entries:
        if 'url' in e and e['url']:
            # Use URL as deduplication key
            unique_dict[e['url']] = e
        else:
            # Entry missing URL - use title as fallback or keep as-is
            fallback_key = e.get('title', f"no_url_{len(entries_without_url)}")
            if fallback_key not in unique_dict:
                unique_dict[fallback_key] = e
                entries_without_url.append(e)
    
    unique_entries = list(unique_dict.values())
    
    if entries_without_url:
        print(f"⚠️  Warning: {len(entries_without_url)} entries missing URL field (using title as fallback)")
    
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


