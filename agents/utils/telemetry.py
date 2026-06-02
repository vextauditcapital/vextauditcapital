import os
import logging
import requests
import json

logger = logging.getLogger("vext-telemetry")

try:
    import sentry_sdk
    from sentry_sdk.integrations.logging import LoggingIntegration
    HAS_SENTRY = True
except ImportError:
    HAS_SENTRY = False

def init_telemetry():
    """
    Initialises centralized logging and error tracking.
    Integrates Sentry SDK for banking-grade, real-time error reporting and performance tracing.
    """
    sentry_dsn = os.getenv("SENTRY_DSN")
    
    if HAS_SENTRY and sentry_dsn:
        try:
            # Custom logging integration to forward errors automatically
            sentry_logging = LoggingIntegration(
                level=logging.INFO,        # Capture info and above as breadcrumbs
                event_level=logging.ERROR   # Send errors as exception events
            )
            
            sentry_sdk.init(
                dsn=sentry_dsn,
                integrations=[sentry_logging],
                traces_sample_rate=1.0,
                profiles_sample_rate=1.0,
                environment=os.getenv("APP_ENV", "production")
            )
            logger.info("Successfully initialised real-time telemetry with Sentry.")
        except Exception as e:
            logger.warning(f"Sentry telemetry failed to initialise: {e}")
    else:
        logger.info("Running in standard local logging mode (Sentry DSN not configured).")

def send_alert(message: str, channel: str = "critical-alerts"):
    """
    Sends an instant message notification to your operations team via custom webhook integration (Slack/Teams).
    """
    webhook_url = os.getenv("TEAMS_ALERT_WEBHOOK_URL") or os.getenv("SLACK_ALERT_WEBHOOK_URL")
    if not webhook_url:
        logger.debug(f"Alert triggered (no webhook configured): [{channel.upper()}] {message}")
        return
        
    payload = {
        "text": f"🚨 *[VEXT-AUDIT TELEMETRY ALERT]* 🚨\n*Channel:* {channel}\n*Message:* {message}\n*Environment:* {os.getenv('APP_ENV', 'production')}"
    }
    
    try:
        response = requests.post(
            webhook_url,
            data=json.dumps(payload),
            headers={"Content-Type": "application/json"},
            timeout=5
        )
        if response.status_code != 200:
            logger.warning(f"Alert webhook returned non-200 status code: {response.status_code}")
    except Exception as e:
        logger.error(f"Failed to post telemetry alert to slack/teams: {e}")
