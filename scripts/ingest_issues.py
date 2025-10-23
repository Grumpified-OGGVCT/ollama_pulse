#!/usr/bin/env python3
"""
Ollama Pulse - GitHub Issues/PRs Ingestion
Fetches GitHub issues and pull requests mentioning Ollama Turbo Cloud
"""
import json
import os
import time
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


def search_github_issues(query="ollama turbo cloud", max_results=50):
    """
    Search GitHub issues and PRs using the public API
    Args:
        query: Search query string
        max_results: Maximum number of results to fetch
    """
    print(f"📡 Searching GitHub issues: '{query}'...")
    entries = []
    
    try:
        # Use GitHub search API (public, no auth required but rate limited)
        url = "https://api.github.com/search/issues"
        params = {
            "q": f"{query} is:issue is:open",
            "sort": "updated",
            "order": "desc",
            "per_page": min(max_results, 100)
        }
        
        headers = {
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "OllamaPulse/1.0"
        }
        
        # Add token if available in environment
        github_token = os.environ.get("GITHUB_TOKEN")
        if github_token:
            headers["Authorization"] = f"token {github_token}"
        
        response = requests.get(url, params=params, headers=headers, timeout=10)
        
        # Check rate limit
        if response.status_code == 403:
            print("⚠️  GitHub API rate limit reached, using cached data")
            return []
        
        response.raise_for_status()
        data = response.json()
        
        # Process results
        for item in data.get('items', [])[:max_results]:
            entry = {
                "title": item['title'],
                "date": item['updated_at'],
                "summary": (item.get('body') or '')[:300],
                "url": item['html_url'],
                "source": "github_issues",
                "highlights": [
                    f"comments: {item.get('comments', 0)}",
                    f"state: {item['state']}",
                    f"repo: {item['repository_url'].split('/')[-1]}"
                ]
            }
            entries.append(entry)
        
        print(f"✅ Found {len(entries)} GitHub issues/PRs")
        
        # Respect rate limiting
        time.sleep(2)
        
    except Exception as e:
        print(f"❌ Error searching GitHub issues: {e}")
    
    return entries


def search_github_prs(query="ollama turbo service", max_results=30):
    """Search GitHub pull requests specifically"""
    print(f"📡 Searching GitHub PRs: '{query}'...")
    entries = []
    
    try:
        url = "https://api.github.com/search/issues"
        params = {
            "q": f"{query} is:pr is:open",
            "sort": "updated",
            "order": "desc",
            "per_page": min(max_results, 100)
        }
        
        headers = {
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "OllamaPulse/1.0"
        }
        
        # Add token if available
        github_token = os.environ.get("GITHUB_TOKEN")
        if github_token:
            headers["Authorization"] = f"token {github_token}"
        
        response = requests.get(url, params=params, headers=headers, timeout=10)
        
        if response.status_code == 403:
            print("⚠️  GitHub API rate limit reached")
            return []
        
        response.raise_for_status()
        data = response.json()
        
        for item in data.get('items', [])[:max_results]:
            entry = {
                "title": f"[PR] {item['title']}",
                "date": item['updated_at'],
                "summary": (item.get('body') or '')[:300],
                "url": item['html_url'],
                "source": "github_prs",
                "highlights": [
                    f"comments: {item.get('comments', 0)}",
                    "pull request",
                    f"repo: {item['repository_url'].split('/')[-1]}"
                ]
            }
            entries.append(entry)
        
        print(f"✅ Found {len(entries)} GitHub PRs")
        time.sleep(2)
        
    except Exception as e:
        print(f"❌ Error searching GitHub PRs: {e}")
    
    return entries


def save_data(entries):
    """Save entries to JSON file, merging with existing"""
    if not entries:
        print("⚠️  No data to save")
        return
    
    filename = get_today_filename()
    
    # Load existing data
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
    print("🚀 Starting GitHub issues/PRs ingestion...")
    ensure_data_dir()
    
    # Search for Ollama-related issues and PRs
    issues = search_github_issues("ollama turbo cloud", max_results=30)
    prs = search_github_prs("ollama service cloud", max_results=20)
    
    # Combine and save
    all_entries = issues + prs
    save_data(all_entries)
    
    print("✅ GitHub issues/PRs ingestion complete!")


if __name__ == "__main__":
    main()
