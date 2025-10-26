#!/usr/bin/env python3
"""
Ollama Pulse - Dev Blogs Ingestion (14th Data Source)
Tracks Ollama tutorials, guides, and case studies from Dev.to, Hashnode, Medium
"""
import requests
import feedparser
import json
from datetime import datetime
from pathlib import Path
import time

# RSS feeds for developer blogs
DEV_TO_RSS = "https://dev.to/feed/tag/ollama"
HASHNODE_SEARCH = "https://api.hashnode.com/graphql"
MEDIUM_RSS = "https://medium.com/feed/tag/ollama"

def ensure_data_dir():
    Path("data/devblogs").mkdir(parents=True, exist_ok=True)

def get_today_filename():
    return f"data/devblogs/{datetime.now().strftime('%Y-%m-%d')}.json"

def fetch_devto():
    """Fetch Ollama posts from Dev.to"""
    print("📡 Fetching Dev.to posts...")
    entries = []
    
    try:
        feed = feedparser.parse(DEV_TO_RSS)
        
        for entry in feed.entries[:15]:
            item = {
                "title": entry.title,
                "date": entry.get('published', datetime.now().isoformat()),
                "summary": entry.get('summary', '')[:300],
                "url": entry.link,
                "source": "devto",
                "turbo_score": 0.7,
                "highlights": [
                    "tutorial",
                    "dev.to"
                ]
            }
            entries.append(item)
        
        print(f"✅ Found {len(entries)} Dev.to posts")
        
    except Exception as e:
        print(f"⚠️  Error fetching Dev.to: {e}")
    
    return entries

def fetch_hashnode():
    """Fetch Ollama posts from Hashnode"""
    print("📡 Fetching Hashnode posts...")
    entries = []
    
    try:
        query = """
        query {
          searchPostsOfPublication(
            first: 15
            filter: { query: "ollama" }
          ) {
            edges {
              node {
                title
                brief
                url
                publishedAt
                author {
                  name
                }
              }
            }
          }
        }
        """
        
        response = requests.post(
            HASHNODE_SEARCH,
            json={"query": query},
            timeout=15,
            headers={"User-Agent": "OllamaPulse/1.0"}
        )
        
        if response.status_code == 200:
            data = response.json()
            posts = data.get('data', {}).get('searchPostsOfPublication', {}).get('edges', [])
            
            for edge in posts:
                node = edge.get('node', {})
                item = {
                    "title": node.get('title', 'Hashnode Post'),
                    "date": node.get('publishedAt', datetime.now().isoformat()),
                    "summary": node.get('brief', '')[:300],
                    "url": node.get('url', ''),
                    "source": "hashnode",
                    "turbo_score": 0.7,
                    "highlights": [
                        "tutorial",
                        "hashnode",
                        f"author: {node.get('author', {}).get('name', 'unknown')}"
                    ]
                }
                entries.append(item)
            
            print(f"✅ Found {len(entries)} Hashnode posts")
        
    except Exception as e:
        print(f"⚠️  Error fetching Hashnode: {e}")
    
    return entries

def fetch_medium():
    """Fetch Ollama posts from Medium"""
    print("📡 Fetching Medium posts...")
    entries = []
    
    try:
        feed = feedparser.parse(MEDIUM_RSS)
        
        for entry in feed.entries[:15]:
            item = {
                "title": entry.title,
                "date": entry.get('published', datetime.now().isoformat()),
                "summary": entry.get('summary', '')[:300],
                "url": entry.link,
                "source": "medium",
                "turbo_score": 0.7,
                "highlights": [
                    "article",
                    "medium"
                ]
            }
            entries.append(item)
        
        print(f"✅ Found {len(entries)} Medium posts")
        
    except Exception as e:
        print(f"⚠️  Error fetching Medium: {e}")
    
    return entries

def save_data(entries):
    """Save entries to JSON file"""
    filename = get_today_filename()
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(entries, f, indent=2, ensure_ascii=False)
    
    print(f"💾 Saved {len(entries)} entries to {filename}")

def main():
    """Main ingestion function"""
    print("🚀 Starting dev blogs ingestion...")
    ensure_data_dir()
    
    all_entries = []
    
    # Fetch from all sources
    all_entries.extend(fetch_devto())
    time.sleep(1)
    
    all_entries.extend(fetch_hashnode())
    time.sleep(1)
    
    all_entries.extend(fetch_medium())
    
    if all_entries:
        save_data(all_entries)
    
    print("✅ Dev blogs ingestion complete!")

if __name__ == "__main__":
    main()

