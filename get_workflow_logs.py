#!/usr/bin/env python3
"""Get latest workflow run logs from GitHub API"""
import requests
import json

# Get latest morning report workflow runs
response = requests.get(
    'https://api.github.com/repos/Grumpified-OGGVCT/ollama_pulse/actions/workflows/morning_report.yml/runs',
    params={'per_page': 5}
)

if response.status_code != 200:
    print(f"Error: {response.status_code}")
    print(response.text)
    exit(1)

runs = response.json()['workflow_runs']

if not runs:
    print("No workflow runs found")
    exit(1)

# Get the latest run
latest_run = runs[0]
print(f"Latest run: {latest_run['id']}")
print(f"Status: {latest_run['status']}")
print(f"Conclusion: {latest_run['conclusion']}")
print(f"Created: {latest_run['created_at']}")
print(f"URL: {latest_run['html_url']}")

# Get jobs for this run
jobs_response = requests.get(latest_run['jobs_url'])
jobs = jobs_response.json()['jobs']

for job in jobs:
    print(f"\n{'='*60}")
    print(f"Job: {job['name']}")
    print(f"Status: {job['status']} / {job['conclusion']}")
    
    # Get logs URL
    logs_url = job['url'] + '/logs'
    
    print(f"\nGetting logs from: {logs_url}")
    logs_response = requests.get(logs_url)
    
    if logs_response.status_code == 200:
        logs = logs_response.text
        
        # Look for key messages
        if '🤖 Activating multi-model intelligence pipeline' in logs:
            print("\n✅ MODEL PIPELINE WAS ACTIVATED!")
        else:
            print("\n❌ MODEL PIPELINE NOT ACTIVATED")
        
        if 'Enhanced generation not available' in logs:
            print("❌ Import failed for enhanced_report_generator.py")
        
        if 'Model enhancement error:' in logs:
            print("❌ Model enhancement crashed:")
            # Find the error message
            for line in logs.split('\n'):
                if 'Model enhancement error:' in line:
                    print(f"   {line}")
        
        # Save full logs
        log_file = f"workflow_logs_job_{job['id']}.txt"
        with open(log_file, 'w', encoding='utf-8') as f:
            f.write(logs)
        print(f"\nFull logs saved to: {log_file}")
    else:
        print(f"Failed to get logs: {logs_response.status_code}")

print(f"\n{'='*60}\n")
print("Check the log files to see what went wrong!")

