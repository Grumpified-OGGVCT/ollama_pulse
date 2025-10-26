#!/usr/bin/env python3
"""
Ollama Pulse - GitHub Releases Ingestion (13th Data Source)
Tracks official Ollama releases, changelogs, and version updates
"""
import requests
import json
from datetime import datetime
from pathlib import Path
import time

OLLAMA_RELEASES_API = "https://api.github.com/repos/ollama/ollama/releases"

def ensure_data_dir():
    Path("data/releases").mkdir(parents=True, exist_ok=True)

def get_today_filename():
    return f"data/releases/{datetime.now().strftime('%Y-%m-%d')}.json"

def fetch_github_releases():
    """Fetch recent Ollama releases from GitHub"""
    print("📡 Fetching Ollama GitHub releases...")
    entries = []
    
    try:
        response = requests.get(
            OLLAMA_RELEASES_API,
            params={"per_page": 20},
            timeout=15,
            headers={
                "Accept": "application/vnd.github.v3+json",
                "User-Agent": "OllamaPulse/1.0"
            }
        )
        
        response.raise_for_status()
        releases = response.json()
        
        for release in releases:
            # Calculate turbo score (higher for recent releases)
            is_prerelease = release.get('prerelease', False)
            is_draft = release.get('draft', False)
            
            # Higher score for stable releases
            turbo_score = 0.9 if not is_prerelease and not is_draft else 0.6
            
            entry = {
                "title": f"Ollama {release['tag_name']}: {release['name']}",
                "date": release['published_at'],
                "summary": (release.get('body') or '')[:500],
                "url": release['html_url'],
                "source": "ollama_releases",
                "turbo_score": turbo_score,
                "highlights": [
                    f"version: {release['tag_name']}",
                    f"prerelease: {is_prerelease}",
                    f"assets: {len(release.get('assets', []))}",
                    f"author: {release.get('author', {}).get('login', 'unknown')}"
                ]
            }
            entries.append(entry)
        
        print(f"✅ Found {len(entries)} Ollama releases")
        
        # Respect GitHub rate limiting
        time.sleep(1)
        
    except Exception as e:
        print(f"❌ Error fetching releases: {e}")
    
    return entries

def save_data(entries):
    """Save entries to JSON file"""
    filename = get_today_filename()
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(entries, f, indent=2, ensure_ascii=False)
    
    print(f"💾 Saved {len(entries)} entries to {filename}")

def main():
    """Main ingestion function"""
    print("🚀 Starting GitHub releases ingestion...")
    ensure_data_dir()
    
    entries = fetch_github_releases()
    
    if entries:
        save_data(entries)
    
    print("✅ GitHub releases ingestion complete!")

if __name__ == "__main__":
    main()

