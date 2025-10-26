#!/usr/bin/env python3
"""
Review Database System for GrumpiBlogged
Persistent storage and querying of project/model/paper reviews across blog posts

This module provides:
- SQLite database for review history
- Historical context retrieval
- Comparative analysis capabilities
- Trend detection and analytics
"""
import sqlite3
import json
import hashlib
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
from contextlib import contextmanager


# Database location
DB_PATH = Path("data/review_history.db")


@dataclass
class ProjectReview:
    """Represents a single project review"""
    project_identifier: str  # URL or unique ID
    project_name: str
    project_type: str  # 'model', 'tool', 'repo', 'paper'
    review_date: str  # ISO format
    version_tag: Optional[str] = None
    
    # Metrics
    stars: Optional[int] = None
    forks: Optional[int] = None
    downloads: Optional[int] = None
    citations: Optional[int] = None
    
    # Content
    generated_commentary: Optional[str] = None
    persona_used: Optional[str] = None
    sentiment_score: Optional[float] = None
    tags: Optional[str] = None  # JSON array as string
    
    # Metadata
    source_repo: str = 'grumpiblogged'  # 'ollama_pulse' or 'ai_research_daily'
    blog_post_url: Optional[str] = None
    
    # Auto-generated
    id: Optional[int] = None


class ReviewDatabase:
    """Manages the review history database"""
    
    def __init__(self, db_path: Path = DB_PATH):
        self.db_path = db_path
        self._ensure_database()
    
    @contextmanager
    def _get_connection(self):
        """Context manager for database connections"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # Enable column access by name
        try:
            yield conn
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()
    
    def _ensure_database(self):
        """Create database and tables if they don't exist"""
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            # Main reviews table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS project_reviews (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    project_identifier TEXT NOT NULL,
                    project_name TEXT NOT NULL,
                    project_type TEXT NOT NULL,
                    review_date TEXT NOT NULL,
                    version_tag TEXT,
                    
                    -- Metrics
                    stars INTEGER,
                    forks INTEGER,
                    downloads INTEGER,
                    citations INTEGER,
                    
                    -- Content
                    generated_commentary TEXT,
                    persona_used TEXT,
                    sentiment_score REAL,
                    tags TEXT,
                    
                    -- Metadata
                    source_repo TEXT NOT NULL,
                    blog_post_url TEXT,
                    
                    -- Ensure uniqueness
                    UNIQUE(project_identifier, review_date, source_repo)
                )
            ''')
            
            # Indexes for fast lookups
            cursor.execute('''
                CREATE INDEX IF NOT EXISTS idx_project_id 
                ON project_reviews(project_identifier)
            ''')
            
            cursor.execute('''
                CREATE INDEX IF NOT EXISTS idx_review_date 
                ON project_reviews(review_date)
            ''')
            
            cursor.execute('''
                CREATE INDEX IF NOT EXISTS idx_project_type 
                ON project_reviews(project_type)
            ''')
            
            cursor.execute('''
                CREATE INDEX IF NOT EXISTS idx_source_repo 
                ON project_reviews(source_repo)
            ''')
            
            # Metrics tracking table for trend analysis
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS metric_snapshots (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    project_identifier TEXT NOT NULL,
                    snapshot_date TEXT NOT NULL,
                    metric_name TEXT NOT NULL,
                    metric_value REAL NOT NULL,
                    
                    UNIQUE(project_identifier, snapshot_date, metric_name)
                )
            ''')
            
            cursor.execute('''
                CREATE INDEX IF NOT EXISTS idx_metric_project 
                ON metric_snapshots(project_identifier)
            ''')
    
    def add_review(self, review: ProjectReview) -> int:
        """
        Add a new review to the database
        Returns the review ID
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT OR REPLACE INTO project_reviews (
                    project_identifier, project_name, project_type, review_date,
                    version_tag, stars, forks, downloads, citations,
                    generated_commentary, persona_used, sentiment_score, tags,
                    source_repo, blog_post_url
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                review.project_identifier, review.project_name, review.project_type,
                review.review_date, review.version_tag, review.stars, review.forks,
                review.downloads, review.citations, review.generated_commentary,
                review.persona_used, review.sentiment_score, review.tags,
                review.source_repo, review.blog_post_url
            ))
            
            review_id = cursor.lastrowid
            
            # Also store metric snapshots for trend analysis
            if review.stars is not None:
                self._add_metric_snapshot(
                    review.project_identifier, review.review_date, 'stars', review.stars
                )
            if review.forks is not None:
                self._add_metric_snapshot(
                    review.project_identifier, review.review_date, 'forks', review.forks
                )
            if review.downloads is not None:
                self._add_metric_snapshot(
                    review.project_identifier, review.review_date, 'downloads', review.downloads
                )
            if review.citations is not None:
                self._add_metric_snapshot(
                    review.project_identifier, review.review_date, 'citations', review.citations
                )
            
            return review_id
    
    def _add_metric_snapshot(self, project_id: str, date: str, metric_name: str, value: float):
        """Add a metric snapshot for trend tracking"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT OR REPLACE INTO metric_snapshots (
                    project_identifier, snapshot_date, metric_name, metric_value
                ) VALUES (?, ?, ?, ?)
            ''', (project_id, date, metric_name, value))
    
    def get_project_history(self, project_identifier: str, limit: int = 10) -> List[Dict]:
        """
        Get review history for a specific project
        Returns list of reviews ordered by date (newest first)
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT * FROM project_reviews
                WHERE project_identifier = ?
                ORDER BY review_date DESC
                LIMIT ?
            ''', (project_identifier, limit))
            
            return [dict(row) for row in cursor.fetchall()]
    
    def get_latest_review(self, project_identifier: str) -> Optional[Dict]:
        """Get the most recent review for a project"""
        history = self.get_project_history(project_identifier, limit=1)
        return history[0] if history else None
    
    def get_comparative_metrics(self, project_identifier: str, days_back: int = 90) -> Dict:
        """
        Get comparative metrics showing growth/decline over time
        Returns dict with metric changes
        """
        cutoff_date = (datetime.now() - timedelta(days=days_back)).isoformat()
        
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            # Get first and last review in the time period
            cursor.execute('''
                SELECT * FROM project_reviews
                WHERE project_identifier = ? AND review_date >= ?
                ORDER BY review_date ASC
                LIMIT 1
            ''', (project_identifier, cutoff_date))
            first_review = cursor.fetchone()
            
            cursor.execute('''
                SELECT * FROM project_reviews
                WHERE project_identifier = ?
                ORDER BY review_date DESC
                LIMIT 1
            ''', (project_identifier,))
            latest_review = cursor.fetchone()
            
            if not first_review or not latest_review:
                return {}
            
            first = dict(first_review)
            latest = dict(latest_review)
            
            # Calculate changes
            changes = {}
            for metric in ['stars', 'forks', 'downloads', 'citations']:
                if first.get(metric) is not None and latest.get(metric) is not None:
                    old_val = first[metric]
                    new_val = latest[metric]
                    change = new_val - old_val
                    pct_change = (change / old_val * 100) if old_val > 0 else 0
                    
                    changes[metric] = {
                        'old': old_val,
                        'new': new_val,
                        'change': change,
                        'pct_change': round(pct_change, 1),
                        'days': (datetime.fromisoformat(latest['review_date']) - 
                                datetime.fromisoformat(first['review_date'])).days
                    }
            
            return changes
    
    def get_review_count_by_type(self, days_back: int = 30) -> Dict[str, int]:
        """Get count of reviews by project type in the last N days"""
        cutoff_date = (datetime.now() - timedelta(days=days_back)).isoformat()
        
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT project_type, COUNT(*) as count
                FROM project_reviews
                WHERE review_date >= ?
                GROUP BY project_type
                ORDER BY count DESC
            ''', (cutoff_date,))
            
            return {row['project_type']: row['count'] for row in cursor.fetchall()}
    
    def get_trending_projects(self, metric: str = 'stars', days_back: int = 30, limit: int = 10) -> List[Dict]:
        """
        Get projects with highest growth in specified metric
        Returns list of projects with growth stats
        """
        cutoff_date = (datetime.now() - timedelta(days=days_back)).isoformat()
        
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            # Get projects with multiple reviews in the period
            cursor.execute(f'''
                SELECT 
                    project_identifier,
                    project_name,
                    MIN({metric}) as start_value,
                    MAX({metric}) as end_value,
                    MAX({metric}) - MIN({metric}) as growth,
                    COUNT(*) as review_count
                FROM project_reviews
                WHERE review_date >= ? AND {metric} IS NOT NULL
                GROUP BY project_identifier
                HAVING review_count > 1 AND growth > 0
                ORDER BY growth DESC
                LIMIT ?
            ''', (cutoff_date, limit))
            
            results = []
            for row in cursor.fetchall():
                row_dict = dict(row)
                if row_dict['start_value'] > 0:
                    row_dict['growth_pct'] = round(
                        (row_dict['growth'] / row_dict['start_value']) * 100, 1
                    )
                else:
                    row_dict['growth_pct'] = 0
                results.append(row_dict)
            
            return results
    
    def search_reviews(self, 
                      project_type: Optional[str] = None,
                      persona: Optional[str] = None,
                      min_stars: Optional[int] = None,
                      tags: Optional[List[str]] = None,
                      days_back: Optional[int] = None,
                      limit: int = 50) -> List[Dict]:
        """
        Search reviews with various filters
        """
        query = "SELECT * FROM project_reviews WHERE 1=1"
        params = []
        
        if project_type:
            query += " AND project_type = ?"
            params.append(project_type)
        
        if persona:
            query += " AND persona_used = ?"
            params.append(persona)
        
        if min_stars is not None:
            query += " AND stars >= ?"
            params.append(min_stars)
        
        if days_back:
            cutoff_date = (datetime.now() - timedelta(days=days_back)).isoformat()
            query += " AND review_date >= ?"
            params.append(cutoff_date)
        
        if tags:
            # Search for any of the tags in the JSON array
            tag_conditions = " OR ".join(["tags LIKE ?" for _ in tags])
            query += f" AND ({tag_conditions})"
            params.extend([f'%"{tag}"%' for tag in tags])
        
        query += " ORDER BY review_date DESC LIMIT ?"
        params.append(limit)
        
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            return [dict(row) for row in cursor.fetchall()]
    
    def get_project_lifecycle_status(self, project_identifier: str) -> Dict:
        """
        Analyze project lifecycle based on review history
        Returns status like 'emerging', 'growing', 'mature', 'declining', 'abandoned'
        """
        history = self.get_project_history(project_identifier, limit=100)
        
        if not history:
            return {'status': 'unknown', 'reason': 'No review history'}
        
        if len(history) == 1:
            return {'status': 'new', 'reason': 'First review', 'reviews': 1}
        
        # Check review frequency
        first_date = datetime.fromisoformat(history[-1]['review_date'])
        last_date = datetime.fromisoformat(history[0]['review_date'])
        days_span = (last_date - first_date).days
        
        if days_span > 90 and len(history) < 3:
            return {'status': 'abandoned', 'reason': 'Infrequent reviews over long period', 'reviews': len(history)}
        
        # Check metric trends (stars)
        if len(history) >= 3:
            recent_stars = [r['stars'] for r in history[:3] if r.get('stars')]
            older_stars = [r['stars'] for r in history[-3:] if r.get('stars')]
            
            if recent_stars and older_stars:
                recent_avg = sum(recent_stars) / len(recent_stars)
                older_avg = sum(older_stars) / len(older_stars)
                
                growth_rate = ((recent_avg - older_avg) / older_avg * 100) if older_avg > 0 else 0
                
                if growth_rate > 50:
                    return {'status': 'growing', 'reason': f'{growth_rate:.1f}% growth', 'reviews': len(history)}
                elif growth_rate < -20:
                    return {'status': 'declining', 'reason': f'{growth_rate:.1f}% decline', 'reviews': len(history)}
                elif recent_avg > 10000:
                    return {'status': 'mature', 'reason': f'{int(recent_avg)} stars', 'reviews': len(history)}
                else:
                    return {'status': 'stable', 'reason': f'{growth_rate:.1f}% change', 'reviews': len(history)}
        
        return {'status': 'emerging', 'reason': 'Early stage tracking', 'reviews': len(history)}
    
    def generate_historical_context(self, project_identifier: str, current_metrics: Dict) -> str:
        """
        Generate human-readable historical context for blog posts
        Returns formatted string with comparative analysis
        """
        latest_review = self.get_latest_review(project_identifier)
        
        if not latest_review:
            return ""
        
        # Get comparative metrics
        changes_90d = self.get_comparative_metrics(project_identifier, days_back=90)
        changes_30d = self.get_comparative_metrics(project_identifier, days_back=30)
        
        # Get lifecycle status
        lifecycle = self.get_project_lifecycle_status(project_identifier)
        
        context_parts = []
        
        # Add review history note
        history = self.get_project_history(project_identifier)
        if len(history) > 1:
            first_review_date = datetime.fromisoformat(history[-1]['review_date'])
            context_parts.append(
                f"**Previously Reviewed**: First covered {first_review_date.strftime('%B %Y')}, "
                f"tracked {len(history)} times"
            )
        
        # Add growth metrics
        if changes_90d:
            growth_notes = []
            for metric, data in changes_90d.items():
                if data['change'] != 0:
                    sign = "+" if data['change'] > 0 else ""
                    growth_notes.append(
                        f"{metric}: {sign}{data['change']:,} ({sign}{data['pct_change']}%) "
                        f"over {data['days']} days"
                    )
            
            if growth_notes:
                context_parts.append("**Growth**: " + ", ".join(growth_notes))
        
        # Add lifecycle status
        context_parts.append(f"**Status**: {lifecycle['status'].title()} - {lifecycle['reason']}")
        
        # Add previous commentary if available
        if latest_review.get('generated_commentary'):
            prev_commentary = latest_review['generated_commentary'][:200]
            context_parts.append(f"**Previous Take**: \"{prev_commentary}...\"")
        
        return "\n\n".join(context_parts)
    
    def get_database_stats(self) -> Dict:
        """Get overall database statistics"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            cursor.execute("SELECT COUNT(*) as total FROM project_reviews")
            total_reviews = cursor.fetchone()['total']
            
            cursor.execute("SELECT COUNT(DISTINCT project_identifier) as total FROM project_reviews")
            unique_projects = cursor.fetchone()['total']
            
            cursor.execute("SELECT MIN(review_date) as first, MAX(review_date) as last FROM project_reviews")
            date_range = cursor.fetchone()
            
            cursor.execute('''
                SELECT project_type, COUNT(*) as count 
                FROM project_reviews 
                GROUP BY project_type
            ''')
            by_type = {row['project_type']: row['count'] for row in cursor.fetchall()}
            
            cursor.execute('''
                SELECT source_repo, COUNT(*) as count 
                FROM project_reviews 
                GROUP BY source_repo
            ''')
            by_source = {row['source_repo']: row['count'] for row in cursor.fetchall()}
            
            return {
                'total_reviews': total_reviews,
                'unique_projects': unique_projects,
                'date_range': {
                    'first': date_range['first'],
                    'last': date_range['last']
                },
                'by_type': by_type,
                'by_source': by_source
            }


# Convenience functions for quick access
def get_db() -> ReviewDatabase:
    """Get database instance"""
    return ReviewDatabase()


def add_project_review(project_data: Dict) -> int:
    """Quick function to add a review from a dict"""
    review = ProjectReview(**project_data)
    db = get_db()
    return db.add_review(review)


def get_project_context(project_identifier: str, current_metrics: Dict = None) -> str:
    """Quick function to get historical context for a project"""
    db = get_db()
    return db.generate_historical_context(project_identifier, current_metrics or {})


if __name__ == "__main__":
    # Test the database
    print("🗄️  Review Database System")
    print("=" * 50)
    
    db = get_db()
    stats = db.get_database_stats()
    
    print(f"\n📊 Database Statistics:")
    print(f"  Total Reviews: {stats['total_reviews']}")
    print(f"  Unique Projects: {stats['unique_projects']}")
    print(f"  Date Range: {stats['date_range']['first']} to {stats['date_range']['last']}")
    print(f"\n  By Type: {stats['by_type']}")
    print(f"  By Source: {stats['by_source']}")
    
    print("\n✅ Database initialized successfully!")
