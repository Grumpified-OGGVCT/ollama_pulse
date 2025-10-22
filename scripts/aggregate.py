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


def aggregate_data():
    """Aggregate data from all sources"""
    print("🔄 Aggregating data from all sources...")
    
    # Load from all sources
    official = load_source_data("official")
    community = load_source_data("community")
    tools = load_source_data("tools")
    
    print(f"  📊 Official: {len(official)} entries")
    print(f"  📊 Community: {len(community)} entries")
    print(f"  📊 Tools: {len(tools)} entries")
    
    # Combine all
    all_entries = official + community + tools
    
    # Deduplicate by URL
    unique_entries = {e['url']: e for e in all_entries}.values()
    
    # Sort by date (newest first)
    sorted_entries = sorted(
        unique_entries,
        key=lambda x: x.get('date', ''),
        reverse=True
    )
    
    print(f"✅ Aggregated {len(sorted_entries)} unique entries")
    return sorted_entries


def save_aggregated(entries):
    """Save aggregated data"""
    if not entries:
        print("⚠️  No data to save")
        return
    
    filename = get_today_filename()
    
    with open(filename, 'w') as f:
        json.dump(entries, f, indent=2)
    
    print(f"💾 Saved aggregated data to {filename}")


def main():
    """Main aggregation function"""
    print("🚀 Starting data aggregation...")
    ensure_data_dir()
    
    entries = aggregate_data()
    save_aggregated(entries)
    
    print("✅ Data aggregation complete!")


if __name__ == "__main__":
    main()

