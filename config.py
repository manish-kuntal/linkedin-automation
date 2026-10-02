"""Configuration loader. Fail-closed by default."""
from __future__ import annotations

import os
from pathlib import Path

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass


BASE_DIR = Path(__file__).resolve().parent

STATE_DIR = BASE_DIR / "state"
LOG_DIR = BASE_DIR / "logs"
DB_PATH = STATE_DIR / "agent.db"
STOP_FILE = STATE_DIR / "STOP"
PID_FILE = STATE_DIR / "agent.pid"
RUNNING_FLAG = STATE_DIR / "RUNNING"

STATE_DIR.mkdir(exist_ok=True)
LOG_DIR.mkdir(exist_ok=True)


def _bool_env(name: str) -> bool:
    return os.getenv(name, "false").strip().lower() in {
        "1",
        "true",
        "yes",
        "on",
    }


def _int_env(name: str, default: int, minimum: int = 0) -> int:
    try:
        value = int(os.getenv(name, str(default)))
        return max(value, minimum)
    except ValueError:
        return default


class Settings:
    def __init__(self) -> None:
        self.mode = os.getenv("AGENT_MODE", "SAFE_DEMO").strip().upper()

        self.linkedin_official_api_enabled = _bool_env(
            "LINKEDIN_OFFICIAL_API_ENABLED"
        )
        self.linkedin_api_approved = _bool_env(
            "LINKEDIN_API_APPROVED"
        )

        self.linkedin_client_id = os.getenv(
            "LINKEDIN_CLIENT_ID", ""
        ).strip()

        self.linkedin_client_secret = os.getenv(
            "LINKEDIN_CLIENT_SECRET", ""
        ).strip()

        self.linkedin_access_token = os.getenv(
            "LINKEDIN_ACCESS_TOKEN", ""
        ).strip()

        # Hard safety locks.
        # These cannot be enabled through .env.
        self.browser_automation = False
        self.scraping = False
        self.captcha_bypass = False
        self.proxy_evasion = False

        self.ai_api_key = os.getenv("AI_API_KEY", "").strip()

        self.ai_base_url = os.getenv(
            "AI_BASE_URL",
            "https://api.openai.com/v1",
        ).rstrip("/")

        self.ai_model = os.getenv(
            "AI_MODEL",
            "gpt-4o-mini",
        ).strip()

        self.user_interests = [
            x.strip()
            for x in os.getenv(
                "USER_INTERESTS",
                "AI, machine learning, startups, software engineering, cloud",
            ).split(",")
            if x.strip()
        ]

        self.max_actions_per_day = _int_env(
            "MAX_ACTIONS_PER_DAY",
            5,
            1,
        )

        self.max_comments_per_day = _int_env(
            "MAX_COMMENTS_PER_DAY",
            3,
            1,
        )

        self.cooldown_seconds = _int_env(
            "COOLDOWN_SECONDS",
            3600,
            0,
        )

        self.max_suggestions = min(
            _int_env("MAX_SUGGESTIONS", 3, 1),
            3,
        )

        self.telegram_bot_token = os.getenv(
            "TELEGRAM_BOT_TOKEN",
            "",
        ).strip()

        self.telegram_chat_id = os.getenv(
            "TELEGRAM_CHAT_ID",
            "",
        ).strip()

        self.desktop_notifications = _bool_env(
            "DESKTOP_NOTIFICATIONS"
        )

        # Actual LinkedIn automation is allowed only when
        # every required authorization condition is satisfied.
        self.api_automation_allowed = (
            self.linkedin_official_api_enabled
            and self.linkedin_api_approved
            and bool(self.linkedin_client_id)
            and bool(self.linkedin_access_token)
        )

    @property
    def mode_display(self) -> str:
        return {
            "SAFE_DEMO": "SAFE DEMO",
            "LINKEDIN_ASSISTANT": "SAFE ASSISTANT",
            "OFFICIAL_API": "OFFICIAL API",
        }.get(self.mode, "INVALID")

    def validate(self) -> list[str]:
        problems = []

        if self.mode not in {
            "SAFE_DEMO",
            "LINKEDIN_ASSISTANT",
            "OFFICIAL_API",
        }:
            problems.append(
                f"Unknown AGENT_MODE '{self.mode}'."
            )

        if (
            self.mode == "OFFICIAL_API"
            and not self.api_automation_allowed
        ):
            problems.append(
                "OFFICIAL_API requires both approval flags "
                "plus client ID and access token."
            )

        if (
            self.browser_automation
            or self.scraping
            or self.captcha_bypass
            or self.proxy_evasion
        ):
            problems.append(
                "A hard safety lock was unexpectedly enabled."
            )

        return problems


SETTINGS = Settings()


def is_process_running() -> bool:
    if not PID_FILE.exists():
        return False

    try:
        pid = int(
            PID_FILE.read_text(
                encoding="utf-8"
            ).strip()
        )
    except (ValueError, OSError):
        return False

    try:
        import psutil

        return (
            psutil.pid_exists(pid)
            and psutil.Process(pid).is_running()
        )
    except ImportError:
        return RUNNING_FLAG.exists()


def safety_checks() -> list[tuple[str, bool, str]]:
    """
    Return safety checks in a consistent format:

        (check_name, passed, detail)
    """

    gitignore = BASE_DIR / ".gitignore"
    env_file = BASE_DIR / ".env"

    checks: list[tuple[str, bool, str]] = []

    def add(
        name: str,
        ok: bool,
        detail: str = "",
    ) -> None:
        checks.append(
            (
                name,
                bool(ok),
                detail,
            )
        )

    add(
        "No password stored",
        "LINKEDIN_PASSWORD" not in os.environ,
        "LINKEDIN_PASSWORD environment variable is not allowed."
        if "LINKEDIN_PASSWORD" in os.environ
        else "No LinkedIn password variable detected.",
    )

    add(
        "Browser automation disabled",
        SETTINGS.browser_automation is False,
        "Browser automation is hard-disabled.",
    )

    add(
        "Scraping disabled",
        SETTINGS.scraping is False,
        "Scraping is hard-disabled.",
    )

    add(
        "CAPTCHA bypass disabled",
        SETTINGS.captcha_bypass is False,
        "CAPTCHA bypass is hard-disabled.",
    )

    add(
        "Proxy evasion disabled",
        SETTINGS.proxy_evasion is False,
        "Proxy/IP evasion is hard-disabled.",
    )

    gitignore_ok = False

    if gitignore.exists():
        try:
            gitignore_text = gitignore.read_text(
                encoding="utf-8"
            )

            gitignore_ok = ".env" in gitignore_text

        except OSError:
            gitignore_ok = False

    add(
        "Secret protection enabled",
        gitignore_ok,
        ".env is protected by .gitignore."
        if gitignore_ok
        else ".env is missing from .gitignore.",
    )

    add(
        "Emergency stop available",
        STOP_FILE.parent == STATE_DIR,
        "Emergency STOP file location is valid."
        if STOP_FILE.parent == STATE_DIR
        else "STOP file location is invalid.",
    )

    add(
        "State directory available",
        STATE_DIR.exists(),
        "State directory exists."
        if STATE_DIR.exists()
        else "State directory is missing.",
    )

    add(
        "Audit logging directory available",
        LOG_DIR.exists(),
        "Logging directory exists."
        if LOG_DIR.exists()
        else "Logging directory is missing.",
    )

    add(
        "Human approval required by default",
        True,
        "Human approval remains required for external actions.",
    )

    add(
        "Default mode is safe",
        SETTINGS.mode
        in {
            "SAFE_DEMO",
            "LINKEDIN_ASSISTANT",
            "OFFICIAL_API",
        },
        f"Current mode: {SETTINGS.mode_display}.",
    )

    add(
        "Real LinkedIn API is disabled by default",
        not SETTINGS.api_automation_allowed,
        "Official API automation is not configured."
        if not SETTINGS.api_automation_allowed
        else "Official API automation is configured.",
    )

    # A real .env is optional for SAFE_DEMO.
    if env_file.exists():
        try:
            env_text = env_file.read_text(
                encoding="utf-8"
            )

            password_ok = (
                "LINKEDIN_PASSWORD=" not in env_text
            )

            add(
                "No obvious LinkedIn password in .env",
                password_ok,
                "No LinkedIn password found in .env."
                if password_ok
                else "LinkedIn password detected in .env.",
            )

        except OSError as exc:
            add(
                "No obvious LinkedIn password in .env",
                False,
                f"Could not read .env: {exc}",
            )

    return checks