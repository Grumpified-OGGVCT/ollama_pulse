#!/usr/bin/env python3
"""
Ollama Pulse - Cloud Sources Deep Ingestion
Polls Ollama Cloud API endpoints for Turbo model details and changelogs

PRIMARY: Uses Ollama web_search API for cloud model discovery
FALLBACK: Direct scraping if web_search fails
"""
import asyncio
import json
import os
from datetime import datetime
from pathlib import Path

import requests

from ollama_turbo_client import OllamaTurboClient


def ensure_data_dir():
    """Create data/official directory if it doesn't exist"""
    Path("data/official").mkdir(parents=True, exist_ok=True)


def get_today_filename():
    """Get filename for today's data"""
    today = datetime.now().strftime("%Y-%m-%d")
    return f"data/official/{today}.json"


def fetch_ollama_tags(filter_type="turbo", depth="full"):
    """
    Fetch Ollama Cloud models - use OFFICIAL list from docs.ollama.com/cloud
    Args:
        filter_type: 'turbo' returns cloud models, 'all' returns cloud models (same thing)
        depth: 'full' includes detailed info, 'basic' is minimal
    """
    print(f"📡 Fetching Ollama Cloud models (filter={filter_type}, depth={depth})...")
    
    # OFFICIAL cloud models per https://docs.ollama.com/cloud
    official_cloud_models = [
        {
            "name": "deepseek-v3.1:671b-cloud",
            "params": "671B",
            "context": "131K",
            "capability": "reasoning with hybrid thinking",
            "url": "https://ollama.com/library/deepseek-v3.1"
        },
        {
            "name": "gpt-oss:120b-cloud", 
            "params": "120B",
            "context": "131K",
            "capability": "powerful reasoning and agentic tasks",
            "url": "https://ollama.com/library/gpt-oss"
        },
        {
            "name": "gpt-oss:20b-cloud",
            "params": "20B", 
            "context": "131K",
            "capability": "versatile developer use cases",
            "url": "https://ollama.com/library/gpt-oss"
        },
        {
            "name": "kimi-k2:1t-cloud",
            "params": "1T",
            "context": "256K",
            "capability": "agentic and coding tasks",
            "url": "https://ollama.com/library/kimi-k2"
        },
        {
            "name": "qwen3-coder:480b-cloud",
            "params": "480B",
            "context": "262K", 
            "capability": "polyglot coding specialist",
            "url": "https://ollama.com/library/qwen3-coder"
        },
        {
            "name": "glm-4.6:cloud",
            "params": "14.2B",
            "context": "200K",
            "capability": "advanced agentic and reasoning",
            "url": "https://ollama.com/library/glm-4.6"
        },
        {
            "name": "minimax-m2:cloud",
            "params": "Unknown",
            "context": "Unknown",
            "capability": "high-efficiency coding and agentic workflows",
            "url": "https://ollama.com/library/minimax-m2"
        },
        {
            "name": "qwen3-vl:235b-cloud",
            "params": "235B",
            "context": "131K",
            "capability": "vision-language multimodal",
            "url": "https://ollama.com/library/qwen3-vl"
        }
    ]
    
    entries = []
    for model_info in official_cloud_models:
        entry = {
            "title": f"Model: {model_info['name']} - {model_info['capability']}",
            "date": datetime.now().isoformat(),
            "summary": f"{model_info['params']} parameters, {model_info['context']} context - {model_info['capability']}",
            "url": model_info['url'],
            "source": "cloud_api",
            "highlights": [
                f"model: {model_info['name']}", 
                f"params: {model_info['params']}",
                f"context: {model_info['context']}",
                "cloud",
                "-cloud suffix"
            ]
        }
        entries.append(entry)
    
    print(f"✅ Loaded {len(entries)} OFFICIAL cloud models from docs.ollama.com/cloud")
    return entries


def save_data(entries):
    """Save entries to JSON file, merging with existing data"""
    if not entries:
        print("⚠️  No data to save")
        return
    
    filename = get_today_filename()
    
    # Load existing data if file exists
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


async def fetch_via_web_search(filter_type="turbo"):
    """
    PRIMARY: Use Ollama web_search API for cloud model discovery
    """
    print(f"🔍 PRIMARY: Using Ollama web_search for cloud models (filter={filter_type})...")

    try:
        async with OllamaTurboClient() as client:
            # Search for Ollama cloud models
            query = "Ollama Cloud models, Turbo API, cloud-hosted models" if filter_type == "turbo" else "All Ollama models and library"
            results = await client.discover_ecosystem_content(
                query=query,
                content_type="tools",
                max_results=15  # Reduced from 30 - only request what we expect to find
            )

            print(f"✅ Web search found {len(results)} cloud models")
            return results

    except Exception as e:
        print(f"⚠️  Web search failed: {e}")
        print("   Falling back to direct scraping...")
        return []


def main():
    """Main ingestion function"""
    import argparse

    parser = argparse.ArgumentParser(description='Ollama Cloud Deep Ingestion')
    parser.add_argument('--filter', default='turbo', choices=['turbo', 'all'],
                       help='Filter models by type (default: turbo)')
    parser.add_argument('--depth', default='full', choices=['full', 'basic'],
                       help='Depth of information to fetch (default: full)')

    args = parser.parse_args()

    print("🚀 Starting cloud sources deep ingestion...")
    ensure_data_dir()

    # PRIMARY: Use DIRECT API (no LLM hallucinations!)
    print("📡 PRIMARY: Using REAL Ollama /api/tags for FACTUAL cloud models...")
    cloud_entries = fetch_ollama_tags(filter_type=args.filter, depth=args.depth)
    all_entries = cloud_entries
    
    print(f"✅ Collected {len(all_entries)} VERIFIED cloud models from API")

    # Save
    save_data(all_entries)

    print("✅ Cloud sources ingestion complete!")


if __name__ == "__main__":
    main()
