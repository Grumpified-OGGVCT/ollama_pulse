# Direct Tasks for Copilot - No Reading Required

Copy/paste these prompts directly into Copilot.

---

## Task 1: Add Sticky Navigation Menu to Reports

```
In scripts/generate_report.py, find the function generate_report_md() around line 281.

At the very start of the report variable (line ~298), add this HTML navigation menu:

<nav id="report-navigation" style="position: sticky; top: 0; z-index: 1000; background: linear-gradient(135deg, #8B0000 0%, #DC143C 100%); padding: 1rem; margin-bottom: 2rem; border-radius: 8px;">
  <div style="font-size: 1.2rem; font-weight: bold; color: #fff; margin-bottom: 1rem;">📋 Report Navigation</div>
  <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 0.75rem;">
    <a href="#summary" style="display: block; padding: 0.75rem 1rem; background: rgba(255, 255, 255, 0.1); color: #fff; text-decoration: none; border-radius: 4px;">📊 Summary</a>
    <a href="#breakthroughs" style="display: block; padding: 0.75rem 1rem; background: rgba(255, 255, 255, 0.1); color: #fff; text-decoration: none; border-radius: 4px;">⚡ Breakthroughs</a>
    <a href="#official" style="display: block; padding: 0.75rem 1rem; background: rgba(255, 255, 255, 0.1); color: #fff; text-decoration: none; border-radius: 4px;">🎯 Official</a>
    <a href="#community" style="display: block; padding: 0.75rem 1rem; background: rgba(255, 255, 255, 0.1); color: #fff; text-decoration: none; border-radius: 4px;">🛠️ Community</a>
    <a href="#patterns" style="display: block; padding: 0.75rem 1rem; background: rgba(255, 255, 255, 0.1); color: #fff; text-decoration: none; border-radius: 4px;">📈 Patterns</a>
    <a href="#prophecies" style="display: block; padding: 0.75rem 1rem; background: rgba(255, 255, 255, 0.1); color: #fff; text-decoration: none; border-radius: 4px;">🔔 Prophecies</a>
    <a href="#developers" style="display: block; padding: 0.75rem 1rem; background: rgba(255, 255, 255, 0.1); color: #fff; text-decoration: none; border-radius: 4px;">🚀 Developers</a>
    <a href="#bounties" style="display: block; padding: 0.75rem 1rem; background: rgba(255, 255, 255, 0.1); color: #fff; text-decoration: none; border-radius: 4px;">💰 Bounties</a>
  </div>
</nav>

Then find each major section heading and add an anchor div BEFORE it:

<div id="summary"></div>
## 🔬 Ecosystem Intelligence Summary

<div id="breakthroughs"></div>
## ⚡ Breakthrough Discoveries

<div id="official"></div>
## 🎯 Official Veins

<div id="community"></div>
## 🛠️ Community Veins

<div id="patterns"></div>
## 📈 Vein Pattern Mapping

<div id="prophecies"></div>
## 🔔 Prophetic Veins

<div id="developers"></div>
## 🚀 What This Means for Developers

<div id="bounties"></div>
## BOUNTY VEINS

After each section, add a back-to-top link:

<div style="text-align: right; margin: 2rem 0;">
  <a href="#report-navigation" style="padding: 0.5rem 1.5rem; background: linear-gradient(135deg, #8B0000 0%, #DC143C 100%); color: #fff; text-decoration: none; border-radius: 4px; font-weight: bold;">⬆️ Back to Top</a>
</div>

---

Test by running the morning report workflow with Force run enabled.
```

---

## Task 2: Increase Model Temperature for Unique Reports

```
In scripts/enhanced_report_generator.py, find all temperature settings.

Change every temperature=0.7 to use a random value:

import random

# At top of each async function that calls client.generate(), change:
temperature=0.7

# To:
temperature=random.uniform(0.75, 0.95)

This makes each report unique with different LLM creativity each time.

Also find the prompts and add today's date to make them contextual:

f"""Generate insights for {datetime.now().strftime('%B %d, %Y')}...
```

---

## Task 3: Test and Report Errors

```
1. Trigger ingestion: https://github.com/Grumpified-OGGVCT/ollama_pulse/actions/workflows/ingest.yml

2. Verify in logs:
   - Official should show: "0-5 recent releases" (not 30+ entries)
   - Cloud should show: "8 OFFICIAL cloud models"
   
3. Trigger morning report: https://github.com/Grumpified-OGGVCT/ollama_pulse/actions/workflows/morning_report.yml
   - Enable "Force run" checkbox
   
4. Check logs for error lines starting with "❌" or "⚠️"

5. Copy the exact error messages and tell the user what failed.
```

---

## That's It!

Three simple copy-paste prompts. No file reading required.

