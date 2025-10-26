#!/usr/bin/env python3
"""
Ollama Turbo Client for Ollama Pulse

Enhanced with capabilities for reliable data gathering:
- Web Search: Fallback when GitHub API fails
- Structured Outputs: Clean JSON for model/tool metadata
- Rate limiting: Avoid API throttling

Author: Ollama Pulse Intelligence Team
"""

import aiohttp
import asyncio
import json
import os
from typing import List, Dict, Optional
from datetime import datetime
from model_registry import select_model_for_task, select_model_by_complexity, TaskComplexity


class OllamaTurboClient:
    """
    Ollama Cloud API Client optimized for Ollama ecosystem monitoring

    Works in GitHub Actions and locally
    Uses Ollama Cloud API (https://cloud.ollama.ai)
    """

    def __init__(self, api_key: Optional[str] = None, base_url: str = "https://cloud.ollama.ai"):
        self.api_key = api_key or os.getenv("OLLAMA_API_KEY") or os.getenv("OLLAMA_TURBO_CLOUD_API_KEY") or os.getenv("OLLAMA_TURBO_CLOUD_API_KEY_1") or os.getenv("OLLAMA_TURBO_CLOUD_API_KEY_2")
        self.base_url = base_url
        self.session: Optional[aiohttp.ClientSession] = None

    async def __aenter__(self):
        self.session = aiohttp.ClientSession(
            headers={
                'Authorization': f'Bearer {self.api_key}',
                'Content-Type': 'application/json'
            }
        )
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    async def check_model_availability(self) -> List[str]:
        """
        Preflight check: GET /v1/models to verify available models (OpenAI-compatible)

        Returns:
            List of available model IDs
        """
        try:
            url = f"{self.base_url}/v1/models"
            async with self.session.get(url) as response:
                response.raise_for_status()
                data = await response.json()
                models = data.get("data", [])
                model_ids = [m.get("id", "") for m in models]
                return model_ids
        except Exception as e:
            print(f"⚠️  /v1/models preflight check failed: {e}")
            return []

    def get_fallback_model(self, requested_model: str, available_models: List[str]) -> str:
        """
        Get fallback model based on documented fallback chains

        Fallback chains:
        - DeepSeek ↔ GPT-OSS 120B
        - Kimi-K2 ↔ DeepSeek
        - GPT-OSS 20B ↔ GLM-4.6
        - Qwen3-VL → skip gracefully (no fallback)

        Args:
            requested_model: The model that was requested
            available_models: List of available model IDs from /api/tags

        Returns:
            Fallback model ID or requested model if no fallback needed
        """
        # Define fallback chains
        fallback_chains = {
            "deepseek-v3.1:671b-cloud": "gpt-oss:120b-cloud",
            "gpt-oss:120b-cloud": "deepseek-v3.1:671b-cloud",
            "kimi-k2:1t-cloud": "deepseek-v3.1:671b-cloud",
            "gpt-oss:20b-cloud": "glm-4.6:cloud",
            "glm-4.6:cloud": "gpt-oss:20b-cloud",
        }

        # If requested model is available, use it
        if requested_model in available_models:
            return requested_model

        # If Qwen3-VL is unavailable, skip gracefully (return None)
        if "qwen3-vl" in requested_model.lower():
            print(f"⚠️  Vision model {requested_model} unavailable - skipping gracefully")
            return None

        # Try fallback chain
        fallback = fallback_chains.get(requested_model)
        if fallback and fallback in available_models:
            print(f"ℹ️  Using fallback: {requested_model} → {fallback}")
            return fallback

        # If no fallback available, return requested model anyway (will fail later)
        print(f"⚠️  No fallback available for {requested_model}")
        return requested_model

    def resolve_model(self, task_type: str, **flags) -> str:
        """Resolve optimal model using the centralized registry."""
        try:
            return select_model_for_task(task_type, **flags)
        except Exception:
            return flags.get("fallback", "gpt-oss:120b-cloud")

    def resolve_model_by_complexity(self, complexity: "TaskComplexity", task_type: str = "general", **flags) -> str:
        """Resolve model using complexity-based selection via registry."""
        try:
            return select_model_by_complexity(
                complexity,
                task_type,
                flags.get("has_visual_input", False),
                flags.get("requires_coding", False),
            )
        except Exception:
            return flags.get("fallback", "gpt-oss:20b-cloud")

    async def generate(
        self,
        model: str,
        prompt: str,
        max_tokens: int = 1000,
        temperature: float = 0.7,
        web_search: bool = False,
        structured_output: Optional[Dict] = None
    ) -> str:
        """
        Generate text using Ollama Cloud

        Args:
            model: Model name (e.g., 'deepseek-v3.1:671b-cloud')
            prompt: Text prompt
            max_tokens: Maximum tokens to generate
            temperature: Sampling temperature
            web_search: Enable web search capability (fallback)
            structured_output: JSON schema for structured response

        Returns:
            Generated text or JSON string
        """

        url = f"{self.base_url}/v1/chat/completions"

        payload = {
            'model': model,
            'messages': [{'role': 'user', 'content': prompt}],
            'max_tokens': max_tokens,
            'temperature': temperature
        }

        # Enable web search as fallback (if supported)
        if web_search:
            payload['web_search'] = True

        # Enable structured outputs for clean data
        if structured_output:
            payload['response_format'] = {"type": "json_object", "schema": structured_output}

        async with self.session.post(url, json=payload) as response:
            response.raise_for_status()
            data = await response.json()
            return data['choices'][0]['message']['content']

    async def web_search_fallback(
        self,
        query: str,
        max_tokens: int = 2000
    ) -> str:
        """
        Web search fallback when GitHub API fails

        Args:
            query: Search query (e.g., "Latest Ollama models and tools")
            max_tokens: Max response length

        Returns:
            Synthesized search results
        """
        # Use Kimi-K2 for web search synthesis (66.1% Tau-Bench - Agentic Leader)
        # Best for connecting diverse sources and long-form synthesis
        model_id = select_model_for_task("research", requires_long_context=True)
        return await self.generate(
            model=model_id,
            prompt=query,
            max_tokens=max_tokens,
            temperature=0.7,
            web_search=True
        )

    async def discover_ecosystem_content(
        self,
        query: str,
        content_type: str = "general",
        max_results: int = 20
    ) -> List[Dict]:
        """
        PRIMARY discovery method using Ollama web_search API

        Replaces direct API calls to GitHub, Reddit, etc. with AI-powered web search
        that can find content across ALL sources intelligently.

        Args:
            query: Natural language search query
            content_type: Type of content (tools, discussions, tutorials, news)
            max_results: Maximum number of results to return

        Returns:
            List of discovered items with title, url, summary, source
        """
        # Select model based on task type
        model_id = self.resolve_model("research", requires_long_context=True)

        # Craft prompt for structured discovery
        prompt = f"""Search the web for: {query}

Content type: {content_type}
Focus on: Ollama ecosystem (models, tools, integrations, discussions)

Return EXACTLY {max_results} results as a JSON array with this structure:
[
  {{
    "title": "Project/Article title",
    "url": "https://...",
    "summary": "Brief description (1-2 sentences)",
    "source": "github|reddit|hackernews|youtube|blog",
    "date": "YYYY-MM-DD",
    "highlights": ["key", "features"]
  }}
]

IMPORTANT: Return ONLY the JSON array, no other text."""

        try:
            response = await self.generate(
                model=model_id,
                prompt=prompt,
                max_tokens=4000,
                temperature=0.5,
                web_search=True
            )

            # Parse JSON response
            results = json.loads(response)
            return results if isinstance(results, list) else []

        except Exception as e:
            print(f"⚠️  Web search discovery failed: {e}")
            return []

    async def vision_analysis(
        self,
        image_url: str,
        prompt: str,
        max_tokens: int = 1000
    ) -> str:
        """
        Analyze images using vision-capable model

        Uses OLLAMA_VISION_MODEL environment variable if set,
        defaults to qwen3-vl:235b-cloud

        Args:
            image_url: URL to the image to analyze
            prompt: Analysis prompt
            max_tokens: Maximum tokens to generate

        Returns:
            Analysis result
        """
        # Get vision model from environment or use default
        vision_model = os.getenv("OLLAMA_VISION_MODEL", "qwen3-vl:235b-cloud")

        # Check if vision model is available
        available_models = await self.check_model_availability()
        if available_models:
            vision_model = self.get_fallback_model(vision_model, available_models)

            # If vision model unavailable and no fallback, skip gracefully
            if vision_model is None:
                print("⚠️  Vision model unavailable - skipping vision analysis")
                return ""

        try:
            url = f"{self.base_url}/api/chat"

            payload = {
                'model': vision_model,
                'messages': [
                    {
                        'role': 'user',
                        'content': prompt,
                        'images': [image_url]
                    }
                ],
                'stream': False,
                'options': {
                    'num_predict': max_tokens
                }
            }

            async with self.session.post(url, json=payload) as response:
                response.raise_for_status()
                data = await response.json()
                return data['message']['content']

        except Exception as e:
            print(f"⚠️  Vision analysis failed: {e}")
            return ""

    async def extract_structured_metadata(
        self,
        text: str,
        schema: Dict,
        model: str = 'deepseek-v3.1:671b-cloud'
    ) -> Dict:
        """
        Extract structured metadata from unstructured text

        Args:
            text: Unstructured text (e.g., GitHub README)
            schema: JSON schema for output
            model: Model to use

        Returns:
            Parsed JSON matching schema
        """

        prompt = f"""Extract structured information from this text:

{text}

Return ONLY valid JSON matching the schema."""

        response = await self.generate(
            model=model,
            prompt=prompt,
            max_tokens=1000,
            temperature=0.3,  # Lower temp for structured extraction
            structured_output=schema
        )

        return json.loads(response)

    async def analyze_ollama_project(
        self,
        project_name: str,
        description: str,
        stars: int,
        language: str
    ) -> Dict:
        """
        Analyze Ollama ecosystem project with structured output

        Args:
            project_name: Project name
            description: Project description
            stars: GitHub stars
            language: Programming language

        Returns:
            Structured analysis
        """

        prompt = f"""Analyze this Ollama ecosystem project:

Name: {project_name}
Description: {description}
Stars: {stars}
Language: {language}

Provide:
1. Category (model, tool, integration, ui, etc.)
2. Use case (what problem it solves)
3. Maturity level (experimental, emerging, stable, mature)
4. Target audience (developers, researchers, end-users)
5. Key features (list of main capabilities)"""

        schema = {
            "type": "object",
            "properties": {
                "category": {"type": "string"},
                "use_case": {"type": "string"},
                "maturity": {"type": "string", "enum": ["experimental", "emerging", "stable", "mature"]},
                "audience": {"type": "array", "items": {"type": "string"}},
                "features": {"type": "array", "items": {"type": "string"}}
            }
        }

        model_id = select_model_for_task("analysis", requires_reasoning=True)
        response = await self.generate(
            model=model_id,
            prompt=prompt,
            max_tokens=800,
            temperature=0.5,
            structured_output=schema
        )

        return json.loads(response)

    async def iterative_research_workflow(
        self,
        initial_query: str,
        max_iterations: int = 3,
        effort_level: str = "medium"
    ) -> Dict:
        """
        Self-iterative research workflow using GPT-OSS 120B

        Uses GPT-OSS 120B's built-in self-iterative capabilities:
        - Configurable effort levels (low/medium/high)
        - RLHF-tuned reasoning traces for transparency
        - Iterative refinement with explainable steps

        Args:
            initial_query: Research question or task
            max_iterations: Number of refinement iterations
            effort_level: "low", "medium", or "high" reasoning effort

        Returns:
            Dict with final_output, reasoning_trace, iterations
        """

        prompt = f"""Research Task: {initial_query}

Effort Level: {effort_level}
Max Iterations: {max_iterations}

Use your self-iterative capabilities to:
1. Generate initial analysis
2. Critique and identify gaps
3. Refine iteratively
4. Provide final synthesis with full reasoning trace

Show your work at each step."""

        schema = {
            "type": "object",
            "properties": {
                "final_output": {"type": "string"},
                "reasoning_trace": {"type": "array", "items": {"type": "string"}},
                "iterations_used": {"type": "integer"},
                "confidence_score": {"type": "number"}
            }
        }

        model_id = select_model_for_task("synthesis")
        response = await self.generate(
            model=model_id,
            prompt=prompt,
            max_tokens=3000,
            temperature=0.7,
            structured_output=schema
        )

        return json.loads(response)

    async def embed_batch(
        self,
        model: str,
        texts: List[str],
        delay: float = 0.5
    ) -> List[List[float]]:
        """
        Generate embeddings with rate limiting

        Args:
            model: Embedding model (e.g., 'nomic-embed-text')
            texts: List of texts to embed
            delay: Delay between requests (seconds)

        Returns:
            List of embedding vectors
        """
        embeddings = []

        for text in texts:
            url = f"{self.base_url}/api/embeddings"
            payload = {'model': model, 'prompt': text}

            async with self.session.post(url, json=payload) as response:
                response.raise_for_status()
                data = await response.json()
                embeddings.append(data['embedding'])

            # Rate limiting
            await asyncio.sleep(delay)

        return embeddings


# Recommended models for Ollama Pulse (Based on verified 2025 benchmarks + capabilities)
MODELS = {
    # STRUCTURED EXTRACTION - DeepSeek-V3.1 (81.0% GPQA - Group Leader in Science)
    # Best for: Logical analysis, structured data extraction, toggleable Think mode
    'structured_extraction': 'deepseek-v3.1:671b-cloud',

    # WEB SEARCH SYNTHESIS - Kimi-K2 (66.1% Tau-Bench - Agentic Leader)
    # Best for: Connecting diverse sources, long-form synthesis, 256K→1M context
    'web_search': 'kimi-k2:1t-cloud',

    # ITERATIVE RESEARCH/PLANNING - GPT-OSS 120B (97.9% AIME, 1320 Arena Elo)
    # Best for: Self-iterative workflows, template generation, explainable reasoning
    # Special: Configurable effort levels, RLHF-tuned reasoning traces, agent debugging
    'iterative_research': 'gpt-oss:120b-cloud',

    # FAST VALIDATION - GPT-OSS 20B (25-30 t/s - Group Fastest)
    # Best for: Quick fact-checking, rapid validation, high-volume screening
    'fast_validation': 'gpt-oss:20b-cloud',

    # CREATIVE WRITING - GLM-4.6 (Pragmatic, 200K context)
    # Best for: Writing summaries, pragmatic breakdowns, balanced perspectives
    'creative': 'glm-4.6:cloud',

    # EMBEDDINGS - Nomic Embed Text
    'embedding': 'nomic-embed-text'
}

