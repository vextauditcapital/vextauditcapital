import os
import sys
from google.oauth2 import service_account
from googleapiclient.discovery import build

CREDENTIALS_FILE = r"C:\Users\shyam\.gemini\antigravity\scratch\service_account_credentials.json"
SITE_URL = "https://www.vextaudit.com/"
SITEMAP_URL = "https://www.vextaudit.com/sitemap.xml"

def main():
    if not os.path.exists(CREDENTIALS_FILE):
        print(f"Error: service_account_credentials.json not found at {CREDENTIALS_FILE}.")
        print("Please place your downloaded Google Cloud Service Account key file there and re-run.")
        sys.exit(1)

    print("Authenticating with Google Search Console API...")
    scopes = ["https://www.googleapis.com/auth/webmasters"]
    credentials = service_account.Credentials.from_service_account_file(
        CREDENTIALS_FILE, scopes=scopes
    )

    # Build the service
    webmasters_service = build("webmasters", "v3", credentials=credentials)

    print(f"Submitting sitemap '{SITEMAP_URL}' for site '{SITE_URL}'...")
    try:
        webmasters_service.sitemaps().submit(
            siteUrl=SITE_URL, feedpath=SITEMAP_URL
        ).execute()
        print("SUCCESS: Sitemap submitted successfully to Google Search Console!")
    except Exception as e:
        print(f"ERROR submitting sitemap: {e}")

if __name__ == "__main__":
    main()

