"""Optional Windows desktop notification."""
import logging
logger = logging.getLogger("agent")


def notify(title: str, message: str) -> bool:
    try:
        from plyer import notification
        notification.notify(title=title, message=message[:200], timeout=8)
        return True
    except Exception as exc:
        logger.debug("Desktop notification unavailable: %s", exc)
        return False
