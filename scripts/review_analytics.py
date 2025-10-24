#!/usr/bin/env python3
"""
Review Database Analytics CLI
Interactive command-line tool for querying and analyzing the review database

Usage:
    python review_analytics.py stats
    python review_analytics.py trending --days 30
    python review_analytics.py project github:ollama/ollama
    python review_analytics.py search --type repo --min-stars 1000
    python review_analytics.py predictions --days 90
"""
import argparse
import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List

from review_database import ReviewDatabase
from review_integration import ReviewIntegration


class ReviewAnalytics:
    """Analytics and reporting for the review database"""
    
    def __init__(self):
        self.db = ReviewDatabase()
        self.integration = ReviewIntegration()
    
    def print_stats(self):
        """Print overall database statistics"""
        stats = self.db.get_database_stats()
        
        print("\n📊 Review Database Statistics")
        print("=" * 60)
        print(f"Total Reviews: {stats['total_reviews']}")
        print(f"Unique Projects: {stats['unique_projects']}")
        print(f"\nDate Range:")
        print(f"  First Review: {stats['date_range']['first']}")
        print(f"  Latest Review: {stats['date_range']['last']}")
        print(f"\nBy Project Type:")
        for ptype, count in sorted(stats['by_type'].items(), key=lambda x: x[1], reverse=True):
            print(f"  {ptype}: {count}")
        print(f"\nBy Source:")
        for source, count in sorted(stats['by_source'].items(), key=lambda x: x[1], reverse=True):
            print(f"  {source}: {count}")
    
    def print_trending(self, days: int = 30, metric: str = 'stars', limit: int = 10):
        """Print trending projects"""
        trending = self.db.get_trending_projects(metric, days, limit)
        
        print(f"\n🔥 Trending Projects (by {metric}, last {days} days)")
        print("=" * 60)
        
        if not trending:
            print("No trending projects found in this period")
            return
        
        for i, project in enumerate(trending, 1):
            print(f"\n{i}. {project['project_name']}")
            print(f"   Growth: +{project['growth']:,} ({project['growth_pct']}%)")
            print(f"   {metric.title()}: {project['start_value']:,} → {project['end_value']:,}")
            print(f"   Reviews: {project['review_count']}")
    
    def print_project_details(self, project_id: str):
        """Print detailed information about a specific project"""
        history = self.db.get_project_history(project_id, limit=100)
        
        if not history:
            print(f"\n❌ No reviews found for: {project_id}")
            return
        
        latest = history[0]
        lifecycle = self.db.get_project_lifecycle_status(project_id)
        changes_90d = self.db.get_comparative_metrics(project_id, 90)
        
        print(f"\n📦 Project: {latest['project_name']}")
        print("=" * 60)
        print(f"Type: {latest['project_type']}")
        print(f"Identifier: {project_id}")
        print(f"Status: {lifecycle['status'].title()} - {lifecycle['reason']}")
        print(f"\nReview History: {len(history)} reviews")
        print(f"  First: {history[-1]['review_date']}")
        print(f"  Latest: {history[0]['review_date']}")
        
        if latest.get('stars'):
            print(f"\nCurrent Metrics:")
            print(f"  Stars: {latest['stars']:,}")
            if latest.get('forks'):
                print(f"  Forks: {latest['forks']:,}")
            if latest.get('downloads'):
                print(f"  Downloads: {latest['downloads']:,}")
        
        if changes_90d:
            print(f"\n90-Day Changes:")
            for metric, data in changes_90d.items():
                sign = "+" if data['change'] > 0 else ""
                print(f"  {metric.title()}: {sign}{data['change']:,} ({sign}{data['pct_change']}%)")
        
        if latest.get('generated_commentary'):
            print(f"\nLatest Commentary:")
            print(f"  \"{latest['generated_commentary'][:200]}...\"")
            print(f"  - {latest.get('persona_used', 'Unknown')} ({latest['review_date']})")
        
        print(f"\nRecent Reviews:")
        for review in history[:5]:
            print(f"  • {review['review_date']} - {review.get('persona_used', 'Unknown')}")
            if review.get('stars'):
                print(f"    Stars: {review['stars']:,}")
    
    def print_search_results(self, **filters):
        """Print search results with filters"""
        results = self.db.search_reviews(**filters)
        
        print(f"\n🔍 Search Results ({len(results)} found)")
        print("=" * 60)
        
        if not results:
            print("No results found")
            return
        
        for review in results:
            print(f"\n• {review['project_name']}")
            print(f"  Type: {review['project_type']} | Date: {review['review_date']}")
            if review.get('stars'):
                print(f"  Stars: {review['stars']:,}")
            if review.get('generated_commentary'):
                print(f"  \"{review['generated_commentary'][:150]}...\"")
    
    def print_predictions(self, days: int = 90):
        """Print validated predictions"""
        validations = self.integration.find_prediction_validations(days)
        
        print(f"\n🎯 Validated Predictions (last {days} days)")
        print("=" * 60)
        
        if not validations:
            print("No validated predictions found")
            return
        
        for i, val in enumerate(validations, 1):
            print(f"\n{i}. {val['project']}")
            print(f"   Original Review: {val['original_review_date']}")
            print(f"   Growth: +{val['growth']['change']:,} stars ({val['growth']['pct_change']}%)")
            print(f"   Original Take: \"{val['original_commentary'][:150]}...\"")
    
    def generate_trend_report(self, days: int = 30, output_file: str = None):
        """Generate comprehensive trend report"""
        report = self.integration.generate_trend_report(days)
        
        print(f"\n📈 Trend Report ({days} days)")
        print("=" * 60)
        
        print(f"\nReview Activity:")
        for ptype, count in sorted(report['review_counts'].items(), key=lambda x: x[1], reverse=True):
            print(f"  {ptype}: {count} reviews")
        
        print(f"\nTop Trending (by stars):")
        for i, project in enumerate(report['trending_by_stars'][:5], 1):
            print(f"  {i}. {project['project_name']}: +{project['growth']:,} ({project['growth_pct']}%)")
        
        if output_file:
            with open(output_file, 'w') as f:
                json.dump(report, f, indent=2)
            print(f"\n💾 Full report saved to: {output_file}")


def main():
    """CLI entry point"""
    parser = argparse.ArgumentParser(description='Review Database Analytics')
    subparsers = parser.add_subparsers(dest='command', help='Command to run')
    
    # Stats command
    subparsers.add_parser('stats', help='Show database statistics')
    
    # Trending command
    trending_parser = subparsers.add_parser('trending', help='Show trending projects')
    trending_parser.add_argument('--days', type=int, default=30, help='Days to look back')
    trending_parser.add_argument('--metric', type=str, default='stars', choices=['stars', 'forks', 'downloads'])
    trending_parser.add_argument('--limit', type=int, default=10, help='Number of results')
    
    # Project command
    project_parser = subparsers.add_parser('project', help='Show project details')
    project_parser.add_argument('project_id', type=str, help='Project identifier')
    
    # Search command
    search_parser = subparsers.add_parser('search', help='Search reviews')
    search_parser.add_argument('--type', type=str, help='Project type')
    search_parser.add_argument('--persona', type=str, help='Persona used')
    search_parser.add_argument('--min-stars', type=int, help='Minimum stars')
    search_parser.add_argument('--days', type=int, help='Days to look back')
    search_parser.add_argument('--limit', type=int, default=20, help='Number of results')
    
    # Predictions command
    pred_parser = subparsers.add_parser('predictions', help='Show validated predictions')
    pred_parser.add_argument('--days', type=int, default=90, help='Days to look back')
    
    # Report command
    report_parser = subparsers.add_parser('report', help='Generate trend report')
    report_parser.add_argument('--days', type=int, default=30, help='Days to look back')
    report_parser.add_argument('--output', type=str, help='Output file (JSON)')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    analytics = ReviewAnalytics()
    
    if args.command == 'stats':
        analytics.print_stats()
    
    elif args.command == 'trending':
        analytics.print_trending(args.days, args.metric, args.limit)
    
    elif args.command == 'project':
        analytics.print_project_details(args.project_id)
    
    elif args.command == 'search':
        filters = {
            'project_type': args.type,
            'persona': args.persona,
            'min_stars': args.min_stars,
            'days_back': args.days,
            'limit': args.limit
        }
        # Remove None values
        filters = {k: v for k, v in filters.items() if v is not None}
        analytics.print_search_results(**filters)
    
    elif args.command == 'predictions':
        analytics.print_predictions(args.days)
    
    elif args.command == 'report':
        analytics.generate_trend_report(args.days, args.output)


if __name__ == "__main__":
    main()
