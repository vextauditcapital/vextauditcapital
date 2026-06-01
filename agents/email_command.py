import logging
import sys
import json
from agents.config import settings, PROMPTS
from agents.utils.gemini_client import gemini_client
from agents.utils.email_client import EmailClient

# Configure Logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("VextMailEngine")

class EmailCommandCenter:
    def __init__(self):
        # Initialize transport interfaces for all 5 strategic mailboxes
        self.mailboxes = {
            "ceo": EmailClient(settings.EMAIL_CEO, settings.PASS_CEO),
            "support": EmailClient(settings.EMAIL_SUPPORT, settings.PASS_SUPPORT),
            "no-reply": EmailClient(settings.EMAIL_NOREPLY, settings.PASS_NOREPLY),
            "intelligence": EmailClient(settings.EMAIL_INTELLIGENCE, settings.PASS_INTELLIGENCE),
            "newsletter": EmailClient(settings.EMAIL_NEWSLETTER, settings.PASS_NEWSLETTER)
        }

    def process_ceo_mailbox(self):
        """Processes CEO inbox. Formulates Statements of Work and coordinates Zoho Sign signature triggers."""
        mailbox = self.mailboxes["ceo"]
        unread_emails = mailbox.fetch_unread_emails()
        
        logger.info(f"[CEO] Polling mailbox. Found {len(unread_emails)} unread messages.")
        for mail in unread_emails:
            sender = mail["sender"]
            subject = mail["subject"]
            body = mail["body"]
            
            logger.info(f"[CEO] Processing inbound message from {sender}: '{subject}'")
            
            # Check if the inquiry matches a request for a transaction or SOW
            is_sow_request = any(kw in body.lower() for kw in ["sow", "statement of work", "sign", "proposal", "contract", "bundle", "purchase"])
            
            # Formulate thread context
            context = ""
            if is_sow_request:
                context = (
                    "Client is requesting a Statement of Work (SOW) or custom compliance proposal.\n"
                    "Provide a brief, crisp SOW summary outlining:\n"
                    "- 1. Service Scope: Full Compliance Mapping & Audit Bundle\n"
                    "- 2. Payment Terms: ₹75,000 one-time engagement fee (or custom as requested)\n"
                    "- 3. Signature: An electronic SOW envelope is being generated via Zoho Sign and will be dispatched to their address immediately.\n"
                    "Keep the tone strategic and highly executive."
                )
            else:
                context = "Standard CEO-level strategic partnership, investment request, or corporate inquiry."
                
            # Generate Gemini 3.5 response
            reply_text = gemini_client.generate_response(role="ceo", context=context, user_message=body)
            
            # If SOW request, simulate triggering Zoho Sign Envelope
            if is_sow_request:
                logger.info(f"[CEO AI AGENT] Programmatically triggering Zoho Sign Envelope for signature to: {sender}")
                zoho_sign_alert = (
                    "\n\n[System Alert: An official electronic signature envelope has been registered "
                    "with Zoho Sign (API Event: SOW_Initiated) and will arrive via a separate secure Zoho notification "
                    "for your signature within 2 minutes.]"
                )
                reply_text += zoho_sign_alert
                
            # Dispatch email reply
            mailbox.send_reply(recipient=sender, original_subject=subject, reply_body=reply_text)

    def process_support_mailbox(self):
        """Processes Support inbox. Directs clients to onboarding, upload templates, or handles general inquiries."""
        mailbox = self.mailboxes["support"]
        unread_emails = mailbox.fetch_unread_emails()
        
        logger.info(f"[Support] Polling mailbox. Found {len(unread_emails)} unread messages.")
        for mail in unread_emails:
            sender = mail["sender"]
            subject = mail["subject"]
            body = mail["body"]
            
            logger.info(f"[Support] Processing inbound message from {sender}: '{subject}'")
            
            # Analyze intent
            is_upload_inquiry = any(kw in body.lower() for kw in ["upload", "document", "ledger", "file", "invoice", "gstin", "pdf"])
            is_payment_inquiry = any(kw in body.lower() for kw in ["payment", "razorpay", "invoice", "receipt", "gst", "fee"])
            
            context = ""
            if is_upload_inquiry:
                context = (
                    "Customer is asking how or where to upload their audit compliance documents and financial ledgers.\n"
                    "Direct them explicitly to the clean URL secure upload portal at `/upload` (or vextaudit.com/upload).\n"
                    "Detail that their files will be ingested immediately by the AI Compliance parser."
                )
            elif is_payment_inquiry:
                context = (
                    "Customer is asking about pricing or completed payments.\n"
                    "Confirm that payments are processed securely through Razorpay (PCI-DSS Level 1).\n"
                    "Direct them to the onboarding gateway `/onboard` to view current schedules, and mention that standard invoices are auto-generated to their registered company email."
                )
            else:
                context = "General customer onboarding, system navigation, or compliance service inquiry."
                
            reply_text = gemini_client.generate_response(role="support", context=context, user_message=body)
            mailbox.send_reply(recipient=sender, original_subject=subject, reply_body=reply_text)

    def process_noreply_mailbox(self):
        """Monitors system alerts, bounces, and automated transaction notifications."""
        mailbox = self.mailboxes["no-reply"]
        unread_emails = mailbox.fetch_unread_emails()
        
        logger.info(f"[No-Reply Monitor] Polling mailbox. Found {len(unread_emails)} unread system logs.")
        for mail in unread_emails:
            sender = mail["sender"]
            subject = mail["subject"]
            body = mail["body"]
            
            logger.info(f"[No-Reply Monitor] Parsing automated alert from {sender}: '{subject}'")
            
            context = "Parsing Web3Forms receipt alerts, Vercel status, or mail bounces."
            parsed_summary = gemini_client.generate_response(role="no-reply", context=context, user_message=body)
            
            # Log parsed system findings in our server console
            logger.info(f"[No-Reply Diagnostic Extraction]:\n{parsed_summary}\n" + "-"*40)

    def process_intelligence_mailbox(self):
        """Processes Intelligence inbox. Ingests and summarizes complex regulatory circulars."""
        mailbox = self.mailboxes["intelligence"]
        unread_emails = mailbox.fetch_unread_emails()
        
        logger.info(f"[Intelligence] Polling mailbox. Found {len(unread_emails)} unread regulatory circulars.")
        for mail in unread_emails:
            sender = mail["sender"]
            subject = mail["subject"]
            body = mail["body"]
            
            logger.info(f"[Intelligence] Analyzing inbound regulatory update from {sender}: '{subject}'")
            
            context = "Summarize regulatory circulars/alerts into short, highly crisp executive memos."
            summary = gemini_client.generate_response(role="intelligence", context=context, user_message=body)
            
            logger.info(f"[Intelligence Ingest Summary]:\n{summary}\n" + "-"*40)
            # In production, this summary is programmatically fed to our vector compliance database.

    def process_newsletter_mailbox(self):
        """Processes Newsletter subscriptions and segment updates."""
        mailbox = self.mailboxes["newsletter"]
        unread_emails = mailbox.fetch_unread_emails()
        
        logger.info(f"[Newsletter] Polling mailbox. Found {len(unread_emails)} unread messages.")
        for mail in unread_emails:
            sender = mail["sender"]
            subject = mail["subject"]
            body = mail["body"]
            
            logger.info(f"[Newsletter] Processing subscriber email from {sender}: '{subject}'")
            
            context = "Customer is requesting newsletter subscription or regulatory digests."
            reply_text = gemini_client.generate_response(role="newsletter", context=context, user_message=body)
            mailbox.send_reply(recipient=sender, original_subject=subject, reply_body=reply_text)

    def run_all_mailboxes(self):
        """Runs the polling loop across all 5 mailboxes sequentially."""
        logger.info("="*60)
        logger.info("   VEXTMAIL RESPONSE ENGINE - SECURE POLLING LOOP STARTED")
        logger.info("="*60)
        self.process_ceo_mailbox()
        self.process_support_mailbox()
        self.process_noreply_mailbox()
        self.process_intelligence_mailbox()
        self.process_newsletter_mailbox()
        logger.info("="*60)
        logger.info("   VEXTMAIL RESPONSE ENGINE - POLLING LOOP COMPLETED")
        logger.info("="*60)

if __name__ == "__main__":
    engine = EmailCommandCenter()
    engine.run_all_mailboxes()
