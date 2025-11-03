#!/usr/bin/env python3
"""
Comprehensive Social Media Ingestion - ALL platforms with Ollama content
Combines Ollama web_search + direct public APIs for maximum coverage
"""
import asyncio
import requests
from datetime import datetime
from pathlib import Path
import json

from ollama_turbo_client import OllamaTurboClient

def ensure_data_dir():
    Path("data/social_media").mkdir(parents=True, exist_ok=True)

def get_today_filename():
    return f"data/social_media/{datetime.now().strftime('%Y-%m-%d')}.json"

async def search_via_ollama_web_search():
    """
    Use Ollama web_search API for platforms without public APIs
    Covers: X/Twitter, Instagram, Facebook, LinkedIn, TikTok, Threads, Pinterest, Tumblr, Medium
    """
    print("🔍 Using Ollama web_search for closed platforms...")
    
    all_entries = []
    
    async with OllamaTurboClient() as client:
        # Platform-specific queries
        queries = [
            ("🐦 X/Twitter", "Ollama AI tweets discussions mentions hashtag #ollama on Twitter X platform", 12),
            ("📸 Instagram", "Ollama AI visual tutorials demos posts on Instagram platform", 8),
            ("📘 Facebook", "Ollama AI discussions groups pages communities on Facebook Meta", 8),
            ("💼 LinkedIn", "Ollama AI professional discussions posts articles on LinkedIn", 8),
            ("🎵 TikTok", "Ollama AI video tutorials demos on TikTok short-form video", 8),
            ("🧵 Threads", "Ollama AI discussions posts on Threads by Meta Instagram", 6),
            ("📌 Pinterest", "Ollama AI tutorials infographics pins boards on Pinterest", 6),
            ("📝 Tumblr", "Ollama AI blog posts discussions tutorials on Tumblr blogging", 6),
            ("✍️ Medium", "Ollama AI technical articles tutorials guides on Medium blogging", 10),
        ]
        
        for platform_name, query, max_results in queries:
            try:
                print(f"  {platform_name}...")
                results = await client.discover_ecosystem_content(
                    query=query,
                    content_type="discussions",
                    max_results=max_results
                )
                
                # Tag with platform
                for r in results:
                    r['platform'] = platform_name.split()[1]  # Extract platform name
                
                all_entries.extend(results)
                print(f"    ✓ Found {len(results)} references")
                
            except Exception as e:
                print(f"    ⚠️  {platform_name} search failed: {e}")
    
    print(f"✅ Web search found {len(all_entries)} social media references")
    return all_entries

def fetch_mastodon_direct():
    """
    Mastodon has a FREE public API - no auth needed!
    Search #ollama hashtag across mastodon.social
    """
    print("🐘 Mastodon: Direct API (no auth required)...")
    
    entries = []
    
    try:
        # Public hashtag timeline - completely open!
        response = requests.get(
            'https://mastodon.social/api/v1/timelines/tag/ollama',
            params={'limit': 20},
            timeout=10
        )
        response.raise_for_status()
        posts = response.json()
        
        for post in posts[:15]:  # Top 15
            entry = {
                "title": f"Mastodon: {post.get('account', {}).get('display_name', 'User')} on Ollama",
                "date": post.get('created_at', datetime.now().isoformat())[:10],
                "summary": post.get('content', '')[:200].replace('<p>', '').replace('</p>', ''),
                "url": post.get('url', ''),
                "source": "social_media",
                "platform": "Mastodon",
                "highlights": ["mastodon", "ollama", "fediverse"]
            }
            entries.append(entry)
        
        print(f"    ✓ Found {len(entries)} Mastodon posts")
        
    except Exception as e:
        print(f"    ⚠️  Mastodon API failed: {e}")
    
    return entries

def fetch_bluesky_direct():
    """
    Bluesky has a FREE public API - fully open!
    Search for Ollama posts via AT Protocol
    """
    print("🦋 Bluesky: Direct API (AT Protocol)...")
    
    entries = []
    
    try:
        # Public search endpoint - completely open!
        response = requests.get(
            'https://public.api.bsky.app/xrpc/app.bsky.feed.searchPosts',
            params={'q': 'ollama', 'limit': 20},
            timeout=10
        )
        response.raise_for_status()
        data = response.json()
        posts = data.get('posts', [])
        
        for post in posts[:15]:  # Top 15
            author = post.get('author', {})
            record = post.get('record', {})
            
            entry = {
                "title": f"Bluesky: {author.get('displayName', 'User')} on Ollama",
                "date": record.get('createdAt', datetime.now().isoformat())[:10],
                "summary": record.get('text', '')[:200],
                "url": f"https://bsky.app/profile/{author.get('handle', '')}/post/{post.get('uri', '').split('/')[-1]}",
                "source": "social_media",
                "platform": "Bluesky",
                "highlights": ["bluesky", "ollama", "at-protocol"]
            }
            entries.append(entry)
        
        print(f"    ✓ Found {len(entries)} Bluesky posts")
        
    except Exception as e:
        print(f"    ⚠️  Bluesky API failed: {e}")
    
    return entries

def save_data(entries):
    """Save all social media entries"""
    if not entries:
        print("⚠️  No social media data found")
        ensure_data_dir()
        with open(get_today_filename(), 'w') as f:
            json.dump([], f)
        return
    
    ensure_data_dir()
    
    # Deduplicate by URL
    unique_entries = list({e.get('url', e.get('title', '')): e for e in entries}.values())
    
    with open(get_today_filename(), 'w') as f:
        json.dump(unique_entries, f, indent=2)
    
    print(f"💾 Saved {len(unique_entries)} unique social media entries")

def main():
    """
    Comprehensive social media ingestion
    11 platforms total: X, Instagram, Facebook, LinkedIn, TikTok, Threads, 
                        Pinterest, Tumblr, Medium, Mastodon, Bluesky
    """
    print("🚀 Starting COMPREHENSIVE social media ingestion...")
    print("   Platforms: X, Instagram, Facebook, LinkedIn, TikTok, Threads,")
    print("             Pinterest, Tumblr, Medium, Mastodon, Bluesky")
    print()
    
    try:
        # Part 1: Use web_search for closed platforms (9 platforms)
        web_search_entries = asyncio.run(search_via_ollama_web_search())
        
        # Part 2: Direct API for open platforms (2 platforms)
        mastodon_entries = fetch_mastodon_direct()
        bluesky_entries = fetch_bluesky_direct()
        
        # Combine all
        all_entries = web_search_entries + mastodon_entries + bluesky_entries
        
        print(f"\n✅ Total from all platforms: {len(all_entries)} entries")
        print(f"   - Web search: {len(web_search_entries)}")
        print(f"   - Mastodon: {len(mastodon_entries)}")
        print(f"   - Bluesky: {len(bluesky_entries)}")
        
        save_data(all_entries)
        print("\n✅ Social media ingestion complete!")
        
    except Exception as e:
        print(f"❌ Social media ingestion failed: {e}")
        import traceback
        traceback.print_exc()
        # Save empty to prevent workflow failure
        save_data([])

if __name__ == "__main__":
    main()

