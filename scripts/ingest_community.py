#!/usr/bin/env python3
"""
Ollama Pulse - Community Sources Ingestion
Polls X/Twitter, Reddit, Product Hunt for community activity
"""
import json
import os
from datetime import datetime
from pathlib import Path

import requests


def ensure_data_dir():
    """Create data/community directory if it doesn't exist"""
    Path("data/community").mkdir(parents=True, exist_ok=True)


def get_today_filename():
    """Get filename for today's data"""
    today = datetime.now().strftime("%Y-%m-%d")
    return f"data/community/{today}.json"


def fetch_reddit():
    """Fetch Reddit r/ollama posts (using public JSON API)"""
    print("📡 Fetching Reddit r/ollama...")
    try:
        response = requests.get(
            "https://www.reddit.com/r/ollama/new.json",
            headers={"User-Agent": "OllamaPulse/1.0"},
            timeout=10
        )
        response.raise_for_status()
        data = response.json()
        
        entries = []
        for post in data['data']['children'][:20]:  # Last 20 posts
            post_data = post['data']
            entries.append({
                "title": post_data['title'],
                "date": datetime.fromtimestamp(post_data['created_utc']).isoformat(),
                "summary": post_data.get('selftext', '')[:200],
                "url": f"https://reddit.com{post_data['permalink']}",
                "source": "reddit",
                "highlights": [f"upvotes: {post_data['ups']}"]
            })
        
        print(f"✅ Found {len(entries)} Reddit posts")
        return entries
    except Exception as e:
        print(f"❌ Error fetching Reddit: {e}")
        return []


def fetch_twitter_placeholder():
    """Placeholder for Twitter/X search (requires API key)"""
    print("⚠️  Twitter/X search requires API key - skipping")
    # In production, use Twitter API v2 with search endpoint
    # Query: "ollama cloud filter:links min_faves:5"
    return []


def fetch_producthunt_placeholder():
    """Placeholder for Product Hunt search (requires API key)"""
    print("⚠️  Product Hunt search requires API key - skipping")
    # In production, use Product Hunt API
    # Query: "ollama" in tech category
    return []


def save_data(entries):
    """Save entries to JSON file"""
    if not entries:
        print("⚠️  No data to save")
        return
    
    filename = get_today_filename()
    
    # Load existing data if file exists
    existing = []
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            existing = json.load(f)
    
    # Merge and deduplicate by URL
    all_entries = existing + entries
    unique_entries = {e['url']: e for e in all_entries}.values()
    
    # Save
    with open(filename, 'w') as f:
        json.dump(list(unique_entries), f, indent=2)
    
    print(f"💾 Saved {len(unique_entries)} entries to {filename}")


def main():
    """Main ingestion function"""
    print("🚀 Starting community sources ingestion...")
    ensure_data_dir()
    
    # Fetch from all sources
    reddit_entries = fetch_reddit()
    twitter_entries = fetch_twitter_placeholder()
    ph_entries = fetch_producthunt_placeholder()
    
    # Combine and save
    all_entries = reddit_entries + twitter_entries + ph_entries
    save_data(all_entries)
    
    print("✅ Community sources ingestion complete!")


if __name__ == "__main__":
    main()

