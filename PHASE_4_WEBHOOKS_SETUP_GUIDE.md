# 🔗 PHASE 4: GITHUB WEBHOOKS SETUP GUIDE

**Date**: 2025-10-26  
**Status**: ⏳ READY TO CONFIGURE (Requires GitHub PAT)

---

## 🎯 **WHAT THIS DOES**

Connects **Ollama Pulse** → **GrumpiBlogged** via GitHub webhooks so that:

1. **When**: New Ollama Pulse report is committed to `main`
2. **Then**: Automatically triggers GrumpiBlogged workflow
3. **Result**: GrumpiBlogged aggregates Ollama Pulse + AI Research Daily → Meta-report at 18:00 CT

---

## 📋 **ARCHITECTURE**

```
┌─────────────────────────────────────────────────────────────┐
│                    GrumpiBlogged (Meta-Blog)                │
│          Daily 18:00 CT - Multi-Repo Aggregation            │
│                                                              │
│  Workflow: .github/workflows/aggregate_reports.yml          │
│  Script: scripts/generate_meta_report.py                    │
│  Output: docs/posts/meta-report-YYYY-MM-DD.md               │
└─────────────────────────────────────────────────────────────┘
                            ▲
                            │ (GitHub Repository Dispatch)
        ┌───────────────────┼───────────────────┐
        │                   │                   │
┌───────▼────────┐  ┌──────▼──────┐  ┌────────▼────────┐
│ Ollama Pulse   │  │AI Research  │  │  Future Miners  │
│ 08:30 + 16:30  │  │   Daily     │  │   (TBD)         │
│                │  │             │  │                 │
│ Webhook:       │  │ Webhook:    │  │ Webhook:        │
│ trigger_       │  │ (similar)   │  │ (similar)       │
│ grumpiblogged  │  │             │  │                 │
│ .yml           │  │             │  │                 │
└────────────────┘  └─────────────┘  └─────────────────┘
```

---

## 🛠️ **SETUP STEPS**

### **STEP 1: Create GitHub Personal Access Token (PAT)**

**Why**: Ollama Pulse needs permission to trigger GrumpiBlogged workflows

**How**:
1. Go to: https://github.com/settings/tokens
2. Click "Generate new token" → "Generate new token (classic)"
3. **Name**: `GrumpiBlogged Webhook Token`
4. **Expiration**: No expiration (or 1 year)
5. **Scopes**: Check these boxes:
   - ✅ `repo` (Full control of private repositories)
   - ✅ `workflow` (Update GitHub Action workflows)
6. Click "Generate token"
7. **COPY THE TOKEN** (you won't see it again!)

---

### **STEP 2: Add PAT to Ollama Pulse Secrets**

**Why**: Workflow needs the token to trigger GrumpiBlogged

**How**:
1. Go to: https://github.com/Grumpified-OGGVCT/ollama_pulse/settings/secrets/actions
2. Click "New repository secret"
3. **Name**: `GRUMPIBLOGGED_PAT`
4. **Value**: Paste the token from Step 1
5. Click "Add secret"

---

### **STEP 3: Copy Webhook Receiver to GrumpiBlogged**

**Why**: GrumpiBlogged needs a workflow to receive webhook triggers

**How**:
1. Go to GrumpiBlogged repo: https://github.com/Grumpified-OGGVCT/GrumpiBlogged
2. Create file: `.github/workflows/aggregate_reports.yml`
3. Copy content from: `ollama_pulse/GRUMPIBLOGGED_WEBHOOK_RECEIVER.yml`
4. Commit to `main` branch

---

### **STEP 4: Create Meta-Report Generator Script**

**Why**: GrumpiBlogged needs a script to aggregate reports

**File**: `GrumpiBlogged/scripts/generate_meta_report.py`

**What it should do**:
1. Fetch HTML from Ollama Pulse report URL
2. Fetch HTML from AI Research Daily report URL
3. Extract key insights, discoveries, trends
4. Generate unified meta-report in Markdown
5. Include SEO tags, hashtags, social sharing
6. Save to `docs/posts/meta-report-YYYY-MM-DD.md`

**Example structure**:
```python
#!/usr/bin/env python3
"""Generate meta-report aggregating multiple auto-mining repos"""
import argparse
import requests
from bs4 import BeautifulSoup
from datetime import datetime

def fetch_report(url):
    """Fetch and parse report HTML"""
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    # Extract key sections
    return {
        'title': soup.find('h1').text,
        'content': soup.find('body').text,
        # ... more extraction
    }

def generate_meta_report(ollama_pulse_url, ai_research_url):
    """Generate aggregated meta-report"""
    # Fetch reports
    ollama_data = fetch_report(ollama_pulse_url) if ollama_pulse_url else None
    ai_research_data = fetch_report(ai_research_url) if ai_research_url else None
    
    # Generate meta-report
    today = datetime.now().strftime('%Y-%m-%d')
    
    report = f"""---
layout: post
title: "GrumpiBlogged Meta-Report - {today}"
date: {today}
---

# 🤖 GrumpiBlogged Meta-Report - {today}

**Generated**: 18:00 CT on {today}

*Aggregating insights from Ollama Pulse, AI Research Daily, and more...*

---

## 📡 Ollama Pulse Highlights

{ollama_data['summary'] if ollama_data else 'No report available'}

[Read full Ollama Pulse report →]({ollama_pulse_url})

---

## 🔬 AI Research Daily Highlights

{ai_research_data['summary'] if ai_research_data else 'No report available'}

[Read full AI Research Daily report →]({ai_research_url})

---

## 🔗 Cross-Repo Connections

*Patterns and connections across all monitored repos...*

---

## 🔖 Share This Meta-Report

**Hashtags**: #AI #Automation #TechNews #AIResearch #Ollama #MachineLearning

**Share on**: [Twitter](...) | [LinkedIn](...) | [Reddit](...)

"""
    
    return report

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--ollama-pulse', help='Ollama Pulse report URL')
    parser.add_argument('--ai-research', help='AI Research Daily report URL')
    parser.add_argument('--output', required=True, help='Output file path')
    args = parser.parse_args()
    
    report = generate_meta_report(args.ollama_pulse, args.ai_research)
    
    with open(args.output, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"✅ Meta-report saved to {args.output}")
```

---

### **STEP 5: Test the Webhook**

**Manual Test**:
1. Go to: https://github.com/Grumpified-OGGVCT/ollama_pulse/actions/workflows/trigger_grumpiblogged.yml
2. Click "Run workflow"
3. Set `force_trigger: true`
4. Click "Run workflow"
5. Check GrumpiBlogged Actions: https://github.com/Grumpified-OGGVCT/GrumpiBlogged/actions

**Automatic Test**:
1. Wait for next Ollama Pulse report (08:30 or 16:30 CT)
2. Report commits to `main` → Triggers webhook
3. GrumpiBlogged receives trigger → Generates meta-report
4. Check GrumpiBlogged at 18:00 CT for meta-report

---

## 📊 **WORKFLOW DETAILS**

### **Ollama Pulse → GrumpiBlogged Trigger**

**File**: `.github/workflows/trigger_grumpiblogged.yml`

**Triggers**:
- ✅ On push to `main` when `docs/reports/pulse-*.md` changes
- ✅ Manual dispatch with `force_trigger` input

**What it does**:
1. Extracts latest report info (date, URL, description)
2. Sends `repository_dispatch` event to GrumpiBlogged
3. Payload includes: source, report_date, report_url, description, timestamp, commit_sha

**Event type**: `ollama-pulse-update`

---

### **GrumpiBlogged Receiver**

**File**: `GrumpiBlogged/.github/workflows/aggregate_reports.yml`

**Triggers**:
- ✅ `repository_dispatch` with type `ollama-pulse-update`
- ✅ `repository_dispatch` with type `ai-research-daily-update`
- ✅ Schedule: Daily at 18:00 CT (cron: `0 23 * * *`)
- ✅ Manual dispatch with `force_run` input

**What it does**:
1. Fetches latest Ollama Pulse report
2. Fetches latest AI Research Daily report
3. Runs `scripts/generate_meta_report.py`
4. Commits meta-report to `docs/posts/`
5. Pushes to `main` (triggers GitHub Pages rebuild)

---

## 🔐 **SECURITY**

### **Why PAT is Needed**
- GitHub Actions can't trigger workflows in other repos without authentication
- PAT provides secure, scoped access
- Only `repo` and `workflow` scopes needed

### **Best Practices**
- ✅ Use PAT with minimal scopes
- ✅ Store in GitHub Secrets (never commit to code)
- ✅ Set expiration (1 year recommended)
- ✅ Rotate token annually
- ✅ Revoke if compromised

---

## 📁 **FILE STRUCTURE**

### **Ollama Pulse**
```
ollama_pulse/
├── .github/workflows/
│   ├── morning_report.yml          # 08:30 CT report
│   ├── afternoon_report.yml        # 16:30 CT report
│   └── trigger_grumpiblogged.yml   # NEW - Webhook trigger
├── docs/reports/
│   ├── pulse-2025-10-26.md
│   └── ...
└── PHASE_4_WEBHOOKS_SETUP_GUIDE.md # THIS FILE
```

### **GrumpiBlogged**
```
GrumpiBlogged/
├── .github/workflows/
│   └── aggregate_reports.yml       # NEW - Webhook receiver
├── scripts/
│   └── generate_meta_report.py     # NEW - Meta-report generator
├── docs/
│   ├── posts/
│   │   ├── meta-report-2025-10-26.md
│   │   └── ...
│   └── index.html
└── README.md
```

---

## ✅ **VERIFICATION CHECKLIST**

Before going live, verify:

- [ ] **Step 1**: GitHub PAT created with `repo` + `workflow` scopes
- [ ] **Step 2**: PAT added to Ollama Pulse secrets as `GRUMPIBLOGGED_PAT`
- [ ] **Step 3**: `aggregate_reports.yml` copied to GrumpiBlogged
- [ ] **Step 4**: `generate_meta_report.py` created in GrumpiBlogged
- [ ] **Step 5**: Manual test successful (workflow triggered, meta-report generated)
- [ ] **Bonus**: Automatic test successful (report commit → webhook → meta-report)

---

## 🚀 **NEXT STEPS**

1. **Complete setup** (Steps 1-4 above)
2. **Test manually** (Step 5)
3. **Monitor first automatic trigger** (next report at 08:30 or 16:30 CT)
4. **Verify meta-report** (check GrumpiBlogged at 18:00 CT)
5. **Repeat for AI Research Daily** (similar webhook setup)

---

## 📝 **NOTES**

- **Time zones**: All times in Central Time (CT)
- **Cron schedules**: UTC times (adjust for CDT/CST)
- **GitHub Pages**: Auto-rebuilds on push to `main`
- **Rate limits**: GitHub API has rate limits, but webhooks are exempt
- **Debugging**: Check Actions logs for both repos

---

**Built by vein-tappers, for vein-tappers. Connected veins, unified pulse.** ⛏️🩸

