#!/usr/bin/env python3
"""
Ollama Pulse - Tools & Integrations Ingestion
Polls GitHub, n8n marketplace for Ollama integrations

PRIMARY: Uses Ollama web_search API for intelligent discovery
FALLBACK: Direct GitHub API calls if web_search fails
"""
import asyncio
import json
import os
from datetime import datetime
from pathlib import Path

import requests

from ollama_turbo_client import OllamaTurboClient


def ensure_data_dir():
    """Create data/tools directory if it doesn't exist"""
    Path("data/tools").mkdir(parents=True, exist_ok=True)


def get_today_filename():
    """Get filename for today's data"""
    today = datetime.now().strftime("%Y-%m-%d")
    return f"data/tools/{today}.json"


def fetch_github_repos():
    """Fetch GitHub repos with 'ollama' topic"""
    print("📡 Fetching GitHub repos with 'ollama' topic...")
    try:
        response = requests.get(
            "https://api.github.com/search/repositories",
            params={
                "q": "ollama in:topics",
                "sort": "updated",
                "per_page": 20
            },
            headers={"Accept": "application/vnd.github.v3+json"},
            timeout=10
        )
        response.raise_for_status()
        data = response.json()
        
        entries = []
        for repo in data['items']:
            entries.append({
                "title": repo['full_name'],
                "date": repo['updated_at'],
                "summary": repo.get('description', ''),
                "url": repo['html_url'],
                "source": "github",
                "highlights": [
                    f"stars: {repo['stargazers_count']}",
                    f"language: {repo.get('language', 'N/A')}"
                ]
            })
        
        print(f"✅ Found {len(entries)} GitHub repos")
        return entries
    except Exception as e:
        print(f"❌ Error fetching GitHub repos: {e}")
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


async def fetch_via_web_search():
    """
    PRIMARY: Use Ollama web_search API for intelligent tool discovery
    """
    print("🔍 PRIMARY: Using Ollama web_search for tool discovery...")

    try:
        async with OllamaTurboClient() as client:
            # Search for Ollama tools and integrations
            results = await client.discover_ecosystem_content(
                query="Ollama tools, libraries, integrations, and projects on GitHub, npm, PyPI",
                content_type="tools",
                max_results=30
            )

            print(f"✅ Web search found {len(results)} tools")
            return results

    except Exception as e:
        print(f"⚠️  Web search failed: {e}")
        print("   Falling back to direct GitHub API...")
        return []


def main():
    """Main ingestion function"""
    print("🚀 Starting tools & integrations ingestion...")
    ensure_data_dir()

    # PRIMARY: Try Ollama web_search first
    web_search_entries = asyncio.run(fetch_via_web_search())

    # FALLBACK: Use direct GitHub API if web_search failed or returned few results
    if len(web_search_entries) < 10:
        print("📡 FALLBACK: Using direct GitHub API...")
        github_entries = fetch_github_repos()
        all_entries = web_search_entries + github_entries
    else:
        print("✅ Web search provided sufficient results, skipping fallback")
        all_entries = web_search_entries

    # Save
    save_data(all_entries)

    print("✅ Tools & integrations ingestion complete!")


if __name__ == "__main__":
    main()

