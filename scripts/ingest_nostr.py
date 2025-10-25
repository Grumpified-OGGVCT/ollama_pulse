#!/usr/bin/env python3
import json
import time
import random
from datetime import datetime, timedelta
from pathlib import Path

try:
    from pynostr.relay_manager import RelayManager
    from pynostr.filter import Filter
except ImportError:
    print("ERROR: pynostr not installed")
    exit(1)

RELAYS = ["wss://relay.damus.io", "wss://nostr-pub.wellorder.net", "wss://relay.nostr.band"]
OLLAMA_TAGS = ["ollama", "turbo", "cloud", "llm", "ai", "models"]
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
        if tag in OLLAMA_TAGS: score += 0.1
    return min(score, 1.0)

def query_nostr_longform(since_days=1):
    print(f"Connecting to {len(RELAYS)} Nostr relays...")
    since_timestamp = int((datetime.now() - timedelta(days=since_days)).timestamp())
    filt = Filter(kinds=[NIP23_KIND], tags={"t": OLLAMA_TAGS}, since=since_timestamp)
    events = []
    for relay_url in RELAYS:
        try:
            print(f"  Querying {relay_url}...")
            relay = RelayManager()
            relay.add_relay(relay_url)
            relay.add_subscription("pulse-sub", [filt])
            time.sleep(1 + random.random() * 2)
            while relay.message_pool.has_events():
                event_msg = relay.message_pool.get_event()
                event = event_msg.event
                if event.kind == NIP23_KIND:
                    title = "Untitled"
                    summary = ""
                    tags = []
                    for tag in event.tags:
                        if len(tag) > 1:
                            if tag[0] in ["subject", "title"]: title = tag[1]
                            elif tag[0] == "summary": summary = tag[1]
                            elif tag[0] == "t": tags.append(tag[1])
                    if not summary:
                        summary = event.content[:500] if len(event.content) > 500 else event.content
                    turbo_score = calculate_turbo_score(event.content, tags)
                    events.append({
                        "title": title,
                        "summary": summary,
                        "content": event.content,
                        "url": f"nostr:nevent1q...{event.id[:16]}",
                        "source": "nostr_nip23",
                        "author_npub": event.public_key[:16] if hasattr(event, 'public_key') else "unknown",
                        "tags": tags,
                        "turbo_score": round(turbo_score, 2),
                        "created_at": event.created_at if hasattr(event, 'created_at') else int(time.time())
                    })
            relay.close_all_relay_connections()
        except Exception as e:
            print(f"  Warning: Failed to query {relay_url}: {e}")
            continue
    print(f"Found {len(events)} NIP-23 veins from Nostr")
    return events

def save_data(posts):
    ensure_data_dir()
    filename = get_today_filename()
    data = {"timestamp": datetime.now().isoformat(), "source": "nostr", "count": len(posts), "posts": posts}
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"Saved {len(posts)} posts to {filename}")
    if posts:
        sorted_posts = sorted(posts, key=lambda x: x.get('turbo_score', 0), reverse=True)
        print("\nTop 3 by Turbo Score:")
        for i, post in enumerate(sorted_posts[:3], 1):
            print(f"  {i}. [{post['turbo_score']}] {post['title']}")
            print(f"     Tags: {', '.join(post['tags'][:5])}")

def main(depth="light"):
    print("Ollama Pulse - Nostr Ingestion")
    print("=" * 50)
    try:
        posts = query_nostr_longform(since_days=1)
        save_data(posts)
        print("\nNostr ingestion complete!")
    except Exception as e:
        print(f"\nERROR during ingestion: {e}")
        import traceback
        traceback.print_exc()
        exit(1)

if __name__ == "__main__":
    import sys
    depth = sys.argv[1] if len(sys.argv) > 1 else "light"
    main(depth)
