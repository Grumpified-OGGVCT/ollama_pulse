#!/usr/bin/env python3
import requests

# Get current aggregate.py from main branch
response = requests.get(
    'https://raw.githubusercontent.com/Grumpified-OGGVCT/ollama_pulse/main/scripts/aggregate.py'
)

code = response.text

print("Checking if aggregation fix is on main branch...")
print("="*60)

if "entries_without_url" in code:
    print("YES - Fix IS on main branch")
    print("  Found: entries_without_url variable")
    print("  Found: graceful URL handling")
else:
    print("NO - Fix is NOT on main branch")
    print("  Still using old buggy code")

if "unique_dict = {}" in code:
    print("YES - New deduplication logic present")
else:
    print("NO - Still using old dict comprehension")

# Check the actual problematic line
if "{e['url']: e for e in all_entries}" in code:
    print("PROBLEM - Old buggy line still present!")
else:
    print("GOOD - Old buggy line removed")

print("\n" + "="*60)
print("Searching for the exact current deduplication code...")
print("="*60)

# Find the deduplication section
lines = code.split('\n')
for i, line in enumerate(lines):
    if 'Deduplicate' in line or 'unique' in line.lower():
        print(f"Line {i+1}: {line[:100]}")
        # Print surrounding lines
        if i < len(lines) - 5:
            for j in range(i+1, min(i+10, len(lines))):
                print(f"Line {j+1}: {lines[j][:100]}")
            break

