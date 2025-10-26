#!/usr/bin/env python3
"""
CI Smoke Check for Ollama Pulse
Validates OLLAMA_API_KEY and API connectivity before running ingestion
"""

import os
import sys
import requests
from typing import Tuple


def check_api_key() -> Tuple[bool, str]:
    """Check if OLLAMA_API_KEY is set"""
    api_key = (
        os.getenv("OLLAMA_API_KEY") or 
        os.getenv("OLLAMA_TURBO_CLOUD_API_KEY") or 
        os.getenv("OLLAMA_TURBO_CLOUD_API_KEY_1") or 
        os.getenv("OLLAMA_TURBO_CLOUD_API_KEY_2")
    )
    
    if not api_key:
        return False, "❌ OLLAMA_API_KEY not found in environment"
    
    if len(api_key) < 20:
        return False, f"❌ OLLAMA_API_KEY appears invalid (too short: {len(api_key)} chars)"
    
    return True, f"✅ OLLAMA_API_KEY found ({len(api_key)} chars)"


def check_api_tags(api_key: str, base_url: str = "https://cloud.ollama.ai") -> Tuple[bool, str]:
    """Test GET /api/tags endpoint"""
    try:
        response = requests.get(
            f"{base_url}/api/tags",
            headers={"Authorization": f"Bearer {api_key}"},
            timeout=10
        )

        if response.status_code == 200:
            data = response.json()
            models = data.get("models", [])
            return True, f"✅ GET /api/tags successful ({len(models)} models available)"
        else:
            return False, f"❌ GET /api/tags failed: HTTP {response.status_code}"

    except requests.exceptions.Timeout:
        return False, "❌ GET /api/tags timeout (>10s)"
    except Exception as e:
        return False, f"❌ GET /api/tags error: {str(e)}"


def check_api_chat(api_key: str, base_url: str = "https://cloud.ollama.ai") -> Tuple[bool, str]:
    """Test POST /api/chat endpoint with simple message"""
    try:
        response = requests.post(
            f"{base_url}/api/chat",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            },
            json={
                "model": "gpt-oss:20b-cloud",
                "messages": [{"role": "user", "content": "ping"}],
                "stream": False,
                "options": {"num_predict": 10}
            },
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            message = data.get("message", {}).get("content", "")
            return True, f"✅ POST /api/chat successful (response: {len(message)} chars)"
        else:
            return False, f"❌ POST /api/chat failed: HTTP {response.status_code}"
            
    except requests.exceptions.Timeout:
        return False, "❌ POST /api/chat timeout (>30s)"
    except Exception as e:
        return False, f"❌ POST /api/chat error: {str(e)}"


def main():
    """Run all smoke checks"""
    print("🔍 Ollama Pulse CI Smoke Check")
    print("=" * 50)
    
    # Check 1: API Key
    success, message = check_api_key()
    print(f"\n1. API Key Check: {message}")
    if not success:
        print("\n💥 Smoke check FAILED - API key not configured")
        sys.exit(1)
    
    # Get API key for subsequent checks
    api_key = (
        os.getenv("OLLAMA_API_KEY") or 
        os.getenv("OLLAMA_TURBO_CLOUD_API_KEY") or 
        os.getenv("OLLAMA_TURBO_CLOUD_API_KEY_1") or 
        os.getenv("OLLAMA_TURBO_CLOUD_API_KEY_2")
    )
    
    # Check 2: /api/tags
    success, message = check_api_tags(api_key)
    print(f"\n2. API Tags Check: {message}")
    if not success:
        print("\n💥 Smoke check FAILED - API tags endpoint unreachable")
        sys.exit(1)
    
    # Check 3: /api/chat
    success, message = check_api_chat(api_key)
    print(f"\n3. API Chat Check: {message}")
    if not success:
        print("\n💥 Smoke check FAILED - API chat endpoint unreachable")
        sys.exit(1)
    
    print("\n" + "=" * 50)
    print("✅ All smoke checks PASSED - API is ready")
    print("=" * 50)
    sys.exit(0)


if __name__ == "__main__":
    main()

