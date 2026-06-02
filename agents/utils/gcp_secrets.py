import os
import logging

logger = logging.getLogger("vext-gcp-secrets")

try:
    from google.cloud import secretmanager
    HAS_SECRET_MANAGER = True
except ImportError:
    HAS_SECRET_MANAGER = False

def get_secret(secret_id: str, default_val: str = None, project_id: str = None, version_id: str = "latest") -> str:
    """
    Fetches production credentials directly from system memory in Google Secret Manager.
    If Secret Manager library is not installed, or we are in a non-GCP environment,
    or credentials are missing, this falls back gracefully to standard local environment variables.
    
    :param secret_id: Name of the secret inside Secret Manager (e.g. "GEMINI_API_KEY")
    :param default_val: Fallback value if secret not found anywhere
    :param project_id: Google Cloud project ID (falls back to GCP_PROJECT_ID environment variable)
    :param version_id: Version of the secret (defaults to "latest")
    """
    # 1. Primary check: If local environment variable is present, prioritize it for instant local testing override
    env_val = os.getenv(secret_id)
    if env_val:
        return env_val
        
    # 2. GCP Secret Manager resolution
    if HAS_SECRET_MANAGER:
        gcp_project = project_id or os.getenv("GCP_PROJECT_ID") or os.getenv("GOOGLE_CLOUD_PROJECT")
        if gcp_project:
            try:
                client = secretmanager.SecretManagerServiceClient()
                name = f"projects/{gcp_project}/secrets/{secret_id}/versions/{version_id}"
                response = client.access_secret_version(request={"name": name})
                secret_payload = response.payload.data.decode("UTF-8")
                logger.info(f"Retrieved secret '{secret_id}' securely from Google Secret Manager.")
                return secret_payload
            except Exception as e:
                logger.warning(f"GCP Secret Manager failed to retrieve '{secret_id}': {e}. Trying environment fallback.")
        else:
            logger.debug("GCP Project ID not configured; bypassing Google Secret Manager.")
    else:
        logger.debug("google-cloud-secret-manager package is not installed; bypassing Google Secret Manager.")
        
    # 3. Fallback: Return default value
    if default_val is not None:
        return default_val
        
    # Raise runtime warning if critical secret is completely missing
    raise ValueError(f"Secret '{secret_id}' could not be resolved from local environment or GCP Secret Manager.")
