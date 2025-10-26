#!/usr/bin/env python3
"""
Ollama Pulse - Stack Overflow Ingestion (11th Data Source)
Tracks Ollama-related questions, answers, and discussions
"""
import requests
import json
from datetime import datetime
from pathlib import Path
import time

STACK_OVERFLOW_API = "https://api.stackexchange.com/2.3/search/advanced"
OLLAMA_TAGS = ["ollama", "ollama-cloud", "ollama-turbo", "llm"]

def ensure_data_dir():
    Path("data/stackoverflow").mkdir(parents=True, exist_ok=True)

def get_today_filename():
    return f"data/stackoverflow/{datetime.now().strftime('%Y-%m-%d')}.json"

def fetch_stackoverflow_questions():
    """Fetch recent Ollama-related Stack Overflow questions"""
    print("📡 Fetching Stack Overflow questions...")
    entries = []
    
    try:
        # Search for Ollama-related questions
        params = {
            "order": "desc",
            "sort": "activity",
            "q": "ollama",
            "site": "stackoverflow",
            "pagesize": 30
        }

        response = requests.get(
            STACK_OVERFLOW_API,
            params=params,
            timeout=15,
            headers={"User-Agent": "OllamaPulse/1.0"}
        )
        
        response.raise_for_status()
        data = response.json()
        
        for item in data.get('items', []):
            # Calculate turbo score based on activity
            view_count = item.get('view_count', 0)
            answer_count = item.get('answer_count', 0)
            score = item.get('score', 0)
            
            # Higher score for questions with answers and views
            turbo_score = min(1.0, (score * 0.3 + answer_count * 0.4 + min(view_count/100, 0.3)))
            
            # Get title (decode HTML entities)
            import html
            title = html.unescape(item['title'])

            entry = {
                "title": title,
                "date": datetime.fromtimestamp(item['creation_date']).isoformat(),
                "summary": f"Stack Overflow question with {answer_count} answers, {view_count} views",
                "url": item['link'],
                "source": "stackoverflow",
                "turbo_score": round(turbo_score, 2),
                "highlights": [
                    f"views: {view_count}",
                    f"answers: {answer_count}",
                    f"score: {score}",
                    f"tags: {', '.join(item.get('tags', [])[:3])}"
                ]
            }
            entries.append(entry)
        
        print(f"✅ Found {len(entries)} Stack Overflow questions")
        
        # Respect rate limiting (10,000 requests/day)
        time.sleep(1)
        
    except Exception as e:
        print(f"❌ Error fetching Stack Overflow: {e}")
    
    return entries

def save_data(entries):
    """Save entries to JSON file"""
    filename = get_today_filename()
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(entries, f, indent=2, ensure_ascii=False)
    
    print(f"💾 Saved {len(entries)} entries to {filename}")

def main():
    """Main ingestion function"""
    print("🚀 Starting Stack Overflow ingestion...")
    ensure_data_dir()
    
    entries = fetch_stackoverflow_questions()
    
    if entries:
        save_data(entries)
    
    print("✅ Stack Overflow ingestion complete!")

if __name__ == "__main__":
    main()

