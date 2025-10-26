#!/usr/bin/env python3
"""
Ollama Pulse - Manual Tracking Ingestion
Loads projects from tracked_projects.json for inclusion in reports
"""
import json
from datetime import datetime
from pathlib import Path

TRACKED_PROJECTS_FILE = "tracked_projects.json"

def ensure_data_dir():
    Path("data/manual").mkdir(parents=True, exist_ok=True)

def get_today_filename():
    return f"data/manual/{datetime.now().strftime('%Y-%m-%d')}.json"

def load_tracked_projects():
    """Load manually tracked projects from JSON file"""
    print("📡 Loading manually tracked projects...")
    
    try:
        if not Path(TRACKED_PROJECTS_FILE).exists():
            print(f"⚠️  {TRACKED_PROJECTS_FILE} not found, creating template...")
            create_template()
            return []
        
        with open(TRACKED_PROJECTS_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        projects = data.get('projects', [])
        
        # Add today's date if not specified
        for project in projects:
            if 'date' not in project:
                project['date'] = datetime.now().isoformat()
            
            # Ensure required fields
            if 'source' not in project:
                project['source'] = 'manual_tracking'
            
            if 'turbo_score' not in project:
                project['turbo_score'] = 0.8  # Default high score for manual entries
        
        print(f"✅ Loaded {len(projects)} manually tracked projects")
        return projects
        
    except Exception as e:
        print(f"❌ Error loading tracked projects: {e}")
        return []

def create_template():
    """Create template tracked_projects.json if it doesn't exist"""
    template = {
        "_instructions": "Add projects here to manually track them in Ollama Pulse reports.",
        "_format": {
            "title": "Project name",
            "url": "https://github.com/user/repo",
            "summary": "Brief description",
            "source": "manual_tracking",
            "turbo_score": 0.8,
            "highlights": ["tag1", "tag2"]
        },
        "projects": []
    }
    
    with open(TRACKED_PROJECTS_FILE, 'w', encoding='utf-8') as f:
        json.dump(template, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Created template: {TRACKED_PROJECTS_FILE}")

def save_data(entries):
    """Save entries to JSON file"""
    filename = get_today_filename()
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(entries, f, indent=2, ensure_ascii=False)
    
    print(f"💾 Saved {len(entries)} entries to {filename}")

def main():
    """Main ingestion function"""
    print("🚀 Starting manual tracking ingestion...")
    ensure_data_dir()
    
    entries = load_tracked_projects()
    
    if entries:
        save_data(entries)
    else:
        print("ℹ️  No manually tracked projects found")
    
    print("✅ Manual tracking ingestion complete!")

if __name__ == "__main__":
    main()

