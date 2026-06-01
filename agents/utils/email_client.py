import imaplib
import smtplib
import email
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import sys
import logging
from agents.config import settings

# Setup standard logging safely
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamFileHandler('agents_operations.log', encoding='utf-8') if hasattr(logging, 'StreamFileHandler') else logging.FileHandler('agents_operations.log', encoding='utf-8')] if False else [logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("VextMailClient")

class EmailClient:
    def __init__(self, email_address: str, password: str):
        self.email_address = email_address
        self.password = password
        self.is_mock = "placeholder" in password or password == "MOCK_PASSWORD" or "workspace_app" in password

    def fetch_unread_emails(self) -> list:
        """
        Connects via IMAP to Gmail/Google Workspace and fetches unread messages.
        If credentials are placeholders, returns simulated test emails to facilitate local verification.
        """
        if self.is_mock:
            logger.info(f"[{self.email_address}] Mock connection active. Returning sample test emails.")
            # Return realistic sample emails based on mailbox role
            if "ceo" in self.email_address:
                return [
                    {
                        "id": "1",
                        "sender": "aditya.birla@manufacturing-corp.in",
                        "subject": "Inquiry regarding Full Audit Bundle and SOW",
                        "body": "Hello CEO, we want to purchase the Full Audit Bundle (₹75,000) for our factory operations. Can you send the Statement of Work (SOW) so we can sign it? Thank you, Aditya.",
                        "raw_msg": None
                    }
                ]
            elif "support" in self.email_address:
                return [
                    {
                        "id": "2",
                        "sender": "finance@saas-startup.io",
                        "subject": "Where do I upload our GST ledger?",
                        "body": "Hi Support, we just completed the payment for GST Audit Compliance. Where do we upload our documents and ledgers? Regards, Meera.",
                        "raw_msg": None
                    }
                ]
            elif "intelligence" in self.email_address:
                return [
                    {
                        "id": "3",
                        "sender": "notifications@gstcouncil.gov.in",
                        "subject": "GST Council Circular 12/2026 - Revision of tax filing rules",
                        "body": "Official Circular: The GST Council has revised the statutory audit threshold and reporting format effective July 1, 2026. Review rules immediately.",
                        "raw_msg": None
                    }
                ]
            elif "newsletter" in self.email_address:
                return [
                    {
                        "id": "4",
                        "sender": "karan.mehta@fintech-ventures.com",
                        "subject": "Subscribe to weekly compliance digest",
                        "body": "Hi, please add me to your newsletter subscription. I am the risk manager at Fintech Ventures.",
                        "raw_msg": None
                    }
                ]
            else:
                return []

        messages_list = []
        try:
            # Secure connection to Gmail IMAP
            mail = imaplib.IMAP4_SSL(settings.IMAP_SERVER, settings.IMAP_PORT)
            mail.login(self.email_address, self.password)
            mail.select("inbox")
            
            # Search for UNSEEN (unread) emails
            status, response = mail.search(None, "UNSEEN")
            if status != "OK":
                return []
                
            email_ids = response[0].split()
            for e_id in email_ids:
                status, msg_data = mail.fetch(e_id, "(RFC822)")
                if status != "OK":
                    continue
                
                raw_email = msg_data[0][1]
                msg = email.message_from_bytes(raw_email)
                
                # Extract headers safely
                subject = msg.get("Subject", "(No Subject)")
                sender = msg.get("From", "(No Sender)")
                
                # Extract text body safely
                body = ""
                if msg.is_multipart():
                    for part in msg.walk():
                        content_type = part.get_content_type()
                        content_disposition = str(part.get("Content-Disposition"))
                        if content_type == "text/plain" and "attachment" not in content_disposition:
                            try:
                                body = part.get_payload(decode=True).decode("utf-8", errors="ignore")
                            except:
                                pass
                else:
                    try:
                        body = msg.get_payload(decode=True).decode("utf-8", errors="ignore")
                    except:
                        pass
                
                messages_list.append({
                    "id": e_id.decode("utf-8"),
                    "sender": sender,
                    "subject": subject,
                    "body": body,
                    "raw_msg": msg
                })
            
            mail.logout()
        except Exception as e:
            logger.error(f"Failed to fetch emails for {self.email_address}: {e}")
        
        return messages_list

    def send_reply(self, recipient: str, original_subject: str, reply_body: str, original_msg_id=None):
        """
        Sends an email reply via SMTP.
        If credentials are placeholders, simulates the action.
        """
        subject = f"Re: {original_subject}" if not original_subject.startswith("Re:") else original_subject
        
        if self.is_mock:
            logger.info(f"[{self.email_address}] Simulated SMTP mail SENT to: {recipient}")
            logger.info(f"[{self.email_address}] Subject: {subject}")
            logger.info(f"[{self.email_address}] Reply content:\n{reply_body}\n" + "="*50)
            return True
            
        try:
            # Configure SMTP connection with standard TLS handshake
            smtp = smtplib.SMTP(settings.SMTP_SERVER, settings.SMTP_PORT)
            smtp.starttls()
            smtp.login(self.email_address, self.password)
            
            # Construct standard threaded MIME Multipart mail
            msg = MIMEMultipart()
            msg["From"] = self.email_address
            msg["To"] = recipient
            msg["Subject"] = subject
            
            # If responding to a specific thread, set thread reference headers
            if original_msg_id:
                msg["In-Reply-To"] = original_msg_id
                msg["References"] = original_msg_id
                
            msg.attach(MIMEText(reply_body, "plain", "utf-8"))
            
            smtp.send_message(msg)
            smtp.quit()
            logger.info(f"[{self.email_address}] Outbound mail successfully sent to {recipient}")
            return True
        except Exception as e:
            logger.error(f"[{self.email_address}] SMTP failure sending to {recipient}: {e}")
            return False
