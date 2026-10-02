# LinkedIn AI Engagement Agent

> **Educational & Research Project**
>
> An AI-assisted LinkedIn engagement workflow designed for learning, experimentation, and responsible automation research.  
> **Author: Manish Kuntal**

---

## Project Overview

The **LinkedIn AI Engagement Agent** is a safety-first Python application that helps analyze LinkedIn content and generate relevant comment suggestions using an AI model.

The project is intentionally designed around **human approval** rather than uncontrolled automation.

### Core workflow

```text
                 ┌──────────────────────┐
                 │   LinkedIn Content   │
                 │  / Manual Post Data  │
                 └──────────┬───────────┘
                            │
                            ▼
                 ┌──────────────────────┐
                 │     Discovery        │
                 │  Content Collection  │
                 └──────────┬───────────┘
                            │
                            ▼
                 ┌──────────────────────┐
                 │   AI / Rule Engine   │
                 │ Topic + Relevance    │
                 └──────────┬───────────┘
                            │
                            ▼
                 ┌──────────────────────┐
                 │    Recommender       │
                 │ REVIEW / MAYBE / SKIP│
                 └──────────┬───────────┘
                            │
                            ▼
                 ┌──────────────────────┐
                 │  Comment Generator   │
                 │  Gemini / AI Model   │
                 └──────────┬───────────┘
                            │
                            ▼
                 ┌──────────────────────┐
                 │   Human Approval     │
                 └──────────┬───────────┘
                            │
                            ▼
                 ┌──────────────────────┐
                 │ Manual LinkedIn Post │
                 └──────────────────────┘
```

---

## ⚠️ Safety Philosophy

This project is built with a **protected-by-design** approach.

The following mechanisms are intentionally blocked:

- Browser automation
- LinkedIn scraping
- CAPTCHA bypass
- Proxy rotation for evasion
- Rate-limit bypass
- Policy bypass
- Fake engagement
- Automatic uncontrolled commenting
- Automatic generation of misleading personal experiences

The application can generate suggestions, but the user remains responsible for reviewing and publishing content.

> **This project is for educational purposes only. Users must follow LinkedIn's current Terms, API policies, developer documentation, and applicable laws.**

---

# Features

## AI Features

- Topic classification
- Relevance scoring
- Interest matching
- AI-generated comment suggestions
- Deterministic fallback analysis
- Gemini/OpenAI-compatible API architecture
- Configurable user interests
- Suggestion limits

## Engagement Features

- REVIEW / MAYBE / SKIP recommendations
- Manual approval workflow
- Manual copy-and-post workflow
- Post URL display
- Duplicate post tracking
- SQLite persistence

## Safety Features

- Emergency stop
- Daily action limits
- Daily comment limits
- Cooldown period
- Browser automation blocked
- Scraping blocked
- Policy bypass blocked
- Official API disabled by default
- Human approval before external engagement

## Developer Features

- Python virtual environment
- `.env` configuration
- Modular architecture
- SQLite database
- Automated tests
- CLI interface
- Gemini-compatible AI integration
- Windows `.bat` launcher

---

# Technology Stack

| Component | Technology |
|---|---|
| Language | Python 3.12+ |
| AI Provider | Google Gemini |
| AI Interface | OpenAI-compatible Python client |
| Database | SQLite |
| Configuration | `.env` / python-dotenv |
| Testing | pytest |
| CLI | Python CLI |
| Platform | Windows / Linux / macOS |
| Version Control | Git |
| External API | LinkedIn Official API only when properly authorized |

---

# System Requirements

## Minimum

- Python 3.11+
- 4 GB RAM
- 1 GB free storage
- Internet connection for AI API usage
- Windows 10/11, Linux, or macOS
- Git (recommended)

## Recommended

- Python 3.12+
- 8 GB RAM
- SSD storage
- Stable internet connection
- Git
- Google Gemini API access

No dedicated GPU is required because the default AI processing is API-based.

---

# Installation

## 1. Clone the repository

```cmd
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd linkedin-agent
```

If you already have the project:

```cmd
cd C:\Users\manis\linkedin-agent
```

---

## 2. Create a virtual environment

### Windows

```cmd
python -m venv .venv
```

Activate it:

```cmd
.venv\Scripts\activate
```

You should see:

```text
(.venv)
```

before your command prompt.

### Linux/macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
```

---

# 3. Upgrade pip

```cmd
python -m pip install --upgrade pip
```

---

# 4. Install dependencies

If the repository contains `requirements.txt`:

```cmd
pip install -r requirements.txt
```

Typical packages used by this project include:

```text
python-dotenv
openai
pytest
```

Do not manually install random packages if `requirements.txt` already defines the project's dependencies.

---

# 5. Configure environment variables

Create:

```text
.env
```

Example:

```env
AGENT_MODE=LINKEDIN_ASSISTANT
APP_MODE=LINKEDIN_ASSISTANT

# AI Provider
AI_API_KEY=YOUR_GEMINI_API_KEY
AI_BASE_URL=https://generativelanguage.googleapis.com/v1beta/openai/
AI_MODEL=gemini-2.5-flash

# Interests
USER_INTERESTS=AI, machine learning, startups, software engineering, cloud

# LinkedIn Official API
LINKEDIN_OFFICIAL_API_ENABLED=false
LINKEDIN_API_APPROVED=false

LINKEDIN_CLIENT_ID=
LINKEDIN_CLIENT_SECRET=
LINKEDIN_ACCESS_TOKEN=

# OAuth
LINKEDIN_REDIRECT_URI=http://127.0.0.1:8000/auth/linkedin/callback
LINKEDIN_SCOPE=w_member_social

# Safety
MAX_ACTIONS_PER_DAY=5
MAX_COMMENTS_PER_DAY=3
COOLDOWN_SECONDS=3600
MAX_SUGGESTIONS=3

# Notifications
TELEGRAM_BOT_TOKEN=
TELEGRAM_CHAT_ID=
DESKTOP_NOTIFICATIONS=false
```

### Important

Never commit `.env` to GitHub.

Your `.gitignore` should contain:

```gitignore
.env
.venv/
__pycache__/
*.pyc
*.db
*.sqlite
```

---

# Gemini Configuration

This project can use Google's Gemini API through its OpenAI-compatible interface.

The important configuration is:

```env
AI_BASE_URL=https://generativelanguage.googleapis.com/v1beta/openai/
```

and:

```env
AI_API_KEY=YOUR_GEMINI_API_KEY
```

The API key must remain private.

### Test Gemini

Run:

```cmd
python -c "import os; from dotenv import load_dotenv; from openai import OpenAI; load_dotenv(); c=OpenAI(api_key=os.getenv('AI_API_KEY'),base_url=os.getenv('AI_BASE_URL')); r=c.chat.completions.create(model=os.getenv('AI_MODEL'),messages=[{'role':'user','content':'Reply with exactly: GEMINI_OK'}]); print(r.choices[0].message.content)"
```

Expected:

```text
GEMINI_OK
```

---

# Running the Project

## Show status

```cmd
python main.py
```

Example:

```text
============================================
 LinkedIn AI Engagement Agent
============================================
Status: STOPPED
Mode: SAFE ASSISTANT
LinkedIn Automation: DISABLED
Official API: NOT CONFIGURED
Browser Automation: BLOCKED
Scraping: BLOCKED
Policy Bypass: BLOCKED

Safety Status: PROTECTED BY DESIGN
Risk: Cannot be guaranteed to be zero.
Emergency Stop: ENABLED
============================================
```

---

# Available Commands

The application supports the following command structure:

```text
python main.py <command>
```

Common commands:

```cmd
python main.py
python main.py test
python main.py demo
python main.py safety-check
python main.py status
python main.py logs
python main.py start
python main.py start-bg
python main.py stop
```

Use:

```cmd
python main.py test
```

to verify the application.

---

# Windows One-Click Launcher

The project includes:

```text
start_agent.bat
```

It automatically:

1. Opens the project directory
2. Activates `.venv`
3. Starts the Python application
4. Displays the agent status

Run:

```cmd
start_agent.bat
```

Or double-click the `.bat` file.

---

# Project Structure

```text
linkedin-agent/
│
├── main.py
├── config.py
├── requirements.txt
├── .env
├── .gitignore
├── start_agent.bat
│
├── agent/
│   ├── __init__.py
│   ├── orchestrator.py
│   ├── analyzer.py
│   └── recommender.py
│
├── ai/
│   ├── __init__.py
│   ├── llm.py
│   ├── prompts.py
│   └── scoring.py
│
├── linkedin/
│   ├── __init__.py
│   ├── discovery.py
│   └── official_api.py
│
├── storage/
│   ├── __init__.py
│   └── database.py
│
├── tests/
│   ├── test_agent.py
│   └── mock_posts.json
│
└── manual_posts.json
```

---

# Architecture

## 1. `main.py`

The CLI entry point.

Responsibilities:

- Start the application
- Run tests
- Run demo mode
- Show status
- Run safety checks
- Start/stop the agent

---

## 2. `config.py`

Central configuration and safety validation.

Responsible for:

- Environment variables
- Agent mode
- AI configuration
- LinkedIn configuration
- Safety limits
- API enablement checks

---

## 3. `agent/orchestrator.py`

The main workflow controller.

It connects:

```text
Discovery
   ↓
Analyzer
   ↓
Recommender
   ↓
AI suggestions
   ↓
Human approval
```

---

## 4. `linkedin/discovery.py`

Responsible for discovering input content.

Current safe modes include:

### SAFE_DEMO

Uses:

```text
tests/mock_posts.json
```

### LINKEDIN_ASSISTANT

Uses:

```text
manual_posts.json
```

This allows the system to work without scraping LinkedIn.

---

# 5. `linkedin/official_api.py`

Contains the controlled interface for LinkedIn's official API.

The application is designed to **fail closed** when official API authorization/configuration is not valid.

The official API must not be replaced with:

- Selenium scraping
- Playwright scraping
- Browser DOM extraction
- Cookie automation
- CAPTCHA bypass
- Proxy evasion

---

# 6. `ai/llm.py`

AI provider abstraction.

The application communicates with the AI model through an OpenAI-compatible client interface.

Current configuration can point that client to Gemini.

Conceptually:

```text
Application
     │
     ▼
AI Client
     │
     ▼
Gemini OpenAI-Compatible Endpoint
     │
     ▼
Gemini Model
```

---

# 7. `ai/scoring.py`

Deterministic scoring layer.

It can evaluate:

- Topic matches
- Interest matches
- Keyword relevance
- Content signals

This provides a fallback when an external AI model is unavailable.

---

# 8. `ai/prompts.py`

Contains controlled prompts for AI-generated suggestions.

The prompt design avoids:

- Generic spam
- Fake personal stories
- Misleading claims
- Repetitive comments
- Engagement bait

---

# 9. `agent/recommender.py`

Converts analysis into an action recommendation.

Possible outcomes:

```text
REVIEW
MAYBE
SKIP
```

The recommendation is based on configured rules and relevance signals.

---

# 10. `storage/database.py`

SQLite persistence layer.

Used for:

- Processed post tracking
- Duplicate prevention
- Agent history
- Local state

No external database server is required.

---

# Data Flow

```text
┌─────────────────────┐
│   Input Post Data   │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│     Discovery       │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│     Analyzer        │
│ Topic + Relevance   │
└──────────┬──────────┘
           │
           ├──────────────┐
           ▼              ▼
┌────────────────┐  ┌────────────────┐
│ Rule Scoring   │  │  Gemini / LLM  │
└───────┬────────┘  └───────┬────────┘
        │                   │
        └─────────┬─────────┘
                  ▼
        ┌───────────────────┐
        │    Recommender    │
        └─────────┬─────────┘
                  │
          ┌───────┼────────┐
          ▼       ▼        ▼
       REVIEW   MAYBE     SKIP
          │       │
          └───┬───┘
              ▼
      ┌─────────────────┐
      │ Comment Suggest │
      └────────┬────────┘
               ▼
      ┌─────────────────┐
      │ Human Approval  │
      └────────┬────────┘
               ▼
      ┌─────────────────┐
      │ Manual Publish  │
      └─────────────────┘
```

---

# Recommendation Logic

The agent does not blindly comment on everything.

Example:

```text
Post
 │
 ├── Relevant?
 │      │
 │      ├── No ────────> SKIP
 │      │
 │      └── Yes
 │           │
 │           ▼
 │       AI Analysis
 │           │
 │           ▼
 │      Recommendation
 │           │
 │       ┌───┴────┐
 │       ▼        ▼
 │    REVIEW     MAYBE
 │       │        │
 │       └───┬────┘
 │           ▼
 │      Generate Suggestions
 │           │
 │           ▼
 │      Human Approval
```

---

# Example Input

```json
[
  {
    "id": "example-001",
    "author": "Example Author",
    "text": "We deployed our AI workload locally and reduced cloud dependency.",
    "url": "https://www.linkedin.com/posts/example"
  }
]
```

The agent can analyze:

```text
Topic: AI
Relevance: 80%
Matched interests: AI, cloud
Recommendation: REVIEW
```

Then generate a contextual question such as:

```text
What trade-off mattered most when deciding between local deployment and cloud infrastructure?
```

The user decides whether to use it.

---

# Safety Controls

## Action Limits

Configured through:

```env
MAX_ACTIONS_PER_DAY=5
MAX_COMMENTS_PER_DAY=3
COOLDOWN_SECONDS=3600
MAX_SUGGESTIONS=3
```

These limits reduce accidental excessive activity.

---

# Emergency Stop

The application contains an emergency-stop mechanism.

The goal is to prevent the application from continuing external activity if a safety condition fails.

---

# Official LinkedIn API

The project supports an architecture for official LinkedIn API integration.

However:

```env
LINKEDIN_OFFICIAL_API_ENABLED=false
```

should remain disabled until:

1. The correct LinkedIn product is enabled.
2. Required permissions are actually granted.
3. OAuth credentials are valid.
4. The API endpoints are implemented and tested.
5. Non-destructive API calls succeed.
6. The application's safety checks pass.

Do **not** enable an API merely because an access token exists.

---

# OAuth Configuration

Example:

```env
LINKEDIN_CLIENT_ID=
LINKEDIN_CLIENT_SECRET=
LINKEDIN_ACCESS_TOKEN=

LINKEDIN_REDIRECT_URI=http://127.0.0.1:8000/auth/linkedin/callback
LINKEDIN_SCOPE=w_member_social
```

Keep all credentials private.

Never upload:

```text
.env
client secrets
access tokens
API keys
database files containing sensitive information
```

to a public repository.

---

# Testing

Run:

```cmd
python main.py test
```

Or directly:

```cmd
pytest -q
```

Expected project tests should complete without failures.

---

# Demo Mode

For safe development:

```env
AGENT_MODE=SAFE_DEMO
```

Then:

```cmd
python main.py demo
```

Demo mode uses:

```text
tests/mock_posts.json
```

and does not require real LinkedIn activity.

---

# Assistant Mode

For the manual assistant workflow:

```env
AGENT_MODE=LINKEDIN_ASSISTANT
```

The current safe implementation uses manually supplied post data rather than scraping LinkedIn.

This makes the system useful for testing the complete:

```text
Input → AI → Recommendation → Suggestion → Human Approval
```

pipeline without browser automation.

---

# Troubleshooting

## Python not found

Check:

```cmd
python --version
```

Install Python 3.11+ if necessary.

---

## Virtual environment not activated

Run:

```cmd
.venv\Scripts\activate
```

---

## Dependency error

Run:

```cmd
python -m pip install --upgrade pip
pip install -r requirements.txt
```

---

## Gemini error

Check:

```env
AI_API_KEY=
AI_BASE_URL=https://generativelanguage.googleapis.com/v1beta/openai/
AI_MODEL=
```

Do not expose your API key when asking for help.

---

## Agent still shows SAFE DEMO

Check:

```cmd
findstr "AGENT_MODE APP_MODE" .env
```

For assistant mode:

```text
AGENT_MODE=LINKEDIN_ASSISTANT
```

---

## LinkedIn API says NOT CONFIGURED

Check:

```env
LINKEDIN_OFFICIAL_API_ENABLED=false
```

The current project intentionally reports the official API as disabled until the integration is verified.

---

# Development Workflow

A recommended development cycle:

```text
1. Change code
      ↓
2. Run syntax check
      ↓
3. Run tests
      ↓
4. Run SAFE_DEMO
      ↓
5. Review logs
      ↓
6. Test AI provider
      ↓
7. Test assistant workflow
      ↓
8. Verify safety checks
      ↓
9. Only then consider official API integration
```

Useful commands:

```cmd
python -m py_compile main.py
python main.py test
python main.py safety-check
python main.py demo
```

---

# Git Workflow

Initialize:

```cmd
git init
```

Check files:

```cmd
git status
```

Add:

```cmd
git add .
```

Commit:

```cmd
git commit -m "Initial LinkedIn AI engagement agent"
```

Connect your GitHub repository:

```cmd
git remote add origin <YOUR_GITHUB_REPOSITORY_URL>
```

Push:

```cmd
git branch -M main
git push -u origin main
```

---

# Security Checklist

Before pushing to GitHub:

```text
[ ] .env is ignored
[ ] API keys are not present in source code
[ ] LinkedIn client secret is not committed
[ ] LinkedIn access token is not committed
[ ] Telegram token is not committed
[ ] SQLite sensitive data is not committed
[ ] Browser automation is disabled
[ ] Scraping is disabled
[ ] Policy bypass is disabled
[ ] Safety tests pass
[ ] README contains no real credentials
```

---

# Educational Use

This project can be used to study:

- Python application architecture
- Environment configuration
- REST API integration
- OAuth concepts
- AI API integration
- Prompt engineering
- Recommendation systems
- Rule-based scoring
- SQLite persistence
- CLI application design
- Automated testing
- Safety engineering
- Human-in-the-loop AI
- Git/GitHub workflows

---

# Learning Architecture

```text
Python
  │
  ├── Configuration
  │
  ├── CLI
  │
  ├── AI Integration
  │
  ├── API Integration
  │
  ├── Database
  │
  ├── Testing
  │
  └── Safety Engineering
          │
          ▼
   Human-in-the-Loop
          │
          ▼
   Responsible AI Workflow
```

---

# Future Development

Potential educational extensions:

- Improved URL-based post input
- Better local content analysis
- Structured AI evaluation
- Analytics dashboard
- Comment-quality scoring
- Local model support
- Additional notification providers
- OAuth lifecycle management
- Official LinkedIn API capabilities where permitted
- More comprehensive automated tests

Any external-action feature should remain subject to the relevant platform's current API permissions and policies.

---

# License

Choose and add an appropriate open-source license before publishing this repository publicly.

For example:

```text
MIT License
```

Do not claim a license unless a license file is actually included in the repository.

---

# Disclaimer

This repository is an **educational project** created for learning and experimentation with AI-assisted workflows.

It is not affiliated with, endorsed by, or sponsored by LinkedIn or Google.

Users are responsible for:

- Their API credentials
- Their generated content
- Their LinkedIn activity
- Compliance with applicable platform policies
- Compliance with applicable laws and regulations

---

# Author

**Manish Kuntal**

Educational / research project.

---

## Quick Start

```cmd
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd linkedin-agent
python -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Configure `.env`, then:

```cmd
python main.py test
```

Run the safe assistant:

```cmd
python main.py
```

Run the demo:

```cmd
python main.py demo
```

Or use:

```cmd
start_agent.bat
```

---

**LinkedIn AI Engagement Agent — Educational AI Engineering Project**
