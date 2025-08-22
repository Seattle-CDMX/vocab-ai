import base64
import json
import logging
import os

logger = logging.getLogger("agent.config")


def parse_google_credentials():
    """Parse Google Cloud credentials from environment variable with proper error handling.

    Supports both regular JSON and base64-encoded JSON for better compatibility
    with different deployment environments.
    """
    credentials_b64 = os.getenv("GOOGLE_APPLICATION_CREDENTIALS_B64")
    credentials_json = os.getenv("GOOGLE_APPLICATION_CREDENTIALS_JSON")

    # Try base64-encoded credentials first (more robust for env vars)
    if credentials_b64:
        try:
            decoded_json = base64.b64decode(credentials_b64).decode("utf-8")
            credentials_data = json.loads(decoded_json)
            logger.info(
                "Successfully loaded Google Cloud credentials from base64 environment variable"
            )
            return credentials_data
        except Exception as e:
            logger.error(f"Failed to parse base64 credentials: {e}")

    # Fall back to regular JSON credentials
    if credentials_json:
        try:
            credentials_data = json.loads(credentials_json)
            logger.info(
                "Successfully loaded Google Cloud credentials from JSON environment variable"
            )
            return credentials_data
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse GOOGLE_APPLICATION_CREDENTIALS_JSON: {e}")
            logger.error(
                "Hint: Try using GOOGLE_APPLICATION_CREDENTIALS_B64 with base64-encoded JSON instead"
            )
            return None
        except Exception as e:
            logger.error(f"Unexpected error parsing Google credentials: {e}")
            return None

    logger.warning(
        "Neither GOOGLE_APPLICATION_CREDENTIALS_JSON nor GOOGLE_APPLICATION_CREDENTIALS_B64 environment variables are set"
    )
    return None
