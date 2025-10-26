#!/usr/bin/env python3
"""Test SearXNG instances"""

import requests
import json

instances = [
    'https://search.privacyguide.org',
    'https://searx.be',
    'https://searxng.site',
    'https://searx.space',
    'https://searx.info'
]

print("Testing SearXNG instances for JSON API support...")
print("=" * 70)

for instance in instances:
    try:
        print(f"\nTesting: {instance}")
        response = requests.get(
            f"{instance}/search",
            params={"q": "ollama", "format": "json"},
            timeout=5,
            headers={"User-Agent": "OllamaPulse/1.0"}
        )
        print(f"  Status: {response.status_code}")
        print(f"  Content-Type: {response.headers.get('content-type', 'unknown')}")
        print(f"  Response length: {len(response.text)}")
        
        if response.status_code == 200:
            try:
                data = response.json()
                results = data.get('results', [])
                print(f"  ✅ JSON parsed successfully")
                print(f"  Results found: {len(results)}")
                if results:
                    print(f"  Sample: {results[0].get('title', 'N/A')[:60]}")
            except json.JSONDecodeError as e:
                print(f"  ❌ JSON parse error: {str(e)[:50]}")
                print(f"  First 100 chars: {response.text[:100]}")
        else:
            print(f"  ❌ HTTP error")
    
    except requests.Timeout:
        print(f"  ❌ Timeout")
    except Exception as e:
        print(f"  ❌ Error: {str(e)[:50]}")

print("\n" + "=" * 70)

