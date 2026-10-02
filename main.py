"""LinkedIn AI Engagement Agent - safe CMD entry point."""
from __future__ import annotations
import logging
import os
import signal
import subprocess
import sys
from pathlib import Path

import config
from config import SETTINGS, STOP_FILE, PID_FILE, RUNNING_FLAG, LOG_DIR


def setup_logging() -> None:
    fmt = logging.Formatter(
        "%(asctime)s %(levelname)s %(message)s", "%Y-%m-%d %H:%M:%S"
    )
    for name, fname in (
        ("agent", "agent.log"),
        ("security", "security.log"),
        ("actions", "actions.log"),
    ):
        lg = logging.getLogger(name)
        lg.setLevel(logging.INFO)
        if not lg.handlers:
            handler = logging.FileHandler(LOG_DIR / fname, encoding="utf-8")
            handler.setFormatter(fmt)
            lg.addHandler(handler)


def banner() -> None:
    running = config.is_process_running()
    print("=" * 44)
    print(" LinkedIn AI Engagement Agent")
    print("=" * 44)
    print(f"Status: {'RUNNING' if running else 'STOPPED'}")
    print(f"Mode: {SETTINGS.mode_display}")
    print(
        "LinkedIn Automation: APPROVED OFFICIAL API ONLY"
        if SETTINGS.api_automation_allowed
        else "LinkedIn Automation: DISABLED"
    )
    print(
        f"Official API: {'CONFIGURED' if SETTINGS.api_automation_allowed else 'NOT CONFIGURED'}"
    )
    print("Browser Automation: BLOCKED")
    print("Scraping: BLOCKED")
    print("Policy Bypass: BLOCKED")
    print()
    print("Safety Status: PROTECTED BY DESIGN")
    print("Risk: Cannot be guaranteed to be zero.")
    print("Emergency Stop: ENABLED")
    print("=" * 44)


def cmd_start() -> None:
    if config.is_process_running():
        print("Agent is already running.")
        return

    STOP_FILE.unlink(missing_ok=True)

    from agent.orchestrator import Orchestrator
    try:
        Orchestrator().run(once=False)
    finally:
        RUNNING_FLAG.unlink(missing_ok=True)
        PID_FILE.unlink(missing_ok=True)


def cmd_start_background() -> None:
    if config.is_process_running():
        print("Agent is already running.")
        return

    print("Starting agent in a new console...")
    kwargs = {}
    if os.name == "nt":
        kwargs["creationflags"] = subprocess.CREATE_NEW_CONSOLE

    subprocess.Popen(
        [sys.executable, str(Path(__file__).resolve()), "start"],
        cwd=str(config.BASE_DIR),
        **kwargs,
    )


def cmd_stop() -> None:
    STOP_FILE.write_text("manual", encoding="utf-8")
    print("STOP signal written. The running agent will stop at its next safe checkpoint.")


def cmd_status() -> None:
    banner()


def cmd_demo() -> None:
    STOP_FILE.unlink(missing_ok=True)
    from agent.orchestrator import Orchestrator
    Orchestrator().run(once=True)


def cmd_test() -> None:
    result = subprocess.run(
        [sys.executable, "-m", "pytest", "tests", "-v"],
        cwd=str(config.BASE_DIR),
    )
    raise SystemExit(result.returncode)


def cmd_safety_check() -> None:
    checks = config.safety_checks()
    print("LinkedIn AI Agent Safety Check\n")
    failed = []
    for name, ok, detail in checks:
        print(f"[{'PASS' if ok else 'FAIL'}] {name}" + (f" — {detail}" if detail else ""))
        if not ok:
            failed.append(name)

    print()
    if failed:
        print("Production mode: BLOCKED")
        for item in failed:
            print(f"Reason: {item}")
        raise SystemExit(1)

    print("Safety configuration: READY")
    print("Note: READY does not mean zero-risk or authorize LinkedIn API access.")


def cmd_logs() -> None:
    for fname in ("agent.log", "security.log", "actions.log"):
        path = LOG_DIR / fname
        print(f"\n----- {fname} (last 20 lines) -----")
        if not path.exists():
            print("(empty)")
            continue
        lines = path.read_text(encoding="utf-8").splitlines()
        print("\n".join(lines[-20:]))


def usage() -> None:
    print("Usage: python main.py [start|start-bg|stop|status|test|demo|safety-check|logs]")


if __name__ == "__main__":
    setup_logging()
    signal.signal(signal.SIGINT, lambda *_: STOP_FILE.write_text("ctrl-c", encoding="utf-8"))
    if hasattr(signal, "SIGBREAK"):
        signal.signal(signal.SIGBREAK, lambda *_: STOP_FILE.write_text("ctrl-break", encoding="utf-8"))

    cmd = sys.argv[1].lower() if len(sys.argv) > 1 else "status"
    commands = {
        "start": cmd_start,
        "start-bg": cmd_start_background,
        "stop": cmd_stop,
        "status": cmd_status,
        "test": cmd_test,
        "demo": cmd_demo,
        "safety-check": cmd_safety_check,
        "logs": cmd_logs,
    }
    commands.get(cmd, usage)()
