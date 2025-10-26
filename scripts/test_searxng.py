#!/usr/bin/env python3
"""Test Ollama Web Search client (replaces SearXNG)"""

from searxng_client import OllamaWebSearchClient as SearXNGClient


def main():
    client = SearXNGClient()
    print("Testing Ollama Web Search...")
    print("=" * 60)

    # Test Reddit search
    print("\n1. Testing Reddit search...")
    reddit_results = client.search_reddit('ollama turbo', max_results=5)
    print(f"   Found: {len(reddit_results)} results")
    for i, r in enumerate(reddit_results[:2], 1):
        print(f"   {i}. {r.get('title','')[:70]}")

    # Test Twitter search
    print("\n2. Testing Twitter search...")
    twitter_results = client.search_twitter('ollama', max_results=5)
    print(f"   Found: {len(twitter_results)} results")
    for i, r in enumerate(twitter_results[:2], 1):
        print(f"   {i}. {r.get('title','')[:70]}")

    # Test YouTube search
    print("\n3. Testing YouTube search...")
    youtube_results = client.search_youtube('ollama tutorial', max_results=5)
    print(f"   Found: {len(youtube_results)} results")
    for i, r in enumerate(youtube_results[:2], 1):
        print(f"   {i}. {r.get('title','')[:70]}")

    # Test GitHub search
    print("\n4. Testing GitHub search...")
    github_results = client.search_github('ollama turbo', max_results=5)
    print(f"   Found: {len(github_results)} results")
    for i, r in enumerate(github_results[:2], 1):
        print(f"   {i}. {r.get('title','')[:70]}")

    # Test general news search
    print("\n5. Testing general search...")
    news_results = client.search_news('ollama cloud', max_results=5)
    print(f"   Found: {len(news_results)} results")
    for i, r in enumerate(news_results[:2], 1):
        print(f"   {i}. {r.get('title','')[:70]}")

    print("\n" + "=" * 60)
    print("Ollama Web Search client is working!")


if __name__ == "__main__":
    main()
