#!/usr/bin/env python3
"""
Ollama Pulse - Nostr NIP-23 Long-Form Publisher
Publishes daily EchoVein reports to Nostr network with viral hashtags and SEO optimization
"""
import json
import os
import sys
import time
from datetime import datetime
from pathlib import Path

try:
    from pynostr.relay_manager import RelayManager
    from pynostr.event import Event
    from pynostr.key import PrivateKey
except ImportError:
    print("ERROR: pynostr not installed. Run: pip install pynostr websocket-client")
    sys.exit(1)

# Nostr Configuration
RELAYS = [
    "wss://relay.damus.io",
    "wss://nos.lol",
    "wss://relay.nostr.band",
    "wss://nostr.wine",
    "wss://relay.snort.social",
    "wss://relay.current.fyi",
    "wss://nostr-pub.wellorder.net",
    "wss://relay.nostr.info"
]

# NIP-23 Long-form content kind
NIP23_KIND = 30023

# Viral hashtags for Nostr (tested and trending)
VIRAL_HASHTAGS = [
    "ollama",           # Core topic
    "ai",               # Broad reach
    "llm",              # Technical audience
    "opensource",       # Community appeal
    "aitools",          # Tool builders
    "machinelearning",  # ML community
    "genai",            # Generative AI trend
    "aidev",            # Developer focus
    "localai",          # Privacy-focused
    "selfhosted",       # Self-hosting community
    "bitcoin",          # Nostr native audience
    "nostr",            # Platform tag
    "echovein",         # Brand identity
    "turbo",            # Ollama Turbo specific
    "cloudmodels"       # Cloud models trend
]

# SEO Keywords for discoverability
SEO_KEYWORDS = [
    "Ollama ecosystem",
    "AI development",
    "local LLM",
    "machine learning tools",
    "open source AI",
    "Ollama Turbo",
    "Ollama Cloud",
    "AI innovation",
    "developer tools",
    "AI trends"
]


def load_private_key():
    """Load Nostr private key from environment or config"""
    # Try environment variable first
    nsec = os.getenv("NOSTR_PRIVATE_KEY")
    
    # Try config file
    if not nsec:
        config_file = Path("../config/nostr_key.txt")
        if config_file.exists():
            nsec = config_file.read_text().strip()
    
    if not nsec:
        print("WARNING: No Nostr private key found. Set NOSTR_PRIVATE_KEY env var or create config/nostr_key.txt")
        print("Generating temporary key for this session...")
        private_key = PrivateKey()
        print(f"Temporary nsec: {private_key.bech32()}")
        print(f"Temporary npub: {private_key.public_key.bech32()}")
        return private_key
    
    return PrivateKey.from_nsec(nsec)


def get_today_report():
    """Load today's generated report"""
    today = datetime.now().strftime("%Y-%m-%d")
    report_file = Path(f"../docs/reports/pulse-{today}.md")
    
    if not report_file.exists():
        print(f"ERROR: Report not found: {report_file}")
        return None, None
    
    content = report_file.read_text(encoding='utf-8')
    
    # Extract title from first heading
    title = f"Ollama Pulse – {today}"
    for line in content.split('\n'):
        if line.startswith('# '):
            title = line.replace('# ', '').strip()
            break
    
    return title, content


def create_nip23_event(private_key, title, content, published_at=None):
    """Create NIP-23 long-form content event with SEO optimization"""
    if published_at is None:
        published_at = int(datetime.now().timestamp())
    
    # Generate summary (first 200 chars of content, excluding front matter)
    lines = content.split('\n')
    summary_lines = []
    in_front_matter = False
    for line in lines:
        if line.strip() == '---':
            in_front_matter = not in_front_matter
            continue
        if not in_front_matter and line.strip() and not line.startswith('#'):
            summary_lines.append(line.strip())
            if len(' '.join(summary_lines)) > 200:
                break
    
    summary = ' '.join(summary_lines)[:200] + "..."
    
    # Create event with NIP-23 tags
    event = Event(
        kind=NIP23_KIND,
        content=content,
        public_key=private_key.public_key.hex()
    )
    
    # Required NIP-23 tags
    event.add_tag("d", f"ollama-pulse-{datetime.now().strftime('%Y-%m-%d')}")  # Unique identifier
    event.add_tag("title", title)
    event.add_tag("summary", summary)
    event.add_tag("published_at", str(published_at))
    
    # Image tag (GitHub Pages banner)
    event.add_tag("image", "https://grumpified-oggvct.github.io/ollama_pulse/assets/banner.png")
    
    # Category/Subject tags for SEO
    event.add_tag("subject", "AI Development")
    event.add_tag("subject", "Ollama Ecosystem")
    event.add_tag("category", "Technology")
    event.add_tag("category", "Artificial Intelligence")
    
    # Viral hashtags (t tags)
    for tag in VIRAL_HASHTAGS:
        event.add_tag("t", tag.lower())
    
    # SEO keywords (custom tags)
    for keyword in SEO_KEYWORDS[:5]:  # Limit to top 5 to avoid spam
        event.add_tag("keyword", keyword)
    
    # Author/Publisher info
    event.add_tag("author", "EchoVein Oracle")
    event.add_tag("published_by", "Ollama Pulse")
    
    # Links
    event.add_tag("r", "https://grumpified-oggvct.github.io/ollama_pulse")
    event.add_tag("r", "https://github.com/Grumpified-OGGVCT/ollama_pulse")
    
    # Donation links (zap-enabled)
    event.add_tag("donation", "https://ko-fi.com/grumpified")
    event.add_tag("lightning", "lnbc1...")  # Add actual Lightning address if available
    
    # Sign the event
    private_key.sign_event(event)
    
    return event


def publish_to_relays(event, relays=RELAYS):
    """Publish event to multiple Nostr relays"""
    relay_manager = RelayManager()
    
    # Add all relays
    for relay_url in relays:
        try:
            relay_manager.add_relay(relay_url)
            print(f"✓ Connected to {relay_url}")
        except Exception as e:
            print(f"✗ Failed to connect to {relay_url}: {e}")
    
    # Publish event
    print(f"\n📡 Publishing event {event.id[:16]}...")
    relay_manager.publish_event(event)
    
    # Wait for confirmations
    time.sleep(5)
    
    # Check for OK messages
    success_count = 0
    while relay_manager.message_pool.has_ok_notices():
        ok_msg = relay_manager.message_pool.get_ok_notice()
        if ok_msg.event_id == event.id:
            success_count += 1
            print(f"✓ Published to relay (confirmation {success_count})")
    
    # Close connections
    relay_manager.close_all_relay_connections()
    
    return success_count


def generate_nostr_links(event):
    """Generate shareable Nostr links"""
    note_id = event.id
    npub = event.public_key
    
    # Nostr client links
    links = {
        "Damus": f"nostr:note1{note_id}",
        "Snort": f"https://snort.social/e/{note_id}",
        "Iris": f"https://iris.to/{note_id}",
        "Nostrudel": f"https://nostrudel.ninja/#/n/{note_id}",
        "Primal": f"https://primal.net/e/{note_id}"
    }
    
    return links


def main():
    print("🌐 Ollama Pulse - Nostr NIP-23 Publisher\n")
    
    # Load private key
    print("🔑 Loading Nostr identity...")
    private_key = load_private_key()
    npub = private_key.public_key.bech32()
    print(f"✓ Publishing as: {npub}\n")
    
    # Load today's report
    print("📄 Loading today's report...")
    title, content = get_today_report()
    
    if not content:
        print("ERROR: No report to publish")
        return 1
    
    print(f"✓ Loaded: {title}")
    print(f"✓ Content length: {len(content)} characters\n")
    
    # Create NIP-23 event
    print("📝 Creating NIP-23 long-form event...")
    event = create_nip23_event(private_key, title, content)
    print(f"✓ Event ID: {event.id}")
    print(f"✓ Hashtags: {', '.join(['#' + t for t in VIRAL_HASHTAGS[:8]])}")
    print(f"✓ Keywords: {', '.join(SEO_KEYWORDS[:3])}\n")
    
    # Publish to relays
    print("🚀 Publishing to Nostr relays...")
    success_count = publish_to_relays(event)
    
    print(f"\n✅ Published to {success_count}/{len(RELAYS)} relays")
    
    # Generate shareable links
    print("\n🔗 Shareable links:")
    links = generate_nostr_links(event)
    for client, url in links.items():
        print(f"  {client}: {url}")
    
    # Save publication record
    record_file = Path(f"../data/nostr/published-{datetime.now().strftime('%Y-%m-%d')}.json")
    record_file.parent.mkdir(parents=True, exist_ok=True)
    
    record = {
        "event_id": event.id,
        "npub": npub,
        "title": title,
        "published_at": datetime.now().isoformat(),
        "relays": RELAYS,
        "success_count": success_count,
        "hashtags": VIRAL_HASHTAGS,
        "keywords": SEO_KEYWORDS,
        "links": links
    }
    
    with open(record_file, 'w', encoding='utf-8') as f:
        json.dump(record, f, indent=2)
    
    print(f"\n💾 Publication record saved to {record_file}")
    print("\n🎉 Nostr publication complete!")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())

