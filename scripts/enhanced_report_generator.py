#!/usr/bin/env python3
"""
Enhanced Report Generator - FULL MODEL ACTIVATION
Uses multi-model pipeline with proper role assignments per benchmarks
"""
import asyncio
import json
import os
import random
from datetime import datetime
from typing import List, Dict
from ollama_turbo_client import OllamaTurboClient
from model_registry import select_model_for_task

class EnhancedReportGenerator:
    """Multi-model report generation pipeline using optimal model assignments"""
    
    def __init__(self):
        self.client = None
    
    async def analyze_breakthrough_discoveries(self, high_turbo_items: List[Dict]) -> List[Dict]:
        """
        ANALYSIS STAGE: DeepSeek-V3.1 (81.0% GPQA - Science/Analysis Leader)
        Provides deep structured analysis of breakthrough items
        """
        print("🔬 ANALYSIS STAGE: DeepSeek-V3.1 analyzing breakthroughs...")
        
        analyzed_items = []
        async with OllamaTurboClient() as client:
            for item in high_turbo_items[:5]:  # Top 5 breakthroughs
                try:
                    analysis = await client.analyze_ollama_project(
                        project_name=item.get('title', 'Unknown'),
                        description=item.get('summary', ''),
                        stars=item.get('turbo_score', 0) * 1000,  # Approximate
                        language="Unknown"
                    )
                    
                    item['llm_analysis'] = analysis
                    item['analyzed_by'] = 'deepseek-v3.1:671b-cloud'
                    analyzed_items.append(item)
                    print(f"  ✓ Analyzed: {item.get('title', '')[:50]}")
                    
                except Exception as e:
                    print(f"  ⚠️  Analysis failed for {item.get('title', '')[:30]}: {e}")
                    analyzed_items.append(item)  # Include without analysis
        
        return analyzed_items
    
    async def synthesize_developer_insights(self, aggregated: List[Dict], insights: Dict) -> str:
        """
        SYNTHESIS STAGE: GPT-OSS 120B (97.9% AIME, 1320 Elo - Reasoning/Synthesis Leader)
        Generates the comprehensive "What This Means for Developers" section
        """
        print("🧠 SYNTHESIS STAGE: GPT-OSS 120B generating developer insights...")
        
        async with OllamaTurboClient() as client:
            # Prepare context
            official_items = [e for e in aggregated if e.get('source') in ['blog', 'cloud_page', 'cloud_api']][:5]
            tool_items = [e for e in aggregated if e.get('source') in ['github', 'reddit']][:10]
            patterns = insights.get('patterns', {})
            
            context = f"""
OFFICIAL UPDATES ({len(official_items)} items):
{json.dumps([{'title': e.get('title'), 'summary': e.get('summary')} for e in official_items], indent=2)}

COMMUNITY TOOLS ({len(tool_items)} items):
{json.dumps([{'title': e.get('title'), 'highlights': e.get('highlights', [])} for e in tool_items], indent=2)}

DETECTED PATTERNS:
{json.dumps(list(patterns.keys()), indent=2)}
"""
            
            prompt = f"""You are EchoVein, writing the "What This Means for Developers" section of the Ollama Pulse report.

{context}

Generate a comprehensive, conversational developer-focused analysis with these sections:

1. **💡 What can we build with this?**
   - 3-5 concrete project ideas based on today's tools
   - Be specific with use cases and combinations

2. **🔧 How can we leverage these tools?**
   - Code examples (Python preferred)
   - Show integration patterns
   - Real, working snippets

3. **🎯 What problems does this solve?**
   - Real developer pain points
   - How today's updates address them
   - Practical benefits

4. **✨ What's now possible that wasn't before?**
   - New capabilities unlocked
   - Paradigm shifts
   - Exciting possibilities

5. **🔬 What should we experiment with next?**
   - Immediate action items
   - 3-5 specific experiments to try

6. **🌊 How can we make it better?**
   - Community contribution ideas
   - Gaps to fill
   - Next-level innovations

Make it conversational, exciting, and ACTIONABLE. Include real code where appropriate.
Target: 800-1200 words of genuinely useful content.

Developer Insights:"""

            model_id = select_model_for_task("synthesis", requires_reasoning=True)
            # Vary temperature for uniqueness (different each day)
            daily_temp = random.uniform(0.75, 0.92)
            response = await client.generate(
                model=model_id,
                prompt=prompt,
                max_tokens=3000,
                temperature=daily_temp
            )
            print(f"  ✓ Using temperature: {daily_temp:.2f} for creative variation")
            
            print(f"  ✓ Generated {len(response)} chars of developer insights")
            return response
    
    async def generate_rag_powered_prophecies(self, patterns: Dict, rag_engine) -> List[Dict]:
        """
        PROPHECY STAGE: Kimi-K2:1T (66.1% Tau-Bench - Agentic/Research Leader) + RAG
        Uses historical context to generate confident predictions
        """
        print("🔮 PROPHECY STAGE: Kimi-K2 + RAG generating prophecies...")
        
        prophecies = []
        
        for pattern_name, items in patterns.items():
            if len(items) < 3:  # Skip small patterns
                continue
            
            cluster_summary = f"Pattern: {pattern_name} with {len(items)} items"
            past_yield = {"pattern_size": len(items), "items": len(items)}
            
            # Use RAG engine if available
            prophecy_data = rag_engine.generate_prophecy(
                cluster_summary=cluster_summary,
                past_yield=past_yield,
                use_rag=True
            ) if rag_engine else {
                "prophecy": f"The {pattern_name.replace('_', ' ')} vein is pulsing with {len(items)} signals.",
                "confidence": "MEDIUM"
            }
            
            prophecies.append({
                "pattern": pattern_name,
                "observation": f"{len(items)} independent projects converging",
                "inference": prophecy_data.get('prophecy', 'Unknown'),
                "confidence": prophecy_data.get('confidence', 'MEDIUM').lower(),
                "rag_enabled": prophecy_data.get('rag_enabled', False)
            })
        
        print(f"  ✓ Generated {len(prophecies)} RAG-powered prophecies")
        return prophecies
    
    async def polish_final_prose(self, report_draft: str) -> str:
        """
        CREATIVE POLISH STAGE: GLM-4.6 (Pragmatic, 200K context)
        Final pass for readability, flow, and EchoVein personality
        """
        print("✨ POLISH STAGE: GLM-4.6 enhancing readability...")
        
        async with OllamaTurboClient() as client:
            prompt = f"""You are EchoVein's editor. Polish this draft report for maximum readability and engagement.

DRAFT REPORT:
{report_draft[:10000]}  # First 10K chars to stay in context

Your job:
1. Enhance flow and transitions
2. Add personality (vein metaphors, ecosystem insights)
3. Ensure technical accuracy
4. Make it exciting to read
5. Keep all facts and data intact

Return the polished opening sections (first ~3000 chars). Maintain EchoVein's voice!

Polished Report:"""
            
            model_id = select_model_for_task("creative")
            response = await client.generate(
                model=model_id,
                prompt=prompt,
                max_tokens=4000,
                temperature=0.8  # Higher for creativity
            )
            
            print(f"  ✓ Polished {len(response)} chars")
            return response
    
    async def enrich_pattern_analysis(self, pattern_name: str, items: List[Dict]) -> str:
        """
        PATTERN ANALYSIS: Kimi-K2 (Long-context research)
        Generates rich analysis of why patterns matter
        """
        async with OllamaTurboClient() as client:
            items_summary = "\n".join([
                f"- {item.get('title', 'Unknown')}: {item.get('summary', '')[:100]}"
                for item in items[:5]
            ])
            
            prompt = f"""Analyze this emerging pattern in the Ollama ecosystem:

PATTERN: {pattern_name.replace('_', ' ').title()}
ITEMS ({len(items)} detected):
{items_summary}

Provide:
1. WHY this pattern matters (2-3 sentences)
2. WHAT it enables for developers (1-2 sentences)
3. WHERE this is heading (prediction, 1 sentence)

Keep it concise but insightful. Use ecosystem perspective.

Analysis:"""
            
            model_id = select_model_for_task("research", requires_long_context=True)
            response = await client.generate(
                model=model_id,
                prompt=prompt,
                max_tokens=500,
                temperature=0.6
            )
            
            return response

# Export for use in generate_report.py
async def enhance_report_with_models(aggregated, insights, rag_engine=None):
    """Main entry point: enhance report with full model pipeline"""
    generator = EnhancedReportGenerator()
    
    results = {
        'breakthrough_analyses': [],
        'developer_insights': '',
        'prophecies': [],
        'pattern_analyses': {}
    }
    
    try:
        # Stage 1: Analyze breakthroughs (DeepSeek)
        high_turbo = sorted(
            [e for e in aggregated if e.get('turbo_score', 0) >= 0.7],
            key=lambda x: x.get('turbo_score', 0),
            reverse=True
        )[:5]
        
        if high_turbo:
            results['breakthrough_analyses'] = await generator.analyze_breakthrough_discoveries(high_turbo)
        
        # Stage 2: Generate developer insights (GPT-OSS)
        results['developer_insights'] = await generator.synthesize_developer_insights(aggregated, insights)
        
        # Stage 3: Generate prophecies with RAG (Kimi-K2)
        patterns = insights.get('patterns', {})
        if rag_engine:
            results['prophecies'] = await generator.generate_rag_powered_prophecies(patterns, rag_engine)
        
        # Stage 4: Enrich pattern analysis (Kimi-K2)
        for pattern_name, items in list(patterns.items())[:3]:  # Top 3 patterns
            if len(items) >= 3:
                analysis = await generator.enrich_pattern_analysis(pattern_name, items)
                results['pattern_analyses'][pattern_name] = analysis
        
        print("✅ Multi-model enhancement complete!")
        return results
        
    except Exception as e:
        print(f"⚠️  Model enhancement failed: {e}")
        return results  # Return partial results


