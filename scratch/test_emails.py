import imaplib
import smtplib
import sys

# Ensure UTF-8 output on Windows standard terminal to prevent cp1252 exceptions
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

credentials = [
    ("ceo@vextaudit.com", "aoksbhinewtvfitv"),
    ("support@vextaudit.com", "ocrafvrdzfnmakxa"),
    ("no-reply@vextaudit.com", "ofxqupiswrzpvfhk"),
    ("intelligence@vextaudit.com", "tiedhaheeumcgqgm"),
    ("newsletter@vextaudit.com", "gtjtibrluudnolmb")
]

print("==========================================")
print("TESTING IMAP LOGINS (Google Workspace)")
print("==========================================")
for email, pw in credentials:
    try:
        mail = imaplib.IMAP4_SSL("imap.gmail.com", 993)
        mail.login(email, pw)
        print(f"SUCCESS: {email} IMAP login passed.")
        mail.logout()
    except Exception as e:
        print(f"FAILED: {email} IMAP login failed -> {e}")

print("\n==========================================")
print("TESTING SMTP LOGINS (Google Workspace)")
print("==========================================")
for email, pw in credentials:
    try:
        smtp = smtplib.SMTP("smtp.gmail.com", 587)
        smtp.starttls()
        smtp.login(email, pw)
        print(f"SUCCESS: {email} SMTP login passed.")
        smtp.quit()
    except Exception as e:
        print(f"FAILED: {email} SMTP login failed -> {e}")
