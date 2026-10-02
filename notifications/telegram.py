"""Telegram notification only. It never grants action permission."""
import logging
import config

logger = logging.getLogger("agent")


def notify(text: str) -> bool:
    token = config.SETTINGS.telegram_bot_token
    chat_id = config.SETTINGS.telegram_chat_id
    if not token or not chat_id:
        return False
    try:
        import requests
        response = requests.post(
            f"https://api.telegram.org/bot{token}/sendMessage",
            json={"chat_id": chat_id, "text": text[:4000]},
            timeout=10,
        )
        return response.status_code == 200
    except Exception as exc:
        logger.warning("Telegram notification failed: %s", str(exc)[:120])
        return False
