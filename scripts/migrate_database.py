#!/usr/bin/env python3
"""
Database Migration Script
Backfills the review database with data from existing blog posts

This script:
1. Scans all existing blog posts in docs/_posts/
2. Extracts project data from Ollama Pulse and AI Research Daily posts
3. Populates the review database with historical data
4. Handles both Ollama Pulse and AI Research Daily formats
"""
import json
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
import frontmatter

from review_database import ReviewDatabase, ProjectReview
from review_integration import ReviewIntegration


class DatabaseMigration:
    """Handles migration of existing blog data into the database"""
    
    def __init__(self, posts_dir: Path = Path("docs/_posts")):
        self.posts_dir = posts_dir
        self.db = ReviewDatabase()
        self.integration = ReviewIntegration()
        self.stats = {
            'posts_processed': 0,
            'reviews_created': 0,
            'errors': 0
        }
    
    def extract_github_projects_from_markdown(self, content: str) -> List[Dict]:
        """Extract GitHub project mentions from markdown content"""
        projects = []
        
        # Pattern: [project-name](github-url) with optional stars/forks
        # Example: [ollama/ollama](https://github.com/ollama/ollama) ⭐ 50K
        pattern = r'\[([^\]]+)\]\((https://github\.com/[^\)]+)\)(?:\s*⭐\s*([0-9KM.]+))?'
        
        for match in re.finditer(pattern, content):
            name = match.group(1)
            url = match.group(2)
            stars_str = match.group(3)
            
            stars = None
            if stars_str:
                # Convert "50K" to 50000, "1.5M" to 1500000
                stars_str = stars_str.upper().replace(',', '')
                if 'K' in stars_str:
                    stars = int(float(stars_str.replace('K', '')) * 1000)
                elif 'M' in stars_str:
                    stars = int(float(stars_str.replace('M', '')) * 1000000)
                else:
                    try:
                        stars = int(stars_str)
                    except:
                        pass
            
            projects.append({
                'name': name,
                'url': url,
                'stars': stars
            })
        
        return projects
    
    def extract_commentary_for_project(self, content: str, project_name: str) -> Optional[str]:
        """Extract the commentary/description for a specific project from markdown"""
        # Look for the project name followed by text until the next project or section
        pattern = rf'{re.escape(project_name)}[^\n]*\n([^\n#]+)'
        match = re.search(pattern, content, re.MULTILINE)
        
        if match:
            return match.group(1).strip()
        
        return None
    
    def parse_ollama_pulse_post(self, post_path: Path) -> List[ProjectReview]:
        """Parse an Ollama Pulse blog post and extract reviews"""
        reviews = []
        
        try:
            # Load post with frontmatter
            with open(post_path, 'r', encoding='utf-8') as f:
                post = frontmatter.load(f)
            
            content = post.content
            metadata = post.metadata
            
            # Extract date from filename or frontmatter
            date_match = re.search(r'(\d{4}-\d{2}-\d{2})', post_path.name)
            if date_match:
                review_date = date_match.group(1)
            else:
                review_date = metadata.get('date', datetime.now().isoformat())
            
            # Extract persona if mentioned
            persona = None
            if 'persona' in metadata:
                persona = metadata['persona']
            else:
                # Try to detect from content
                for p in ['Hype-Caster', 'Mechanic', 'Curious Analyst', 'Trend-Spotter', 'Informed Enthusiast']:
                    if p in content:
                        persona = p
                        break
            
            # Extract GitHub projects
            projects = self.extract_github_projects_from_markdown(content)
            
            for project in projects:
                project_id = self.integration.normalize_project_identifier(project['url'])
                commentary = self.extract_commentary_for_project(content, project['name'])
                
                review = ProjectReview(
                    project_identifier=project_id,
                    project_name=project['name'],
                    project_type='repo',
                    review_date=review_date,
                    stars=project.get('stars'),
                    generated_commentary=commentary,
                    persona_used=persona,
                    source_repo='ollama_pulse',
                    blog_post_url=f"/posts/{post_path.stem}"
                )
                
                reviews.append(review)
        
        except Exception as e:
            print(f"❌ Error parsing {post_path.name}: {e}")
            self.stats['errors'] += 1
        
        return reviews
    
    def parse_ai_research_post(self, post_path: Path) -> List[ProjectReview]:
        """Parse an AI Research Daily blog post and extract reviews"""
        reviews = []
        
        try:
            with open(post_path, 'r', encoding='utf-8') as f:
                post = frontmatter.load(f)
            
            content = post.content
            metadata = post.metadata
            
            # Extract date
            date_match = re.search(r'(\d{4}-\d{2}-\d{2})', post_path.name)
            review_date = date_match.group(1) if date_match else datetime.now().isoformat()
            
            # Extract arXiv papers
            arxiv_pattern = r'\[([^\]]+)\]\((https://arxiv\.org/abs/[^\)]+)\)'
            
            for match in re.finditer(arxiv_pattern, content):
                paper_title = match.group(1)
                paper_url = match.group(2)
                
                project_id = self.integration.normalize_project_identifier(paper_url)
                commentary = self.extract_commentary_for_project(content, paper_title)
                
                review = ProjectReview(
                    project_identifier=project_id,
                    project_name=paper_title,
                    project_type='paper',
                    review_date=review_date,
                    generated_commentary=commentary,
                    persona_used='The Scholar',
                    source_repo='ai_research_daily',
                    blog_post_url=f"/posts/{post_path.stem}"
                )
                
                reviews.append(review)
        
        except Exception as e:
            print(f"❌ Error parsing {post_path.name}: {e}")
            self.stats['errors'] += 1
        
        return reviews
    
    def migrate_all_posts(self, dry_run: bool = False):
        """Migrate all existing blog posts into the database"""
        print("�� Starting database migration...")
        print(f"📁 Scanning: {self.posts_dir}")
        print(f"�� Dry run: {dry_run}")
        print("=" * 60)
        
        if not self.posts_dir.exists():
            print(f"❌ Posts directory not found: {self.posts_dir}")
            return
        
        # Get all markdown files
        post_files = sorted(self.posts_dir.glob("*.md"))
        print(f"\n📄 Found {len(post_files)} blog posts")
        
        for post_file in post_files:
            print(f"\n📝 Processing: {post_file.name}")
            
            # Determine post type
            if 'ollama' in post_file.name.lower() or 'pulse' in post_file.name.lower():
                reviews = self.parse_ollama_pulse_post(post_file)
            elif 'lab' in post_file.name.lower() or 'research' in post_file.name.lower():
                reviews = self.parse_ai_research_post(post_file)
            else:
                print(f"  ⚠️  Unknown post type, skipping")
                continue
            
            print(f"  Found {len(reviews)} projects/papers")
            
            if not dry_run:
                for review in reviews:
                    try:
                        self.db.add_review(review)
                        self.stats['reviews_created'] += 1
                    except Exception as e:
                        print(f"    ❌ Error storing review: {e}")
                        self.stats['errors'] += 1
            
            self.stats['posts_processed'] += 1
        
        # Print summary
        print("\n" + "=" * 60)
        print("📊 Migration Summary:")
        print(f"  Posts Processed: {self.stats['posts_processed']}")
        print(f"  Reviews Created: {self.stats['reviews_created']}")
        print(f"  Errors: {self.stats['errors']}")
        
        if not dry_run:
            db_stats = self.db.get_database_stats()
            print(f"\n🗄️  Database Stats:")
            print(f"  Total Reviews: {db_stats['total_reviews']}")
            print(f"  Unique Projects: {db_stats['unique_projects']}")
            print(f"  By Type: {db_stats['by_type']}")
        
        print("\n✅ Migration complete!")


def main():
    """Run migration"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Migrate blog posts to review database')
    parser.add_argument('--dry-run', action='store_true', help='Run without writing to database')
    parser.add_argument('--posts-dir', type=str, default='docs/_posts', help='Path to posts directory')
    
    args = parser.parse_args()
    
    migration = DatabaseMigration(Path(args.posts_dir))
    migration.migrate_all_posts(dry_run=args.dry_run)


if __name__ == "__main__":
    main()
