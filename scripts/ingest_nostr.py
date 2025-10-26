#!/usr/bin/env python3
"""
Ollama Pulse - Nostr Ingestion (10th Data Source)
Uses direct WebSocket connection to query NIP-23 long-form content
"""
import json
import time
import websocket
from datetime import datetime, timedelta
from pathlib import Path

RELAYS = [
    "wss://relay.damus.io",
    "wss://nostr-pub.wellorder.net", 
    "wss://relay.nostr.band"
]

OLLAMA_KEYWORDS = ["ollama", "turbo", "cloud", "llm", "ai", "models"]
NIP23_KIND = 30023

def ensure_data_dir():
    Path("data/nostr").mkdir(parents=True, exist_ok=True)

def get_today_filename():
    return f"data/nostr/{datetime.now().strftime('%Y-%m-%d')}.json"

def calculate_turbo_score(content, tags):
    score = 0.0
    content_lower = content.lower()
    for kw in ["ollama turbo", "ollama cloud", "cloud api", "turbo api"]:
        if kw in content_lower: score += 0.3
    for kw in ["turbo", "cloud", "api", "performance", "optimization"]:
        if kw in content_lower: score += 0.15
    for tag in [t.lower() for t in tags]:
        if tag in OLLAMA_KEYWORDS: score += 0.1
    return min(score, 1.0)

def query_relay(relay_url, since_timestamp):
    events = []
    try:
        ws = websocket.create_connection(relay_url, timeout=10)
        
        # Send REQ message for NIP-23 events
        req_filter = {
            "kinds": [NIP23_KIND],
            "since": since_timestamp,
            "limit": 100
        }
        req_msg = json.dumps(["REQ", "ollama-pulse", req_filter])
        ws.send(req_msg)
        
        # Collect events for 5 seconds
        start = time.time()
        while time.time() - start < 5:
            try:
                msg = ws.recv()
                data = json.loads(msg)
                
                if data[0] == "EVENT" and data[1] == "ollama-pulse":
                    event = data[2]
                    
                    # Extract metadata
                    title = "Untitled"
                    summary = ""
                    tags = []
                    
                    for tag in event.get("tags", []):
                        if len(tag) > 1:
                            if tag[0] in ["title", "subject"]: title = tag[1]
                            elif tag[0] == "summary": summary = tag[1]
                            elif tag[0] == "t": tags.append(tag[1])
                    
                    content = event.get("content", "")
                    if not summary:
                        summary = content[:500]
                    
                    # Filter for Ollama-related content
                    content_lower = content.lower()
                    if any(kw in content_lower for kw in OLLAMA_KEYWORDS):
                        turbo_score = calculate_turbo_score(content, tags)
                        
                        events.append({
                            "title": title,
                            "summary": summary,
                            "content": content,
                            "url": f"https://njump.me/{event.get('id', '')}",
                            "source": "nostr_nip23",
                            "author_npub": event.get("pubkey", "")[:16],
                            "tags": tags,
                            "turbo_score": round(turbo_score, 2),
                            "created_at": event.get("created_at", int(time.time()))
                        })
                
                elif data[0] == "EOSE":
                    break
                    
            except websocket.WebSocketTimeoutError:
                break
        
        ws.close()
        
    except Exception as e:
        print(f"  Warning: {relay_url} failed: {e}")
    
    return events

def main():
    print("Ollama Pulse - Nostr Ingestion")
    print("=" * 50)
    
    since = int((datetime.now() - timedelta(days=1)).timestamp())
    all_events = []
    
    for relay in RELAYS:
        print(f"Querying {relay}...")
        events = query_relay(relay, since)
        all_events.extend(events)
        print(f"  Found {len(events)} Ollama-related events")
    
    # Deduplicate by URL
    unique_events = {e["url"]: e for e in all_events}.values()
    unique_events = list(unique_events)
    
    # Save
    ensure_data_dir()
    filename = get_today_filename()
    data = {
        "timestamp": datetime.now().isoformat(),
        "source": "nostr",
        "count": len(unique_events),
        "posts": unique_events
    }
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"\nSaved {len(unique_events)} unique posts to {filename}")
    
    if unique_events:
        sorted_posts = sorted(unique_events, key=lambda x: x.get('turbo_score', 0), reverse=True)
        print("\nTop 3 by Turbo Score:")
        for i, post in enumerate(sorted_posts[:3], 1):
            print(f"  {i}. [{post['turbo_score']}] {post['title']}")

if __name__ == "__main__":
    main()
