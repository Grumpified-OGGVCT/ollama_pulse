#!/usr/bin/env python3
"""
Update docs/index.html with latest reports
Dynamically generates the report list from actual markdown files
"""
from pathlib import Path
from datetime import datetime
import re

def extract_frontmatter(md_file: Path) -> dict:
    """Extract frontmatter from markdown file"""
    content = md_file.read_text(encoding='utf-8')
    
    # Extract frontmatter
    match = re.search(r'^---\n(.*?)\n---', content, re.DOTALL)
    if not match:
        return {}
    
    frontmatter = {}
    for line in match.group(1).split('\n'):
        if ':' in line:
            key, value = line.split(':', 1)
            frontmatter[key.strip()] = value.strip()
    
    return frontmatter

def generate_index_html():
    """Generate index.html from report files"""
    # Get script directory and navigate to repo root
    script_dir = Path(__file__).parent
    repo_root = script_dir.parent
    reports_dir = repo_root / 'docs' / 'reports'
    reports = []

    # Scan all markdown files
    for md_file in sorted(reports_dir.glob('pulse-*.md'), reverse=True):
        frontmatter = extract_frontmatter(md_file)
        
        date = frontmatter.get('date', md_file.stem.replace('pulse-', ''))
        title = frontmatter.get('title', f'Ollama ecosystem discoveries from {date}')
        generated = frontmatter.get('generated', date)
        
        # Extract just the date part if it's a full timestamp
        if 'T' in generated or ' ' in generated:
            # Parse and format nicely
            try:
                dt = datetime.fromisoformat(generated.replace('Z', '+00:00'))
                generated = dt.strftime('%I:%M %p CST on %Y-%m-%d')
            except:
                pass
        
        reports.append({
            'date': date,
            'title': title,
            'generated': generated,
            'filename': md_file.stem + '.html'
        })
    
    # Generate HTML
    html = '''---
layout: default
title: Ollama Pulse - Daily Ecosystem Intelligence
---

<div style="margin-bottom: 20px;">
  <h2 style="color: #60a5fa;">Welcome to Ollama Pulse</h2>
  <p style="color: #94a3b8;">Daily ecosystem intelligence tracking the Ollama world. Navigate through reports, search for topics, and customize your reading experience with accessibility controls.</p>
  
  <div style="background: #1e293b; padding: 16px; border-radius: 8px; margin: 16px 0; border: 1px solid #334155;">
    <h3 style="color: #60a5fa; margin-top: 0;">🎯 Features</h3>
    <ul style="color: #e2e8f0; line-height: 1.8;">
      <li><strong>Navigation:</strong> Use Next/Previous buttons or arrow keys to browse reports</li>
      <li><strong>Search:</strong> Press <kbd style="background: #0f172a; padding: 2px 6px; border-radius: 3px;">/</kbd> to search across reports</li>
      <li><strong>Accessibility:</strong> Click the ♿ button (bottom-right) to customize font size and zoom</li>
      <li><strong>Keyboard Shortcuts:</strong> <kbd>h</kbd> for home, <kbd>n</kbd> for next, <kbd>p</kbd> for previous</li>
    </ul>
  </div>
</div>

<div class="controls">
  <input type="text" id="search" placeholder="🔍 Search reports by date or keyword..." />
  <select id="sort">
    <option value="date-desc">Newest First</option>
    <option value="date-asc">Oldest First</option>
  </select>
</div>

<div id="report-list">
'''
    
    # Add report cards
    for i, report in enumerate(reports):
        latest_badge = ' <span style="background: #60a5fa; color: #0f172a; padding: 2px 8px; border-radius: 4px; font-size: 12px; font-weight: bold;">LATEST</span>' if i == 0 else ''
        
        html += f'''  <div class="card">
    <h3>📡 Report: {report['date']}{latest_badge}</h3>
    <p>{report['title']}</p>
    <p class="meta">Generated: {report['generated']}</p>
    <a href="reports/{report['filename']}">Read full report →</a>
  </div>
'''
    
    html += '''
</div>

<script>
// Simple search and sort for index page
(function() {
  const searchInput = document.getElementById('search');
  const sortSelect = document.getElementById('sort');
  const reportList = document.getElementById('report-list');
  const cards = Array.from(reportList.querySelectorAll('.card'));
  
  searchInput.addEventListener('input', function(e) {
    const query = e.target.value.toLowerCase();
    cards.forEach(card => {
      const text = card.textContent.toLowerCase();
      card.style.display = text.includes(query) ? 'block' : 'none';
    });
  });
  
  sortSelect.addEventListener('change', function(e) {
    const sorted = cards.sort((a, b) => {
      const dateA = a.querySelector('h3').textContent.match(/\\d{4}-\\d{2}-\\d{2}/)[0];
      const dateB = b.querySelector('h3').textContent.match(/\\d{4}-\\d{2}-\\d{2}/)[0];
      return e.target.value === 'date-desc' ? dateB.localeCompare(dateA) : dateA.localeCompare(dateB);
    });
    sorted.forEach(card => reportList.appendChild(card));
  });
})();
</script>
'''

    # Write to file
    index_file = repo_root / 'docs' / 'index.html'
    index_file.write_text(html, encoding='utf-8')
    print(f"✅ Updated {index_file} with {len(reports)} reports")

if __name__ == '__main__':
    generate_index_html()

