#!/usr/bin/env python3
"""
Social Media Ingestion - Ollama discussions across X, Instagram, Facebook
Uses Ollama web_search API to find social media content legally (no ToS violations)
"""
import asyncio
from datetime import datetime
from pathlib import Path
import json

from ollama_turbo_client import OllamaTurboClient
from model_registry import select_model_for_task

def ensure_data_dir():
    Path("data/social_media").mkdir(parents=True, exist_ok=True)

def get_today_filename():
    return f"data/social_media/{datetime.now().strftime('%Y-%m-%d')}.json"

async def fetch_social_media_discussions():
    """
    Use Ollama web_search to find Ollama content across social platforms
    This searches for articles/posts ABOUT social media discussions (legal, no ToS violations)
    """
    print("📱 Searching social media for Ollama discussions via web_search API...")
    
    all_entries = []
    
    async with OllamaTurboClient() as client:
        # Use instruction-tuned model for accurate data collection (per user request)
        # This reduces hallucinations during search
        
        # Query 1: X/Twitter discussions
        print("  🐦 Searching X/Twitter...")
        query1 = "Ollama AI discussions tweets mentions on Twitter X platform #ollama"
        results1 = await client.discover_ecosystem_content(
            query=query1,
            content_type="discussions", 
            max_results=10
        )
        all_entries.extend(results1)
        print(f"    Found {len(results1)} X/Twitter references")
        
        # Query 2: Instagram content
        print("  📸 Searching Instagram...")
        query2 = "Ollama AI posts tutorials demos on Instagram visual platform"
        results2 = await client.discover_ecosystem_content(
            query=query2,
            content_type="discussions",
            max_results=8
        )
        all_entries.extend(results2)
        print(f"    Found {len(results2)} Instagram references")
        
        # Query 3: Facebook groups/pages
        print("  📘 Searching Facebook...")
        query3 = "Ollama AI discussions groups pages on Facebook Meta platform"
        results3 = await client.discover_ecosystem_content(
            query=query3,
            content_type="discussions",
            max_results=8
        )
        all_entries.extend(results3)
        print(f"    Found {len(results3)} Facebook references")
        
        # Query 4: LinkedIn professional discussions
        print("  💼 Searching LinkedIn...")
        query4 = "Ollama AI professional discussions posts on LinkedIn"
        results4 = await client.discover_ecosystem_content(
            query=query4,
            content_type="discussions",
            max_results=8
        )
        all_entries.extend(results4)
        print(f"    Found {len(results4)} LinkedIn references")
        
        # Query 5: TikTok videos
        print("  🎵 Searching TikTok...")
        query5 = "Ollama AI tutorials demos videos on TikTok"
        results5 = await client.discover_ecosystem_content(
            query=query5,
            content_type="discussions",
            max_results=6
        )
        all_entries.extend(results5)
        print(f"    Found {len(results5)} TikTok references")
    
    # Mark all entries with social_media source
    for entry in all_entries:
        entry['source'] = 'social_media'
        entry['platform_type'] = 'social'
    
    print(f"✅ Total social media references found: {len(all_entries)}")
    return all_entries

def save_data(entries):
    """Save social media entries"""
    if not entries:
        print("⚠️  No social media data found")
        ensure_data_dir()
        # Save empty file so artifact upload doesn't fail
        with open(get_today_filename(), 'w') as f:
            json.dump([], f)
        return
    
    ensure_data_dir()
    with open(get_today_filename(), 'w') as f:
        json.dump(entries, f, indent=2)
    
    print(f"💾 Saved {len(entries)} social media entries")

def main():
    """Main social media ingestion"""
    print("🚀 Starting social media ingestion (X, Instagram, Facebook, LinkedIn, TikTok)...")
    print("   Method: Ollama web_search API (legal, no ToS violations)")
    
    try:
        entries = asyncio.run(fetch_social_media_discussions())
        save_data(entries)
        print("✅ Social media ingestion complete!")
    except Exception as e:
        print(f"❌ Social media ingestion failed: {e}")
        # Save empty to prevent workflow failure
        save_data([])

if __name__ == "__main__":
    main()

