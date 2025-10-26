"""
Ollama Web Search Integration for Ollama Pulse
Uses Ollama's native web search API (https://docs.ollama.com/capabilities/web-search)
Handles ALL online searches with fallback to free APIs
"""

import requests
import json
import os
from typing import List, Dict, Optional
from datetime import datetime

class OllamaWebSearchClient:
    """
    Ollama Web Search Integration
    Uses Ollama's official web search API: https://ollama.com/api/web_search
    Requires OLLAMA_API_KEY environment variable
    """

    def __init__(self, api_key: Optional[str] = None, timeout=10):
        self.api_key = api_key or os.getenv("OLLAMA_API_KEY")
        self.timeout = timeout
        self.base_url = "https://ollama.com/api"

        if not self.api_key:
            print("⚠️  OLLAMA_API_KEY not set - web search will be limited")
        else:
            print("✅ Ollama Web Search API initialized")

    def search(self, query: str, max_results: int = 5) -> List[Dict]:
        """
        Search using Ollama's web search API

        Args:
            query: Search query
            max_results: Max results to return (default 5, max 10)

        Returns:
            List of search results with title, url, content
        """
        if not self.api_key:
            print(f"⚠️  OLLAMA_API_KEY not set - cannot perform web search")
            return []

        try:
            response = requests.post(
                f"{self.base_url}/web_search",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "query": query,
                    "max_results": min(max_results, 10)
                },
                timeout=self.timeout
            )

            if response.status_code == 200:
                data = response.json()
                results = []

                for item in data.get('results', []):
                    results.append({
                        "title": item.get('title', ''),
                        "url": item.get('url', ''),
                        "summary": item.get('content', '')[:300],
                        "source": "ollama_web_search",
                        "date": datetime.now().isoformat()
                    })

                print(f"✅ Ollama Web Search: Found {len(results)} results for '{query}'")
                return results
            else:
                print(f"⚠️  Ollama Web Search error: {response.status_code}")
                return []

        except Exception as e:
            print(f"⚠️  Ollama Web Search failed: {e}")
            return []

    def search_reddit(self, query: str, max_results: int = 5) -> List[Dict]:
        """Search Reddit"""
        return self.search(f"{query} site:reddit.com", max_results=max_results)

    def search_twitter(self, query: str, max_results: int = 5) -> List[Dict]:
        """Search Twitter/X"""
        return self.search(f"{query} site:twitter.com", max_results=max_results)

    def search_youtube(self, query: str, max_results: int = 5) -> List[Dict]:
        """Search YouTube"""
        return self.search(f"{query} site:youtube.com", max_results=max_results)

    def search_github(self, query: str, max_results: int = 5) -> List[Dict]:
        """Search GitHub"""
        return self.search(f"{query} site:github.com", max_results=max_results)

    def search_news(self, query: str, max_results: int = 5) -> List[Dict]:
        """Search news"""
        return self.search(query, max_results=max_results)

    def web_fetch(self, url: str) -> Optional[Dict]:
        """
        Fetch and parse a web page using Ollama's web fetch API

        Args:
            url: URL to fetch

        Returns:
            Dict with title, content, and links
        """
        if not self.api_key:
            print(f"⚠️  OLLAMA_API_KEY not set - cannot fetch web page")
            return None

        try:
            response = requests.post(
                f"{self.base_url}/web_fetch",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                },
                json={"url": url},
                timeout=self.timeout
            )

            if response.status_code == 200:
                data = response.json()
                print(f"✅ Ollama Web Fetch: Retrieved {url}")
                return data
            else:
                print(f"⚠️  Ollama Web Fetch error: {response.status_code}")
                return None

        except Exception as e:
            print(f"⚠️  Ollama Web Fetch failed: {e}")
            return None


# Convenience functions
def search_all(query: str, max_results: int = 5) -> List[Dict]:
    """General search using Ollama Web Search API"""
    client = OllamaWebSearchClient()
    return client.search(query, max_results=max_results)

def search_reddit(query: str, max_results: int = 5) -> List[Dict]:
    """Search Reddit"""
    client = OllamaWebSearchClient()
    return client.search_reddit(query, max_results=max_results)

def search_twitter(query: str, max_results: int = 5) -> List[Dict]:
    """Search Twitter/X"""
    client = OllamaWebSearchClient()
    return client.search_twitter(query, max_results=max_results)

def search_youtube(query: str, max_results: int = 5) -> List[Dict]:
    """Search YouTube"""
    client = OllamaWebSearchClient()
    return client.search_youtube(query, max_results=max_results)

def search_github(query: str, max_results: int = 5) -> List[Dict]:
    """Search GitHub"""
    client = OllamaWebSearchClient()
    return client.search_github(query, max_results=max_results)

def search_news(query: str, max_results: int = 5) -> List[Dict]:
    """Search news"""
    client = OllamaWebSearchClient()
    return client.search_news(query, max_results=max_results)

def web_fetch(url: str) -> Optional[Dict]:
    """Fetch and parse a web page"""
    client = OllamaWebSearchClient()
    return client.web_fetch(url)

# Backwards compatibility alias for old tests/imports
SearXNGClient = OllamaWebSearchClient


