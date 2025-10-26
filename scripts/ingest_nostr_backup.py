#!/usr/bin/env python3
"""
Ollama Pulse - Nostr Ingestion (10th Data Source)
Fetches NIP-23 long-form content from Nostr relays
Filters for Ollama/Turbo/Cloud/LLM related content
"""
import json
import os
import time
from datetime import datetime, timedelta
from pathlib import Path

try:
    from pynostr.relay_manager import RelayManager
    from pynostr.filter import Filter, Filters
    from pynostr.event import EventKind
    from pynostr.message_type import ClientMessageType
except ImportError:
    print("⚠️  pynostr not installed. Run: pip install pynostr websocket-client")
    exit(1)


# Nostr relays to connect to
RELAYS = [
    "wss://relay.damus.io",
    "wss://nostr-pub.wellorder.net",
    "wss://relay.nostr.band"
]

# Tags to filter for
OLLAMA_TAGS = ["ollama", "turbo", "cloud", "llm", "ai", "models"]

# NIP-23 long-form content kind
NIP23_KIND = 30023


def ensure_data_dir():
    """Create data/nostr directory if it doesn't exist"""
    Path("data/nostr").mkdir(parents=True, exist_ok=True)


def get_today_filename():
    """Get filename for today's data"""
    today = datetime.now().strftime("%Y-%m-%d")
    return f"data/nostr/{today}.json"


def calculate_turbo_score(content, tags):
    """
    Calculate Turbo relevance score (0-1 scale)
    Based on keywords and tags
    """
    score = 0.0
    content_lower = content.lower()
    
    # High-value keywords (0.3 each)
    high_value = ["ollama turbo", "ollama cloud", "cloud api", "turbo api"]
    for keyword in high_value:
        if keyword in content_lower:
            score += 0.3
    
    # Medium-value keywords (0.15 each)
    medium_value = ["turbo", "cloud", "api", "performance", "optimization"]
    for keyword in medium_value:
        if keyword in content_lower:
            score += 0.15
    
    # Tag bonus (0.1 per relevant tag)
    tag_list = [t.lower() for t in tags]
    for tag in OLLAMA_TAGS:
        if tag in tag_list:
            score += 0.1
    
    # Cap at 1.0
    return min(score, 1.0)


def fetch_nostr_content(hours_back=24):
    """
    Fetch NIP-23 long-form content from Nostr relays
    
    Args:
        hours_back: How many hours back to search (default 24)
    
    Returns:
        List of relevant posts with metadata
    """
    print(f"🔌 Connecting to {len(RELAYS)} Nostr relays...")
    
    relay_manager = RelayManager()
    for relay in RELAYS:
        relay_manager.add_relay(relay)
    
    # Calculate timestamp for filtering (Unix timestamp)
    since_timestamp = int((datetime.now() - timedelta(hours=hours_back)).timestamp())
    
    # Create filter for NIP-23 long-form content
    filters = Filters([
        Filter(
            kinds=[NIP23_KIND],
            since=since_timestamp
        )
    ])
    
    print(f"📡 Requesting NIP-23 content from last {hours_back} hours...")
    
    # Subscribe to events
    subscription_id = relay_manager.add_subscription_on_all_relays(filters)
    
    # Wait for events to arrive
    time.sleep(5)  # Give relays time to respond
    
    # Collect events
    events = []
    while relay_manager.message_pool.has_events():
        event_msg = relay_manager.message_pool.get_event()
        events.append(event_msg.event)
    
    print(f"📥 Received {len(events)} total events")
    
    # Close connections
    relay_manager.close_all_relay_connections()
    
    # Filter and process events
    relevant_posts = []
    
    for event in events:
        # Extract content and tags
        content = event.content
        tags = [tag[1] for tag in event.tags if len(tag) > 1 and tag[0] in ['t', 'hashtag']]
        
        # Check if content is relevant to Ollama
        content_lower = content.lower()
        is_relevant = any(keyword in content_lower for keyword in OLLAMA_TAGS)
        
        if not is_relevant:
            continue
        
        # Extract metadata
        title = ""
        summary = ""
        published_at = None
        
        for tag in event.tags:
            if len(tag) > 1:
                if tag[0] == "title":
                    title = tag[1]
                elif tag[0] == "summary":
                    summary = tag[1]
                elif tag[0] == "published_at":
                    try:
                        published_at = int(tag[1])
                    except:
                        pass
        
        # Calculate Turbo score
        turbo_score = calculate_turbo_score(content, tags)
        
        # Build post object
        post = {
            "id": event.id,
            "pubkey": event.public_key,
            "created_at": event.created_at,
            "published_at": published_at or event.created_at,
            "title": title or f"Nostr Post {event.id[:8]}",
            "summary": summary or content[:200] + "..." if len(content) > 200 else content,
            "content": content,
            "tags": tags,
            "turbo_score": round(turbo_score, 2),
            "url": f"https://njump.me/{event.id}",  # Nostr web viewer
            "source": "nostr"
        }
        
        relevant_posts.append(post)
    
    print(f"✅ Found {len(relevant_posts)} Ollama-related posts")
    
    # Sort by Turbo score (highest first)
    relevant_posts.sort(key=lambda x: x["turbo_score"], reverse=True)
    
    return relevant_posts


def save_data(posts):
    """Save posts to JSON file"""
    ensure_data_dir()
    filename = get_today_filename()
    
    data = {
        "timestamp": datetime.now().isoformat(),
        "source": "nostr",
        "count": len(posts),
        "posts": posts
    }
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"💾 Saved {len(posts)} posts to {filename}")
    
    # Print top 3 by Turbo score
    if posts:
        print("\n🔥 Top 3 by Turbo Score:")
        for i, post in enumerate(posts[:3], 1):
            print(f"  {i}. [{post['turbo_score']}] {post['title']}")
            print(f"     Tags: {', '.join(post['tags'][:5])}")
            print(f"     URL: {post['url']}")


def main():
    """Main execution"""
    print("🩸⛏️ Ollama Pulse - Nostr Ingestion")
    print("=" * 50)
    
    try:
        # Fetch content from last 24 hours
        posts = fetch_nostr_content(hours_back=24)
        
        # Save to file
        save_data(posts)
        
        print("\n✅ Nostr ingestion complete!")
        
    except Exception as e:
        print(f"\n❌ Error during ingestion: {e}")
        import traceback
        traceback.print_exc()
        exit(1)


if __name__ == "__main__":
    main()

