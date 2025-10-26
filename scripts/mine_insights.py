#!/usr/bin/env python3
"""
Ollama Pulse - Insights Mining
Uses embeddings + clustering to detect patterns and infer implications
"""
import json
import os
import re
from datetime import datetime
from pathlib import Path

try:
    from sentence_transformers import SentenceTransformer
    from sklearn.cluster import KMeans
    import numpy as np
    EMBEDDINGS_AVAILABLE = True
except ImportError:
    print("⚠️  sentence-transformers or scikit-learn not available - using fallback mode")
    EMBEDDINGS_AVAILABLE = False


def ensure_data_dir():
    """Create data/insights directory if it doesn't exist"""
    Path("data/insights").mkdir(parents=True, exist_ok=True)


def get_today_filename():
    """Get filename for today's insights"""
    today = datetime.now().strftime("%Y-%m-%d")
    return f"data/insights/{today}.json"


def load_aggregated_data():
    """Load today's aggregated data"""
    today = datetime.now().strftime("%Y-%m-%d")
    filename = f"data/aggregated/{today}.json"
    
    if not os.path.exists(filename):
        print(f"❌ No aggregated data found for {today}")
        return []
    
    with open(filename, 'r') as f:
        return json.load(f)


def generate_dynamic_queries(entries):
    """
    Generate dynamic search queries based on yesterday's patterns
    This enables adaptive discovery of emerging trends
    """
    print("🔮 Generating dynamic queries from patterns...")
    
    # Count keyword frequencies
    keyword_counts = {}
    for entry in entries:
        text = (entry.get('title', '') + ' ' + entry.get('summary', '')).lower()
        
        # Extract relevant keywords
        keywords = ['voice', 'stt', 'tts', 'multimodal', 'vision', 
                   'turbo', 'cloud', 'api', 'integration', 'agent',
                   'rag', 'embedding', 'vector', 'search']
        
        for keyword in keywords:
            if keyword in text:
                keyword_counts[keyword] = keyword_counts.get(keyword, 0) + 1
    
    # Generate queries for top trending keywords
    dynamic_queries = []
    sorted_keywords = sorted(keyword_counts.items(), key=lambda x: x[1], reverse=True)
    
    for keyword, count in sorted_keywords[:5]:  # Top 5 trends
        if count >= 3:  # Threshold for significance
            query = f"ollama turbo {keyword} integrations site:github.com"
            dynamic_queries.append(query)
            print(f"  💡 Generated query: '{query}' (detected {count}x)")
    
    return dynamic_queries


def detect_patterns_simple(entries):
    """Simple pattern detection using regex (fallback mode)"""
    print("🔍 Detecting patterns (simple mode)...")
    
    patterns = {
        "multimodal": [],
        "cloud_models": [],
        "no_code": [],
        "voice": [],
        "coding": [],
        "turbo_services": []
    }
    
    for entry in entries:
        text = (entry.get('title', '') + ' ' + entry.get('summary', '')).lower()
        
        if re.search(r'(multimodal|vision|image|qwen3-vl)', text):
            patterns["multimodal"].append(entry)
        
        if re.search(r'(-cloud|ollama cloud|turbo)', text):
            patterns["cloud_models"].append(entry)
        
        if re.search(r'(n8n|zapier|make|no-code)', text):
            patterns["no_code"].append(entry)
        
        if re.search(r'(voice|stt|tts|speech)', text):
            patterns["voice"].append(entry)
        
        if re.search(r'(code|coding|coder|programming)', text):
            patterns["coding"].append(entry)
        
        if re.search(r'(turbo|service|api|proxy)', text):
            patterns["turbo_services"].append(entry)
    
    # Filter patterns with at least 2 items
    significant_patterns = {k: v for k, v in patterns.items() if len(v) >= 2}
    
    print(f"✅ Found {len(significant_patterns)} significant patterns")
    return significant_patterns


def detect_patterns_ml(entries):
    """Advanced pattern detection using embeddings + clustering"""
    print("🔍 Detecting patterns (ML mode)...")
    
    # Extract text for embedding
    texts = [e.get('title', '') + ' ' + e.get('summary', '') for e in entries]
    
    # Generate embeddings
    model = SentenceTransformer('all-MiniLM-L6-v2')
    embeddings = model.encode(texts)
    
    # Cluster (3-5 clusters based on data size)
    n_clusters = min(5, max(3, len(entries) // 10))
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    labels = kmeans.fit_predict(embeddings)
    
    # Group by cluster
    clusters = {}
    for i, label in enumerate(labels):
        if label not in clusters:
            clusters[label] = []
        clusters[label].append(entries[i])
    
    # Tag clusters
    tagged_patterns = {}
    for cluster_id, cluster_entries in clusters.items():
        # Analyze cluster content
        combined_text = ' '.join([e.get('title', '') + ' ' + e.get('summary', '') for e in cluster_entries]).lower()
        
        # Determine cluster theme
        if 'multimodal' in combined_text or 'vision' in combined_text:
            theme = "multimodal_hybrids"
        elif 'cloud' in combined_text:
            theme = "cloud_models"
        elif 'n8n' in combined_text or 'zapier' in combined_text:
            theme = "no_code_wrappers"
        elif 'voice' in combined_text or 'stt' in combined_text:
            theme = "voice_integration"
        else:
            theme = f"cluster_{cluster_id}"
        
        tagged_patterns[theme] = cluster_entries
    
    print(f"✅ Found {len(tagged_patterns)} ML-detected patterns")
    return tagged_patterns


def infer_implications(patterns):
    """Apply heuristic rules to infer implications"""
    print("💡 Inferring implications...")
    
    inferences = []
    
    for pattern_name, entries in patterns.items():
        # Density rule: >3 items = emerging trend
        if len(entries) >= 3:
            inferences.append({
                "pattern": pattern_name,
                "observation": f"{len(entries)} items detected",
                "inference": "Emerging trend - scale to 2x more use-cases",
                "confidence": "high" if len(entries) >= 5 else "medium"
            })
        
        # Combo rules
        if pattern_name == "multimodal_hybrids" or pattern_name == "multimodal":
            inferences.append({
                "pattern": pattern_name,
                "observation": "Multimodal cloud models available",
                "inference": "Unlocks real-time apps; next: AR/VR agents for education/healthcare",
                "confidence": "high"
            })
        
        if pattern_name == "no_code_wrappers" or pattern_name == "no_code":
            inferences.append({
                "pattern": pattern_name,
                "observation": "No-code integrations growing",
                "inference": "Simplifies enterprise automations; disrupts SaaS like Zapier",
                "confidence": "medium"
            })
    
    print(f"✅ Generated {len(inferences)} inferences")
    return inferences


def save_insights(patterns, inferences, dynamic_queries=None):
    """Save insights to JSON"""
    filename = get_today_filename()
    
    insights = {
        "date": datetime.now().isoformat(),
        "patterns": {k: [{"title": e.get('title'), "url": e.get('url')} for e in v] for k, v in patterns.items()},
        "inferences": inferences,
        "dynamic_queries": dynamic_queries or [],
        "stats": {
            "total_patterns": len(patterns),
            "total_inferences": len(inferences),
            "total_items": sum(len(v) for v in patterns.values())
        }
    }
    
    with open(filename, 'w') as f:
        json.dump(insights, f, indent=2)
    
    print(f"💾 Saved insights to {filename}")


def main():
    """Main mining function"""
    print("🚀 Starting insights mining...")
    ensure_data_dir()
    
    # Load data
    entries = load_aggregated_data()
    if not entries:
        print("⚠️  No data to mine")
        return
    
    print(f"📊 Mining {len(entries)} entries...")
    
    # Generate dynamic queries for future searches
    dynamic_queries = generate_dynamic_queries(entries)
    
    # Detect patterns
    if EMBEDDINGS_AVAILABLE and len(entries) >= 10:
        patterns = detect_patterns_ml(entries)
    else:
        patterns = detect_patterns_simple(entries)
    
    # Infer implications
    inferences = infer_implications(patterns)
    
    # Save
    save_insights(patterns, inferences, dynamic_queries)
    
    print("✅ Insights mining complete!")


if __name__ == "__main__":
    main()

