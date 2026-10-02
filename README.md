# LinkedIn AI Engagement Agent

A local Windows AI assistant for analyzing LinkedIn content and generating human-reviewed engagement suggestions.

## Safety-first design

- No browser automation.
- No LinkedIn scraping.
- No CAPTCHA bypass.
- No proxy/IP evasion.
- No password storage.
- Real LinkedIn actions are blocked unless an officially authorized API configuration exists.
- Human approval is required for engagement actions.
- Emergency STOP flag.
- SQLite audit logs.
- Fail-closed behavior.

## Setup

```bat
cd linkedin-agent
py -3.11 -m venv .venv
.venv\Scripts\activate
python -m pip install -r requirements.txt
copy .env.example .env
```

Keep the `.env` LinkedIn API flags false for the initial demo.

## Run

```bat
python main.py safety-check
python main.py test
python main.py demo
python main.py status
python main.py start
python main.py stop
python main.py logs
```

`demo` processes the local mock posts in `tests/mock_posts.json`.

## AI

If `AI_API_KEY` is empty, the application uses a deterministic offline heuristic. This makes the first run possible without an AI API.

## Assistant mode

Set:

```env
AGENT_MODE=LINKEDIN_ASSISTANT
```

Then create `manual_posts.json` in the project root using the same schema as the mock file. The program does not fetch LinkedIn itself.

## Production API

Do not enable `LINKEDIN_OFFICIAL_API_ENABLED` or `LINKEDIN_API_APPROVED` unless the exact current LinkedIn API permission and use case have been independently verified and approved for your application.

The API execution methods are intentionally fail-closed until that verification is completed.

## Emergency stop

From another CMD:

```bat
python main.py stop
```

or press `CTRL+C` in the running console.

## Important

No system can guarantee zero account risk. The project is designed to minimize unnecessary risk by refusing browser automation, scraping, policy bypass, and unapproved external actions.
