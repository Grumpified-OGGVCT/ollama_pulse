#!/usr/bin/env python3
"""
Run full Ollama Pulse workflow: ingests + report generation + Nostr posting
"""
import subprocess
import sys
from datetime import datetime
from pathlib import Path

def run_command(cmd, description):
    """Run a command and report status"""
    print(f"\n{'='*60}")
    print(f"🚀 {description}")
    print(f"{'='*60}")
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=120)
        if result.stdout:
            print(result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr)
        if result.returncode == 0:
            print(f"✅ {description} - SUCCESS")
            return True
        else:
            print(f"⚠️ {description} - FAILED (code: {result.returncode})")
            return False
    except subprocess.TimeoutExpired:
        print(f"⏱️ {description} - TIMEOUT (120s)")
        return False
    except Exception as e:
        print(f"❌ {description} - ERROR: {e}")
        return False

def main():
    print("📡 OLLAMA PULSE - FULL WORKFLOW")
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # List of all 10 ingests
    ingests = [
        ("python scripts/ingest_official.py", "1️⃣  Ingest Official (Ollama blog, Cloud API)"),
        ("python scripts/ingest_cloud.py", "2️⃣  Ingest Cloud (Ollama Turbo/Cloud)"),
        ("python scripts/ingest_community.py", "3️⃣  Ingest Community (GitHub discussions)"),
        ("python scripts/ingest_issues.py", "4️⃣  Ingest Issues (GitHub issues)"),
        ("python scripts/ingest_tools.py", "5️⃣  Ingest Tools (GitHub repositories)"),
        ("python scripts/ingest_bounties.py", "6️⃣  Ingest Bounties (Reward opportunities)"),
        ("python scripts/ingest_nostr.py", "7️⃣  Ingest Nostr (Decentralized network)"),
        ("python scripts/mine_insights.py", "8️⃣  Mine Insights (Pattern detection)"),
        ("python scripts/aggregate.py", "9️⃣  Aggregate Data (Consolidation)"),
    ]
    
    results = {}
    
    # Run ingests
    print("\n" + "="*60)
    print("📥 PHASE 1: DATA INGESTION (10 sources)")
    print("="*60)
    
    for cmd, desc in ingests:
        results[desc] = run_command(cmd, desc)
    
    # Generate report
    print("\n" + "="*60)
    print("📝 PHASE 2: REPORT GENERATION")
    print("="*60)
    results["Report Generation"] = run_command(
        "python scripts/generate_report.py",
        "Generate Daily EchoVein Report"
    )
    
    # Post to Nostr
    print("\n" + "="*60)
    print("🌐 PHASE 3: NOSTR PUBLISHING")
    print("="*60)
    results["Nostr Publishing"] = run_command(
        "python scripts/post_to_nostr.py",
        "Post Report to Nostr Network"
    )
    
    # Summary
    print("\n" + "="*60)
    print("📊 WORKFLOW SUMMARY")
    print("="*60)
    
    success_count = sum(1 for v in results.values() if v)
    total_count = len(results)
    
    for task, success in results.items():
        status = "✅" if success else "⚠️"
        print(f"{status} {task}")
    
    print(f"\nCompleted: {success_count}/{total_count}")
    print(f"Finished: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Check for latest report
    today = datetime.now().strftime("%Y-%m-%d")
    report_path = Path(f"docs/reports/pulse-{today}.md")
    if report_path.exists():
        size = report_path.stat().st_size
        print(f"\n✅ Latest report generated: {report_path} ({size} bytes)")
    else:
        print(f"\n⚠️ Report not found at {report_path}")
    
    return 0 if success_count == total_count else 1

if __name__ == "__main__":
    sys.exit(main())

