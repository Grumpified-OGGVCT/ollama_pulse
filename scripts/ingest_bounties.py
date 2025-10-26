#!/usr/bin/env python3
import json, re, time, random, requests
from datetime import datetime
from pathlib import Path

def ensure_data_dir():
    Path("data/bounties").mkdir(parents=True, exist_ok=True)

def get_today_filename():
    return f"data/bounties/{datetime.now().strftime('%Y-%m-%d')}.json"

def ethical_delay():
    time.sleep(1 + random.random() * 4)

def extract_reward_amount(text):
    if not text:
        return "TBD"
    match = re.search(r'\$(\d+(?:,\d{3})*(?:\.\d{2})?[KkMm]?)', text)
    return f"${match.group(1)}" if match else "TBD"

def fetch_github_bounties():
    print("📡 Fetching GitHub bounties...")
    try:
        headers = {"User-Agent": "OllamaPulseBot/1.0", "Accept": "application/vnd.github.v3+json"}
        all_bounties = []
        
        for query in ['ollama bounty is:open', 'ollama reward is:open']:
            ethical_delay()
            response = requests.get(
                "https://api.github.com/search/issues",
                params={"q": query, "per_page": 20},
                headers=headers,
                timeout=10
            )
            
            if response.status_code == 200:
                for item in response.json().get('items', []):
                    combined = f"{item.get('title', '')} {item.get('body', '')}"
                    if 'ollama' in combined.lower():
                        all_bounties.append({
                            "title": item['title'],
                            "source": "github_issues",
                            "reward": extract_reward_amount(combined),
                            "summary": (item.get('body', '') or '')[:200],
                            "url": item['html_url'],
                            "deadline": None,
                            "date": item['created_at'],
                            "highlights": [f"comments: {item.get('comments', 0)}"]
                        })
        
        print(f"✅ Found {len(all_bounties)} GitHub bounties")
        return all_bounties
    except Exception as e:
        print(f"❌ Error: {e}")
        return []

def main():
    print("🎯 Starting bounty ingestion...")
    ensure_data_dir()
    bounties = fetch_github_bounties()
    
    with open(get_today_filename(), 'w') as f:
        json.dump(bounties, f, indent=2)
    
    print(f"✅ Saved {len(bounties)} bounties")

if __name__ == "__main__":
    main()
