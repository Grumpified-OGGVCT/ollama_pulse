#!/usr/bin/env python3
"""
Direct test of the model pipeline to see what's actually working
"""
import os
import asyncio

# Set API key
os.environ['OLLAMA_API_KEY'] = os.getenv('OLLAMA_API_KEY', 'YOUR_KEY_HERE')

print("="*60)
print("MODEL PIPELINE DIAGNOSTIC TEST")
print("="*60)

# Test 1: Can we import?
print("\nTest 1: Imports")
try:
    from enhanced_report_generator import enhance_report_with_models, EnhancedReportGenerator
    print("✅ enhanced_report_generator.py imports successfully")
except Exception as e:
    print(f"❌ IMPORT FAILED: {e}")
    exit(1)

# Test 2: Can we create client?
print("\nTest 2: Ollama Client")
try:
    from ollama_turbo_client import OllamaTurboClient
    print("✅ OllamaTurboClient imports successfully")
except Exception as e:
    print(f"❌ CLIENT IMPORT FAILED: {e}")
    exit(1)

# Test 3: Can we select models?
print("\nTest 3: Model Selection")
try:
    from model_registry import select_model_for_task
    
    analysis_model = select_model_for_task("analysis", requires_reasoning=True)
    synthesis_model = select_model_for_task("synthesis", requires_reasoning=True)
    research_model = select_model_for_task("research", requires_long_context=True)
    
    print(f"✅ Analysis model: {analysis_model}")
    print(f"✅ Synthesis model: {synthesis_model}")  
    print(f"✅ Research model: {research_model}")
except Exception as e:
    print(f"❌ MODEL SELECTION FAILED: {e}")
    exit(1)

# Test 4: Can we actually call a model?
print("\nTest 4: Live API Call")

async def test_api_call():
    try:
        async with OllamaTurboClient() as client:
            response = await client.generate(
                model="gpt-oss:20b-cloud",  # Fastest model
                prompt="Say 'MODELS ARE WORKING' in exactly those words.",
                max_tokens=50,
                temperature=0.1
            )
            
            if "MODELS ARE WORKING" in response or "working" in response.lower():
                print(f"✅ API CALL SUCCESSFUL!")
                print(f"   Response: {response[:200]}")
                return True
            else:
                print(f"⚠️ API returned unexpected response:")
                print(f"   {response[:200]}")
                return False
                
    except Exception as e:
        print(f"❌ API CALL FAILED: {e}")
        return False

# Run test
if asyncio.run(test_api_call()):
    print("\n" + "="*60)
    print("✅ ALL TESTS PASSED - Models should be working!")
    print("="*60)
else:
    print("\n" + "="*60)
    print("❌ API TEST FAILED - Models are NOT working")
    print("="*60)

