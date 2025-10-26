#!/usr/bin/env python3
"""
Review Database Integration for Blog Generators
Integrates the review database with existing blog generation scripts

This module provides helper functions to:
- Extract project data from Ollama Pulse aggregated data
- Store reviews after blog generation
- Retrieve historical context before generation
- Generate comparative analysis
"""
import json
import os
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
from urllib.parse import urlparse

# Try Supabase first, fallback to SQLite
try:
    if os.getenv('SUPABASE_URL') and os.getenv('SUPABASE_KEY'):
        from supabase_database import SupabaseReviewDatabase as ReviewDatabase, ProjectReview, get_project_context
        print("✅ Using Supabase PostgreSQL database")
    else:
        raise ImportError("Supabase credentials not found")
except (ImportError, Exception) as e:
    print(f"⚠️  Supabase unavailable, using SQLite: {e}")
    from review_database import ReviewDatabase, ProjectReview, get_project_context


class ReviewIntegration:
    """Integrates review database with blog generation workflow"""
    
    def __init__(self):
        self.db = ReviewDatabase()
    
    def extract_project_from_github_url(self, url: str) -> Optional[str]:
        """Extract project identifier from GitHub URL"""
        # Match patterns like github.com/owner/repo
        match = re.search(r'github\.com/([^/]+/[^/]+)', url)
        if match:
            return match.group(1).rstrip('/')
        return None
    
    def normalize_project_identifier(self, url: str) -> str:
        """
        Normalize project identifier for consistent storage
        Handles GitHub URLs, model names, paper DOIs, etc.
        """
        # GitHub repos
        github_id = self.extract_project_from_github_url(url)
        if github_id:
            return f"github:{github_id}"
        
        # Ollama models (e.g., ollama.com/library/llama2)
        if 'ollama.com' in url:
            parts = url.split('/')
            if len(parts) >= 2:
                return f"ollama:{parts[-2]}/{parts[-1]}"
        
        # arXiv papers
        if 'arxiv.org' in url:
            match = re.search(r'(\d{4}\.\d{4,5})', url)
            if match:
                return f"arxiv:{match.group(1)}"
        
        # Default: use the full URL
        return url
    
    def extract_metrics_from_highlights(self, highlights: List[str]) -> Dict:
        """Extract numeric metrics from highlight strings"""
        metrics = {}
        
        for highlight in highlights:
            # Stars: "stars: 1234"
            if 'stars:' in highlight.lower():
                match = re.search(r'stars:\s*(\d+)', highlight, re.IGNORECASE)
                if match:
                    metrics['stars'] = int(match.group(1))
            
            # Forks: "forks: 123"
            if 'forks:' in highlight.lower():
                match = re.search(r'forks:\s*(\d+)', highlight, re.IGNORECASE)
                if match:
                    metrics['forks'] = int(match.group(1))
            
            # Downloads: "downloads: 5000"
            if 'downloads:' in highlight.lower():
                match = re.search(r'downloads:\s*(\d+)', highlight, re.IGNORECASE)
                if match:
                    metrics['downloads'] = int(match.group(1))
            
            # Citations: "citations: 42"
            if 'citations:' in highlight.lower():
                match = re.search(r'citations:\s*(\d+)', highlight, re.IGNORECASE)
                if match:
                    metrics['citations'] = int(match.group(1))
        
        return metrics
    
    def determine_project_type(self, item: Dict) -> str:
        """Determine project type from item data"""
        url = item.get('url', '')
        source = item.get('source', '')
        
        if 'github.com' in url:
            return 'repo'
        elif 'ollama.com' in url or 'model' in source.lower():
            return 'model'
        elif 'arxiv.org' in url or 'paper' in source.lower():
            return 'paper'
        elif 'tool' in source.lower() or 'integration' in source.lower():
            return 'tool'
        else:
            return 'unknown'
    
    def process_ollama_pulse_item(self, item: Dict, review_date: str, 
                                  commentary: str = None, persona: str = None) -> Optional[ProjectReview]:
        """
        Convert an Ollama Pulse aggregated item into a ProjectReview
        
        Args:
            item: Dict from aggregated data
            review_date: ISO date string
            commentary: Generated commentary for this item
            persona: Persona used for generation
        
        Returns:
            ProjectReview object or None if item can't be processed
        """
        url = item.get('url')
        if not url:
            return None
        
        project_id = self.normalize_project_identifier(url)
        project_name = item.get('title', 'Unknown Project')
        project_type = self.determine_project_type(item)
        
        # Extract metrics
        highlights = item.get('highlights', [])
        metrics = self.extract_metrics_from_highlights(highlights)
        
        # Extract tags
        tags = []
        if 'tags' in item:
            tags = item['tags']
        elif 'highlights' in item:
            # Use highlights as tags
            tags = [h.split(':')[0].strip() for h in highlights if ':' in h]
        
        review = ProjectReview(
            project_identifier=project_id,
            project_name=project_name,
            project_type=project_type,
            review_date=review_date,
            version_tag=item.get('version'),
            stars=metrics.get('stars'),
            forks=metrics.get('forks'),
            downloads=metrics.get('downloads'),
            citations=metrics.get('citations'),
            generated_commentary=commentary,
            persona_used=persona,
            tags=json.dumps(tags) if tags else None,
            source_repo='ollama_pulse',
            blog_post_url=None  # Will be set after blog is published
        )
        
        return review
    
    def get_historical_context_for_items(self, items: List[Dict]) -> Dict[str, str]:
        """
        Get historical context for a list of items
        Returns dict mapping project_identifier to context string
        """
        context_map = {}

        for item in items:
            url = item.get('url')
            if not url:
                continue

            project_id = self.normalize_project_identifier(url)

            # Get historical context using our own db instance
            context = self.db.generate_historical_context(project_id, item)
            if context:
                context_map[project_id] = context

        return context_map
    
    def store_reviews_from_blog_post(self, items: List[Dict], commentaries: Dict[str, str],
                                    review_date: str, persona: str, blog_url: str = None):
        """
        Store reviews after blog post generation
        
        Args:
            items: List of items from aggregated data
            commentaries: Dict mapping project_id to generated commentary
            review_date: ISO date string
            persona: Persona used
            blog_url: URL of published blog post
        """
        stored_count = 0
        
        for item in items:
            url = item.get('url')
            if not url:
                continue
            
            project_id = self.normalize_project_identifier(url)
            commentary = commentaries.get(project_id, '')
            
            review = self.process_ollama_pulse_item(item, review_date, commentary, persona)
            if review:
                review.blog_post_url = blog_url
                self.db.add_review(review)
                stored_count += 1
        
        print(f"✅ Stored {stored_count} reviews in database")
        return stored_count
    
    def generate_trend_report(self, days_back: int = 30) -> Dict:
        """
        Generate a trend analysis report
        Useful for monthly/weekly summary posts
        """
        report = {
            'period_days': days_back,
            'trending_by_stars': self.db.get_trending_projects('stars', days_back, limit=10),
            'trending_by_forks': self.db.get_trending_projects('forks', days_back, limit=10),
            'review_counts': self.db.get_review_count_by_type(days_back),
            'stats': self.db.get_database_stats()
        }
        
        return report
    
    def find_prediction_validations(self, days_back: int = 90) -> List[Dict]:
        """
        Find projects where previous predictions came true
        Looks for projects marked as "promising" that grew significantly
        """
        validations = []
        
        # Search for reviews with positive sentiment
        promising_reviews = self.db.search_reviews(
            days_back=days_back,
            limit=100
        )
        
        for review in promising_reviews:
            # Check if it grew significantly since then
            changes = self.db.get_comparative_metrics(
                review['project_identifier'],
                days_back=days_back
            )
            
            if changes.get('stars', {}).get('pct_change', 0) > 100:
                validations.append({
                    'project': review['project_name'],
                    'original_review_date': review['review_date'],
                    'original_commentary': review['generated_commentary'],
                    'growth': changes['stars']
                })
        
        return validations


# Convenience functions for integration
def get_integration() -> ReviewIntegration:
    """Get integration instance"""
    return ReviewIntegration()


def enhance_blog_with_history(items: List[Dict]) -> Dict[str, str]:
    """
    Quick function to get historical context for blog items
    Returns dict mapping project URLs to context strings
    """
    integration = get_integration()
    return integration.get_historical_context_for_items(items)


def store_blog_reviews(items: List[Dict], commentaries: Dict[str, str],
                       review_date: str, persona: str, blog_url: str = None):
    """Quick function to store reviews after blog generation"""
    integration = get_integration()
    return integration.store_reviews_from_blog_post(
        items, commentaries, review_date, persona, blog_url
    )


if __name__ == "__main__":
    # Test the integration
    print("🔗 Review Database Integration")
    print("=" * 50)
    
    integration = get_integration()
    
    # Test with sample data
    sample_item = {
        'url': 'https://github.com/ollama/ollama',
        'title': 'Ollama - Get up and running with large language models',
        'highlights': ['stars: 50000', 'forks: 3500', 'language: Go'],
        'source': 'github'
    }
    
    project_id = integration.normalize_project_identifier(sample_item['url'])
    print(f"\n📝 Sample Project ID: {project_id}")
    
    review = integration.process_ollama_pulse_item(
        sample_item,
        datetime.now().isoformat(),
        "This is a test commentary",
        "test_persona"
    )
    
    if review:
        print(f"  Name: {review.project_name}")
        print(f"  Type: {review.project_type}")
        print(f"  Stars: {review.stars}")
        print(f"  Forks: {review.forks}")
    
    print("\n✅ Integration module ready!")
