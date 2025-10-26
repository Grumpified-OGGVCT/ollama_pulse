# 📌 Manual Project Tracking Guide

## Overview

Ollama Pulse now supports **manual project tracking** via a simple JSON file. This lets you add projects to daily reports without waiting for them to appear in automated ingestion.

---

## 🚀 Quick Start

### 1. Edit `tracked_projects.json`

Open the file in the repo root and add your projects to the `projects` array:

```json
{
  "projects": [
    {
      "title": "My Awesome Ollama Project",
      "url": "https://github.com/user/awesome-ollama",
      "summary": "A revolutionary Ollama integration for XYZ",
      "turbo_score": 0.9,
      "highlights": ["integration", "production-ready", "typescript"]
    }
  ]
}
```

### 2. Commit and Push

```bash
git add tracked_projects.json
git commit -m "track: add My Awesome Ollama Project"
git push
```

### 3. Wait for Next Report

Your project will appear in the next daily report (08:30 AM or 04:30 PM CST)!

---

## 📋 Field Reference

| Field | Required | Type | Description | Example |
|-------|----------|------|-------------|---------|
| `title` | ✅ Yes | string | Project name or description | `"Ollama Python Client"` |
| `url` | ✅ Yes | string | Project URL (GitHub, website, etc.) | `"https://github.com/ollama/ollama-python"` |
| `summary` | ✅ Yes | string | Brief description (1-2 sentences) | `"Official Python library for Ollama"` |
| `turbo_score` | ⚠️ Optional | number (0-1) | Relevance score (default: 0.8) | `0.9` |
| `highlights` | ⚠️ Optional | array | Tags/keywords | `["python", "official", "client"]` |
| `date` | ⚠️ Optional | ISO string | Publication date (default: today) | `"2025-10-26T00:00:00Z"` |
| `source` | ⚠️ Optional | string | Source identifier (default: `manual_tracking`) | `"manual_tracking"` |

---

## 💡 Examples

### Example 1: GitHub Repository

```json
{
  "title": "Ollama WebUI - Beautiful Chat Interface",
  "url": "https://github.com/user/ollama-webui",
  "summary": "Modern web interface for Ollama with streaming support and model switching",
  "turbo_score": 0.85,
  "highlights": ["webui", "react", "streaming", "production"]
}
```

### Example 2: Blog Post / Tutorial

```json
{
  "title": "Building Production LLM Apps with Ollama Cloud",
  "url": "https://myblog.com/ollama-cloud-production",
  "summary": "Complete guide to deploying Ollama Cloud in production with monitoring and scaling",
  "turbo_score": 0.9,
  "highlights": ["tutorial", "production", "cloud", "devops"]
}
```

### Example 3: Tool / Integration

```json
{
  "title": "Ollama VSCode Extension",
  "url": "https://marketplace.visualstudio.com/items?itemName=user.ollama-vscode",
  "summary": "AI-powered code completion using Ollama models directly in VSCode",
  "turbo_score": 0.95,
  "highlights": ["vscode", "extension", "code-completion", "productivity"]
}
```

### Example 4: Research / Paper

```json
{
  "title": "Optimizing Ollama Inference Performance",
  "url": "https://arxiv.org/abs/2025.12345",
  "summary": "Research paper on GPU optimization techniques for Ollama model inference",
  "turbo_score": 0.8,
  "highlights": ["research", "performance", "gpu", "optimization"]
}
```

---

## 🎯 Best Practices

### ✅ DO:
- **Add projects you're actively working on** or want to promote
- **Use descriptive titles** that explain what the project does
- **Include relevant tags** in `highlights` for better categorization
- **Set appropriate turbo_score** (0.8-1.0 for high-quality projects)
- **Keep summaries concise** (1-2 sentences max)

### ❌ DON'T:
- **Don't add spam** or unrelated projects
- **Don't duplicate** projects already in automated ingestion
- **Don't use excessive highlights** (3-5 tags is ideal)
- **Don't set turbo_score below 0.5** (won't appear in reports)

---

## 🔄 How It Works

1. **Hourly Ingestion**: `ingest_manual.py` runs every hour
2. **Loads JSON**: Reads `tracked_projects.json` from repo root
3. **Validates**: Ensures required fields are present
4. **Saves**: Stores to `data/manual/YYYY-MM-DD.json`
5. **Aggregates**: Merges with other sources in `aggregate.py`
6. **Reports**: Appears in daily reports with `manual_tracking` source tag

---

## 🛠️ Advanced Usage

### Multiple Projects

```json
{
  "projects": [
    {
      "title": "Project 1",
      "url": "https://...",
      "summary": "...",
      "turbo_score": 0.9,
      "highlights": ["tag1", "tag2"]
    },
    {
      "title": "Project 2",
      "url": "https://...",
      "summary": "...",
      "turbo_score": 0.85,
      "highlights": ["tag3", "tag4"]
    }
  ]
}
```

### Temporary Tracking

To track a project for a limited time, add it with a specific date:

```json
{
  "title": "Ollama Hackathon Winner",
  "url": "https://...",
  "summary": "...",
  "date": "2025-10-26T00:00:00Z",
  "turbo_score": 0.95,
  "highlights": ["hackathon", "winner", "2025"]
}
```

Then remove it after the event.

---

## 📊 Monitoring

Check if your projects are being tracked:

```bash
# View today's manual tracking data
cat data/manual/$(date +%Y-%m-%d).json

# Check aggregated data
cat data/aggregated/$(date +%Y-%m-%d).json | grep "manual_tracking"
```

---

## 🐛 Troubleshooting

### Project Not Appearing in Reports

1. **Check JSON syntax**: Use a JSON validator
2. **Verify turbo_score**: Must be ≥ 0.3 to pass filtering
3. **Check workflow logs**: Look for errors in GitHub Actions
4. **Wait for next report**: Changes only appear in next scheduled report

### JSON Validation Error

```bash
# Validate JSON locally
python -m json.tool tracked_projects.json
```

---

## 🎉 That's It!

You can now manually track any Ollama-related project in your daily reports. No need to wait for automated discovery or ask for help!

**Questions?** Open an issue or check the main README.

