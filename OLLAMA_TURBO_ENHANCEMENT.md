# Ollama Turbo Enhancement for Ollama Pulse

## What Was Added

Enhanced Ollama Pulse with **Ollama Turbo capabilities** specifically optimized for reliable data gathering:

### 1. **Web Search** - Fallback When GitHub API Fails
- **Model**: `deepseek-v3.1:671b-cloud`
- **Use**: When GitHub API rate limits or fails
- **Method**: `web_search_fallback(query)`
- **Example**: "Latest Ollama models and tools released"

### 2. **Structured Outputs** - Clean Model/Tool Metadata
- **Use**: Extract structured data from GitHub READMEs
- **Method**: `extract_structured_metadata(text, schema)`
- **Example**: Parse project metadata into clean JSON

### 3. **Project Analysis** - Categorize Ollama Projects
- **Use**: Analyze and categorize Ollama ecosystem projects
- **Method**: `analyze_ollama_project(name, description, stars, language)`
- **Returns**: Category, use case, maturity, audience, features

### 4. **Rate Limiting** - Avoid API Throttling
- **Built-in delays** between requests
- **Exponential backoff** on failures
- **Configurable** delay times

## New File

**`scripts/ollama_turbo_client.py`** - Complete Ollama Turbo client with:
- `OllamaTurboClient` class
- Ollama-specific helper methods
- Recommended models for different tasks

## How to Use

### Basic Usage

```python
from ollama_turbo_client import OllamaTurboClient, MODELS
import os

api_key = os.getenv('OLLAMA_CLOUD_API_KEY')

async with OllamaTurboClient(api_key) as client:
    # Web search fallback
    results = await client.web_search_fallback(
        "Latest Ollama models and tools"
    )
    
    # Analyze a project
    analysis = await client.analyze_ollama_project(
        project_name="ollama-webui",
        description="Web interface for Ollama",
        stars=1500,
        language="Python"
    )
    
    # Extract structured metadata
    metadata = await client.extract_structured_metadata(
        text=readme_content,
        schema={
            "type": "object",
            "properties": {
                "category": {"type": "string"},
                "features": {"type": "array"}
            }
        }
    )
```

### Integration with Existing Scripts

Add to ingestion scripts as fallback:

```python
# At top of file
from ollama_turbo_client import OllamaTurboClient, MODELS

# In main function
async with OllamaTurboClient(os.getenv('OLLAMA_CLOUD_API_KEY')) as client:
    try:
        # Try GitHub API first
        data = await fetch_from_github()
    except Exception as e:
        # Fallback to web search
        print(f"GitHub API failed: {e}")
        print("Using Ollama web search fallback...")
        data = await client.web_search_fallback(
            "Latest Ollama ecosystem updates"
        )
```

## GitHub Actions Setup

Add secret to repository:
1. Go to: https://github.com/Grumpified-OGGVCT/ollama_pulse/settings/secrets/actions
2. Click "New repository secret"
3. Name: `OLLAMA_CLOUD_API_KEY`
4. Value: `9b014e010c694d3ba5e266d6a306998c.O9OH8hhDlI32xxVAgpNNrETF`
5. Click "Add secret"

Update workflow files to use the secret:

```yaml
env:
  OLLAMA_CLOUD_API_KEY: ${{ secrets.OLLAMA_CLOUD_API_KEY }}
```

## Models Available

- **deepseek-v3.1:671b-cloud** - Analysis and structured extraction
- **qwen3-coder:30b-cloud** - Creative writing for summaries
- **nomic-embed-text** - Embeddings for clustering

## Benefits

1. **More Reliable** - Web search fallback when GitHub API fails
2. **Cleaner Data** - Structured outputs for project metadata
3. **Better Analysis** - Categorize and analyze projects automatically
4. **Rate Limiting** - Built-in delays to avoid throttling
5. **Works in CI** - Ollama Cloud API works in GitHub Actions

## Example: Enhanced Ingestion with Fallback

```python
async def ingest_with_fallback():
    """Ingest Ollama data with web search fallback"""
    
    async with OllamaTurboClient(os.getenv('OLLAMA_CLOUD_API_KEY')) as client:
        projects = []
        
        try:
            # Try GitHub API
            projects = await fetch_github_projects()
        except Exception as e:
            print(f"⚠️  GitHub API failed: {e}")
            print("🔍 Using web search fallback...")
            
            # Fallback to web search
            search_result = await client.web_search_fallback(
                "Latest Ollama models, tools, and integrations on GitHub"
            )
            
            # Parse search results into projects
            projects = parse_search_results(search_result)
        
        # Analyze each project with structured output
        for project in projects:
            analysis = await client.analyze_ollama_project(
                project_name=project['name'],
                description=project['description'],
                stars=project['stars'],
                language=project['language']
            )
            
            project['analysis'] = analysis
        
        return projects
```

## Next Steps

1. Add `OLLAMA_CLOUD_API_KEY` secret to GitHub
2. Integrate into ingestion scripts as fallback
3. Test with real data
4. Monitor usage and adjust delays as needed

---

**Status**: Ready to use
**Author**: Ollama Pulse Intelligence Team
**Date**: 2025-10-24

