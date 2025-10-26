# coding: utf-8
#!/usr/bin/env python3
"""Supabase PostgreSQL database adapter for review history"""
import os
import json
from pathlib import Path
from datetime import datetime, date, timedelta
from typing import List, Dict, Optional
from dataclasses import dataclass, asdict

try:
    from supabase import create_client, Client
    SUPABASE_AVAILABLE = True
except ImportError:
    SUPABASE_AVAILABLE = False
    print("⚠️  Supabase not available - install: pip install supabase")


@dataclass
class ProjectReview:
    """Represents a single project review"""
    project_identifier: str
    project_name: str
    project_type: str
    review_date: str
    source_repo: str
    persona_used: str = "EchoVein"
    version_tag: Optional[str] = None
    stars: Optional[int] = None
    forks: Optional[int] = None
    downloads: Optional[int] = None
    citations: Optional[int] = None
    generated_commentary: Optional[str] = None
    sentiment_score: Optional[float] = None
    tags: Optional[List[str]] = None
    blog_post_url: Optional[str] = None


class SupabaseReviewDatabase:
    """Manages review history in Supabase PostgreSQL"""
    
    def __init__(self):
        if not SUPABASE_AVAILABLE:
            raise ImportError("Supabase library not installed")
        
        # Get credentials from environment
        self.url = os.getenv('SUPABASE_URL', 'https://cgadwztoroibkjumvrdo.supabase.co')
        self.key = os.getenv('SUPABASE_KEY')
        
        if not self.key:
            raise ValueError("SUPABASE_KEY environment variable not set")
        
        # Create Supabase client
        self.client: Client = create_client(self.url, self.key)
    
    def add_review(self, review: ProjectReview) -> int:
        """Add a new review to the database"""
        try:
            # Convert dataclass to dict
            data = asdict(review)
            
            # Convert tags list to JSON if present
            if data.get('tags'):
                data['tags'] = json.dumps(data['tags']) if isinstance(data['tags'], list) else data['tags']
            
            # Remove None values
            data = {k: v for k, v in data.items() if v is not None}
            
            # Insert into Supabase
            result = self.client.table('project_reviews').insert(data).execute()
            
            if result.data:
                return result.data[0]['id']
            return 0
            
        except Exception as e:
            print(f"⚠️  Error adding review: {e}")
            return 0
    
    def get_project_history(self, project_identifier: str, limit: int = 10) -> List[Dict]:
        """Get review history for a specific project"""
        try:
            result = self.client.table('project_reviews')\
                .select('*')\
                .eq('project_identifier', project_identifier)\
                .order('review_date', desc=True)\
                .limit(limit)\
                .execute()
            
            return result.data if result.data else []
            
        except Exception as e:
            print(f"⚠️  Error getting project history: {e}")
            return []
    
    def get_recent_reviews(self, days: int = 7, limit: int = 100) -> List[Dict]:
        """Get recent reviews from the last N days"""
        try:
            cutoff_date = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')
            
            result = self.client.table('project_reviews')\
                .select('*')\
                .gte('review_date', cutoff_date)\
                .order('review_date', desc=True)\
                .limit(limit)\
                .execute()
            
            return result.data if result.data else []
            
        except Exception as e:
            print(f"⚠️  Error getting recent reviews: {e}")
            return []
    
    def generate_historical_context(self, project_identifier: str, current_metrics: Dict) -> str:
        """Generate historical context for a project"""
        history = self.get_project_history(project_identifier, limit=5)
        
        if not history:
            return ""
        
        # Build context string
        context_parts = []
        context_parts.append(f"Historical Context for {project_identifier}:")
        context_parts.append(f"  - First seen: {history[-1]['review_date']}")
        context_parts.append(f"  - Total reviews: {len(history)}")

        # Add metrics comparison if available
        if current_metrics.get('stars') and history[0].get('stars'):
            star_change = current_metrics['stars'] - history[0]['stars']
            if star_change > 0:
                context_parts.append(f"  - Stars: +{star_change} since last review")
        
        return "\n".join(context_parts)
    
    def search_projects(self, query: str, limit: int = 20) -> List[Dict]:
        """Search for projects by name or identifier"""
        try:
            result = self.client.table('project_reviews')\
                .select('project_identifier, project_name, project_type, MAX(review_date) as last_review')\
                .or_(f'project_name.ilike.%{query}%,project_identifier.ilike.%{query}%')\
                .limit(limit)\
                .execute()
            
            return result.data if result.data else []
            
        except Exception as e:
            print(f"⚠️  Error searching projects: {e}")
            return []
    
    def get_trending_projects(self, days: int = 7, min_reviews: int = 2) -> List[Dict]:
        """Get projects with multiple reviews in recent days (trending)"""
        try:
            cutoff_date = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')
            
            # Use raw SQL for complex aggregation
            query = f"""
                SELECT 
                    project_identifier,
                    project_name,
                    project_type,
                    COUNT(*) as review_count,
                    MAX(review_date) as last_review,
                    MIN(review_date) as first_review
                FROM project_reviews
                WHERE review_date >= '{cutoff_date}'
                GROUP BY project_identifier, project_name, project_type
                HAVING COUNT(*) >= {min_reviews}
                ORDER BY review_count DESC, last_review DESC
                LIMIT 20
            """
            
            result = self.client.rpc('exec_sql', {'query': query}).execute()
            return result.data if result.data else []
            
        except Exception as e:
            print(f"⚠️  Error getting trending projects: {e}")
            return []


# Convenience functions
def get_supabase_db() -> SupabaseReviewDatabase:
    """Get Supabase database instance"""
    return SupabaseReviewDatabase()


def add_project_review(project_data: Dict) -> int:
    """Quick function to add a review from a dict"""
    review = ProjectReview(**project_data)
    db = get_supabase_db()
    return db.add_review(review)


def get_project_context(project_identifier: str, current_metrics: Dict = None) -> str:
    """Quick function to get historical context for a project"""
    db = get_supabase_db()
    return db.generate_historical_context(project_identifier, current_metrics or {})


if __name__ == "__main__":
    # Test connection
    try:
        db = SupabaseReviewDatabase()
        print("Supabase connection successful!")
        
        # Test query
        recent = db.get_recent_reviews(days=30, limit=5)
        print(f"Found {len(recent)} recent reviews")
        
        for review in recent:
            print(f"  - {review['project_name']} ({review['review_date']})")

    except Exception as e:
        print(f"Supabase connection failed: {e}")

