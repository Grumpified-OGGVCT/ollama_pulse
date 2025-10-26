#!/usr/bin/env python3
"""
Ollama Pulse - Cloud Sources Deep Ingestion
Polls Ollama Cloud API endpoints for Turbo model details and changelogs

PRIMARY: Uses Ollama web_search API for cloud model discovery
FALLBACK: Direct scraping if web_search fails
"""
import asyncio
import json
import os
from datetime import datetime
from pathlib import Path

import requests

from ollama_turbo_client import OllamaTurboClient


def ensure_data_dir():
    """Create data/official directory if it doesn't exist"""
    Path("data/official").mkdir(parents=True, exist_ok=True)


def get_today_filename():
    """Get filename for today's data"""
    today = datetime.now().strftime("%Y-%m-%d")
    return f"data/official/{today}.json"


def fetch_ollama_tags(filter_type="turbo", depth="full"):
    """
    Fetch Ollama API tags for cloud models
    Args:
        filter_type: Filter for 'turbo' or 'all' models
        depth: 'full' includes detailed model cards, 'basic' is quick
    """
    print(f"📡 Fetching Ollama tags (filter={filter_type}, depth={depth})...")
    entries = []
    
    try:
        # Try to fetch from ollama.com/api/tags (if publicly available)
        # This is a placeholder - adjust URL based on actual API
        response = requests.get(
            "https://ollama.com/library",
            timeout=10
        )
        response.raise_for_status()
        
        # Extract cloud models from the library page
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Look for model links or cards
        models = []
        for link in soup.find_all('a', href=True):
            href = link.get('href', '')
            if '/library/' in href:
                model_name = href.split('/library/')[-1]
                if filter_type == "turbo" and "turbo" not in model_name.lower():
                    continue
                models.append(model_name)
        
        # Create entries for found models
        for model in models[:20]:  # Limit to 20 models
            entry = {
                "title": f"Cloud Model: {model}",
                "date": datetime.now().isoformat(),
                "summary": f"Available cloud model variant: {model}",
                "url": f"https://ollama.com/library/{model}",
                "source": "cloud_api",
                "highlights": [f"model: {model}", "cloud variant"]
            }
            entries.append(entry)
        
        print(f"✅ Found {len(entries)} cloud models")
        
    except Exception as e:
        print(f"⚠️  Could not fetch cloud tags: {e}")
        # Fallback: return known cloud models
        fallback_models = [
            "qwen3-coder-480b-cloud", "glm-4.6-cloud", "gpt-oss-120b-cloud",
            "llama-3.2-turbo", "mixtral-turbo"
        ]
        for model in fallback_models:
            entry = {
                "title": f"Cloud Model: {model}",
                "date": datetime.now().isoformat(),
                "summary": f"Known cloud model variant: {model}",
                "url": f"https://ollama.com/library/{model}",
                "source": "cloud_api",
                "highlights": [f"model: {model}", "cloud variant", "turbo"]
            }
            entries.append(entry)
        print(f"✅ Using fallback: {len(entries)} known cloud models")
    
    return entries


def save_data(entries):
    """Save entries to JSON file, merging with existing data"""
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


async def fetch_via_web_search(filter_type="turbo"):
    """
    PRIMARY: Use Ollama web_search API for cloud model discovery
    """
    print(f"🔍 PRIMARY: Using Ollama web_search for cloud models (filter={filter_type})...")

    try:
        async with OllamaTurboClient() as client:
            # Search for Ollama cloud models
            query = "Ollama Cloud models, Turbo API, cloud-hosted models" if filter_type == "turbo" else "All Ollama models and library"
            results = await client.discover_ecosystem_content(
                query=query,
                content_type="tools",
                max_results=15  # Reduced from 30 - only request what we expect to find
            )

            print(f"✅ Web search found {len(results)} cloud models")
            return results

    except Exception as e:
        print(f"⚠️  Web search failed: {e}")
        print("   Falling back to direct scraping...")
        return []


def main():
    """Main ingestion function"""
    import argparse

    parser = argparse.ArgumentParser(description='Ollama Cloud Deep Ingestion')
    parser.add_argument('--filter', default='turbo', choices=['turbo', 'all'],
                       help='Filter models by type (default: turbo)')
    parser.add_argument('--depth', default='full', choices=['full', 'basic'],
                       help='Depth of information to fetch (default: full)')

    args = parser.parse_args()

    print("🚀 Starting cloud sources deep ingestion...")
    ensure_data_dir()

    # PRIMARY: Try Ollama web_search first
    web_search_entries = asyncio.run(fetch_via_web_search(filter_type=args.filter))

    # FALLBACK: Use direct scraping if web_search failed or returned few results
    if len(web_search_entries) < 5:
        print("📡 FALLBACK: Using direct scraping...")
        cloud_entries = fetch_ollama_tags(filter_type=args.filter, depth=args.depth)
        all_entries = web_search_entries + cloud_entries
    else:
        print("✅ Web search provided sufficient results, skipping fallback")
        all_entries = web_search_entries

    # Save
    save_data(all_entries)

    print("✅ Cloud sources ingestion complete!")


if __name__ == "__main__":
    main()
