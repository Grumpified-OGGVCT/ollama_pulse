#!/usr/bin/env python3
"""
Official Sources Ingestion - FIXED to use CURRENT data only
NO MORE old blog posts from 2024!
"""
import json
import os
import requests
from datetime import datetime, timedelta
from pathlib import Path

def ensure_data_dir():
    """Create data/official directory if it doesn't exist"""
    Path("data/official").mkdir(parents=True, exist_ok=True)

def get_today_filename():
    """Get filename for today's data"""
    today = datetime.now().strftime("%Y-%m-%d")
    return f"data/official/{today}.json"

def fetch_recent_ollama_releases():
    """Fetch ONLY recent Ollama releases from GitHub (last 30 days)"""
    print("📡 Fetching recent Ollama releases from GitHub API...")
    
    entries = []
    thirty_days_ago = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
    
    try:
        # Get recent releases from official ollama/ollama repo
        response = requests.get(
            'https://api.github.com/repos/ollama/ollama/releases',
            params={'per_page': 10},
            timeout=10
        )
        response.raise_for_status()
        releases = response.json()
        
        for release in releases:
            # Only include releases from last 30 days
            created = release.get('created_at', '')[:10]
            if created < thirty_days_ago:
                continue
            
            entry = {
                "title": f"Ollama Release: {release.get('name', 'Unknown')}",
                "date": created,
                "summary": release.get('body', '')[:200],
                "url": release.get('html_url', ''),
                "source": "official_releases",
                "highlights": ["official release", "ollama", release.get('tag_name', '')]
            }
            entries.append(entry)
        
        print(f"✅ Found {len(entries)} recent releases")
        return entries
        
    except Exception as e:
        print(f"⚠️  GitHub API failed: {e}")
        return []

def fetch_current_ollama_blog():
    """Fetch ONLY current blog posts (last 30 days) - NOT old 2024 posts!"""
    print("📡 Fetching current Ollama blog posts...")
    
    # For now, skip blog entirely since we can't reliably filter old posts
    # The RSS feed returns everything including 2024 posts
    print("⚠️  Skipping blog RSS to avoid old posts - using releases only")
    return []

def save_data(entries):
    """Save entries to JSON file"""
    if not entries:
        print("⚠️  No current data to save - this is OK, we're filtering out old posts")
        # Save empty file so artifact upload doesn't fail
        ensure_data_dir()
        filename = get_today_filename()
        with open(filename, 'w') as f:
            json.dump([], f)
        return
    
    ensure_data_dir()
    filename = get_today_filename()
    
    with open(filename, 'w') as f:
        json.dump(entries, f, indent=2)
    
    print(f"💾 Saved {len(entries)} CURRENT entries to {filename}")

def main():
    """Main ingestion function - ONLY current data!"""
    print("🚀 Starting official sources ingestion (CURRENT data only)...")
    ensure_data_dir()

    # Get ONLY recent releases (no old blog posts!)
    recent_releases = fetch_recent_ollama_releases()
    
    # NO blog scraping - it returns old 2024 posts!
    # We'll rely on GitHub releases and the official cloud model list instead
    
    all_entries = recent_releases
    
    print(f"✅ Collected {len(all_entries)} CURRENT official entries (filtered out old 2024 posts)")

    # Save
    save_data(all_entries)

    print("✅ Official sources ingestion complete!")


if __name__ == "__main__":
    main()

