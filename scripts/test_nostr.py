#!/usr/bin/env python3
import json
import time
from datetime import datetime, timedelta
from pathlib import Path

try:
    from pynostr.relay_manager import RelayManager
    from pynostr.filters import FiltersList, Filters
    from pynostr.event import Event
    from pynostr.message_type import ClientMessageType
except ImportError as e:
    print(f"ERROR: pynostr import failed: {e}")
    exit(1)

RELAYS = ["wss://relay.damus.io"]
OLLAMA_TAGS = ["ollama", "turbo", "cloud"]
NIP23_KIND = 30023

def main():
    print("Testing Nostr connection...")
    try:
        relay_manager = RelayManager()
        relay_manager.add_relay(RELAYS[0])
        
        since = int((datetime.now() - timedelta(days=1)).timestamp())
        filters = Filters([{
            "kinds": [NIP23_KIND],
            "since": since,
            "limit": 10
        }])
        
        relay_manager.add_subscription_on_all_relays("test", filters)
        time.sleep(5)
        
        count = 0
        while relay_manager.message_pool.has_events():
            event_msg = relay_manager.message_pool.get_event()
            count += 1
            print(f"Event {count}: {event_msg.event.id[:16]}")
        
        relay_manager.close_all_relay_connections()
        print(f"\nReceived {count} events")
        
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
