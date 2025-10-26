#!/usr/bin/env python3
"""
Ollama Pulse - Discord Ingestion (15th Data Source)
Tracks Ollama discussions from Discord servers (requires webhook/bot setup)
"""
import json
from datetime import datetime
from pathlib import Path

def ensure_data_dir():
    Path("data/discord").mkdir(parents=True, exist_ok=True)

def get_today_filename():
    return f"data/discord/{datetime.now().strftime('%Y-%m-%d')}.json"

def fetch_discord_placeholder():
    """
    Placeholder for Discord integration
    
    To enable Discord ingestion:
    1. Create a Discord bot at https://discord.com/developers/applications
    2. Add bot to Ollama-related servers
    3. Use discord.py library to fetch messages
    4. Filter for Ollama-related keywords
    
    For now, returns empty list
    """
    print("📡 Discord ingestion (placeholder - requires bot setup)")
    print("   To enable: Set up Discord bot and add DISCORD_BOT_TOKEN to secrets")
    
    # Placeholder - would fetch from Discord API
    entries = []
    
    # Example structure for when implemented:
    # entries = [
    #     {
    #         "title": "Discord: User discussion about Ollama",
    #         "date": datetime.now().isoformat(),
    #         "summary": "Message content...",
    #         "url": "https://discord.com/channels/...",
    #         "source": "discord",
    #         "turbo_score": 0.6,
    #         "highlights": ["community", "discord"]
    #     }
    # ]
    
    return entries

def save_data(entries):
    """Save entries to JSON file"""
    if not entries:
        print("⚠️  No Discord data to save (bot not configured)")
        return
    
    filename = get_today_filename()
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(entries, f, indent=2, ensure_ascii=False)
    
    print(f"💾 Saved {len(entries)} entries to {filename}")

def main():
    """Main ingestion function"""
    print("🚀 Starting Discord ingestion...")
    ensure_data_dir()
    
    entries = fetch_discord_placeholder()
    
    if entries:
        save_data(entries)
    else:
        print("ℹ️  Discord ingestion skipped (requires bot configuration)")
    
    print("✅ Discord ingestion complete!")

if __name__ == "__main__":
    main()

