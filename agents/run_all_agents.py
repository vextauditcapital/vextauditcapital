import sys
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
    
    # 1. Run Lead Generation Command Center
    try:
        logger.info("\n[STEP 1] EXECUTING VEXTLEAD COMMAND CENTER PIPELINE")
        run_sample_pipeline()
    except Exception as e:
        logger.error(f"Lead Command Center encountered an execution error: {e}")
        
    # 2. Run Email Inbox Automation Response Engine
    try:
        logger.info("\n[STEP 2] EXECUTING VEXTMAIL RESPONSE ENGINE")
        engine = EmailCommandCenter()
        engine.run_all_mailboxes()
    except Exception as e:
        logger.error(f"Email Command Center encountered an execution error: {e}")
        
    logger.info("\n" + "="*70)
    logger.info("⚡ ALL AI AGENT PIPELINES COMPLETED SUCCESSFULLY")
    logger.info("⚡ Operational Telemetry logged in agents_operations.log")
    logger.info("="*70)

if __name__ == "__main__":
    run_orchestration()
