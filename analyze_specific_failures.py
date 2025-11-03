#!/usr/bin/env python3
import requests

# Get latest failed ingestion run
response = requests.get(
    'https://api.github.com/repos/Grumpified-OGGVCT/ollama_pulse/actions/workflows/ingest.yml/runs',
    params={'per_page': 5}
)

runs = response.json()['workflow_runs']
failed_runs = [r for r in runs if r['conclusion'] == 'failure']

if not failed_runs:
    print("No failed runs found!")
    exit(0)

latest_failed = failed_runs[0]
print(f"Latest Failed Run: {latest_failed['id']}")
print(f"Created: {latest_failed['created_at']}")
print(f"URL: {latest_failed['html_url']}\n")

# Get jobs for this run
jobs_response = requests.get(latest_failed['jobs_url'])
jobs = jobs_response.json()['jobs']

print("="*60)
print("JOB STATUS BREAKDOWN")
print("="*60)

for job in jobs:
    status_emoji = "PASS" if job['conclusion'] == 'success' else "FAIL" if job['conclusion'] == 'failure' else "SKIP"
    print(f"{status_emoji:6} - {job['name']}")
    
    # If failed, show which step
    if job['conclusion'] == 'failure':
        for step in job['steps']:
            if step['conclusion'] == 'failure':
                print(f"         Failed at: {step['name']}")

print("\n" + "="*60)
print("FAILURE ANALYSIS")
print("="*60)

# Count failure types
failure_by_step = {}
for job in jobs:
    if job['conclusion'] == 'failure':
        for step in job['steps']:
            if step['conclusion'] == 'failure':
                step_name = step['name']
                failure_by_step[step_name] = failure_by_step.get(step_name, 0) + 1

for step_name, count in sorted(failure_by_step.items(), key=lambda x: x[1], reverse=True):
    print(f"{count} failures in: {step_name}")

print("\n" + "="*60)
print("ACTION REQUIRED")
print("="*60)
print("\nGo to these URLs to see detailed logs:")
for job in jobs:
    if job['conclusion'] == 'failure':
        print(f"\n{job['name']}:")
        print(f"  {job['html_url']}")

