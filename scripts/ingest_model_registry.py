#!/usr/bin/env python3
"""
Ollama Pulse - Model Registry Ingestion (12th Data Source)
Tracks new models, updates, and popularity from ollama.com/library
"""
import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime
from pathlib import Path
import time

OLLAMA_LIBRARY_URL = "https://ollama.com/library"

def ensure_data_dir():
    Path("data/model_registry").mkdir(parents=True, exist_ok=True)

def get_today_filename():
    return f"data/model_registry/{datetime.now().strftime('%Y-%m-%d')}.json"

def fetch_model_library():
    """Scrape Ollama model library for new/updated models"""
    print("📡 Fetching Ollama model library...")
    entries = []
    
    try:
        response = requests.get(
            OLLAMA_LIBRARY_URL,
            timeout=15,
            headers={"User-Agent": "OllamaPulse/1.0"}
        )
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find model cards (adjust selectors based on actual HTML structure)
        model_cards = soup.find_all('a', class_='model-card') or soup.find_all('div', class_='model')
        
        if not model_cards:
            # Fallback: try to find any links to /library/
            model_links = soup.find_all('a', href=lambda x: x and '/library/' in x)
            model_cards = model_links[:30]  # Limit to 30
        
        for card in model_cards[:30]:
            try:
                # Extract model info
                if card.name == 'a':
                    model_url = card.get('href', '')
                    if not model_url.startswith('http'):
                        model_url = f"https://ollama.com{model_url}"
                    
                    model_name = card.get_text(strip=True) or model_url.split('/')[-1]
                else:
                    model_name = card.get_text(strip=True)
                    model_url = OLLAMA_LIBRARY_URL
                
                # Skip empty entries
                if not model_name:
                    continue
                
                # Calculate turbo score (higher for popular models)
                # This is a placeholder - could be enhanced with download counts
                turbo_score = 0.7  # Default score for model registry items
                
                entry = {
                    "title": f"Model: {model_name}",
                    "date": datetime.now().isoformat(),
                    "summary": f"Ollama model available in library: {model_name}",
                    "url": model_url,
                    "source": "ollama_models",
                    "turbo_score": turbo_score,
                    "highlights": [
                        "model registry",
                        "ollama library"
                    ]
                }
                entries.append(entry)
                
            except Exception as e:
                print(f"⚠️  Error parsing model card: {e}")
                continue
        
        print(f"✅ Found {len(entries)} models in library")
        
    except Exception as e:
        print(f"❌ Error fetching model library: {e}")
    
    return entries

def save_data(entries):
    """Save entries to JSON file"""
    filename = get_today_filename()
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(entries, f, indent=2, ensure_ascii=False)
    
    print(f"💾 Saved {len(entries)} entries to {filename}")

def main():
    """Main ingestion function"""
    print("🚀 Starting model registry ingestion...")
    ensure_data_dir()
    
    entries = fetch_model_library()
    
    if entries:
        save_data(entries)
    
    print("✅ Model registry ingestion complete!")

if __name__ == "__main__":
    main()

