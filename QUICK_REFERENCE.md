# Ollama Pulse Workflows - Quick Reference Card

**Print this and keep it handy!** 📋

---

## ⏰ Schedule

| Workflow | Time (CT) | Frequency | Cron (CDT) | Cron (CST) |
|----------|-----------|-----------|------------|------------|
| **Ingestion** | Every hour :00 | Hourly | `0 *` | `0 *` |
| **Morning Report** | 08:30 CT | Daily | `30 13` | `30 14` |
| **Afternoon Report** | 16:30 CT | Daily | `30 21` | `30 22` |
| **GrumpiBlogged Trigger** | On report push | Event-driven | N/A | N/A |

---

## 🚀 Manual Triggers

### Trigger Ingestion Now

1. Go to [Actions](https://github.com/Grumpified-OGGVCT/ollama_pulse/actions)
2. Click "Ollama Pulse Ingestion"
3. Click "Run workflow" button (top right)
4. Click green "Run workflow" button
5. Wait 2-4 minutes

### Trigger Report Now

1. Go to [Actions](https://github.com/Grumpified-OGGVCT/ollama_pulse/actions)
2. Click "Ollama Pulse Morning Report" (or Afternoon)
3. Click "Run workflow" button
4. ✅ Enable "Force run even if not 08:30 CT" checkbox
5. Click green "Run workflow" button
6. Wait 1-2 minutes

### Force GrumpiBlogged Webhook

1. Go to [Actions](https://github.com/Grumpified-OGGVCT/ollama_pulse/actions)
2. Click "Trigger GrumpiBlogged Meta-Report"
3. Click "Run workflow" → "Run workflow"

---

## 🔍 Quick Debug

### Workflow Failed? Check This:

```bash
# 1. Are secrets configured?
Settings → Secrets → Actions

# 2. View run logs
Actions → Click failed run → Click failed step

# 3. Check annotations
Click "Annotations" tab in failed run

# 4. Download artifacts
Click run → Scroll to "Artifacts" → Download
```

### Common Fixes

| Error | Solution |
|-------|----------|
| "OLLAMA_API_KEY not configured" | Add secret in Settings → Secrets |
| "No data available to generate report" | Run ingestion workflow first |
| "Git push failed" | Retry will auto-resolve (3 attempts) |
| "Time gate skipped" | Normal for DST coverage cron |

---

## 📊 Health Indicators

### ✅ Healthy System

- Morning report: publishes at 08:30-08:45 CT
- Afternoon report: publishes at 16:30-16:45 CT
- Ingestion: completes in 2-4 minutes every hour
- No git push failures after 3 attempts
- GitHub Pages updates within 2 minutes

### ⚠️ Needs Attention

- Reports more than 2 hours old
- Ingestion taking >5 minutes
- Repeated git push failures
- Missing data directories
- Secrets expiring soon

### 🚨 Critical Issues

- No reports in 24 hours → Check workflows disabled
- All ingestion runs failing → Check OLLAMA_API_KEY
- GitHub Pages not deploying → Check Pages settings
- Constant git conflicts → Check for manual commits

---

## 🔐 Required Secrets

### Must Have ✅

- `GH_PAT`: GitHub Personal Access Token (repo scope)
- `OLLAMA_API_KEY`: From https://ollama.com/settings/keys

### Optional ⚠️

- `SUPABASE_URL`: PostgreSQL database
- `SUPABASE_KEY`: Database auth token
- `NOSTR_PRIVATE_KEY`: Nostr nsec for publishing
- `GRUMPIBLOGGED_PAT`: GitHub PAT (repo + workflow scopes)
- `DISCORD_BOT_TOKEN`: For Discord ingestion

---

## 🎯 Quick Actions

### View Latest Report

https://grumpified-oggvct.github.io/ollama_pulse

### Check Workflow Status

https://github.com/Grumpified-OGGVCT/ollama_pulse/actions

### View Recent Commits

```bash
git log --oneline --graph --all -20
```

### Check Data Freshness

```bash
ls -lt data/aggregated/ | head -5
```

---

## 📞 Emergency Contacts

**Repository**: https://github.com/Grumpified-OGGVCT/ollama_pulse  
**Issues**: https://github.com/Grumpified-OGGVCT/ollama_pulse/issues  
**GitHub Actions Docs**: https://docs.github.com/en/actions  
**Ollama API Docs**: https://github.com/ollama/ollama/blob/main/docs/api.md

---

**Print Date**: November 2, 2025  
**Version**: 2.0 (Post-Workflow-Fixes)

