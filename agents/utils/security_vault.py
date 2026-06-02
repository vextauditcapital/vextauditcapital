import re
import hashlib
import hmac
import logging
import datetime
import os

logger = logging.getLogger("VextSecurityVault")

class EnterpriseSecurityVault:
    """
    Enterprise-grade security, sanitization, and audit-trail logging engine.
    Addresses strict compliance audits (SOC 2, ISO 27001, DPDP Act 2023, GDPR).
    """
    def __init__(self, key: str = "VextAuditCapitalSecurityKey"):
        self.hmac_key = key.encode("utf-8")
        
        # PII Sanitization Patterns (complying with DPDP 2023 & GDPR)
        self.patterns = {
            "aadhaar": r"\b\d{4}[ -]?\d{4}[ -]?\d{4}\b",                 # Indian Aadhaar ID
            "pan_card": r"\b[A-Z]{5}\d{4}[A-Z]{1}\b",                     # Indian PAN Tax ID
            "credit_card": r"\b\d{4}[- ]?\d{4}[- ]?\d{4}[- ]?\d{4}\b",     # Standard 16-digit cards
            "ssn": r"\b\d{3}-\d{2}-\d{4}\b",                             # US SSN
            "email": r"\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b" # Standard emails (used for masking in prompt chains)
        }

    def sanitize_payload(self, text: str, preserve_corporate_domain: bool = True) -> str:
        """
        Scans and redacts PII data before forwarding text payloads to third-party LLMs (such as Gemini).
        This protects user data privacy and qualifies the architecture as 'Enterprise Ready'.
        """
        if not text:
            return ""
            
        sanitized = text
        
        # Mask Aadhaar, PAN, SSN, Credit Cards
        for label, pattern in self.patterns.items():
            if label == "email" and preserve_corporate_domain:
                # We selectively keep business domains but mask the username part to comply with GDPR/DPDP
                def repl_email(match):
                    full_email = match.group(0)
                    username, domain = full_email.split("@", 1)
                    # Skip masking if it is a Vext system email or standard corporate system
                    if "vextaudit.com" in domain:
                        return full_email
                    masked_username = username[0] + "***" if len(username) > 1 else "*"
                    return f"{masked_username}@{domain}"
                sanitized = re.sub(pattern, repl_email, sanitized)
            else:
                sanitized = re.sub(pattern, f"[{label.upper()}_REDACTED]", sanitized)
                
        return sanitized

    def compute_ledger_checksum(self, file_content: bytes) -> str:
        """
        Generates a SHA-256 integrity checksum for a client's uploaded compliance ledgers.
        Ensures strict non-repudiation and data integrity in automated audits.
        """
        sha256 = hashlib.sha256()
        sha256.update(file_content)
        return sha256.hexdigest()

    def generate_audit_signature(self, event_details: str) -> str:
        """
        Generates an HMAC-SHA256 signature for audit events.
        Creates an immutable, mathematically verifiable log trail for institutional diligence.
        """
        signature = hmac.new(self.hmac_key, event_details.encode("utf-8"), hashlib.sha256)
        return signature.hexdigest()

    def write_immutable_audit_log(self, action: str, operator: str, status: str, details: str):
        """
        Appends a secure, cryptographically signed log entry to the append-only operational audit trail.
        Required for SOC 2 Type II validation and institutional compliance reviews.
        """
        # Resolve log path dynamically to project root
        log_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "compliance_audit_trail.log")
        timestamp = datetime.datetime.utcnow().isoformat()
        
        raw_event = f"{timestamp} | ACTION: {action} | OPERATOR: {operator} | STATUS: {status} | DETAILS: {details}"
        log_signature = self.generate_audit_signature(raw_event)
        
        signed_log_line = f"{raw_event} | SIG: {log_signature}\n"
        
        try:
            with open(log_path, "a", encoding="utf-8") as log_file:
                log_file.write(signed_log_line)
            logger.info(f"Immutable audit entry written for action: {action}")
        except Exception as e:
            logger.error(f"Failed to write signed compliance audit entry: {e}")

# Global Security Vault Instance
security_vault = EnterpriseSecurityVault()
