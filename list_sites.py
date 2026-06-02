import os
from google.oauth2 import service_account
from googleapiclient.discovery import build

CREDENTIALS_FILE = r"C:\Users\shyam\.gemini\antigravity\scratch\service_account_credentials.json"

def main():
    if not os.path.exists(CREDENTIALS_FILE):
        print(f"Error: credentials not found.")
        return

    scopes = ["https://www.googleapis.com/auth/webmasters.readonly"]
    credentials = service_account.Credentials.from_service_account_file(
        CREDENTIALS_FILE, scopes=scopes
    )
    
    webmasters_service = build("webmasters", "v3", credentials=credentials)
    
    try:
        print("Fetching verified sites for this service account...")
        site_list = webmasters_service.sites().list().execute()
        
        sites = site_list.get('siteEntry', [])
        if not sites:
            print("No sites verified or accessible for this service account.")
            print("Please add this email as a User in Search Console: vext-automation-service-accoun@vextaudit-automation.iam.gserviceaccount.com")
        else:
            print("\nAccessible properties in Search Console:")
            for s in sites:
                print(f"  - Site URL: {s.get('siteUrl')} (Permission Level: {s.get('permissionLevel')})")
    except Exception as e:
        print(f"Error listing sites: {e}")

if __name__ == "__main__":
    main()
