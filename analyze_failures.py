#!/usr/bin/env python3
import requests
import json

workflows = [
    ('ingest.yml', 'Ingestion'),
    ('morning_report.yml', 'Morning Report'),
    ('afternoon_report.yml', 'Afternoon Report')
]

print("="*60)
print("ANALYZING OVERNIGHT WORKFLOW FAILURES")
print("="*60)

for workflow_file, workflow_name in workflows:
    print(f"\n{'='*60}")
    print(f"Workflow: {workflow_name}")
    print('='*60)
    
    # Get recent runs
    response = requests.get(
        f'https://api.github.com/repos/Grumpified-OGGVCT/ollama_pulse/actions/workflows/{workflow_file}/runs',
        params={'per_page': 20}
    )
    
    if response.status_code != 200:
        print(f"Failed to fetch: {response.status_code}")
        continue
    
    runs = response.json()['workflow_runs']
    
    # Count by status
    failed = [r for r in runs if r['conclusion'] == 'failure']
    success = [r for r in runs if r['conclusion'] == 'success']
    
    print(f"\nLast 20 runs:")
    print(f"  Failed: {len(failed)}")
    print(f"  Success: {len(success)}")
    
    if failed:
        print(f"\n  Most Recent Failures:")
        for run in failed[:5]:
            print(f"    - {run['created_at'][:19]} - Run #{run['id']}")
            print(f"      URL: {run['html_url']}")
    
    if failed:
        # Get details on most recent failure
        latest_fail = failed[0]
        print(f"\n  Latest Failure Details:")
        jobs_response = requests.get(latest_fail['jobs_url'])
        jobs = jobs_response.json()['jobs']
        
        for job in jobs:
            if job['conclusion'] == 'failure':
                print(f"\n    Failed Job: {job['name']}")
                print(f"    Conclusion: {job['conclusion']}")
                
                # Get steps
                for step in job['steps']:
                    if step['conclusion'] == 'failure':
                        print(f"      ❌ Step failed: {step['name']}")
                        print(f"         Started: {step['started_at']}")
                        print(f"         Completed: {step['completed_at']}")

print("\n" + "="*60)
print("Analysis complete - check the URLs above for detailed logs")
print("="*60)

