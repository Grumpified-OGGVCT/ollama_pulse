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


def fetch_youtube_transcripts():
    """Fetch YouTube videos about Ollama Turbo Cloud"""
    print("📡 Fetching YouTube videos...")
    entries = []
    
    try:
        # Use YouTube RSS feed (no API key required)
        # Search for Ollama channel or specific queries
        import feedparser
        
        # Try Ollama-related search results via RSS (limited but free)
        # Note: Full implementation would use yt-dlp for transcripts
        feed_url = "https://www.youtube.com/feeds/videos.xml?q=ollama+turbo+cloud"
        
        feed = feedparser.parse(feed_url)
        
        for entry in feed.entries[:5]:  # Last 5 videos
            video_entry = {
                "title": f"[Video] {entry.title}",
                "date": entry.get('published', datetime.now().isoformat()),
                "summary": entry.get('summary', '')[:200],
                "url": entry.link,
                "source": "youtube",
                "highlights": ["video tutorial", "ollama tutorial"]
            }
            entries.append(video_entry)
        
        print(f"✅ Found {len(entries)} YouTube videos")
        
    except Exception as e:
        print(f"⚠️  Could not fetch YouTube: {e}")
    
    return entries


def fetch_hackernews():
    """Fetch Hacker News posts about Ollama"""
    print("📡 Fetching Hacker News...")
    entries = []
    
    try:
        # Use Algolia HN Search API (free, no key needed)
        url = "https://hn.algolia.com/api/v1/search"
        params = {
            "query": "ollama cloud",
            "tags": "story",
            "hitsPerPage": 20
        }
        
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        for hit in data.get('hits', []):
            if not hit.get('url'):
                continue
            
            entry = {
                "title": hit.get('title', 'No title'),
                "date": hit.get('created_at', datetime.now().isoformat()),
                "summary": hit.get('story_text', '')[:200],
                "url": hit.get('url'),
                "source": "hackernews",
                "highlights": [f"points: {hit.get('points', 0)}", f"comments: {hit.get('num_comments', 0)}"]
            }
            entries.append(entry)
        
        print(f"✅ Found {len(entries)} Hacker News posts")
        
    except Exception as e:
        print(f"⚠️  Could not fetch Hacker News: {e}")
    
    return entries


def fetch_huggingface_discussions():
    """Fetch HuggingFace discussions about Ollama"""
    print("📡 Fetching HuggingFace discussions...")
    entries = []
    
    try:
        # Use HuggingFace API to search discussions
        url = "https://huggingface.co/api/discussions"
        params = {
            "search": "ollama turbo",
            "limit": 20
        }
        
        response = requests.get(url, params=params, timeout=10, headers={"User-Agent": "OllamaPulse/1.0"})
        
        if response.status_code == 200:
            data = response.json()
            discussions = data if isinstance(data, list) else []
            
            for discussion in discussions[:20]:
                entry = {
                    "title": discussion.get('title', 'Discussion'),
                    "date": discussion.get('created_at', datetime.now().isoformat()),
                    "summary": discussion.get('description', '')[:200],
                    "url": f"https://huggingface.co/discussions/{discussion.get('id', '')}",
                    "source": "huggingface",
                    "highlights": ["model discussion", "huggingface"]
                }
                entries.append(entry)
        
        print(f"✅ Found {len(entries)} HuggingFace discussions")
        
    except Exception as e:
        print(f"⚠️  Could not fetch HuggingFace: {e}")
    
    return entries


def fetch_newsletters():
    """Fetch newsletters about Ollama"""
    print("📡 Fetching newsletters...")
    entries = []
    
    try:
        import feedparser
        
        # Try common newsletter RSS feeds
        # Note: Adjust URLs based on actual newsletter sources
        newsletter_feeds = [
            "https://ollama.substack.com/feed",  # If exists
        ]
        
        for feed_url in newsletter_feeds:
            try:
                feed = feedparser.parse(feed_url)
                for entry in feed.entries[:5]:
                    newsletter_entry = {
                        "title": f"[Newsletter] {entry.title}",
                        "date": entry.get('published', datetime.now().isoformat()),
                        "summary": entry.get('summary', '')[:200],
                        "url": entry.link,
                        "source": "newsletter",
                        "highlights": ["newsletter", "announcement"]
                    }
                    entries.append(newsletter_entry)
            except Exception as feed_err:
                print(f"  ⚠️  Could not fetch {feed_url}: {feed_err}")
        
        print(f"✅ Found {len(entries)} newsletter items")
        
    except Exception as e:
        print(f"⚠️  Could not fetch newsletters: {e}")
    
    return entries


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
    youtube_entries = fetch_youtube_transcripts()
    hn_entries = fetch_hackernews()
    hf_entries = fetch_huggingface_discussions()
    newsletter_entries = fetch_newsletters()
    
    # Combine and save
    all_entries = (reddit_entries + twitter_entries + ph_entries + 
                   youtube_entries + hn_entries + hf_entries + newsletter_entries)
    save_data(all_entries)
    
    print("✅ Community sources ingestion complete!")


if __name__ == "__main__":
    main()

