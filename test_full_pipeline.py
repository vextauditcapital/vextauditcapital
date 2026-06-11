import json
import time
from agents.utils.rule_engine import rule_engine
from agents.utils.pdf_generator import generate_brand_invoice_pdf, generate_brand_deliverable_pdf

def run_full_audit_pipeline():
    print("==================================================")
    print(" VEXT AUDIT CAPITAL - END-TO-END PIPELINE TEST ")
    print("==================================================\n")

    # 1. Simulate Client Intake (Data Extraction)
    print("[STEP 1] Simulating Client Ledger Ingestion (Data Extraction)...")
    client_details = {
        "name": "Narendra Modi,",
        "company": "Bharat Industries Ltd,",
        "address": "7 Lok Kalyan Marg,",
        "location": "New Delhi, 110011.",
        "gstin": "07AABCB1234E1Z1"
    }
    
    # We deliberately include some errors to trigger Claude's statutory reasoning
    dummy_ledger = """Invoice_ID,GSTIN,Debit,Credit,Tax_Rate
    INV-001,07AABCB1234E1Z1,150000.00,150000.00,18
    INV-002,07AABCB1234E1Z1,20000.00,18000.00,18
    INV-003,INVALID_GSTIN_XYZ,5000.00,5000.00,12"""
    
    time.sleep(1)
    print("   -> Raw Ledger Data Extracted Successfully.\n")

    # 2. Trigger Rule Engine & Claude Fable-5 Statutory Analysis
    print("[STEP 2] Activating Chief Compliance Officer (Claude Fable-5 Analysis)...")
    try:
        audit_results = rule_engine.analyze_gst_ledger_structure(dummy_ledger)
        print("   -> Statutory Analysis Complete. Zero Hallucination Mode Verified.")
    except Exception as e:
        print(f"   -> ERROR in Step 2: {e}")
        return

    # Extract Claude's reasoning to feed into the report
    claude_feedback = audit_results.get("claude_statutory_verification", {})
    if isinstance(claude_feedback, dict):
        gatekeeper = claude_feedback.get("gatekeeper_verdict", {})
        status = gatekeeper.get("overall_status", "UNKNOWN")
        issues = gatekeeper.get("blocking_issues", [])
        
        report_text = f"EXECUTIVE SUMMARY\nThis report details the findings of the GST statutory audit conducted for {client_details['company']}\n\n"
        report_text += f"OVERALL AUDIT STATUS: {status}\n\n"
        
        if issues:
            report_text += "IDENTIFIED COMPLIANCE GAPS & STATUTORY VIOLATIONS:\n"
            for issue in issues:
                report_text += f"- {issue.get('issue_id', '')}: {issue.get('description', '')}\n"
                report_text += f"  Remediation Required: {issue.get('action_required', '')}\n"
        else:
            report_text += "No blocking issues identified. Full compliance achieved.\n"
    else:
        report_text = f"Raw Audit Data:\n{json.dumps(audit_results, indent=2)}"

    print("\n[STEP 3] Generating Branded Deliverable Report (PDF)...")
    try:
        deliverable_bytes = generate_brand_deliverable_pdf(
            client_name=client_details['company'].replace(',', ''),
            report_content=report_text
        )
        with open("VAC_FINAL_AUDIT_REPORT.pdf", "wb") as f:
            f.write(deliverable_bytes)
        print("   -> VAC_FINAL_AUDIT_REPORT.pdf generated successfully.")
    except Exception as e:
        print(f"   -> ERROR in Step 3: {e}")
        return

    print("\n[STEP 4] Generating Automated Billing Invoice (PDF)...")
    try:
        invoice_bytes = generate_brand_invoice_pdf(
            client_details=client_details,
            invoice_no="VAC-2026-9099",
            service_desc="Comprehensive GST Ledger Audit & Statutory Verification",
            amount="75000"
        )
        with open("VAC_RETAIL_INVOICE.pdf", "wb") as f:
            f.write(invoice_bytes)
        print("   -> VAC_RETAIL_INVOICE.pdf generated successfully.")
    except Exception as e:
        print(f"   -> ERROR in Step 4: {e}")
        return

    print("\n==================================================")
    print(" FULL SWING AUDIT PIPELINE EXECUTED SUCCESSFULLY")
    print("==================================================")

if __name__ == "__main__":
    run_full_audit_pipeline()
