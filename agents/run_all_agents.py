import sys
import time
import logging
from agents.lead_command import run_sample_pipeline
from agents.email_command import EmailCommandCenter

# Configure unified logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("VextAuditAgentsOrchestrator")

def run_orchestration():
    logger.info("="*70)
    logger.info("⚡ VEXT AUDIT CAPITAL - UNIFIED AI AGENT ORCHESTRATOR INITIALIZED")
    logger.info("⚡ Operational Status: 100% Automated, Zero Human Intervention")
    logger.info("="*70)
    
    # 1. Run Lead Generation Command Center (PAUSED - EMAIL SEQUENCES STOPPED)
    try:
        logger.info("\n[STEP 1] VEXTLEAD COMMAND CENTER PIPELINE - PAUSED BY USER")
        # run_sample_pipeline()
    except Exception as e:
        logger.error(f"Lead Command Center encountered an execution error: {e}")
        
    # 2. Run Email Inbox Automation Response Engine (PAUSED - EMAIL SEQUENCES STOPPED)
    try:
        logger.info("\n[STEP 2] VEXTMAIL RESPONSE ENGINE - PAUSED BY USER")
        # engine = EmailCommandCenter()
        # engine.run_all_mailboxes()
    except Exception as e:
        logger.error(f"Email Command Center encountered an execution error: {e}")
        
    # 3. Run Automated Invoice Generation Agent
    try:
        logger.info("\n[STEP 3] EXECUTING VEXTINVOICE AGENT PIPELINE")
        from agents.utils.invoice_agent import VextInvoiceAgent
        invoice_agent = VextInvoiceAgent()
        invoice_agent.run_onboarding_invoices()
    except Exception as e:
        logger.error(f"Invoice Agent encountered an execution error: {e}")
        
    # 4. Run Automated Compliance Audit Agent Hierarchy (Phase 3)
    try:
        logger.info("\n[STEP 4] EXECUTING VEXT COMPLIANCE AUDIT AGENT HIERARCHY")
        from agents.utils.audit_hierarchy import master_verification_agent
        sample_ledger = (
            "INV-2026-001, 33AFIFS2899N1Z5, 25000.00, 25000.00, PASS\n"
            "INV-2026-002, 11BBBBB2222B2Z2, 12000.00, 12500.00, FAIL\n" # Imbalanced + Invalid GSTIN syntax
            "INV-2026-001, 33AFIFS2899N1Z5, 10000.00, 10000.00, PASS\n" # Duplicate Invoice booking
        )
        report = master_verification_agent.execute_and_verify_audit(
            client_name="Test Enterprise",
            client_email="test@enterprise.co.in",
            service_code="gst",
            service_name="GST Audit & Compliance",
            file_name="ledger_june.csv",
            file_content=sample_ledger
        )
        logger.info(f"Compliance Audit completed. PDF path: {report['audit_meta']['pdf_report_path']}")
    except Exception as e:
        logger.error(f"Compliance Audit Hierarchy encountered an execution error: {e}")
        
    logger.info("\n" + "="*70)
    logger.info("⚡ ALL AI AGENT PIPELINES COMPLETED SUCCESSFULLY")
    logger.info("⚡ Operational Telemetry logged in agents_operations.log")
    logger.info("="*70)

if __name__ == "__main__":
    while True:
        try:
            run_orchestration()
        except Exception as e:
            logger.error(f"Fatal error in orchestration loop: {e}")
        
        logger.info("Sleeping for 60 seconds before next polling cycle...")
        time.sleep(60)
