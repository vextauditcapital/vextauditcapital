import re
import json
import os
import logging

logger = logging.getLogger("VextRuleEngine")

class LocalComplianceRuleEngine:
    """
    Proprietary Local Compliance Rule & Document Structural Validator.
    Acts as VAC's technical moat, ensuring the system runs local analytical checks
    rather than operating as a basic LLM API wrapper.
    """
    def __init__(self):
        # Local cached compliance schema and regulatory rules
        self.gstin_pattern = r"^\d{2}[A-Z]{5}\d{4}[A-Z]{1}[A-Z\d]{1}[Z]{1}[A-Z\d]{1}$"
        self.pan_pattern = r"^[A-Z]{5}\d{4}[A-Z]{1}$"

    def analyze_gst_ledger_structure(self, file_content: str) -> dict:
        """
        Parses raw text/CSV financial ledgers locally.
        Runs static validation rules, cross-matches calculations, and reports structured gaps.
        """
        lines = file_content.split("\n")
        total_rows = len(lines)
        gstin_found = []
        invalid_gstins = []
        imbalanced_transactions = []
        
        # Simulated parsing of columns (e.g., Invoice, GSTIN, Debit, Credit, Tax_Rate)
        for idx, line in enumerate(lines):
            # Try to extract GSTIN patterns
            matches = re.findall(r"\b\d{2}[A-Z]{5}\d{4}[A-Z]{1}[A-Z\d]{1}[Z]{1}[A-Z\d]{1}\b", line)
            for m in matches:
                gstin_found.append(m)
                if not re.match(self.gstin_pattern, m):
                    invalid_gstins.append({"row": idx + 1, "value": m})
            
            # Simple debit-credit balancing scan
            amounts = re.findall(r"\b\d+\.\d{2}\b", line)
            if len(amounts) >= 2:
                try:
                    debit = float(amounts[0])
                    credit = float(amounts[1])
                    if abs(debit - credit) > 0.001 and idx > 0: # If transaction line doesn't balance
                        imbalanced_transactions.append({"row": idx + 1, "debit": debit, "credit": credit})
                except ValueError:
                    pass

        # Calculate localized structured score
        integrity_score = 100.0
        if invalid_gstins:
            integrity_score -= len(invalid_gstins) * 5
        if imbalanced_transactions:
            integrity_score -= len(imbalanced_transactions) * 10
            
        integrity_score = max(10.0, integrity_score)

        return {
            "file_type": "GST Ledger",
            "total_rows_scanned": total_rows,
            "unique_gstins_detected": list(set(gstin_found)),
            "invalid_gstin_alerts": invalid_gstins,
            "imbalanced_transactions": imbalanced_transactions,
            "structural_integrity_score": integrity_score,
            "status": "PASS" if integrity_score >= 80 else "FAIL_REQUIRES_AI_REMEDIATION"
        }

    def verify_dpdp_readiness_checklist(self, questionnaire_answers: dict) -> dict:
        """
        Statically evaluates user inputs for DPDP Readiness to provide a baseline scoring matrix
        before handing over complex document evaluation to Gemini 3.5.
        """
        critical_keys = ["data_consent_acquired", "has_privacy_officer", "data_breach_response_plan", "right_to_withdraw_consent"]
        missing_mandatory = []
        score = 100.0

        for key in critical_keys:
            val = questionnaire_answers.get(key)
            if not val or str(val).lower() in ["false", "no", "0", "none"]:
                missing_mandatory.append(key)
                score -= 25.0

        return {
            "framework": "DPDP Act 2023",
            "compliance_readiness_score": score,
            "missing_mandatory_controls": missing_mandatory,
            "status": "READY" if score == 100.0 else "GAP_DETECTED"
        }

# Global Rule Engine Instance
rule_engine = LocalComplianceRuleEngine()
